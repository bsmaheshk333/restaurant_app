from django import forms
from .models import Menu, MenuItems, Order


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['restaurant',  'menu_title', 'description']


class MenuItemsForm(forms.ModelForm):
    class Meta:
        model = MenuItems
        fields = ['menu', 'name', 'description', 'price']


