from django.contrib import admin
from .models import Setup
# Register your models here.
class adminSetup(admin.ModelAdmin):
    list_display = ['btc', 'eth', 'bnb', 'ada', 'ltc', 'link', 'xrp']

admin.site.register(Setup, adminSetup)