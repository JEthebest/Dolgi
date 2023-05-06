from django.contrib import admin

from apps.debts.models import Tranzaction, Contact


@admin.register(Tranzaction)
class TranzactionAdmin(admin.ModelAdmin):
    pass


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    pass
