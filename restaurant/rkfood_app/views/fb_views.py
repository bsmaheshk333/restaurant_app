from django.shortcuts import (render, redirect, HttpResponseRedirect,
                              Http404, HttpResponse)
from rkfood_app.models import (Restaurant,Menu,
                               MenuItems,
                               Customer,
                               Order)
from django.template import TemplateDoesNotExist
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import login_required, login_not_required


base_html = 'base.html'


# ======== API section =============
# it is good idea to isolate the APIs from views logic
# ======== End API section ==========

def home(request):
    context = {}
    try:
        menu_items_qs = MenuItems.objects.all()
        context['menu_items'] = menu_items_qs
        return render(request, base_html, context)
    except MenuItems.DoesNotExist:
        return HttpResponse(f"No data found")
    except TemplateDoesNotExist as ex:
        return HttpResponse(f"""<h1 class="m" style='text-align:center; color: red;'>
        Templates does not exist</h1>""")


def create_user_profile(request):
    pass


def customer_login(request):
    pass


def customer_register(request):
    pass


def customer_logout(request):
    pass


def customer_cart(request):
    """
    customer adds selected item to the cart
    """
    pass


def customer_order(request):
    """
    customer proceed to order
    # address is not required
    """
    pass


def customer_checkout(request):
    pass


def customer_receipt(request):
    # provide user a receipt mentioning the items they ordered and along with price details
    pass

