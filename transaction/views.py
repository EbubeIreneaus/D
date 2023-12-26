import json
import re

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.mail import mail_admins, EmailMultiAlternatives
from django.db import transaction
from django.utils import timezone

from authentication.models import Profile
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import DepositForm
from account.models import Account
from .models import Transaction
import random
import string
from mail import Mail
from .serializers import TransactionSerializer as ts


# Create your views here.


class customException(Exception):
    pass
def updateTransactions(userId):
    try:
        with transaction.atomic():
            now = timezone.now()
            ts = Transaction.objects.filter(profile__id=userId)
            tplan = {'standard':0.25,'silver':0.599,'premium':3.6,'ultra':9.0}
            for x in ts:
                if x.type == 'invest' and now >= x.end_date and x.progress == 'active':
                    trans = Transaction.objects.get(pk = x.pk)
                    account = Account.objects.get(profile__id = trans.profile.id)
                    earning = float(tplan[trans.plan]) * float(trans.amount)
                    trans.progress = 'completed'
                    account.balance = float(account.balance) + float(trans.amount) + float(earning)
                    account.active_investment -= trans.amount
                    account.Total_earnings = float(account.Total_earnings) + earning
                    trans.save()
                    account.save()
    except Exception as e:
        print(str(e))
    return True

def validate_deposit(amount, plan, profileId):
    if not amount or amount == '' or amount is None or not plan or plan == '' or plan is None:
        return False
    if (100 <= amount <= 2000) and plan != 'standard':
        return False
    if (2001 <= amount <= 20000) and plan != 'silver':
        return False
    if (20001 <= amount <= 100000) and plan != 'premium':
        return False
    if (amount > 100000) and plan != 'ultra':
        return False
    try:
        account = Account.objects.get(profile__id=profileId)
        if account.balance < amount:
            return False
    except Exception:
        return False
    return True


def getTransact(request):
    profileId = request.GET.get('profileId', '')
    if updateTransactions(profileId):
        try:
            transactions = Transaction.objects.filter(profile__id=profileId).order_by('-id')
            st = ts(transactions, many=True)
            return JsonResponse(st.data, safe=False)
        except Exception as e:
            return HttpResponse(str(e))


def send_deposit_mail(amount, id, channel, address, email):
    try:
        mail = Mail(subject="New Transaction Summary")
        mail.recipient = [email]
        mail.html_message = f'<h2 style="text-align:center"><strong>New Transaction Summary</strong></h2><p><strong>you just initiated a new transaction. ' \
                            'below are the details of your transaction</strong></p><br><ul><li><strong><span style="font-size:16px">Transaction Id:</span>' \
                            f' {id}</strong></li><br><li><strong><span style="font-size:16px">Transaction Amount:</span>' \
                            f' {amount}/strong></li><br><li><strong><span style="font-size:16px"><strong>Transaction Type: Deposit</strong></span></strong></li>' \
                            f'<li><span style="font-size:16px"><strong>Payment Channel: {channel}</strong></span></li><br><li><span style="font-size:16px">' \
                            f'<strong>Channel Address:  {address} </strong></span></li><li><span style="font-size:16px">' \
                            '<strong>Transaction Status: pending</strong></span></li></ul><br>' \
                            '\<p><span style="font-size:16px">Kindly reply this mail with a proof of payment or reach us out at' \
                            ' <a href="mailto:support@digitalassets.com.ng">support@digitalassets.com.ng</a>&nbsp;or visit ' \
                            '<a href="https://digitalassets.com">https://digitalassets.com</a>&nbsp;</span></p>' \
                            '<h3><span style="color:#2ecc71"><br>' \
                            '<span style="font-size:12px"><strong><span style="font-family:Arial,Helvetica,sans-serif">' \
                            'Thank you for investing with Digital Assets, your finacial growth is all we care for</span></strong>' \
                            '</span></span></h3>'
        mail.send_mail()
    except Exception as e:
        pass


def send_invest_mail(amount, id, plan, email):
    roi = 0
    period = None
    if plan == 'standard':
        roi = 0.25 * amount
        period = "5days"
    elif plan == "silver":
        plan = 0.599 * amount
        period = "7days"
    elif plan == "premium":
        roi = 3.6 * amount
        period = "30days"
    elif plan == "ultra":
        roi = 9 * amount
        period = "90days"
    total_return = f'${float(roi + amount):,.2f}'
    roi = f'${roi:,.2f}'
    amount = f'${amount:,.2f}'
    try:
        mail = Mail(subject="New Transaction Summary")
        mail.recipient = [email]
        mail.html_message = '<h2 style="text-align:center"><strong>New Transaction Summary</strong></h2><p>' \
                            '<span style="font-size:16px"><strong>new investment alert</strong></span></p>' \
                            f'<p><span style="font-size:16px"><strong>PLAN: {plan}</strong></span></p>' \
                            f'<p><span style="font-size:16px"><strong>AMOUNT: {amount}</strong></span></p>' \
                            f'<p><span style="font-size:16px"><strong>RETURN OF INVESTMENT: {roi}</strong></span></p>' \
                            f'<p><span style="font-size:16px"><strong>TOTAL RETURN: {total_return}</strong></span></p>' \
                            '<p><span style="font-family:Arial,Helvetica,sans-serif"><span style="font-size:16px">' \
                            f'<strong>INVESTMENT PERIOD: {period}</strong></span></span></p>' \
                            '<p><span style="font-size:16px">Kindly&nbsp; reach us out at ' \
                            '<a href="mailto:support@digitalassets.com.ng">support@digitalassets.com.ng</a>' \
                            '&nbsp;or visit <a href="https://digitalassets.com">https://digitalassets.com</a>&nbsp;' \
                            'if You have any issues.</span></p><h3><span style="color:#2ecc71">' \
                            '<span style="font-size:12px"><strong><span style="font-family:Arial,Helvetica,sans-serif">' \
                            'Thank you for investing with Digital Assets, your financial growth is all we care for</span>' \
                            '</strong></span></span></h3>'
        mail.send_mail()
    except Exception as e:
        pass


def generate_transact_key(length):
    key = ''
    for i in range(length):
        key += random.choice(string.ascii_letters + string.digits)
    try:
        t = Transaction.objects.get(transact_id=key)
        generate_transact_key(length)
    except Transaction.DoesNotExist:
        pass
    return key


@csrf_exempt
def deposit(request):
    data = json.loads(request.body)
    dp = {
        'channel': data['channel'],
        "amount": data['amount']
    }
    profileId = request.headers.get('profile-id', '')
    key = generate_transact_key(30)
    try:
        profile = Profile.objects.get(id=profileId)
        deposit = DepositForm(dp)
        if deposit.is_valid():
            amount = deposit.cleaned_data['amount']
            channel = deposit.cleaned_data['channel']
            transaction = Transaction.objects.create(profile=profile, transact_id=key, amount=amount, channel=channel,
                                                     type='deposit')
            send_deposit_mail(amount=amount, id=key, channel=channel, address=data['wallet'], email=profile.user.email)
            return JsonResponse({'status': 'success', 'id': transaction.transact_id, 'channel': channel,
                                 'address': data['wallet']})
        else:
            return JsonResponse({'status': 'failed', 'code': str(deposit.errors)})
    except Exception as e:
        return JsonResponse({'status': 'failed', "code": str(e)})


@csrf_exempt
def invest(request):
    data = json.loads(request.body)
    key = generate_transact_key(30)

    try:
        try:
            profile = Profile.objects.get(id=data['profileId'])
        except Profile.DoesNotExist:
            return JsonResponse({'status': 'failed', 'code': 'user_not_found'})

        if not validate_deposit(amount=data['amount'], plan=data['plan'], profileId=data['profileId']):
            return JsonResponse({'status': 'failed', 'code': 'bad_data_integrity'})

        transaction = Transaction(profile=profile, transact_id=key, plan=data['plan'], amount=data['amount'],
                                  type='invest')
        account = Account.objects.get(profile__id=data['profileId'])
        account.balance = account.balance - data['amount']
        account.active_investment += data['amount']
        transaction.save()
        account.save()
        try:
            send_invest_mail(amount=data['amount'], id=transaction.id, plan=data['plan'], email=profile.user.email)
        except Exception:
            pass
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'failed', 'code': str(e)})


def validate_withdraw(amount, profileid, wallet_address, password):
    try:
        amount = int(amount)
        if re.search('[!@#$%^()-+=:;\'\"<>?~]', wallet_address):
            raise customException('Invalid Wallet Address')
        if type(amount) != int:
            raise customException('amount must be a number, undefined character given')
        try:
            profile = Profile.objects.get(id=profileid)
            user = User.objects.get(id=profile.user.id)
            user = authenticate(username=user.username, password=password)
            if user is None:
                raise customException("Incorrect Password")
        except:
            raise customException("Incorrect Password")
        account = Account.objects.get(profile__id=profileid)
        if account.balance < amount:
            raise customException('Insufficient Funds !!!')

    except Account.DoesNotExist:
        return {'status': 'failed', 'code': 'unidentified user please Sign In again!!!'}

    except customException as e:
        return {'status': 'failed', 'code': str(e)}
    except Exception as e:
        return {'status': 'failed', 'code': 'unknown error please try again later!!!'}
    return {'status': 'true'}


@csrf_exempt
def withdraw(request):
    data = json.loads(request.body)
    key = generate_transact_key(30)

    try:
        try:
            profile = Profile.objects.get(id=data['profileId'])
        except Profile.DoesNotExist:
            return JsonResponse({'status': 'failed', 'code': 'user_not_found'})

        validate = validate_withdraw(amount=data['amount'], profileid=profile.id, wallet_address=data['wallet'],
                                     password=data['password'])
        if validate['status'] != 'true':
            return JsonResponse({'status': 'failed', 'code': str(validate['code'])})
        Transaction.objects.create(profile=profile, transact_id=key, amount=data['amount'],
                                   channel=data['channel'], address=data['wallet'], type='withdraw')
        return JsonResponse({'status': 'success'})

    except Exception as e:
        return JsonResponse({'status': 'failed', 'code': str(e)})

@csrf_exempt
def pay_slip(request):
    transactId = request.POST.get('id', '')
    amount = request.POST.get('amount', '')
    channel = request.POST.get('channel', '')
    file = request.FILES.get('file', '')

    try:
        message = f'<h4><font color="#000000" style=""><span style="font-family: &quot;Arial Black&quot;;">' \
                  f'<b style="">Some just sent you a payment slip:</b></span></font></h4><p><font color="#000000" face="Arial Black">' \
                  f'<b>Id: </b><span> {transactId} </span></font></p>' \
                  f'<p><font color="#000000" face="Arial Black"><b>Amount:</b><span> {amount} </span></font></p>' \
                  f'<p><font color="#000000" face="Arial Black"><b>Channel:</b><span> {channel} </span></font></p>' \
                  f'<p style="text-align: left;"><font color="#000000" face="Arial Black"><span style="font-family: Arial;">' \
                  f'see payment slip below</span></font></p>'
        try:
            email = EmailMultiAlternatives(
                subject="Payment Confirmation",
                body="Someone Just Sent A payment slip",
                to=["okigweebube7@gmail.com"],

            )
            email.attach_alternative(message, 'text/html')
            email.attach(file.name, file.read(), file.content_type)
            email.send(fail_silently=False)
        except Exception as e:
            return JsonResponse({'status': 'failed', "code": str(e)})
        return JsonResponse({'status': 'success'})
    except:
        return JsonResponse({'status': 'failed'})
