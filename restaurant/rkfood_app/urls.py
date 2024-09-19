from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import fb_views


urlpatterns = [
    path("", fb_views.home, name="base"),
    path("search_item/", fb_views.search_item, name="search_item"),
    path('login/', fb_views.customer_login, name="login"),
    path('register/', fb_views.customer_register, name="register"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
