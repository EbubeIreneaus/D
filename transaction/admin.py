from django.contrib import admin
from .models import Transaction
# Register your models here.


class transAdmin(admin.ModelAdmin):
    list_display = ('profile', 'type', 'plan', 'amount', 'channel','progress')
    search_fields = ['id', 'transact_id', 'profile']

admin.site.register(Transaction, transAdmin)