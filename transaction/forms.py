from django.forms import ModelForm
from .models import Transaction


class DepositForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ['channel', 'amount']
