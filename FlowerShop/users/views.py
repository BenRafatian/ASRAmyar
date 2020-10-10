from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, ProfileUpdateForm, UserChangeForm
from django.contrib.auth.forms import PasswordChangeForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, f'Your account has been created! You are now able to log in')
            return redirect('users:login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):

    user = request.user

    if request.method == 'POST':
        user_form = UserChangeForm(user, request.POST)
        print(user_form)
        print(request.POST)
        print(user)
        print("------------------------------------------")
        pass_form = PasswordChangeForm(user, request.POST)
        profile_form = ProfileUpdateForm(request.POST,
                                         request.FILES,
                                         instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Your account has been updated!')
            print("''''''''''''''''''''''''''''''''''''''''''")
            return redirect('users:profile')

    else:
        email = request.user.email
        first_name = request.user.first_name
        last_name = request.user.last_name
        user_form = UserChangeForm(user, initial={
            'email': email,
            'first_name': first_name,
            'last_name': last_name
        })
        pass_form = PasswordChangeForm(user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'pass_form': pass_form
    }

    return render(request, 'users/profile.html', context)


@login_required
def dashboard(request):
    return render(request, 'users/dashboard.html')
