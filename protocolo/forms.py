from django import forms
from django.forms import Form, ModelForm
from protocolo.models import Protocolo, EmitenteDestinatario, Funcionario, Endereco


class FuncionarioForm(ModelForm):
    class Meta:
        model = Funcionario
        fields = ["nome", "email", "documento", "contato"]


class EnderecoForm(ModelForm):
    class Meta:
        model = Endereco
        fields = ["cep", "estado", "cidade", "bairro", "rua"]


class EmitenteDestinatarioForm(ModelForm):
    class Meta:
        model = EmitenteDestinatario
        fields = ["nome", "email", "documento", "telefone", "endereco"]


class ProtocoloForm(ModelForm):
    class Meta:
        model: Protocolo
        fields = ["emitente", "destinatario", "data_entrega", "volumes"]
