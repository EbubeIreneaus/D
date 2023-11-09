from django.contrib import admin
from .models import Transaction
# Register your models here.


class transAdmin(admin.ModelAdmin):
    list_display = ('profile', 'type', 'plan', 'amount', 'channel','progress')


admin.site.register(Transaction, transAdmin)