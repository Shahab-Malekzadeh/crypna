"""
module docstring
"""
from django import forms
from django.contrib.auth.forms import AuthenticationForm

from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget

from .models import User


class ProfileForm(forms.ModelForm):
    """
    class docstring
    """

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ProfileForm, self).__init__(*args, **kwargs)

        self.fields['username'].help_text = None
        if not user.is_superuser:
            self.fields['username'].disabled = True
            self.fields['email'].disabled = True
            self.fields['is_author'].disabled = True

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name',
                  'is_author', 'bio']


class LoginForm(AuthenticationForm):
    captcha = ReCaptchaField(widget=ReCaptchaWidget())

    class Meta:
        fields = ('username', 'password', 'captcha', )
