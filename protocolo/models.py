from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class FuncionarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class Funcionario(AbstractBaseUser, PermissionsMixin):
    permissao = [("Gerente", "Gerente"), ("Funcionário", "Funcionário"),
                 ("Estagiário", "Estagiário"), ("Visitante", "Visitante")]

    nome = models.CharField("Nome", max_length=45)
    documento = models.CharField("Documento", max_length=11, unique=True)
    telefone = models.CharField("Telefone", max_length=45, null=True)
    email = models.EmailField("E-mail", max_length=45, unique=True)
    permissao = models.CharField(
        "Permissão", max_length=45, choices=permissao, default='Funcionário')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = FuncionarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome', 'documento', 'telefone']

    def __str__(self):
        return self.email
    


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
