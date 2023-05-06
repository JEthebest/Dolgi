from django.db import models

from apps.users.models import User


TRANZACTION_CHOICE = (
    ('Займ', 'Займ'),
    ('Долг', 'Долг'),
)


class Contact(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=90)

    def __str__(self):
        return self.name


class Tranzaction(models.Model):
    type = models.CharField(
        max_length=20, choices=TRANZACTION_CHOICE,
        default='Займ', verbose_name='Tranzaction type',
    )
    agent = models.ForeignKey(
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
        return self.description
