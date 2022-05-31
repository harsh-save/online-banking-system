from django.shortcuts import render, redirect
from .forms import AccountForm, Usercreate, UserLoginForm, AdminLoginForm
from django.contrib.auth import authenticate
from .models import User, AccountDetails, Feedback
import random
import string
from transactions.models import Transactions
from django.contrib import messages
from django.core.mail import send_mail
from banking_system.settings import EMAIL_HOST_USER
import re
import datetime
import decimal
from .filters import userFilter
from django.template.loader import get_template
from main.utils import render_to_pdf
from django.http import HttpResponse
from django.core.exceptions import ValidationError


def admin_login(request):
    # Credentials
    username_org = "Administrator"
    password_org = "admin123"
    admin_login_form = AdminLoginForm(request.POST or None)
    if request.method == 'POST' and admin_login_form.is_valid():

        # account_no=user_login_form.cleaned_data['account_number']
        username = admin_login_form.cleaned_data['username']
        password = admin_login_form.cleaned_data['password']

       # user=authenticate(email=email,password=password)
        print(username)
        print(password)

        if (username == username_org and password == password_org):
            # login(request,user)
            return redirect('admin_main')

        else:
            messages.success(
                request, f"Login failed.Please check the email and password")

        """try:
            user=user_login_form.login(request)
        except ObjectDoesNotExist:
            print('har')
        if user:
            login(request,user)
            return redirect('landing_page')"""

    context = {
        'admin_login_form': admin_login_form
    }

    return render(request, 'admin/admin_login.html', context)


def admin_landing(request):
    # users = User.objects.all().select_related('details')
    # users = User.objects.select_related('details').all()
    acccounts = AccountDetails.objects.all()
    # print(users)
    # par_user=User.objects.get(pk=4)
    # acc_bal=AccountDetails.objects.get(account_number=4800434559)
    # acc_bal = User.objects.select_related('details').get(pk=4)
    # print(acc_bal)
    # acc=AccountDetails.objects.get(user=acc_bal)
    # bal = acc_bal.details.balance
    # print(bal)
    # recevier_acc = 4800434559
    # acc_det = AccountDetails.objects.get(account_number=recevier_acc)
    # rec = acc_det.balance
    # print(rec)
    # acc=rec.details.filter(account_number=recevier_acc)
    # print(acc)
    """acc_obj = AccountDetails.objects.select_related('user').all()
    print(type(users))

    search_acc = request.GET.get('search_acc_no')
    if search_acc != '' and search_acc is not None:
        acc_obj = acc_obj.filter(account_number__icontains=search_acc)
        search_id = acc_obj.values('user_id')
        acc = AccountDetails.objects.filter(user__id=search_id)
        print(acc)
        # users = User.objects.filter(id=search_id)
        # print(acc_obj.values('user_id'))"""
    # context = {'users': users}
    account_filter = userFilter(request.GET, queryset=acccounts)
    acccounts = account_filter.qs
    context = {'accounts': acccounts, 'account_filter': account_filter}

    return render(request, 'admin/accounts.html', context)


def search_details(request):
    pass


def random_password_generator():  # Working function
    LETTERS = string.ascii_letters
    NUMBERS = string.digits
    # PUNCTUATION = string.punctuation
    temp_password = f'{LETTERS}{NUMBERS}'
    temp_password = list(temp_password)
    random.shuffle(temp_password)
    final_password = random.choices(temp_password, k=10)
    final_password = ''.join(final_password)
    return final_password


def random_username_generator():  # Working function
    letters = string.ascii_letters
    numbers = string.digits
    temp_username = f'{letters}{numbers}'
    temp_username = list(temp_username)
    random.shuffle(temp_username)
    final_username = random.choices(temp_username, k=10)
    final_username = ''.join(final_username)
    if User.objects.filter(username=final_username).exists():
        random_username_generator()
        return final_username
    else:
        return final_username


def register(request):
    users = User.objects.all().select_related('details')
    generated_username = random_username_generator()
    generated_password = random_password_generator()
    passw = 'harsh'
    inititial_dict = {
        'username': generated_username,
        'password1': generated_password,
        'password2': generated_password,

    }
    user_form = Usercreate(request.POST or None, initial=inititial_dict)
    acc_form = AccountForm(request.POST or None,)
    # if user_form.is_valid() and acc_form.is_valid():
    """email_field = user_form.cleaned_data.get('email')
        phone_field = acc_form.cleaned_data.get('phone')
        date_field = acc_form.cleaned_data.get('dob')
        balance_field = acc_form.cleaned_data.get('balance')"""

    #password1 = acc_form.cleaned_data.get('password1')
    #password2 = acc_form.cleaned_data.get('password2')

    """regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        # email_check=User.objects.get(email=email_field)
        if(re.search(regex, email_field) == False):
            print("re")
            messages.error(request, f"Recheck the entered email address")

        elif(User.objects.filter(email=email_field).exists()):
            print("elif")
            messages.error(
                request, f"User with the same email address already exists")
        elif(date_field):

            try:
                datetime.datetime.strftime(date_field, '%m-%d-%Y')
            except ValueError:
                messages.error(request, f"Invalid Date of birth")"""

    if(user_form.is_valid() and acc_form.is_valid()):
        user = user_form.save(commit=False)
        acc_details = acc_form.save(commit=False)
        password = user_form.cleaned_data.get("password1")
        email = user_form.cleaned_data.get('email')
        print(email)
        user.set_password(password)
        user.save()
        # print(user)
        acc_details.user = user
        acc_details.save()
        subject = "Username and password"
        content = "Username : "+email+"   "+"Password: "+password
        to = email
        send_mail(subject, content, EMAIL_HOST_USER, [to])
        messages.success(
            request, f"User has been registered successfully and email is sent")
        """user = user_form.save(commit=False)
            acc_details = acc_form.save(commit=False)
            password = user_form.cleaned_data.get("password1")
            email = user_form.cleaned_data.get('email')
            print(email)
            user.set_password(password)
            user.save()
        # print(user)
            acc_details.user = user
            acc_details.save()
            subject = "Username and password"
            content = "Username : "+email+"   "+"Password: "+password
            to = email
            send_mail(subject, content, EMAIL_HOST_USER, [to])
            messages.success(request, f"User has been registered successfully and email is sent")"""

        # raise ValidationError('User exists')
        """messages.error(
                request, f"User with the same email address already exists")"""

        """if(User.objects.get(email=email_field)):
            messages.error(
                request, f"User with the same email address already exists")"""

        """if(date_field):
            try:
                datetime.datetime.strftime(date_field, '%m-%d-%Y')
            except ValueError:
                messages.error(request, f"Invalid Date of birth")"""

        """if(balance_field):
            try:
                print(type(balance_field))
                decimal.Decimal(balance_field)
            except ValueError:
                messages.error(request, f"Invalid balance amount entered")"""

        """if(phone_field):

            try:
                int(phone_field)
                float(phone_field)
                if (len(phone_field) != 10):
                    raise ValueError

            except ValueError:
                messages.error(
                    request, f"Recheck the phone number you entered")"""

        """if(password1 != password2):
            messages.error(
                request, f"Passwords don't match")"""
        """else:

            user = user_form.save(commit=False)
            acc_details = acc_form.save(commit=False)
            password = user_form.cleaned_data.get("password1")
            email = user_form.cleaned_data.get('email')
            print(email)
            user.set_password(password)
            user.save()
        # print(user)
            acc_details.user = user
            acc_details.save()
            subject = "Username and password"
            content = "Username : "+email+"   "+"Password: "+password
            to = email
            send_mail(subject, content, EMAIL_HOST_USER, [to])
            messages.success(
                request, f"User has been registered successfully and email is sent")"""

    return render(request, 'admin/register_user.html', {"user_form": user_form, "acc_form": acc_form, 'users': users})


def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username_iexact=username).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'A user with the user'


def transactions(request):
    transactions = Transactions.objects.all()

    return render(request, 'admin/transactions.html', {'transactions': transactions})


def feedback_view(request):
    feedback = Feedback.objects.all()
    return render(request, 'admin/feedback_view.html', {'feedback': feedback})


"""def login(request):
    if request.user.is_authenticated:
        pass
    else:
        user_login_form=UserLoginForm(request.POST or None)
        if user_login_form.is_valid():
            username=user_login_form.cleaned_data.get('username')
            password=user_login_form.cleaned_data.get('password')
            user=authenticate(username=username,password=password)
            return redirect('admin_main')

        context={
            'user_login_form':user_login_form
        }
        return render(request,'admin_panel/user_login.html',context)"""


def logout():
    pass


def transfer(request):
    pass


def generate_username(request):
    name = request.GET.get('full_name' or None)
    # print(name)


def account_details(request, pk=None):
    if pk:
        user = User.objects.select_related('details').get(pk=pk)
    context = {'user': user}
    return render(request, 'admin/account_details.html', context)


def admin_report(request):
    transaction_performed = Transactions.objects.all()
    template = get_template('admin/admin_report.html')
    context = {'transactions': transaction_performed}
    # html = template.render(context)
    pdf = render_to_pdf('admin/admin_report.html', context)
    return HttpResponse(pdf, content_type='application/pdf')
