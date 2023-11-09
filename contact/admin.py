from django.contrib import admin
from .models import Feedback
# Register your models here.
class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'subject', 'date')

admin.site.register(Feedback, ContactAdmin)