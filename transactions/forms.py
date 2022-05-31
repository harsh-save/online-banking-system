from django.contrib.auth.forms import UserChangeForm
from django import forms
from accounts.models import User, AccountDetails
from django.core.exceptions import ValidationError
import datetime
import decimal
import re


class userchange(UserChangeForm, forms.Form):
    class Meta:

        model = User
        fields = ['username', 'email']
        exclude = ['password']

    """def clean_email(self):
       regex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
        email_field = self.cleaned_data.get("email")
        print(type(email_field))
        if(re.search(regex, email_field) == False):
            raise ValidationError("Recheck the email address entered")
        elif(User.objects.filter(email=email_field).exists()):
            raise ValidationError(
                "User with same email address already exists")
        else:
            return email_field"""


class accountchange(UserChangeForm):
    class Meta:
        model = AccountDetails
        fields = ['phone', 'address', 'dob', 'full_name']

    def clean_phone(self):
        phone_field = self.cleaned_data.get("phone")
        try:
            # int(phone_field)
            # float(phone_field)
            if(len(phone_field) != 10):
                raise ValueError
        except ValueError:
            raise ValidationError("Recheck the phone number entered")
        return phone_field

    def clean_dob(self):
        date_field = self.cleaned_data.get("dob")
        try:
            datetime.datetime.strftime(date_field, '%m-%d-%Y')
        except ValueError:
            raise ValidationError("Recheck the entered Date of Birth")
        return date_field

    """def clean_balance(self):
        balance_field = self.cleaned_data.get("balance")
        try:
            decimal.Decimal(balance_field)
        except ValueError:
            raise ValidationError("Recheck the amount you entered")
        return balance_field"""

    """def clean_full_name(self):
        name_field = self.cleaned_data.get("full_name")

        if(name_field.isalpha() == True):
            return name_field
        else:
            raise ValidationError("Full name should contain only alphabets")"""
