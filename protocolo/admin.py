from django.contrib import admin

# Register your models here.
from .models import Funcionario, EmitenteDestinatario, Protocolo, Endereco


@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('user', 'nome', 'documento',
                    'telefone', 'email', 'permissao')


class EmitenteDestinatarioInline(admin.TabularInline):
    model = EmitenteDestinatario
    extra = 1


@admin.register(Endereco)
class RegistroAdmin(admin.ModelAdmin):
    inlines = [EmitenteDestinatarioInline]
    list_display = ('cep', 'estado', 'cidade', 'bairro', 'rua')


@admin.register(Protocolo)
class ProtocoloAdmin(admin.ModelAdmin):
    list_display = ('data_entrega', 'data_retirada', 'qtd_volumes',
                    'id_emitente', 'id_destinatario', 'id_funcionario', 'situacao')
