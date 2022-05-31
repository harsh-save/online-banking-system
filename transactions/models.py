from django.db import models
#from accounts.models import User,AccountDetails
from django.db.models.signals import pre_save
import random
import string
# Create your models here.


class Transactions(models.Model):
    #user = models.ForeignKey(AccountDetails,on_delete=models.CASCADE,null=True)
    transaction_id = models.CharField(max_length=15, null=True)
    account_no = models.CharField(max_length=10, null=True)
    name = models.CharField(max_length=60, null=True)
    # email_address=models.EmailField(max_length=100,null=True)
    operations = models.CharField(max_length=100, null=True)
    date = models.DateTimeField(
        verbose_name="Created date", auto_now_add=True, null=True)
    amount = models.DecimalField(null=True, max_digits=10, decimal_places=2)
    debit_account = models.CharField(max_length=10, null=True)
    credit_account = models.CharField(max_length=10, null=True)


def transaction_id_generator(sender, instance, **kwargs):
    identity = ''.join(random.choices(string.digits, k=12))
    if not instance.transaction_id:
        instance.transaction_id = identity


pre_save.connect(transaction_id_generator, Transactions)
