from django.forms import ModelForm, widgets
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class MinimumLengthValidator:
    def __init__(self, min_length=4):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                _("This password must contain at least %(min_length)d characters."),
                code='password_too_short',
                params={'min_length': self.min_length},
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least %(min_length)d characters."
            % {'min_length': self.min_length}
        )
        
        
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        
        widgets = {
            'username' : forms.widgets.TextInput(attrs={'class':'form-control'}),
            'first_name' : forms.widgets.TextInput(attrs={'class':'form-control'}),
            'last_name' : forms.widgets.TextInput(attrs={'class':'form-control'}),
            'email' : forms.widgets.TextInput(attrs={'class':'form-control'}),
            'password1' : forms.widgets.TextInput(attrs={'class':'form-control'}),
            'password2' : forms.widgets.TextInput(attrs={'class':'form-control'}),
        }

