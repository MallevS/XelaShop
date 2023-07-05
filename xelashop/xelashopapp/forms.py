from django import forms
from .models import *


class ItemForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'color', 'price', 'quantity', 'photo', 'category', 'material']


class CheckoutForm(forms.ModelForm):
    PAYMENT_CHOICES = [
        ('bank_transfer', 'Bank Transfer'),
        ('paypal', 'Paypal'),
        ('credit_card', 'Credit Card'),
    ]

    payment_method = forms.ChoiceField(choices=PAYMENT_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Order
        fields = ['shipping_address', 'phone', 'shipping_method', 'payment_method']
        labels = {
            'shipping_address': 'Shipping Address',
            'phone': 'Phone Number',
            'shipping_method': 'Shipping Method',
            'payment_method': 'Payment Method',
        }
