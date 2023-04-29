from django.db import models

from apps.users.models import User


TRANZACTION_CHOICE = (
    ('Взял в долг', 'Взять'),
    ('Дал в долг', 'Дать'),
)


class Agent(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=90)

    def __str__(self):
        return self.name


class Debt(models.Model):
    tranzaction_type = models.CharField(
        max_length=20, choices=TRANZACTION_CHOICE,
        default='ВЗЯТЬ', verbose_name='Tranzaction type',
    )
    agent = models.ForeignKey(
        Agent, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description
