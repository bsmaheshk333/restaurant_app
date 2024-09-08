from django.contrib import admin
from .models import Restaurant, Menu, MenuItems, Customer, Order


admin.site.register(Restaurant)
admin.site.register(Menu)
admin.site.register(MenuItems)
admin.site.register(Customer)
admin.site.register(Order)
