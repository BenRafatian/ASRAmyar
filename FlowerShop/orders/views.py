from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView
from django.contrib import messages


from .models import OrderItem, Order
from .forms import OrderCreateForm
from .tasks import order_created
from cart.cart import Cart


@login_required
def order_create(request):
    cart = Cart(request)

    if request.method == 'POST' and cart:
        customer = request.user.profile
        address = request.user.profile.address
        form = OrderCreateForm(customer, address, request.POST, request.FILES)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # clear the cart
            cart.clear()
            order_created.delay(order.id)
            print('hello')
            return render(request,
                          'orders/order/created.html',
                          {'order': order})
    elif request.method == "POST" and not cart:
        if request.user.profile.address:
            print('no order item')
            customer = request.user.profile
            address = request.user.profile.address

            form = OrderCreateForm(customer, address)
            messages.error(request=request, message="No Item in Order")
            return render(request,
                          'orders/order/create.html',
                          {'cart': cart, 'form': form})
    else:
        if request.user.profile.address:
            customer = request.user.profile
            address = request.user.profile.address

            form = OrderCreateForm(customer, address)

    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form})


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "orders/order/list.html"
    context_object_name = "orders"

    def get_queryset(self):
        return self.model.objects.filter(customer=self.request.user.profile)


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = "orders/order/detail.html"
    context_object_name = "order"

    def get_queryset(self):
        return self.model.objects.filter(customer=self.request.user.profile)
