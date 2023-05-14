from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser, models.Model):
    chat_id = models.IntegerField(
        null=True, blank=True,
        verbose_name='Чат id'
    )

    def __str__(self):
        return self.username
