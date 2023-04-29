from django import forms

from apps.debts.models import Debt, Agent


TRANZACTION_CHOICE = (
    ('ВЗЯТЬ', 'Взять'),
    ('ДАТЬ', 'Дать'),
)


class DebtForm(forms.ModelForm):
    class Meta:
        model = Debt
        fields = ['tranzaction_type', 'agent', 'amount', 'description']
        widgets = {
            'tranzaction_type': forms.RadioSelect(choices=TRANZACTION_CHOICE),
        }


class AgentForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = ('name', 'phone_number',)
