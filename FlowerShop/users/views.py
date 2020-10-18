from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import DetailView, CreateView, UpdateView, ListView, DeleteView
from django.contrib.auth import update_session_auth_hash

from orders.models import Order, Address
from .models import Profile
from .forms import (
    UserRegisterForm,
    UserChangeForm,
    ProfileUpdateForm,
    AddressCreateForm,
    AddressUpdateForm
)


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
    if request.method == 'POST' and 'password' in request.POST:
        data = request.POST
        print('password change is in progress')
        pass_form = PasswordChangeForm(data=data, user=user)
        profile_form = ProfileUpdateForm(request.POST,
                                         request.FILES,
                                         instance=request.user.profile)
        if pass_form.is_valid():
            pass_form.save()
            profile_form.save()
            update_session_auth_hash(request, pass_form.user)
            messages.success(
                request, f'Your account\'s informations has been updated!')

            return redirect('users:profile')

    elif request.method == 'POST' and 'info' in request.POST:
        data = request.POST
        print('info change is in progress')
        print(data)
        user_form = UserChangeForm(data=data, instance=user)
        profile_form = ProfileUpdateForm(request.POST,
                                         request.FILES,
                                         instance=request.user.profile)
        if user_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(
                request, f'Your account\'s password has been updated!')
            return redirect('users:profile')
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


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    context_object_name = 'profile'
    template_name = "users/profile.html"

    def get_object(self):
        return get_object_or_404(User, username=self.request.user.username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['last_orders'] = Order.objects.filter(
            customer=self.request.user.profile).order_by('-created')[:3][::1]

        return context

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProfileView, self).dispatch(request, *args, **kwargs)


class AddressCreateView(LoginRequiredMixin, CreateView):
    model = Address
    template_name = "users/address/create.html"
    form_class = AddressCreateForm

    def form_valid(self, form):
        form.instance.profile = self.request.user.profile
        return super().form_valid(form=form)


# TODO: create address show view
class AddressListView(LoginRequiredMixin, ListView):
    model = Address
    context_object_name = 'addresses'
    template_name = "users/address/list.html"

    def get_queryset(self):
        return self.model.objects.filter(profile=self.request.user.profile)


class AddressDetailView(LoginRequiredMixin, DetailView):
    model = Address
    context_object_name = "address"
    template_name = "users/address/detail.html"

    def get_queryset(self):
        return self.model.objects.filter(profile=self.request.user.profile)


class AddressUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Address
    form_class = AddressUpdateForm
    template_name = "users/address/update.html"

    def form_valid(self, form):
        form.instance.profile = self.request.user.profile
        return super().form_valid(form=form)

    # This function allows user to change only their own addresses
    def test_func(self):
        address = self.get_object()
        if self.request.user == address.profile.user:
            return True
        return False


class AddressDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Address
    template_name = "users/address/delete_confirm.html"
    context_object_name = "address"
    # success_url = reversed()

    def test_func(self):
        address = self.get_object()
        if self.request.user == address.profile.user:
            return True
        return False

    def get_success_url(self):
        return reverse_lazy('users:address_list')
