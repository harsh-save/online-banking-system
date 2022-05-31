from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm

from .models import User, AccountDetails
from django.core.exceptions import ValidationError
import re
import datetime
import decimal


class Usercreate(UserCreationForm, forms.Form):
    # username = forms.CharField(widget=forms.TextInput(
    # attrs={'placeholder': 'Enter username', 'class': 'form-control'}))
    # email = forms.CharField(widget=forms.TextInput(
    # attrs={'placeholder': 'Email'}))
    #password = forms.CharField(widget=forms.PasswordInput())
    #password_again = forms.CharField(widget=forms.PasswordInput())
    # password=forms.CharField(widget=forms.TextInput(attrs={'type':'text',}))
    # password_again=forms.CharField(widget=forms.TextInput(attrs={'type':'text'}))
    password1 = forms.CharField(widget=forms.PasswordInput(
        render_value=True, attrs={'type': 'password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(render_value=True))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'password1': forms.TextInput(attrs={'type': 'password'}),
            'password2': forms.TextInput(attrs={'type': 'password'}),
        }

    def clean_email(self):
        regex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
        email_field = self.cleaned_data.get("email")
        if(re.search(regex, email_field) == False):
            raise ValidationError("Recheck the email address entered")
        elif(User.objects.filter(email=email_field).exists()):
            raise ValidationError(
                "User with same email address already exists")
        else:
            return email_field


"""class Usercreate(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter username'}))
    email = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())"""


class AccountForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(attrs={'size': '3'}))
    # full_name=forms.TextInput(attrs={'id':'full_name','onblur':'username()'})
    full_name = forms.CharField(
        widget=forms.TextInput(attrs={'id': 'full_name'}))

    """dob = forms.CharField(widget=forms.TextInput(
        attrs={'palceholder': 'MM/DD/YYYY'}))"""

    """def email_verfy(self):
        if (User.objects.filter(email=email)):
            raise forms.ValidationError('User with same email exists')
        return email"""

    class Meta:
        model = AccountDetails

        fields = ['full_name', 'phone', 'address', 'dob', 'balance']
        widgets = {'dob': forms.TextInput(attrs={'placeholder': 'MM/DD/YYYY'}),
                   'phone': forms.TextInput(attrs={'placeholder': '10 digit required'}),
                   'address': forms.TextInput(attrs={'size': '3'})
                   }
        #full_name= widget= forms.TextInput(attrs={'id':'full_name','onblur':'username()'})

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

    def clean_balance(self):
        balance_field = self.cleaned_data.get("balance")
        try:
            decimal.Decimal(balance_field)
        except ValueError:
            raise ValidationError("Recheck the amount you entered")
        return balance_field

    """def clean_full_name(self):
        name_field = self.cleaned_data.get("full_name")
        if(name_field.isalpha() == False):
            raise ValidationError("Full name should contain only alphabets")
        return name_field"""


class UserLoginForm(forms.Form):
    username = forms.CharField(label="username")
    password = forms.CharField(label="password")

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if (username and password):
            user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("Account Does Not Exist.")
        if not user.check_password(password):
            raise forms.ValidationError("Password Does not Match.")
        if not user.is_active:
            raise forms.ValidationError("Account is not Active.")

        return super(UserLoginForm, self).clean(*args, **kwargs)


class AdminLoginForm(forms.Form):
    username = forms.CharField(label="username")
    password = forms.CharField(widget=forms.PasswordInput)

    """def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if (username and password):
            user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("Account Does Not Exist.")
        if not user.check_password(password):
            raise forms.ValidationError("Password Does not Match.")
        if not user.is_active:
            raise forms.ValidationError("Account is not Active.")

        return super(UserLoginForm, self).clean(*args, **kwargs)"""
