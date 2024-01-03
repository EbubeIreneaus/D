import json

from django.contrib.auth import authenticate
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from django.contrib.auth.models import User
from transaction.models import Transaction
from .models import Profile
import random
import string
from account.models import Account
from mail import Mail


def generate_profile_key(length):
    key = ''
    for i in range(length):
        key += random.choice(string.ascii_letters + string.digits)
    try:
        p = Profile.objects.get(id=key)
        generate_profile_key(length)
    except Profile.DoesNotExist:
        pass
    return key


def generate_key(length):
    key = ''
    for i in range(length):
        key += random.choice(string.ascii_letters + string.digits)
    return key


class Auth(APIView):
    def get(self, request):
        username = request.GET.get('username', '')
        password = request.GET.get('password', '')
        try:
            user = authenticate(username=username, password=password)
            if user is not None:
                profile = Profile.objects.get(user__id=user.id)
                if profile.verified:
                    return JsonResponse({'status': 'success', 'profileId': profile.id})
                else:
                    return JsonResponse({'status': 'unverified', 'profileId': profile.id})
            else:
                return JsonResponse({'status': 'failed', 'code': "user not found"})
        except Exception as e:
            return JsonResponse({'status': 'failed', 'code': str(e)})
            pass

    def post(self, request):
        data = json.loads(request.body)
        referral = None
        if 'referral' in data:
            try:
                referral = Profile.objects.get(user__username=data['referral'])
            except Exception as e:
                pass
        profileId = generate_profile_key(60)

        try:
            user = User.objects.create_user(
                first_name=data['firstname'], last_name=data['lastname'], email=data['email'],
                username=data['username'], password=data['password'])
            profile = Profile.objects.create(id=profileId, user=user, country_code=data['code'],
                                             phone=data['phone'], country=data['country'], referred_by=referral)
            account = Account(profile=profile, bonus=5.00, balance=5.00)
            account.save()
            return JsonResponse({'status': 'success', 'profileId': profile.id})
        except IntegrityError as ie:
            try:
                user = User.objects.get(username=data['username'])
                return JsonResponse({'status': 'failed', 'code': "username_already_exist"})
            except User.DoesNotExist:
                pass
            try:
                user = User.objects.get(email=data['email'])
                return JsonResponse({'status': 'failed', 'code': "email_already_exist"})
            except User.DoesNotExist:
                pass

        except Exception as e:
            return JsonResponse({'status': 'failed', 'code': str(e)})


def resend_link(request):
    profileId = request.GET.get('profileId', '')
    key = generate_key(70)
    try:
        profile = Profile.objects.get(id=profileId)
        profile.key = key
        email = profile.user.email
    except Exception as e:
        return JsonResponse({'status': 'failed', 'code': str(e)})
    try:
        mail = Mail(subject="Email Verification")
        mail.recipient = [email]
        mail.html_message = '<div><div style="font-family: Arial, sans-serif;max-width: 600px;margin: 0 auto;' \
                            'padding: 20px;border: 1px solid #e9e9e9;border-radius: 5px;"><h2> Dear User,' \
                            ' </h2 ><p>Thank you for registering on our website. Please click on the link below ' \
                            'to verify your account:</p ><p><a href = "{link}"style = "display:' \
                            ' inline-block;background-color: #4caf50;border: none;color: white;padding: 10px 20px;' \
                            'text-align: center;text-decoration: none;font-size: 16px;margin: 4px 2px;' \
                            'cursor: pointer;border-radius: 5px;">Verify Account</a></p ><p>' \
                            'If the button does not work, you can also copy and paste the following link into ' \
                            'your browser: </p ><p> {link} </p ><p> We are excited ' \
                            'to have you on board! </p></div>' \
                            '</div>'.format(link=f'https://digitalassetsgrowth.com/auth/verify/{profile.id}/{key}')
        mail.send_mail()
    except Exception as e:
        return HttpResponse(str(e))
    profile.save()
    return JsonResponse({'status': 'success', 'profileId': profile.id})



def psreset_link(request):
    username = request.GET.get('username', '')
    key = generate_key(70)
    try:
        user = User.objects.get(username=username)
        email = user.email
        profile = Profile.objects.get(user__id=user.id)
        profile.key = key
    except Exception as e:
        return JsonResponse({'status': 'failed', 'code': str(e)})
    try:
        mail = Mail(subject="Password Reset")
        mail.recipient = [email]
        mail.html_message = '<div><div style="font-family: Arial, sans-serif;max-width: 600px;margin: 0 auto;' \
                            'padding: 20px;border: 1px solid #e9e9e9;border-radius: 5px;"><h2> Dear User,' \
                            ' </h2 ><p>Thank you for investing with us. Please click on the link below ' \
                            'to reset your password:</p ><p><a href = "{link}"style = "display:' \
                            ' inline-block;background-color: #4caf50;border: none;color: white;padding: 10px 20px;' \
                            'text-align: center;text-decoration: none;font-size: 16px;margin: 4px 2px;' \
                            'cursor: pointer;border-radius: 5px;">Reset Password</a></p ><p>' \
                            'If the button does not work, you can also copy and paste the following link into ' \
                            'your browser: </p ><p> {link} </p ><p> please disregard this email ' \
                            'if you did not request for password resetting</p></div>' \
                            '</div>'.format(link=f'https://digitalassetsgrowth.com/auth/reset/{profile.id}/{key}')
        mail.send_mail()
    except Exception as e:
        return HttpResponse(str(e))
    profile.save()
    return JsonResponse({'status': 'success'})


@csrf_exempt
def verify_account(request):
    data = json.loads(request.body)
    key = data['key']
    profileId = data['profileId']
    try:
        profile = Profile.objects.get(id=profileId)
        if profile.verified:
            return JsonResponse({'status': 'failed'})
        if profile.key == key:
            try:
                account = Account.objects.get(profile__id=profileId)
                account.bonus = 5.00
                account.balance += 5.00
                account.save()
            except:
                pass
            profile.verified = True
            profile.key = None
            profile.save()
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'failed'})
    except Exception as e:
        return JsonResponse({'status': 'failed'})


@csrf_exempt
def reset(request):
    data = json.loads(request.body)
    key = data['key']
    profile_id = request.headers.get('profile-id')
    try:
        profile = Profile.objects.get(id=profile_id)
        user = User.objects.get(id=profile.user.id)
        if profile.key == key:
            user.set_password(data['password'])
            profile.key = None
            user.save()
            profile.save()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'failed', 'code': str(e)})
