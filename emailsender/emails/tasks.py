from celery import shared_task
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils import timezone
from .models import EmailRecipient, EmailTemplate
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import openai
import re
import time

@shared_task(bind=True, rate_limit='10/m')
def send_email_task(self, recipient_id, template_id):
    recipient = EmailRecipient.objects.get(id=recipient_id)
    template = EmailTemplate.objects.get(id=template_id)
    try:
        body = personalize_template(template.body, recipient)
        subject = personalize_template(template.subject, recipient)
        openai.api_key = settings.OPENAI_API_KEY
        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=body,
            max_tokens=250,
            temperature=0.7,
        )
        email_content = response.choices[0].text.strip()
        email = EmailMessage(
            subject,
            email_content,
            settings.DEFAULT_FROM_EMAIL,
            [recipient.email],
        )
        email.content_subtype = 'html'
        email.send()
        recipient.status = 'Sent'
        recipient.sent_time = timezone.now()
        recipient.save()
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'email_status', {'type': 'status_update', 'message': f'Email sent to {recipient.email}'}
        )
    except Exception as e:
        recipient.status = 'Failed'
        recipient.save()
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'email_status', {'type': 'status_update', 'message': f'Failed to send email to {recipient.email}'}
        )

def personalize_template(template, recipient):
    placeholders = re.findall(r'{{\s*(\w+)\s*}}', template)
    for placeholder in placeholders:
        value = getattr(recipient, placeholder.lower(), '')
        template = template.replace(f'{{{{ {placeholder} }}}}', value)
    return template
