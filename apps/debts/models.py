from django.db import models

from apps.users.models import User


class Agent(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Debt(models.Model):
    creditor = models.ForeignKey(
        User, related_name='credit_debts', on_delete=models.CASCADE)
    debtor = models.ForeignKey(
        User, related_name='debit_debts', on_delete=models.CASCADE)
    agent = models.ForeignKey(
        Agent, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description
