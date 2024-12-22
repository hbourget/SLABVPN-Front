from datetime import datetime, timedelta
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class LookupForm(forms.Form):
    ip_addr = forms.GenericIPAddressField(
        label="IP Address",
        widget=forms.TextInput(attrs={'autofocus': True})
    )
    datetime = forms.DateTimeField(
        label="Since",
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
        initial=(datetime.now() - timedelta(days=366)).strftime('%Y-%m-%dT%H:%M')
    )

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
