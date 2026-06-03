from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import CustomerProfile


class CustomerProfileForm(forms.Form):
    first_name = forms.CharField(
        required=False,
        label='First name',
        widget=forms.TextInput(attrs={
            'class': 'profile-edit-input',
            'placeholder': 'Enter first name'
        })
    )

    last_name = forms.CharField(
        required=False,
        label='Last name',
        widget=forms.TextInput(attrs={
            'class': 'profile-edit-input',
            'placeholder': 'Enter last name'
        })
    )

    email = forms.EmailField(
        required=True,
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'profile-edit-input',
            'placeholder': 'Enter email'
        })
    )

    phone_number = forms.CharField(
        required=False,
        label='Phone number',
        widget=forms.TextInput(attrs={
            'class': 'profile-edit-input',
            'placeholder': 'Enter phone number'
        })
    )

    city = forms.CharField(
        required=False,
        label='City',
        widget=forms.TextInput(attrs={
            'class': 'profile-edit-input',
            'placeholder': 'Enter your city'
        })
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.customer_profile = kwargs.pop('customer_profile')
        super().__init__(*args, **kwargs)

        self.fields['first_name'].initial = self.user.first_name
        self.fields['last_name'].initial = self.user.last_name
        self.fields['email'].initial = self.user.email
        self.fields['phone_number'].initial = self.customer_profile.phone_number
        self.fields['city'].initial = self.customer_profile.city

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.exclude(id=self.user.id).filter(email=email).exists():
            raise forms.ValidationError('This email is already used.')

        return email

    def save(self):
        self.user.first_name = self.cleaned_data['first_name']
        self.user.last_name = self.cleaned_data['last_name']
        self.user.email = self.cleaned_data['email']
        self.user.username = self.cleaned_data['email']
        self.user.save()

        self.customer_profile.phone_number = self.cleaned_data['phone_number']
        self.customer_profile.city = self.cleaned_data['city']
        self.customer_profile.save()

        return self.user


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


class CustomerProfileForm(forms.Form):
    first_name = forms.CharField(
        required=False,
        label='First name',
        widget=forms.TextInput(attrs={
            'class': 'profile-edit-input',
            'placeholder': 'Enter first name'
        })
    )

    last_name = forms.CharField(
        required=False,
        label='Last name',
        widget=forms.TextInput(attrs={
            'class': 'profile-edit-input',
            'placeholder': 'Enter last name'
        })
    )

    email = forms.EmailField(
        required=True,
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'profile-edit-input',
            'placeholder': 'Enter email'
        })
    )

    phone_number = forms.CharField(
        required=False,
        label='Phone number',
        widget=forms.TextInput(attrs={
            'class': 'profile-edit-input',
            'placeholder': 'Enter phone number'
        })
    )

    city = forms.CharField(
        required=False,
        label='City',
        widget=forms.TextInput(attrs={
            'class': 'profile-edit-input',
            'placeholder': 'Enter your city'
        })
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.customer_profile = kwargs.pop('customer_profile')
        super().__init__(*args, **kwargs)

        self.fields['first_name'].initial = self.user.first_name
        self.fields['last_name'].initial = self.user.last_name
        self.fields['email'].initial = self.user.email
        self.fields['phone_number'].initial = self.customer_profile.phone_number
        self.fields['city'].initial = self.customer_profile.city

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.exclude(id=self.user.id).filter(email=email).exists():
            raise forms.ValidationError('This email is already used.')

        return email

    def save(self):
        self.user.first_name = self.cleaned_data['first_name']
        self.user.last_name = self.cleaned_data['last_name']
        self.user.email = self.cleaned_data['email']
        self.user.username = self.cleaned_data['email']
        self.user.save()

        self.customer_profile.phone_number = self.cleaned_data['phone_number']
        self.customer_profile.city = self.cleaned_data['city']
        self.customer_profile.save()

        return self.user