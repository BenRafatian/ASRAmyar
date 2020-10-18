from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.OrderListView.as_view(), name="orders"),
    path('<int:pk>/', views.OrderDetailView.as_view(), name="order_detail"),
    path('create/', views.order_create, name='order_create'),
]
