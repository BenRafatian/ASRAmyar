from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserChangeForm, ProfileUpdateForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from users.models import Profile
from django.views.generic import DetailView
from orders.models import Order


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
def profile_update(request):

    user = request.user
    # TODO: if request.method=="POST" and "password_change_button_name" in request.POST --> user password form and same for informatinon form
    if request.method == 'POST':
        data = request.POST
        print(data)
        user_form = UserChangeForm(data=data, instance=user)
        pass_form = PasswordChangeForm(data=data, user=user)
        profile_form = ProfileUpdateForm(request.POST,
                                         request.FILES,
                                         instance=request.user.profile)
        if user_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Your account has been updated!')

            return redirect('users:profile_update')

    else:
        email = request.user.email
        first_name = request.user.first_name
        last_name = request.user.last_name
        user_form = UserChangeForm(instance=user, initial={
            'email': email,
            'first_name': first_name,
            'last_name': last_name
        })
        pass_form = PasswordChangeForm(user=user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'pass_form': pass_form
    }

    return render(request=request, template_name='users/update.html', context=context)


class ProfileView(DetailView):
    model = User
    context_object_name = 'profile'
    template_name = "users/profile.html"

    def get_object(self):
        return get_object_or_404(User, username=self.request.user.username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['last_orders'] = Order.objects.filter(
            customer=self.request.user.profile).order_by('-created')[:3]
        return context
