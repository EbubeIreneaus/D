import json

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from authentication.models import Profile
from .serializers import AccountSerial
from.models import Account
from django.http import JsonResponse
from authentication.serializers import ProfileSerial
# Create your views here.

def accountDetails(request, profileId):

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


