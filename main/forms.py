from django.contrib.auth import authenticate
from django import forms
from accounts.backends import CustomBackend
from django.contrib.auth.forms import UserChangeForm
from accounts.models import User, AccountDetails


class UserLoginForm(forms.Form):
    #account_number = forms.CharField(label="Account number")
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput)

    """def clean(self, *args, **kwargs):

        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        account_number=self.cleaned_data.get("account_number")
        #if (email and password and account_number):
        #user = authenticate(email=email, password=password,account_number=account_number)
        user = CustomBackend.authenticate(self,email=email, password=password,account_number=account_number)
        if not user:
            raise forms.ValidationError("Account Does Not Exist.")
        if not user.check_password(password):
            raise forms.ValidationError("Password Does not Match.")
        if not user.is_active:
            raise forms.ValidationError("Account is not Active.")

        return super(UserLoginForm, self).clean(*args, **kwargs)
        if not user or not user.is_active:
            raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
        return self.cleaned_data"""

    """def login(self, request):
        account_no = self.cleaned_data.get('account_number')
        password = self.cleaned_data.get('password')
        email = self.cleaned_data.get('email')
        #user = authenticate(account_number=account_no, password=password,email=email)
        return user"""


class FeedbackForm(forms.Form):
    subject = forms.CharField(label="Subject")
    feedback = forms.CharField(label="Feedback")


class userchange(UserChangeForm, forms.Form):
    class Meta:

        model = User
        fields = ['username']
        exclude = ['password']


class accountchange(UserChangeForm):
    class Meta:
        model = AccountDetails
        fields = ['phone']
