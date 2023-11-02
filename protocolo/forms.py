from django import forms
from django.forms import Form, ModelForm
from protocolo.models import Protocolo, EmitenteDestinatario, Funcionario, Endereco
from django.utils import timezone


class FuncionarioForm(ModelForm):
    class Meta:
        model = Funcionario
        fields = ["nome", "email", "documento", "telefone", 'permissao']


class EnderecoForm(ModelForm):
    class Meta:
        model = Endereco
        fields = ["cep", "estado", "cidade", "bairro", "rua"]


class EmitenteDestinatarioForm(ModelForm):
    class Meta:
        model = EmitenteDestinatario
        fields = ["nome", "email", "documento", "telefone", "id_endereco"]


class ProtocoloForm(forms.ModelForm):
    emitente_nome = forms.CharField(max_length=100)
    destinatario_nome = forms.CharField(max_length=100)

    class Meta:
        model = Protocolo
        fields = ['qtd_volumes', 'situacao']

    def save(self, commit=True):
        protocolo = super(ProtocoloForm, self).save(commit=False)
        emitente_nome = self.cleaned_data.get('emitente_nome')
        destinatario_nome = self.cleaned_data.get('destinatario_nome')

        # Recupere os IDs do emitente e do destinatário com base nos nomes
        emitente = EmitenteDestinatario.objects.get(nome=emitente_nome)
        destinatario = EmitenteDestinatario.objects.get(nome=destinatario_nome)

        protocolo.id_emitente = emitente
        protocolo.id_destinatario = destinatario

        if commit:
            protocolo.save()
        return protocolo


class ProtocoloEditForm(forms.ModelForm):
    class Meta:
        model = Protocolo
        fields = ['id_emitente', 'id_destinatario',
                  'id_funcionario', 'qtd_volumes', 'data_retirada', 'situacao']

    emitente_nome = forms.CharField(max_length=100, required=False)
    destinatario_nome = forms.CharField(max_length=100, required=False)

    def __init__(self, *args, **kwargs):
        super(ProtocoloEditForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['emitente_nome'].initial = self.instance.id_emitente.nome
            self.fields['destinatario_nome'].initial = self.instance.id_destinatario.nome

    def save(self, commit=True):
        protocolo = super(ProtocoloForm, self).save(commit=False)
        emitente_nome = self.cleaned_data.get('emitente_nome')
        destinatario_nome = self.cleaned_data.get('destinatario_nome')
        

        emitente = EmitenteDestinatario.objects.get(nome=emitente_nome)
        destinatario = EmitenteDestinatario.objects.get(nome=destinatario_nome)

        protocolo.id_emitente = emitente
        protocolo.id_destinatario = destinatario

        situacao = self.cleaned_data.get('situacao')
        if situacao == 'retirado':
            self.cleaned_data['data_retirada'] = timezone.now()

        if commit:
            protocolo.save()
        return protocolo
