from django import forms
from django.forms import Form, ModelForm
from protocolo.models import Protocolo, EmitenteDestinatario, Funcionario
from simplecep import CEPField


class FuncionarioForm(ModelForm):
    class Meta:
        model = Funcionario
        fields = ["nome", "email", "documento", "contato"]


class EnderecoForm(Form):
    cep = CEPField(
        label='Your CEP',
        autofill={
            # key is the data-type and value is the form-field name
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
