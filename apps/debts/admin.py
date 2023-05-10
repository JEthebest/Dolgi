from django.contrib import admin

from apps.debts.models import Transaction, Contact


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    pass


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    pass
