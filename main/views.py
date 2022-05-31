#import xlsxwriter
from reportlab.platypus import SimpleDocTemplate, Table
from reportlab.lib.pagesizes import letter
from django.shortcuts import render, redirect
from .forms import UserLoginForm, FeedbackForm, userchange, accountchange
from django.contrib.auth import authenticate, login, logout
from accounts.models import User, AccountDetails, Feedback
from transactions.models import Transactions
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from accounts.backends import CustomBackend
from django.contrib.auth.forms import UserChangeForm
from .otp import generate_otp
from django.core import serializers
#from pyxml2pdf import xm
from .utils import render_to_pdf
from django.template.loader import get_template
from django.http import HttpResponse
from itertools import chain
user_var = None


def landing_page(request):
    return render(request, 'landing/index.html')


def account_page(request):
    return render(request, 'landing/account_base.html')


def login_page(request):
    user_login_form = UserLoginForm(request.POST or None)
    if request.method == 'POST' and user_login_form.is_valid():
        # account_no=user_login_form.cleaned_data['account_number']
        email = user_login_form.cleaned_data['email']
        password = user_login_form.cleaned_data['password']

        user = authenticate(email=email, password=password)

        if user:
            login(request, user)
            return redirect('landing_page')

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
        'user_login_form': user_login_form
    }

    return render(request, 'landing/login.html', context)

    #user_login_form = UserLoginForm(request.POST or None)
    """if request.POST and user_login_form.is_valid():
        #user=user_login_form.login(request)
        if user:
            login(request,user)
            return redirect('landing_page')

    else:
        print('harsh')

    try:
        user =user_login_form.login(request)
    except User.DoesNotExist:
        print('error')
    if user:
            login(request,user)
            return redirect('landing_page')"""

    # if request.user.is_authenticated:
    # pass
   # else:

    #account_no = user_login_form.cleaned_data.get('account_number')
    #   email = user_login_form.cleaned_data.get('email')
    #  password = user_login_form.cleaned_data.get('password')
    # user = authenticate(account_number=account_no,
    #                    email=email, password=password)

    # if user is not None:
    #    login(request,user)#,backend='accounts.backends.CustomBackend'
    #messages.success(request, "Message sent." )
    #   return redirect('landing_page')
    # else:
    #   print('work')
    #  return redirect('landing_page')

    # context = {
    #   'user_login_form': user_login_form
    # }
    # return render(request, 'landing/login.html', context)"""


def otp(request):
    if request.method == 'POST':
        gen_otp = generate_otp()
        revived_otp = request.POST['otp']
        if generate_otp == revived_otp:
            login(request, user_var)
            redirect('landing_page')
        else:
            messages.success(
                request, f"Login failed.Please check the email and password")
    else:
        return render(request, 'landing/otp')


def logout_page(request):
    logout(request)
    return redirect('landing_page')


def transaction_history(request):
    current_user = request.user
    account_detail_obj = AccountDetails.objects.get(user=current_user)
    account_transaction_history = account_detail_obj.account_number
    """transaction_performed = Transactions.objects.filter(
        account_no=account_transaction_history)"""
    transaction_performed_1 = Transactions.objects.filter(
        credit_account=account_transaction_history)
    transaction_performed_2 = Transactions.objects.filter(
        debit_account=account_transaction_history)
    transactions = list(
        chain(transaction_performed_1, transaction_performed_2))
    #transactions = transaction_performed.values()

    """XMLSerializer = serializers.get_serializer("xml")
    xml_serializer = XMLSerializer()

    with open('state.xml', 'w') as out:
        xml_serializer.serialize(transaction_performed, stream=out)

    xml2pdf.genpdf(state.xml, state1.pdf)

    lst = list(transactions)
    dict = transactions.__dict__
    dict2 = dict.values()
    # print(dict2)

    workbook = xlsxwriter.Workbook('state.xlsx')
    worksheet = workbook.add_worksheet()
    row = 0
    col = 0
    for credit_acc, debit_acc, name, operation in lst.items():
        worksheet.write(row, col,     item)
        worksheet.write(row, col + 1, cost)
        row += 1
    workbook.close()"""

    return render(request, 'landing/transaction_history.html', {'transactions': transactions})


def statement(request):
    current_user = request.user
    account_detail_obj = AccountDetails.objects.get(user=current_user)
    account_transaction_history = account_detail_obj.account_number
    """transaction_performed = Transactions.objects.filter(
        account_no=account_transaction_history)
    transactions = transaction_performed.values()"""
    transaction_performed_1 = Transactions.objects.filter(
        credit_account=account_transaction_history)
    transaction_performed_2 = Transactions.objects.filter(
        debit_account=account_transaction_history)
    transactions = list(
        chain(transaction_performed_1, transaction_performed_2))

    template = get_template('landing/statement.html')
    """context = {
        "credit_account": transaction_performed.values('credit_account'),
        "debit_account": transactions.debit_account,
        # "operation": transactions.operations
    }"""
    context = {'transactions': transactions}
    html = template.render(context)
    pdf = render_to_pdf('landing/statement.html', context)
    return HttpResponse(pdf, content_type='application/pdf')


def feedback(request):
    if (request.method == 'POST'):
        current_user = request.user
        account_obj = AccountDetails.objects.get(user=current_user)
        feedback_obj = Feedback()
        feedback_obj.user_account_no = account_obj.account_number
        feedback_obj.user_name = account_obj.full_name
        feedback_obj.subject = request.POST['subject']
        feedback_obj.message = request.POST['feedback']
        feedback_obj.save()
        messages.success(
            request, f"Feedback registered!!Your feedback is valuable to us")

    return render(request, 'landing/feedback.html')


def edit_details(request):
    user_form = userchange(instance=request.user)
    detail_form = accountchange(instance=request.user.details)

    if request.method == 'POST':
        form_1 = userchange(request.POST, instance=request.user)
        form_2 = accountchange(request.POST, instance=request.user.details)
        if form_1.is_valid() and form_2.is_valid():
            data = form_2.cleaned_data.get("phone")
            if(len(data) != 10):
                messages.error(
                    request, f"Invalid phone number! Please check the entered number")

            else:
                form_1.save()
                form_2.save()
                messages.success(
                    request, f"Details updated successfully!")

            # print(data)
            # form_1.save()
            # form_2.save()
            # return render(request, 'landing/edit_details.html')

    # else:
    #user_form = userchange(instance=request.user)
    #detail_form = accountchange(instance=request.user.details)
    context = {'user_form': user_form, 'detail_form': detail_form}
    return render(request, 'landing/edit_details.html', context)


def about_us(request):
    return render(request, 'landing/about_us.html')
