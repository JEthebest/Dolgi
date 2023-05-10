# Generated by Django 4.2 on 2023-05-10 14:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('debts', '0004_alter_contact_user_alter_transaction_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='contact',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='debts.contact'),
        ),
    ]
