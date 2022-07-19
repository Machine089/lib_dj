from django import forms
import datetime

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as gl


class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text='Enter a date between now and four weeks')

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']
        if data < datetime.date.today():
            raise ValidationError(gl('Invalid date - renewal in post'))
        if data > datetime.date.today():
            raise ValidationError(gl('Invalid date - renewal more than four weeks ahead'))
        return data
