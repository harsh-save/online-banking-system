# Generated by Django 3.0.8 on 2021-02-03 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_account_no', models.CharField(blank=True, max_length=15, null=True, verbose_name='Account number')),
                ('user_name', models.CharField(blank=True, max_length=1000, null=True)),
                ('subject', models.CharField(blank=True, max_length=1000, null=True)),
                ('message', models.CharField(blank=True, max_length=10000, null=True)),
            ],
        ),
    ]