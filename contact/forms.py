from django import forms
from .models import Feedback


class ContactForm(forms.ModelForm):
    class Meta:
        model = Feedback
        # fields = ['first_name','last_name','email','subject','message']
        fields = '__all__'
