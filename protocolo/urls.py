from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views

urlpatterns = [
    path('', views.protocolo, name='protocolo'),
    path('cadastrar_protocolo/', views.cadastrar_protocolo,
         name='cadastrar_protocolo'),
    path('protocolos/<int:protocolo_id>/editar/',
         views.editar_protocolo, name='editar_protocolo')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
