from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views

urlpatterns = [
    path('', views.protocolo, name='protocolo'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cadastrar_protocolo/', views.cadastrar_protocolo, name='cadastrar_protocolo'),
    path('protocolos/editar/', views.editar_protocolo, name='editar_protocolo'),
    path('protocolos/excluir/', views.excluir_protocolo, name='excluir_protocolo'),
    path('autocomplete_usuarios/', views.autocomplete_usuarios, name='autocomplete_usuarios'),
    path('usuarios', views.usuarios, name='usuarios'),
    path('cadastrar_usuario/', views.cadastrar_usuarios, name='cadastrar_usuario'),
    path('usuarios/editar/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/excluir/', views.excluir_usuario, name='excluir_usuario'),
    path('usuarios/autocomplete_usuarios/', views.autocomplete_usuarios, name='autocomplete_usuarios'),
    path('funcionarios/', views.funcionarios, name='funcionarios'),
    path('funcionarios/cadastrar_funcionario', views.cadastrar_funcionario, name='cadastrar_funcionario'),
    path('funcionarios/editar_funcionario', views.editar_funcionario, name='editar_funcionario'),
    path('funcionarios/excluir_funcionario', views.excluir_funcionario, name='excluir_funcionario'),
    path('configuracoes/', views.configuracoes, name='configuracoes'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
