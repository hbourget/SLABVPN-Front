from django import forms
from datetime import datetime, timedelta

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
