from django import forms
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    PasswordChangeForm
)
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserChangeForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['email', ]

    def __init__(self, username, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        self.username = username
        for i in kwargs:
            print(i)

    def save(self, commit=True):
        instance = get_object_or_404(User, username=self.username)
        # self.email =
        print("++++++++++++++++++++++++++++++++++++++++")
        print(instance)
        if not instance.pk:
            instance.username = self.username

        if commit:
            # print(instance.username)
            print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
            instance.save(force_update=True)
        return instance


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['image']
