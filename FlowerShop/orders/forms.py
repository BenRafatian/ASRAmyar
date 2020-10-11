from django import forms
from .models import Order, Profile, Address


class OrderCreateForm(forms.ModelForm):

    def __init__(self, customer, address, *args, **kwargs):
        super(OrderCreateForm, self).__init__(*args, **kwargs)
        self.customer = customer
        self.address = address

    def save(self, commit=True):
        instance = super(OrderCreateForm, self).save(commit=False)
        if not instance.pk:
            instance.customer = self.customer
            instance.address = self.address
        if commit:
            instance.save()
        return instance

    class Meta:
        model = Order
        fields = ['id']
