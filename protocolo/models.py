from django.db import models


class Permissao(models.Model):
    permissoes = ["Gerente", "Funcionário", "Estagiário", "Visitante"]
    descricao = models.CharField(max_length=45, choices=permissoes)


class Perfil(models.Model):
    descricao = models.CharField(max_length=45)
    id_perimssao = models.ForeignKey(Permissao)


class Usuario(models.Model):
    nome = models.CharField(max_length=45)
    senha = models.CharField(max_length=30)
    id_perfil = models.ForeignKey(Perfil)


class EmitenteDestinatario(models.Model):
    nome = models.CharField(max_length=45)
    documento = models.CharField(max_length=11)
    telefone = models.CharField(max_length=11)
    email = models.CharField(max_length=45)


class Situacao(models.Model):
    situacoes = ["PENDENTE", "RETIRADO", "CANCELADO"]
    descricao = models.CharField(max_length=45, choices=situacoes)


class Protocolo(models.Model):
    data_entrega = models.DateField()
    data_retirada = models.DateField()
    id_emitente = models.ForeignKey(EmitenteDestinatario)
    id_destinatario = models.ForeignKey(EmitenteDestinatario)
    id_usuario = models.ForeignKey(Usuario)
    id_situacao = models.ForeignKey(Situacao)
    qtd_volumes = models.IntegerField(max_length=11)
