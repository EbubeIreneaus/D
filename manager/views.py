from django.core.mail import EmailMultiAlternatives
from django.forms import model_to_dict
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Setup
from mail import Mail
# Create your views here.

def convert(request):
    source = request.GET.get('source', '')
    destination = request.GET.get('destination', '')
    no = request.GET.get('amount', '')
    try:
        setups = Setup.objects.get(pk=1)
        setups = model_to_dict(setups)
        source_unit_price = float(setups[source])
        destination_unit_price = float(setups[destination])
        source_price = float(source_unit_price) * float(no)
        return JsonResponse({'status':'success', 'return': source_price/destination_unit_price})
    except Exception as e:
        return JsonResponse({'status':'failed', 'code':str(e)})

def getWithdrawCharges(request):
    try:
        setups = Setup.objects.get(pk=1)
        return JsonResponse({'charges': setups.withdraw_charges})
    except:
        return JsonResponse({'charges': 0})

@csrf_exempt
def notifyAdminForVerification(request):
    firstname = request.POST.get('firstname', 'nill')
    lastname = request.POST.get('lastname', 'nill')
    middlename = request.POST.get('middlename', 'nill')
    country = request.POST.get('country', 'nill')
    address = request.POST.get('address', 'nill')
    city = request.POST.get('city', 'nill')
    dob = request.POST.get('dob', 'nill')
    postal = request.POST.get('postal', 'nill')
    idDocs = request.POST.get('id', 'nill')
    username = request.POST.get('username', 'nill')
    email = request.POST.get('email', 'nill')
    docImg = request.FILES.get('IDCard', 'nill')
    selfieImg = request.FILES.get('selfie', 'nill')

    message = '<div style="padding: 0 1rem; max-width:646px; margin:auto">' \
              '<h2>Presonnal Information</h2>' \
              '<ul style="list-style: none; color: rgba(0, 0, 0, 0.5); font-weight: 600; font-size: 0.875rem; ' \
              'margin-bottom: 1rem; padding-left: 1rem;">' \
              '<li style="margin-bottom: 0.5rem; padding-right: 1rem; ">' \
              '<i style="margin-right: 0.5rem;" class="">First Name:</i>' \
              f'<span style="float: right;">{firstname}</span></li>' \
              '<li style="margin-bottom: 0.5rem; padding-right: 1rem; ">' \
              '<i style="margin-right: 0.5rem;" class="">Last Name:</i>' \
              f'<span style="float: right;">{lastname}</span></li>' \
              '<li style="margin-bottom: 0.5rem; padding-right: 1rem; ">' \
              '<i style="margin-right: 0.5rem;" class="">Middle Name:</i>' \
              f'<span style="float: right;">{middlename}</span></li>' \
              '<li style="margin-bottom: 0.5rem; padding-right: 1rem; ">' \
              '<i style="margin-right: 0.5rem;" class="">Date Of Birth:</i>' \
              f'<span style="float: right;">{dob}</span>' \
              '</li>' \
              '</ul>' \
              '<h2>Location &amp; Address</h2>' \
              '<ul style="list-style: none; color: rgba(0, 0, 0, 0.5); font-weight: 600; font-size: 0.875rem; ' \
              'margin-bottom: 1rem; padding-left: 1rem;">' \
              '<li style="margin-bottom: 0.5rem; padding-right: 1rem; ">' \
              '<i style="margin-right: 0.5rem;" class="fa fa-user">Country:</i>' \
              f'<span style="float: right;">{country}</span></li>' \
              '<li style="margin-bottom: 0.5rem; padding-right: 1rem; ">' \
              '<i style="margin-right 0.5rem;" class="fa fa-user">City:</i>' \
              f'<span style="float: right;">{city}</span>' \
              '</li><li style="margin-bottom: 0.5rem; padding-right: 1rem; ">' \
              '<i style="margin-right: 0.5rem;" class="fa fa-user">Residential Address:</i>' \
              f'<span style="float: right;">{address}</span></li>' \
              '<li style="margin-bottom: 0.5rem; padding-right: 1rem; ">' \
              '<i style="margin-right: 0.5rem;" class="fa fa-user">Postal code:</i>' \
              f'<span style="float: right;">{postal}</span></li></ul><h2>Documents</h2>' \
              '<ul style="list-style: none; color: rgba(0, 0, 0, 0.5); font-weight: 600; font-size: 0.875rem; ' \
              'margin-bottom: 1rem; padding-left: 1rem;"><li style="margin-bottom: 0.5rem; padding-right: 1rem; ">' \
              '<i style="margin-right: 0.5rem;" class="fa fa-user">Document Type:</i>' \
              f'<span style="float: right;">{idDocs}</span></li></ul><h2>Digital Assets Account</h2>' \
              '<ul style="list-style: none; color: rgba(0, 0, 0, 0.5); font-weight: 600; font-size: 0.875rem;' \
              ' margin-bottom: 1rem; padding-left: 1rem;">'\
              '<li style="margin-bottom: 0.5rem; padding-right: 1rem; ">' \
              '<i style="margin-right: 0.5rem;" class="fa fa-user">username:</i>' \
              f'<span style="float: right;">{username}</span></li>' \
              '<li style="margin-bottom: 0.5rem; padding-right: 1rem; ">' \
              '<i style="margin-right: 0.5rem;" class="fa fa-user">email:</i>' \
              f'<span style="float: right;">{email}</span></li></ul><br />' \
              '<div class="w-full "><p class="text-sm mt-2 mb-4 text-black/50">see documents images below:</p>' \
              '</div></div>'

    try:
        email = EmailMultiAlternatives(
            subject="Account Verification",
            body="Request to verify account",
            to=["okigweebube7@gmail.com", 'service@digitalassets.com.ng'],

        )
        email.attach_alternative(message, 'text/html')
        email.attach(docImg.name, docImg.read(), docImg.content_type)
        email.attach(selfieImg.name, selfieImg.read(), selfieImg.content_type)
        email.send(fail_silently=False)
    except Exception as e:
        return JsonResponse({'status': 'failed', "code": str(e)})
    return JsonResponse({'status': 'success'})

@csrf_exempt
def notifyAdminForVerificationPlus(request):
    address = request.POST.get('address', 'nill')
    city = request.POST.get('city', 'nill')
    postal = request.POST.get('postal', 'nill')
    username = request.POST.get('username', 'nill')
    email = request.POST.get('email', 'nill')
    docImg = request.FILES.get('IDCard', 'nill')


    message = '<div style="padding: 0 1rem; max-width:646px; margin:auto">' \
              '<h2>Location &amp; Address</h2>' \
              '<ul style="list-style: none; color: rgba(0, 0, 0, 0.5); font-weight: 600; font-size: 0.875rem; ' \
              'margin-bottom: 1rem; padding-left: 1rem;">' \
              '<li style="margin-bottom: 0.5rem; padding-right: 1rem; ">' \
              '<i style="margin-right 0.5rem;" class="fa fa-user">City:</i>' \
              f'<span style="float: right;">{city}</span>' \
              '</li><li style="margin-bottom: 0.5rem; padding-right: 1rem; ">' \
              '<i style="margin-right: 0.5rem;" class="fa fa-user">Residential Address:</i>' \
              f'<span style="float: right;">{address}</span></li>' \
              '<li style="margin-bottom: 0.5rem; padding-right: 1rem; ">' \
              '<i style="margin-right: 0.5rem;" class="fa fa-user">Postal code:</i>' \
              f'<span style="float: right;">{postal}</span></li></ul><h2>Documents</h2>' \
              '<ul style="list-style: none; color: rgba(0, 0, 0, 0.5); font-weight: 600; font-size: 0.875rem; ' \
              'margin-bottom: 1rem; padding-left: 1rem;"></ul><h2>Digital Assets Account</h2>' \
              '<ul style="list-style: none; color: rgba(0, 0, 0, 0.5); font-weight: 600; font-size: 0.875rem;' \
              ' margin-bottom: 1rem; padding-left: 1rem;">'\
              '<li style="margin-bottom: 0.5rem; padding-right: 1rem; ">' \
              '<i style="margin-right: 0.5rem;" class="fa fa-user">username:</i>' \
              f'<span style="float: right;">{username}</span></li>' \
              '<li style="margin-bottom: 0.5rem; padding-right: 1rem; ">' \
              '<i style="margin-right: 0.5rem;" class="fa fa-user">email:</i>' \
              f'<span style="float: right;">{email}</span></li></ul><br />' \
              '<div class="w-full "><p class="text-sm mt-2 mb-4 text-black/50">see documents images below:</p>' \
              '</div></div>'

    try:
        email = EmailMultiAlternatives(
            subject="Account Plus Verification",
            body="Request to verify account to Plus",
            to=["okigweebube7@gmail.com", 'service@digitalassets.com.ng'],

        )
        email.attach_alternative(message, 'text/html')
        email.attach(docImg.name, docImg.read(), docImg.content_type)
        email.send(fail_silently=False)
    except Exception as e:
        return JsonResponse({'status': 'failed', "code": str(e)})
    return JsonResponse({'status': 'success'})