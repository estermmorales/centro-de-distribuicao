from django.db import models


class Permissao(models.Model):
    permissoes = [("GR", "Gerente"), ("FUN", "Funcionário"),
                  ("EST", "Estagiário"), ("VIS", "Visitante")]
    descricao = models.CharField(max_length=45, choices=permissoes)


class Perfil(models.Model):
    descricao = models.CharField(max_length=45)
    id_perimssao = models.ForeignKey(Permissao, on_delete=models.DO_NOTHING)


class Usuario(models.Model):
    nome = models.CharField(max_length=45)
    senha = models.CharField(max_length=30)
    id_perfil = models.ForeignKey(Perfil, on_delete=models.DO_NOTHING)


class EmitenteDestinatario(models.Model):
    nome = models.CharField(max_length=45)
    documento = models.CharField(max_length=11)
    telefone = models.CharField(max_length=11)
    email = models.CharField(max_length=45)


class Situacao(models.Model):
    situacoes = [("PEN", "PENDENTE"), ("RET", "RETIRADO"),
                 ("CAN", "CANCELADO")]
    descricao = models.CharField(max_length=45, choices=situacoes)


class Protocolo(models.Model):
    data_entrega = models.DateField()
    data_retirada = models.DateField()
    id_emitente = models.ForeignKey(
        EmitenteDestinatario, on_delete=models.DO_NOTHING, related_name="id_emitente")
    id_destinatario = models.ForeignKey(
        EmitenteDestinatario, on_delete=models.DO_NOTHING, related_name="id_destinatario")
    id_usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)
    id_situacao = models.ForeignKey(Situacao, on_delete=models.DO_NOTHING)
    qtd_volumes = models.IntegerField()
