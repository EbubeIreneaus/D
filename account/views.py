from django.shortcuts import render
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
