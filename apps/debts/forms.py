from django import forms

from apps.debts.models import Tranzaction, Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('name', 'phone_number',)


class TranzactionForm(forms.ModelForm):
    class Meta:
        model = Tranzaction
        fields = ['amount', 'description']


class RepayForm(forms.ModelForm):
    class Meta:
        model = Tranzaction
        fields = ['amount']


class TranzactionContactForm(forms.ModelForm):
    class Meta:
        model = Tranzaction
        fields = ['agent', 'amount', 'description']
