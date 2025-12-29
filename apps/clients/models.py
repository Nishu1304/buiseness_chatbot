from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=255)
    whatsapp_number = models.CharField(max_length=20, unique=True)
    timezone = models.CharField(max_length=50, default="Asia/Kolkata")
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ClientFeature(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE)

    faqs = models.BooleanField(default=True)
    leads = models.BooleanField(default=True)
    appointments = models.BooleanField(default=False)
    orders = models.BooleanField(default=False)
    payments = models.BooleanField(default=False)
    sentiment = models.BooleanField(default=False)

    def __str__(self):
        return f"Features for {self.client.name}"
