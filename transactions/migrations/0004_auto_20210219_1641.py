# Generated by Django 3.0.8 on 2021-02-19 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0003_transactions_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactions',
            name='credit_account',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='transactions',
            name='debit_account',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
