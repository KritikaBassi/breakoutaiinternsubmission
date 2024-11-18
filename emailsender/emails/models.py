from django.db import models

class EmailRecipient(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=255, null=True, blank=True)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    products = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=50, default='Pending')
    delivery_status = models.CharField(max_length=50, default='N/A')
    scheduled_time = models.DateTimeField(null=True, blank=True)
    sent_time = models.DateTimeField(null=True, blank=True)
    opens = models.IntegerField(default=0)
    bounces = models.IntegerField(default=0)

    def __str__(self):
        return self.email

class EmailTemplate(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()

    def __str__(self):
        return self.subject
