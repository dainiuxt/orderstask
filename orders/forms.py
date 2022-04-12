from django import forms
from .models import Order, ProductOrder
from django.contrib.auth.models import User

class DateInput(forms.DateInput):
    input_type = 'date'

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status', 'date']
        widgets = {
            'user': forms.HiddenInput(), 'date': DateInput(), 
            }

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class RowForm(forms.ModelForm):
    class Meta:
        model = ProductOrder
        fields = ['order', 'selection', 'quantity']
        # widgets = {
        #     'order': forms.HiddenInput()}

class RowFormUpdate(forms.ModelForm):
    class Meta:
        model = ProductOrder
        fields = ['order', 'selection', 'quantity']
        # widgets = {
        #     'order': forms.HiddenInput(), 'productorder_id': forms.HiddenInput()}
