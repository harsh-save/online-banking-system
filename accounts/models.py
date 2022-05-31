from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
from django.db.models.signals import pre_save
import random
import string
import datetime
# Create your models here.


class User(AbstractUser):
    username = models.CharField(
        max_length=30, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class AccountDetails(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="details", primary_key=True)
    phone = models.CharField(verbose_name="Mobile number",
                             max_length=10, null=True, blank=False)
    address = models.TextField(
        verbose_name="Address", max_length=300, null=False, blank=False, default="def")
    dob = models.DateField(verbose_name="birth date",
                           max_length=15, null=True, blank=False)
    account_number = models.CharField(
        verbose_name="Account number", max_length=15, null=True, blank=True)
    created_date = models.DateTimeField(
        verbose_name="Created date", auto_now_add=True, null=True)
    full_name = models.CharField(max_length=100, null=True)
    balance = models.DecimalField(null=True, max_digits=10, decimal_places=2)
    """age = models.CharField(
        verbose_name='age', max_length=5, null=True, blank=True)"""

# Signals


def account_number_generator(sender, instance, **kwargs):
    iden = ''.join(random.choices(string.digits, k=10))
    if not instance.account_number:
        instance.account_number = iden


pre_save.connect(account_number_generator, AccountDetails)


"""def password_generator(sender,instance,** kwargs):
    LETTERS=string.ascii_letters
    NUMBERS=string.digits
    PUNCTUATION=string.punctuation
    temp_password=f'{LETTERS}{NUMBERS}{PUNCTUATION}'
    temp_password=list(temp_password)
    random.shuffle(temp_password)
    final_password=random.choices(temp_password,k=10)
    final_password=''.join(final_password)
    if not instance.password1 and instance.password2:
        instance.password1=final_password
        instance.password2=final_password

pre_save.connect(password_generator,User)"""


class Feedback(models.Model):
    user_account_no = models.CharField(
        verbose_name="Account number", max_length=15, null=True, blank=True)
    user_name = models.CharField(max_length=1000, blank=True, null=True)
    subject = models.CharField(max_length=1000, blank=True, null=True)
    message = models.CharField(max_length=10000, null=True, blank=True)
