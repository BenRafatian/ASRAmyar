from django.shortcuts import render
from .models import OrderItem, Order
from .forms import OrderCreateForm
from .tasks import order_created
from cart.cart import Cart
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


@login_required
def order_create(request):
    cart = Cart(request)

    if request.method == 'POST':
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
            return render(request,
                          'orders/order/created.html',
                          {'order': order})
    else:
        if request.user.profile.address:
            customer = request.user.profile
            address = request.user.profile.address

            form = OrderCreateForm(customer, address)

    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form})
