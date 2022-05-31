from django.shortcuts import render
from accounts.models import User, AccountDetails
from django.contrib import messages
from django.db.models.functions import Cast
from decimal import Decimal
from .models import Transactions
from django.core.mail import send_mail
from banking_system.settings import EMAIL_HOST_USER
from .forms import userchange, accountchange
import re
# Create your views here.


def transfer(request):
    current_user = request.user
    if request.method == 'POST':
        try:

            receiver_account_number = request.POST['recevier_number']
            amount = Decimal(request.POST['amount'])
            account_info = AccountDetails.objects.get(user=current_user)
            sender_balance = account_info.balance
            if sender_balance < amount:
                messages.info(request, 'Insuffient balance')
            elif (sender_balance-amount) < 1000:
                messages.info(
                    request, 'Minimum balance is 1000 and is not maintained')
            else:

                receiver_account = AccountDetails.objects.get(
                    account_number=receiver_account_number)
                receiver_balance = receiver_account.balance
                sender_balance_final = sender_balance-amount
                account_info.balance = sender_balance_final
                account_info.save()
                debit_transaction = Transactions()
                debit_transaction.debit_account = account_info.account_number
                debit_transaction.credit_account = receiver_account.account_number
                debit_transaction.name = account_info.full_name
                debit_transaction.operations = 'Transfer'
                debit_transaction.amount = amount
                debit_transaction.save()
                receiver_balance = receiver_balance+amount
                receiver_account.balance = receiver_balance
                receiver_account.save()
                """credit_transaction = Transactions()
                credit_transaction.account_no = receiver_account.account_number
                credit_transaction.name = receiver_account.full_name
                credit_transaction.operations = 'Credit'
                credit_transaction.amount = amount
                credit_transaction.save()"""
                subject = "Transaction notification"
                content_credit = "RS "+str(
                    amount)+" has been credited to your account with account number: "+receiver_account.account_number
                content_debit = "RS "+str(
                    amount)+" has been debited from your account with account number "+account_info.account_number

                to_credit = receiver_account.user.email
                to_debit = account_info.user.email
                send_mail(subject, content_credit,
                          EMAIL_HOST_USER, [to_credit])
                send_mail(subject, content_debit, EMAIL_HOST_USER, [to_debit])

                messages.success(
                    request, f"Transfer successfully completed")

        except:
            messages.warning(
                request, f"Transfer failed. Check the account number and amount you entered")
    context = {'account_number': 'account_number'}
    return render(request, 'transactions/transfer.html', context)


def deposit(request, pk=None):
    if pk:
        user = User.objects.select_related('details').get(pk=pk)
        print(user)
        if request.method == 'POST':
            print()
            deposit_account = AccountDetails.objects.get(user=user)
            account_balance = deposit_account.balance
            try:
                amount = Decimal(request.POST['amount'])

                final_deposit = account_balance+amount
            # print(type(amount))
                deposit_account.balance = final_deposit
                deposit_account.save()
        #########
                deposit_transaction = Transactions()
        # deposit_transaction.user=user
                deposit_transaction.account_no = user.details.account_number
                deposit_transaction.credit_account = user.details.account_number
                deposit_transaction.name = user.details.full_name
        # deposit_transaction.email_address=user.email
                deposit_transaction.amount = amount
                deposit_transaction.operations = 'Deposit'
                deposit_transaction.save()
                subject = "Transcation notification"
                content = "RS "+str(
                    amount)+" is credited into the account number "+deposit_account.account_number
        # content="jhfhfj"
                to = user.email
                send_mail(subject, content, EMAIL_HOST_USER, [to])
                messages.success(
                    request, f"Amount deposited successfully and transaction notification email send to customer")
                # raise Exception()

            except:
                messages.warning(
                    request, f"Deposit could not be conducted.Check the value you entered")

            # if isinstance(amount,Decimal):
                # print()
            """final_deposit=account_balance+amount
                    # print(type(amount))
                deposit_account.balance=final_deposit
                deposit_account.save()
            #########
                deposit_transaction=Transactions()
            # deposit_transaction.user=user
                deposit_transaction.account_no=user.details.account_number
                deposit_transaction.name=user.details.full_name
            # deposit_transaction.email_address=user.email
                deposit_transaction.amount=amount
                deposit_transaction.operations='Deposit'
                deposit_transaction.save()
                subject="Transcation notification"
                content=str(amount)+" is credited into the account number "+ \
                            deposit_account.account_number
            # content="jhfhfj"
                to = user.email
                send_mail(subject,content,EMAIL_HOST_USER,[to])
                messages.success(
                    request,f"Amount deposited successfully and confirmation mail send")
        # print(user.details.account_number)"""

            """else:
                    raise InvalidOperation """

            """    final_deposit=account_balance+amount
                    deposit_account.balance=final_deposit
                    deposit_account.save()
            #########
                    deposit_transaction=Transactions()
            # deposit_transaction.user=user
                    deposit_transaction.account_no=user.details.account_number
                    deposit_transaction.name=user.details.full_name
            # deposit_transaction.email_address=user.email
                    deposit_transaction.amount=amount
                    deposit_transaction.operations='Deposit'
                    deposit_transaction.save()
                    subject="Transcation notification"
                    content=str(
                        amount)+" is credited into the account number "+deposit_account.account_number
            # content="jhfhfj"
                    to = user.email
                    send_mail(subject,content,EMAIL_HOST_USER,[to])
                    messages.success(request,f"Amount deposited successfully and confirmation mail send")"""

        # print(user.details.account_number)
    # else:
 #   user=request.user

    # if request.method='POST':

    # account=AccountDetails.objects.get(user=pk)
    # print(account)
    return render(request, 'transactions/deposit.html', {'user': user})


def check_phone(phone_number):
    if (len(phone_number) != 10):
        return False


def check_email(email_address):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if(re.search(regex, email_address)):
        return False


def edit_user_details(request, pk=None):
    """user_form = userchange(instance=request.user)
    detail_form = accountchange(instance=request.user.details)"""
    if pk:
        user = User.objects.select_related('details').get(pk=pk)
        # user_form = userchange(instance=request.user)
        user_form = userchange(instance=user)
        # detail_form = accountchange(instance=request.user.details)
        detail_form = accountchange(instance=user.details)
        form_1 = userchange(request.POST or None, instance=user)
        form_2 = accountchange(request.POST or None, instance=user.details)

        """if request.method == 'POST':
            form_1 = userchange(request.POST, instance=user)
            form_2 = accountchange(request.POST, instance=user.details)
            if form_1.is_valid() and form_2.is_valid():
                form_email = form_1.cleaned_data.get('email')
                form_phone = form_2.cleaned_data.get('phone')
                res_1 = check_email(form_email)
                res_2 = check_phone(form_phone)
                if res_1:
                    messages.error(request, f"Invalid Email address")
                else:
                    form_1.save()
                    messages.success(
                        request, f"Changes were successfull. But may take time to reflect. Do not refresh!!")
                if res_2:
                    messages.error(request, f"Invalid Phone number")
                else:
                    form_2.save()
                    messages.success(
                        request, f"Changes were successfull. But may take time to reflect. Do not refresh!!")"""
        if (form_1.is_valid() and form_2.is_valid()):
            form_1.save()
            form_2.save()
            messages.success(
                request, f"Changes were successfull. But may take time to reflect. Do not refresh!!")

    # user_form = userchange(instance=request.user)
    # detail_form = accountchange(instance=request.user.details)
    context = {'user_form': form_1, 'detail_form': form_2}
    return render(request, 'admin/edit_user_details.html', context)
