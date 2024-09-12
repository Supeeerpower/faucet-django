from django.contrib import admin
from .models import Transaction
# Register your models here.


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ["wallet_address", "tx_hash", "status", "timestamp"]
    list_filter = ["status",]
    search_fields = ("wallet_address", "tx_hash",)
