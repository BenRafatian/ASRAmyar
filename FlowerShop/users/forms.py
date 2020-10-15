from django import forms
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    PasswordChangeForm
)
from .models import Profile, Address


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        self.fields.pop('password')


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['image']


class AddressCreateForm(forms.ModelForm):

    def __init__(self, profile, *args, **kwargs):
        super(AddressCreateForm, self).__init__(*args, **kwargs)
        self.profile = profile

    def save(self, commit=True):
        instance = super(AddressCreateForm, self).save(commit=False)
        if not instance.pk:
            instance.profile = self.profile
        if commit:
            instance.save()
        return instance

    class Meta:
        model = Address
        fields = ['id', 'address_detail', 'state',
                  'postal_code', 'city', 'phone_number']
