from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from mail.forms import StyleFormMixin
from users.models import User
from django import forms


class RegistrationForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class RecoverForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)


class UserForm(StyleFormMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'password', 'first_lastname', 'avatar', 'phone', 'county')

    def __int__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()