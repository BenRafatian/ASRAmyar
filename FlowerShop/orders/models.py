from django.db import models
from shop.models import Product
from django import forms
from users.models import Profile, Address


class Order(models.Model):
    customer = models.ForeignKey(Profile, verbose_name="customer", on_delete=models.CASCADE)

    # total_products_price = models.IntegerField()
    # discount = models.IntegerField()
    # price_after_discount = models.IntegerField()      # sum of total_products_price and discount
    # shipment_price = models.IntegerField()
    # total_vat = models.IntegerField()
    # total_bill_price = models.IntegerField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)


    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Order {self.id}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
