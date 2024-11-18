from django.contrib import admin
from .models import EmailRecipient, EmailTemplate

admin.site.register(EmailRecipient)
admin.site.register(EmailTemplate)
