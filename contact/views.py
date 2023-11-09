import json

from django.shortcuts import render
from .models import Feedback
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from .forms import ContactForm
from mail import Mail
from django.core.mail import mail_admins
# Create your views here.

class Contact(APIView):
    def post(self, request):
        # data = json.loads()
        f = ContactForm(json.loads(request.body))
        if f.is_valid():
            f.save()
            message = f'<h4><font color="#000000" style=""><span style="font-family: &quot;Arial Black&quot;;">' \
                      f'<b style="">Some just sent you a message:</b></span></font></h4><p><font color="#000000" face="Arial Black">' \
                      f'<b>Full Name:</b><span> {f.cleaned_data["first_name"]} {f.cleaned_data["last_name"]} </span></font></p>' \
                      f'<p><font color="#000000" face="Arial Black"><b>Email:</b><span> {f.cleaned_data["email"]} </span></font></p>' \
                      f'<h2 style="text-align: center; "><font color="#000000" face="Arial Black"><u><span style="font-family: Arial;">' \
                      f'{f.cleaned_data["subject"]}</span>' \
                      f'</u></font></h2><p style="text-align: left;"><font color="#000000" face="Arial Black"><span style="font-family: Arial;">' \
                      f'{f.cleaned_data["message"]}</span></font></p>'
            try:
               mail_admins(subject=f.cleaned_data['subject'], html_message=message, fail_silently=False, message="someone just message you"
                                                                                             "check your admin dashboard")

            except Exception as e:
                return JsonResponse({'status':'failed', "code":str(e)})
            return JsonResponse({'status':'success'})