from django import forms

from mail.models import Mailing
from services import StyleFormMixin


class MailingForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Mailing
        fields = '__all__'