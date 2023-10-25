import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "central.settings")
django.setup()
import random
from faker import Faker
from protocolo.models import Endereco, EmitenteDestinatario, Protocolo

fake = Faker()
# Populando a tabela Endereco
for _ in range(50):
    endereco = Endereco.objects.create(
        cep=fake.zipcode(),
        estado=fake.state(),
        cidade=fake.city(),
        bairro=fake.word(),
        rua=fake.street_name()
    )

# Populando a tabela EmitenteDestinatario e Protocolo
for _ in range(50):
    emitente = EmitenteDestinatario.objects.create(
        nome=fake.name(),
        documento=fake.ssn(),
        telefone=fake.phone_number(),
        email=fake.email(),
        id_endereco=Endereco.objects.get(pk=random.randint(1, 50))
    )

    destinatario = EmitenteDestinatario.objects.create(
        nome=fake.name(),
        documento=fake.ssn(),
        telefone=fake.phone_number(),
        email=fake.email(),
        id_endereco=Endereco.objects.get(pk=random.randint(1, 50))
    )

    data_entrega = fake.date_time_this_decade(before_now=True, after_now=False)
    data_retirada = fake.date_time_this_decade(
        before_now=True, after_now=False)
    qtd_volumes = random.randint(1, 10)
    situacao = random.choice(['Pendente', 'Retirado', 'Cancelado'])

    protocolo = Protocolo.objects.create(
        data_entrega=data_entrega,
        data_retirada=data_retirada,
        id_emitente=emitente,
        id_destinatario=destinatario,
        qtd_volumes=qtd_volumes,
        situacao=situacao
    )
