from django import forms
from .models import *



class ClientForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = '__all__'



class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'


    


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = '__all__'


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = '__all__'



class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'
        widgets = {
            'paid' : forms.CheckboxInput(attrs={'class': 'required checkbox form-control'}),   
        }