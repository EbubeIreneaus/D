from django.contrib import admin
from .models import Account

class accountAdmin(admin.ModelAdmin):
    list_display = ['profile', 'balance', 'active_investment', 'referral_bonus', 'bonus']
    search_fields = ['profile', 'id']
# Register your models here.
admin.site.register(Account, accountAdmin)