from django.forms import model_to_dict
from django.http import JsonResponse
from .models import Setup
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