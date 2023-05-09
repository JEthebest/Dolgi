from django.db import models

from apps.users.models import User


TRANZACTION_CHOICE = (
    ('Займ', 'Займ'),
    ('Погасить займ', 'Погасить займ'),
    ('Долг', 'Долг'),
    ('Принять погашение', 'Принять погашение'),
)


class Contact(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=90)

    def __str__(self):
        return self.name


class Tranzaction(models.Model):
    tranzaction_type = models.CharField(
        max_length=20, choices=TRANZACTION_CHOICE,
        default='Займ', verbose_name='Tranzaction type',
    )
    contact = models.ForeignKey(
        Contact, on_delete=models.CASCADE,
        null=True, blank=True, related_name='tranzactions',
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    publish = models.BooleanField(
        default=True,
        verbose_name='Publish'
    )

    def __str__(self):
        return f'{self.description}-{self.tranzaction_type}'
