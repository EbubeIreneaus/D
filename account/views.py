import json

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from transaction.views import updateTransactions
from authentication.models import Profile
from .serializers import AccountSerial
from.models import Account
from django.http import JsonResponse
from authentication.serializers import ProfileSerial
# Create your views here.

def accountDetails(request, profileId):
    try:
        updateTransactions(profileId)
    except:
        pass
    try:
        account = Account.objects.get(profile__id = profileId)
        serialized_account = AccountSerial(account)
        return JsonResponse(serialized_account.data, safe=False)
    except Account.DoesNotExist:
        return JsonResponse({'status':'failed', 'code':'account_not_found'})
    except Exception as e:
        return JsonResponse({'status': 'failed', 'code': str(e)})

@csrf_exempt
def change_user_data(request):
    data = json.loads(request.body)
    profileId = request.headers.get('profile-id','')
    if data['first_name'] != '' or data['last_name'] != '':
        try:
            profile = Profile.objects.get(id=profileId)
            user = User.objects.get(id=profile.user.id)
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.save()
            return JsonResponse({'status':'success'})
        except Exception:
            pass
    return JsonResponse({'status':'failed'})


@csrf_exempt
def change_profile_data(request):
    data = json.loads(request.body)
    profileId = request.headers.get('profile-id','')
    if data['phone'] != '' or data['country'] != '':
        try:
            profile = Profile.objects.get(id=profileId)
            profile.country = data['country']
            profile.country_code = data['code']
            profile.phone = data['phone']
            profile.save()
            return JsonResponse({'status':'success'})
        except Exception:
            pass
    return JsonResponse({'status':'failed'})

@csrf_exempt
def change_security_data(request):
    data = json.loads(request.body)
    profileId = request.headers.get('profile-id','')
    if data['new'] != '' or data['old'] != '':
        try:
            profile = Profile.objects.get(id=profileId)
            user = authenticate(username=profile.user.username, password=data['old'])
            if user is not None:
                user.set_password(data['new'])
                user.save()
                return JsonResponse({'status':'success'})
        except Exception:
            pass
    return JsonResponse({'status':'failed'})

def get_referrals(request):
    profileId = request.GET.get('profile-id', '')

    try:
        profiles = Profile.objects.filter(referred_by__id=profileId)
        serialProfiles = ProfileSerial(profiles, many=True)
        return JsonResponse(serialProfiles.data, safe=False)
    except Exception as e:
        return JsonResponse({'status':'failed', 'code':str(e)})

def transfer(request):
    profileId = request.headers.get('profile-id', '')
    amount = request.GET.get('amount', '')
    total_debit = amount + (0.2 * amount)
    user = request.GET.get('user', '')
    try:
        profile = Profile.objects.get(id=profileId)
        user = User.objects.get(Q(username=user) | Q(email=user))
        reciever_profile = Profile.objects.get(user__id = user.id)
        sender_acct = Account.objects.get(profile__id = profileId)
        reciever_acct = Account.objects.get(profile__id = reciever_profile.id)
        if float(sender_acct.balance) < float(amount):
            return JsonResponse({'status': 'failed', 'code': 'Insufficient Account Balance!'})
        sender_acct.balance = float(sender_acct.balance) - float(total_debit)
        reciever_acct.balance = float(reciever_acct.balance) + float(amount)
        sender_acct.save()
        reciever_acct.save()
        return JsonResponse({'status': 'success', 'code': 'transfer successfull'})
    except User.DoesNotExist:
        return JsonResponse({'status': 'failed', 'code': 'No account found on our database!'})
    except User.MultipleObjectsReturned:
        return JsonResponse({'status': 'failed', 'code': 'More than one user found try sending with username!!'})
    except Exception as e:
        return JsonResponse({'status': 'failed', 'code': 'unknown Error occured!', 'msg':str(e)})

