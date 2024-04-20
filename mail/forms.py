from django import forms

from mail.models import Client, Mailing, Message
from services import StyleFormMixin


class MailingForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Mailing
        fields = "__all__"


class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        fields = "__all__"


class MessageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Message
        fields = "__all__"
