from django import forms
from django.forms import Form, ModelForm
from protocolo.models import Protocolo, EmitenteDestinatario, Funcionario, Endereco
from simplecep import CEPField


class FuncionarioForm(ModelForm):
    class Meta:
        model = Funcionario
        fields = ["nome", "email", "documento", "contato"]


class EnderecoForm(forms.Form):
    cep = CEPField(
        label='Seu CEP',
        autofill={
            "district": "bairro",
            "state": "estado",
            "city": "cidade",
            "street": "rua",
            "street_number": "numbero_rua",
        }
    )
    estado = forms.CharField()
    cidade = forms.CharField()
    bairro = forms.CharField()
    rua = forms.CharField()
    numbero_rua = forms.CharField()


class EmitenteDestinatarioForm(ModelForm):
    class Meta:
        model = EmitenteDestinatario
        fields = ["nome", "email", "documento", "telefone", "endereco"]


class ProtocoloForm(ModelForm):
    class Meta:
        model: Protocolo
        fields = ["emitente", "destinatario", "data_entrega", "volumes"]


class RegistraProtocolo(forms.Form):
    pass
