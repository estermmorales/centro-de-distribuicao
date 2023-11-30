import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "central.settings")
django.setup()
import random
from faker import Faker
from protocolo.models import Endereco, EmitenteDestinatario, Protocolo

fake = Faker('pt_BR')
faker = Faker()


# Populando a tabela Endereco
for _ in range(10):
    endereco = Endereco.objects.create(
        cep=faker.zipcode(),
        estado=fake.estado_sigla(),
        cidade=fake.city(),
        bairro=fake.bairro(),
        rua=fake.street_name()
    )

# Populando a tabela EmitenteDestinatario e Protocolo
for _ in range(10):
    emitente = EmitenteDestinatario.objects.create(
        nome=fake.name(),
        documento=fake.cpf(),
        telefone=fake.phone_number(),
        email=fake.email(),
        id_endereco=Endereco.objects.get(pk=random.randint(1, 50))
    )

    destinatario = EmitenteDestinatario.objects.create(
        nome=fake.name(),
        documento=fake.cpf(),
        telefone=fake.phone_number(),
        email=fake.email(),
        id_endereco=Endereco.objects.get(pk=random.randint(1, 50))
    )

    data_entrega = fake.date_time_between(start_date='-60d', end_date='now')
    data_retirada = None
    qtd_volumes = random.randint(1, 10)
    situacao = random.choice(['Pendente', 'Retirado', 'Cancelado'])

    if situacao == 'Retirado':
        data_retirada = fake.date_time_between(start_date=data_entrega, end_date='now')

    protocolo = Protocolo.objects.create(
        data_entrega=data_entrega,
        data_retirada=data_retirada,
        id_emitente=emitente,
        id_destinatario=destinatario,
        qtd_volumes=qtd_volumes,
        situacao=situacao
    )
