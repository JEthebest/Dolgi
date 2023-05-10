from django.db import models

from apps.users.models import User


TRANSACTION_CHOICE = (
    ('BORROW', 'Взять в долг'),
    ('REPAY', 'Погасить займ'),
    ('LEND', 'Дать в долг'),
    ('RECEIVE', 'Принять погашение'),
)


class Contact(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='contacts'
    )
    phone_number = models.CharField(max_length=90)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    transaction_type = models.CharField(
        max_length=20, choices=TRANSACTION_CHOICE,
        default='BORROW', verbose_name='Transaction type',
    )
    contact = models.ForeignKey(
        Contact, on_delete=models.CASCADE,
        null=True, blank=True, related_name='transactions',
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.description}-{self.transaction_type}'
