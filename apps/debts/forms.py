from django import forms

from apps.debts.models import Transaction, Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'phone_number']


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'description']
