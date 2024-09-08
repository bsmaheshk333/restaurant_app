from django.db import models
import datetime

"""
Documentation
Models defined:
- Restaurant
- Menu
- Menu Items
- Customer
- Booking
- Order
- Payment
- Feedback (survey)

Relationship:
-> 'Restaurant' can have multiple menu, but each Menu associated with one restaurant.
-> 'Menu' can have multiple of Items i.e Menu Items, but each Menu items can be associated
   with only one Menu.
-> Customer can have multiple bookings, but each booking associated with only one Customer
-> Customer can have multiple orders, but each order ties with only one Customer.
-> Orders & payment can be 1-1 relationship. meaning that, there will be only one record
   booking against each payment.
"""


class Restaurant(models.Model):
    name = models.CharField(max_length=100, verbose_name='Restaurant Name')
    address = models.TextField(max_length=500, verbose_name='address')
    phone_number = models.CharField(max_length=12)
    email_addr = models.EmailField()
    opens_at = models.TimeField(null=False, blank=False)
    close_at = models.TimeField(null=False, blank=False)

    @property
    def formatted_open_time(self):
        return self.opens_at.strftime("%I:%M:%p")

    @property
    def formatted_close_time(self):
        return self.close_at.strftime("%I:%M:%p")

    def __str__(self):
        return f"{self.name} Opens at: {self.formatted_open_time}, Close at: {self.formatted_close_time}"


menu_choice = [
    ('Breakfast', 'Breakfast'),
    ('Lunch', 'Lunch'),
    ('Dinner', 'Dinner')
]


class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE,
                                   related_name='restaurant')
    # breakfast, lunch, dinner
    menu_title = models.CharField(max_length=10, choices=menu_choice, default=menu_choice[0][0])
    description = models.TextField()

    def __str__(self):
        return self.menu_title


class MenuItems(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='main_menu')
    # if in case you have multiple restaurant,
    # restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="restaurant")
    name = models.CharField(max_length=100)
    image = models.ImageField(default="avatar.jpg", upload_to="menu_items/", verbose_name="image of the food")
    description = models.TextField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Customer(models.Model):
    full_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=12, unique=True)
    email = models.EmailField()

    def __str__(self):
        return self.full_name


# class Booking(models.Model):
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='booking')
#     # if there are multiple restaurant please include below relationship,
#     # restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
#     booking_date = models.DateTimeField(auto_now_add=True)
#     # if in case, bookings includes Menu items,
#     # menu_items = models.ForeignKey(MenuItems, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return f"booked by customer {self.customer} on {self.booking_date}"
#
#     @property
#     def format_booking_date(self):
#         return self.booking_date.strftime("%I:%M:%p")


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="customer_ordered")
    # if in case multiple restaurants
    # restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    order_qty = models.IntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20)
    menu_items = models.ForeignKey(MenuItems, on_delete=models.CASCADE, related_name='menu_ordered')

    @property
    def formatted_ordered_date(self):
        return self.order_date.strftime("%I:%M:%p")

    def __str__(self):
        return (f"order details: Name: {self.customer.full_name}, Item: {self.menu_items}, "
                f"Order On: {self.formatted_ordered_date} "
                f"Order Qty: {self.order_qty}, Amount paid: {self.total_amount} Rs. "
                f"Payment Status: {self.payment_status}")


class Payment(models.Model):
    pass
