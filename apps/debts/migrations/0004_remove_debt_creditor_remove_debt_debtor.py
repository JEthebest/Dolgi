# Generated by Django 4.2 on 2023-04-29 07:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('debts', '0003_agent_phone_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='debt',
            name='creditor',
        ),
        migrations.RemoveField(
            model_name='debt',
            name='debtor',
        ),
    ]