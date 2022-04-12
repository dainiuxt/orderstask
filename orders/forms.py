from django import forms
from .models import Order, Profile
from django.contrib.auth.models import User

class DateInput(forms.DateInput):
    input_type = 'date'

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        # fields = fields = '__all__'
        fields = ['status', 'date']
        widgets = {
            'user': forms.HiddenInput(), 'date': DateInput(), 
            }

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


# class ProfileUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Profile
