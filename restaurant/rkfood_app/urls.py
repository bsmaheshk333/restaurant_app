from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import fb_views


urlpatterns = [
    path("", fb_views.home, name="base"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
