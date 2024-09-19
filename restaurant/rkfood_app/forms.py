from django import forms
from .models import Menu, MenuItems, Order, Customer
from django.contrib.auth.models import User



class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['restaurant',  'menu_title', 'description']


class MenuItemsForm(forms.ModelForm):
    class Meta:
        model = MenuItems
        fields = ['menu', 'name', 'description', 'price']


class CustomerRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['phone']
