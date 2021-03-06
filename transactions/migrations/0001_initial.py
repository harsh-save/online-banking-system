# Generated by Django 3.0.8 on 2020-08-26 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.CharField(max_length=15, null=True)),
                ('account_no', models.CharField(max_length=10, null=True)),
                ('name', models.CharField(max_length=60, null=True)),
                ('operations', models.CharField(max_length=100, null=True)),
                ('date', models.DateField(auto_now_add=True, null=True)),
            ],
        ),
    ]
