from django.db import models

# Create your models here.

class Setup(models.Model):
    usd = models.DecimalField(max_digits=10, default=0.0, decimal_places=2)
    btc = models.DecimalField(max_digits=10, default=0.0, decimal_places=2)
    eth = models.DecimalField(max_digits=10, default=0.0, decimal_places=2)
    ltc = models.DecimalField(max_digits=10, default=0.0, decimal_places=2)
    bnb = models.DecimalField(max_digits=10, default=0.0, decimal_places=2)
    link = models.DecimalField(max_digits=10, default=0.0, decimal_places=2)
    ada = models.DecimalField(max_digits=10, default=0.0, decimal_places=2)
    aave = models.DecimalField(max_digits=10, default=0.0, decimal_places=2)
    usdt = models.DecimalField(max_digits=10, default=0.0, decimal_places=2)
    bch = models.DecimalField(max_digits=10, default=0.0, decimal_places=2)
    xrp = models.DecimalField(max_digits=10, default=0.0, decimal_places=2)
    xlm = models.DecimalField(max_digits=10, default=0.0, decimal_places=2)
    date = models.DateField(auto_now=True)