from django import forms

from salon.models import Contact


class SalonContactFrom(forms.ModelForm):
    class Meta:
        fields = ('address', 'zip_code', 'contact', 'web_site', 'timetable')
        model = Contact
