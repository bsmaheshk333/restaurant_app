from django.shortcuts import (render, redirect,
                              get_object_or_404, HttpResponseRedirect,
                              Http404)
from rkfood_app.models import (Restaurant,Menu,
                               MenuItems,
                               Customer,
                               Order)
from django.urls import reverse
from django.db.models import Q
from django.http import JsonResponse
from django.template import TemplateDoesNotExist
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import login_required, login_not_required
from django.http import JsonResponse
from django.contrib import messages
from rkfood_app.forms import CustomerRegistrationForm, MenuForm, MenuItemsForm, CustomerProfileForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import string
from django.db import IntegrityError


base_template = 'base.html'


@login_required(login_url="login/")
def home(request):
    context = {}
    try:
        menu_items = MenuItems.objects.all()
        for item in menu_items:
            print("menu title =", item.menu.menu_title)
        breakfast = Menu.objects.filter(menu_title="Breakfast")
        restaurant = Restaurant.objects.all().first()
        if restaurant:
            close_time = restaurant.formatted_close_time
        else:
            close_time = None
        # context['menu_items'] = menu_items_qs
        # context['close_time'] = close_time
        context = {
            'menu_items': menu_items,
            'close_time': close_time,
            'breakfast': breakfast
        }
        return render(request, base_template, context)
    except MenuItems.DoesNotExist:
        return JsonResponse({"error": 'Model data not exist.'}, status=400)
    except TemplateDoesNotExist as ex:
        return JsonResponse({'error': 'template not exist'}, status=400)


def item_detail_view(request, slug):
    item = MenuItems.objects.get()

def customer_profile(request, id):
    # TODO implement redis
    try:
        context = {}
        user = User.objects.get(id=id)
        profile = Customer.objects.get(user=user)
        # if request.user.is_staff or request.user.is_superuser:
        #     return HttpResponseRedirect(reverse("admin:index"))
        context = {'profile': profile}
        return render(request, 'customer/profile.html',context)
    except Customer.DoesNotExist:
        # do not use JsonResponse render html page instead
        return JsonResponse({'Message': 'user is admin, Please visit the admin site.'}, status=404)
    except TemplateDoesNotExist:
        # do not use JsonResponse render html page instead
        return JsonResponse({'error': 'Template does not exist'}, status=404)


def customer_login(request):
    errors = {}
    # if user is disabled or removed
    if request.user.is_authenticated:
        errors['error'] = 'you must be logged in to access this page'
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        # Validate username and password presence
        if not username:
            errors['username'] = "Invalid username."
        if not password:
            errors['password'] = "Invalid password."

        if not errors:
            # if username and password are provided only then you authenticate
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                with open("user_logged_data.txt", mode="a") as log_file:
                    print(f"{log_file = }")
                    log_file.write(f"user: {request.user}")
                return redirect('/')
            else:
                errors['invalid_creds'] = 'Invalid credentials.'
        # FIXME do not write this in production, json is meant for API
        return JsonResponse({
            'errors': errors,
            'username': username,
            'password': password,
        })
        # return render(request, "customer/login.html",
        #               {'errors': errors,'username': username,'password': password,})

    # If GET request, just render the login form
    return render(request, "customer/login.html")


def customer_register(request):
    if request.method == 'POST':
        username: str = request.POST.get('username', None).strip()
        password: str = request.POST.get('password', None).strip()
        email: str = request.POST.get('email', None).strip()
        phone: str = request.POST.get('phone', None).strip()
        errors = {}
        # validate email
        try:
            validate_email(email)
        except ValidationError:
            errors['email'] = 'invalid email address.'
        # validate username
        is_username_exist = User.objects.filter(username=username).exists()
        if is_username_exist:
            errors['username'] = 'user with this name exist'

        if username in ['admin', 'root', 'superuser']:
            errors['username'] = f'the username {username} is restricted.'

        if not any(char.isdigit() for char in password):
            errors['password'] = 'password must contain at least 1 digit.'

        if not phone.isdigit() or len(phone) < 10:
            errors['phone'] = "phone number must be digits and must be at least 10 digits."

        is_phone_no_exist = Customer.objects.filter(phone=phone).exists()
        if is_phone_no_exist:
            errors['phone'] = "Phone number exist already"

        if errors:
            # better to consider render html template to showcase the error
            return JsonResponse(errors, status=400)
        try:
            user, created = User.objects.get_or_create(username=username, email=email)
                                                       #default= {'password': password, 'email':email})
            if created:
                user.set_password(password)
                user.save()
                Customer.objects.create(user=user, phone=phone)
            else:
                # update phone number if user exist already
                user.customer_profile.phone = phone
                user.customer_profile.save()
            return redirect("login")
        except:
            errors['db'] = 'database error occurred! Please try again.'
            return JsonResponse(errors, status=400)
    else:
        return render(request, "customer/register.html")


def customer_logout(request):
    logout(request)
    with open("user_logged_data.txt", mode="a") as log_file:
        print(f"{log_file = }")
    return redirect("base")


def search_menu_item(request):
    # TODO redis
    context = {}
    if request.method == 'POST':
        query_item = request.POST.get('query_item', None)
        # you can have multiple filter depending on requirement
        # if request.method == 'POST':
        if query_item:
            try:
                model_qs = MenuItems.objects.filter(Q(name__icontains=query_item))
                context['menu_items'] = model_qs
                print(f"{query_item = }")
                return render(request, 'search_items.html', context)
            except TemplateDoesNotExist:
                return JsonResponse({'error': 'template does not exist'}, status=400)
        else:
            return JsonResponse({'error': 'query item not provided'}, status=400)
    else:
        return JsonResponse({'error': 'method not allowed'}, status=400)

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

