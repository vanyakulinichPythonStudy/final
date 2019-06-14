from django import forms
from django.contrib.auth.models import User

FORM_INPUT_CLASS = {'class': 'input is-info'}


class RegisterForm(forms.Form):

    username = forms.CharField(label='Login', max_length=100,
                               widget=forms.TextInput(attrs={**FORM_INPUT_CLASS}))
    password = forms.CharField(label='Password', max_length=100,
                               widget=forms.PasswordInput(attrs={**FORM_INPUT_CLASS}))

    class Meta():
        model = User


class SignInForm(RegisterForm):

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            User.objects.get(username=username)
        except:
            raise forms.ValidationError('User not found. Try again or sign up')
        return username


class SignUpForm(RegisterForm):
    first_name = forms.CharField(
        label="First Name", max_length=100, widget=forms.TextInput(attrs={**FORM_INPUT_CLASS}))
    last_name = forms.CharField(
        label="Last Name", max_length=100, widget=forms.TextInput(attrs={**FORM_INPUT_CLASS}))
    email = forms.EmailField(label="Email", max_length=100,
                             widget=forms.EmailInput(attrs={**FORM_INPUT_CLASS}))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            user = User.objects.get(username=username)
        except:
            return username
        raise forms.ValidationError('User not found. Try again or sign up')
