from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class RegisterForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(min_length=8)
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)
    phone_number = forms.CharField(max_length=20, required=False)
    country = forms.CharField(max_length=2, required=False)

    def clean_email(self):
        email = self.cleaned_data['email'].lower().strip()
        if User.objects.filter(email=email).exists():
            raise ValidationError('A user with this email already exists.')
        return email


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email', '').lower().strip()
        password = cleaned_data.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise ValidationError('Invalid email or password.')
            if not user.is_active:
                raise ValidationError('This user account is inactive.')
            cleaned_data['user'] = user
        return cleaned_data


class AdminLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email', '').lower().strip()
        password = cleaned_data.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise ValidationError('Invalid email or password.')
            if not (user.is_staff or user.is_admin_user):
                raise ValidationError('Admin privileges required.')
            if not user.is_active:
                raise ValidationError('This user account is inactive.')
            cleaned_data['user'] = user
        return cleaned_data
