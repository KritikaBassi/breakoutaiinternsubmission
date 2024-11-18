from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from .models import EmailRecipient, EmailTemplate
from .tasks import send_email_task
import pandas as pd
import re

def upload_csv(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        fs = FileSystemStorage()
        filename = fs.save(csv_file.name, csv_file)
        df = pd.read_csv(fs.path(filename))
        df.fillna('', inplace=True)
        recipients = []
        for _, row in df.iterrows():
            recipient = EmailRecipient(
                email=row.get('Email', ''),
                name=row.get('Name', ''),
                company_name=row.get('Company Name', ''),
                location=row.get('Location', ''),
                products=row.get('Products', '')
            )
            recipients.append(recipient)
        EmailRecipient.objects.bulk_create(recipients)
        messages.success(request, 'Contacts uploaded successfully.')
        return redirect('create_prompt')
    return render(request, 'emails/upload.html')

def create_prompt(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        body = request.POST.get('body')
        EmailTemplate.objects.create(subject=subject, body=body)
        messages.success(request, 'Email template saved successfully.')
        return redirect('schedule_emails')
    columns = EmailRecipient._meta.get_fields()
    context = {'columns': [field.name for field in columns if field.name not in ['id', 'status', 'delivery_status', 'scheduled_time', 'sent_time', 'opens', 'bounces']]}
    return render(request, 'emails/prompt.html', context)

def schedule_emails(request):
    if request.method == 'POST':
        schedule_option = request.POST.get('schedule_option')
        throttle_rate = int(request.POST.get('throttle_rate', 1))
        specific_time = request.POST.get('specific_time')
        interval = int(request.POST.get('interval', 0))
        template = EmailTemplate.objects.last()
        recipients = EmailRecipient.objects.filter(status='Pending')
        for idx, recipient in enumerate(recipients):
            if schedule_option == 'immediate':
                send_email_task.apply_async(args=[recipient.id, template.id], countdown=0)
            elif schedule_option == 'specific_time':
                eta = timezone.datetime.fromisoformat(specific_time)
                send_email_task.apply_async(args=[recipient.id, template.id], eta=eta)
            elif schedule_option == 'staggered':
                send_email_task.apply_async(args=[recipient.id, template.id], countdown=idx * interval)
            recipient.status = 'Scheduled'
            recipient.save()
        messages.success(request, 'Emails scheduled successfully.')
        return redirect('email_status')
    return render(request, 'emails/schedule.html')

def email_status(request):
    recipients = EmailRecipient.objects.all()
    return render(request, 'emails/status.html', {'recipients': recipients})

def dashboard(request):
    total_emails = EmailRecipient.objects.count()
    emails_sent = EmailRecipient.objects.filter(status='Sent').count()
    emails_pending = EmailRecipient.objects.filter(status='Pending').count()
    emails_scheduled = EmailRecipient.objects.filter(status='Scheduled').count()
    emails_failed = EmailRecipient.objects.filter(status='Failed').count()
    emails_opened = EmailRecipient.objects.filter(delivery_status='Opened').count()
    context = {
        'total_emails': total_emails,
        'emails_sent': emails_sent,
        'emails_pending': emails_pending,
        'emails_scheduled': emails_scheduled,
        'emails_failed': emails_failed,
        'emails_opened': emails_opened,
    }
    return render(request, 'emails/dashboard.html', context)
