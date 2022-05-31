from django.contrib.auth import get_user_model
#from .models import User
from django.contrib.auth.backends import ModelBackend
#from accounts.models import User
from accounts.models import AccountDetails
from django.db.models import Q
#User = get_user_model()


"""class CustomBackend():
    def authenticate(self, request, account_number=None, password=None, email=None):
        try:
            user = User.objects.get(account__account_number=account_number, email=email)
            if user and user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None"""

class CustomBackend(object):
    def authenticate(self,account_number,email,password):
        #account_no=kwargs['account_number']
        #email=kwargs['email']
        #password=kwargs['password']
        try:
            #user = User.objects.get(details__account_number=account_number, email=email)
            user= AccountDetails.objects.get(account_number=account_number,email=email,password=password)
            if user and user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
