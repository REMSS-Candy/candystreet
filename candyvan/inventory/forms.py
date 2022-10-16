from django import forms
from django.utils import timezone

from .models import Transaction


class EditTransaction(forms.ModelForm):
    
    class Meta:
        model = Transaction
        fields = ('amount',)


class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=50)
    password = forms.CharField(
        label="Password", widget=forms.PasswordInput(), max_length=100)


class CSVForm(forms.Form):
    date = forms.DateField(
        label="Date to start searching from", initial=timezone.now().date())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].widget.attrs['class'] = "input"
