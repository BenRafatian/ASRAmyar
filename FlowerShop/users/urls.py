from django.urls import path, re_path
from django.contrib.auth import views as auth_views

from . import views


app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),

    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/update/', views.profile_update, name='profile_update'),

    path('address/', views.AddressListView.as_view(), name='address_list'),
    path('address/create/', views.AddressCreateView.as_view(), name='address_create'),
    path('address/<int:pk>/', views.AddressDetailView.as_view(),
         name='address_detail'),
    path('address/update/<int:pk>/',
         views.AddressUpdateView.as_view(), name='address_update'),
    path('address/delete/<int:pk>/',
         views.AddressDeleteView.as_view(), name='address_delete'),

]
