from django.db import models
from django.db.models import Count, Case, When
from django.utils import timezone

# Create your models here.


class Transaction(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        SUCCESS = "success", "Success"
        FAILED = "failed", "Failed"

    wallet_address = models.CharField(max_length=42)
    ip_address = models.CharField(max_length=100)
    tx_hash = models.CharField(max_length=66, null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        ordering = ["-timestamp"]

    def __str__(self):
        return f"Transaction to {self.wallet_address} at {self.timestamp}"
