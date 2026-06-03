from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomerRegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter email',
            'class': 'auth-input',
        })
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter password',
            'class': 'auth-input',
        })
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter password',
            'class': 'auth-input',
        })
    )

    accept_terms = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'auth-checkbox-input',
        })
    )

    class Meta:
        model = User
        fields = [
            'email',
            'password1',
            'password2',
            'accept_terms',
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if email:
            email = email.lower().strip()

            if User.objects.filter(username=email).exists():
                raise forms.ValidationError('An account with this email already exists.')

            if User.objects.filter(email=email).exists():
                raise forms.ValidationError('An account with this email already exists.')

        return email

    def save(self, commit=True):
        user = super().save(commit=False)

        email = self.cleaned_data['email'].lower().strip()

        user.username = email
        user.email = email

        if commit:
            user.save()

        return user


class CustomerLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter email',
            'class': 'auth-input',
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter password',
            'class': 'auth-input',
        })
    )

    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'auth-checkbox-input',
        })
    )