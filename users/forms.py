from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from mail.forms import StyleFormMixin
from users.models import User


class RegistrationForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "password1", "password2")


class RecoverForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ("email",)


class UserForm(StyleFormMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ("email", "password", "first_lastname", "avatar", "phone_number", "country")

    def __int__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].widget = forms.HiddenInput()
