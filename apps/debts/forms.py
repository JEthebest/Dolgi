from django import forms

from apps.debts.models import Debt, Agent


class DebtForm(forms.ModelForm):
    class Meta:
        model = Debt
        fields = ('amount', 'description', 'agent',)


class AgentForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = ('name',)
