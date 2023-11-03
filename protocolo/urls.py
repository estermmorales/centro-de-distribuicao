from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views

urlpatterns = [
    path('', views.protocolo, name='protocolo'),
    path('cadastrar_protocolo/', views.cadastrar_protocolo, name='cadastrar_protocolo'),
    path('protocolos/editar/', views.editar_protocolo, name='editar_protocolo'),
    path('autocomplete_usuarios/', views.autocomplete_usuarios, name='autocomplete_usuarios')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
