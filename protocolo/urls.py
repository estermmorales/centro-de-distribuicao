from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views

urlpatterns = [
    path('', views.protocolo, name='protocolo'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
