from django.forms import ModelForm
from protocolo.models import Protocolo, EmitenteDestinatario, Funcionario


class FuncionarioForm(ModelForm):
    class Meta:
        model = Funcionario
        fields = ["nome", "email", "documento", "contato"]


class EmitenteDestinatarioForm(ModelForm):
    class Meta:
        model = EmitenteDestinatario
        fields = ["nome", "email", "documento", "telefone"]


class ProtocoloForm(ModelForm):
    class Meta:
        model: Protocolo
        fields = []
