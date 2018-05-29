from django import forms
from staffer.models import StafferInfo


class StafferInfoForm(forms.ModelForm):
    class Meta:
        fields = ('date_of_employment', 'phone_number', 'gender', 'passport_data', 'iin', 'staffer')
        model = StafferInfo
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4, 'cols': 15})
        }
