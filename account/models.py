from django.db import models
from authentication.models import Profile


# Create your models here.
class Account(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    balance = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    active_investment = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    total_withdrawal = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    Total_earnings = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    last_deposit = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    last_withdraw = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    # total_deposit = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    # total_withdraw = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    referral_bonus = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    bonus = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    date = models.DateField(auto_now=True)

