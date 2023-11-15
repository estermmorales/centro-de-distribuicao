from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Funcionario(models.Model):
    permissao = [("Gerente", "Gerente"), ("Funcionário", "Funcionário"),
                 ("Estagiário", "Estagiário"), ("Visitante", "Visitante")]

    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    nome = models.CharField("Nome", max_length=45)
    documento = models.CharField("Documento", max_length=11)
    telefone = models.CharField("Telefone", max_length=45, null=True)
    email = models.CharField("E-mail", max_length=45)
    permissao = models.CharField(
        "Permissão", max_length=45, choices=permissao, default='Funcionário')
    


class Endereco(models.Model):
    cep = models.IntegerField("CEP")
    estado = models.CharField("Estado", max_length=45)
    cidade = models.CharField("Cidade", max_length=45)
    bairro = models.CharField("Bairro", max_length=100)
    rua = models.CharField("Rua", max_length=100)


class EmitenteDestinatario(models.Model):
    nome = models.CharField("Nome", max_length=100)
    documento = models.CharField("Documento", max_length=11)
    telefone = models.CharField("Telefone", max_length=11)
    email = models.CharField("E-mail", max_length=45)
    id_endereco = models.ForeignKey(
        Endereco, blank=True, null=True, on_delete=models.CASCADE, unique=False)


class Protocolo(models.Model):
    situacoes = [("Pendente", "Pendente"), ("Retirado", "Retirado"),
                 ("Cancelado", "Cancelado")]
    data_entrega = models.DateField(
        "Data de entrega", default=timezone.now)
    data_retirada = models.DateField("Data de retirada", null=True, blank=True)
    id_emitente = models.ForeignKey(
        EmitenteDestinatario, on_delete=models.DO_NOTHING, related_name="id_emitente")
    id_destinatario = models.ForeignKey(
        EmitenteDestinatario, on_delete=models.DO_NOTHING, related_name="id_destinatario")
    id_funcionario = models.ForeignKey(
        Funcionario, on_delete=models.DO_NOTHING, null=True)
    qtd_volumes = models.IntegerField("Volumes")
    situacao = models.CharField(
        "Situação", max_length=45, choices=situacoes, default='Pendente')
    nome_funcionario = models.CharField("Funcionario", max_length=45, default='Funcionário')

