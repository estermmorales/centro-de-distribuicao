# Generated by Django 3.1.4 on 2023-10-24 02:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('protocolo', '0004_auto_20231023_2312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='funcionario',
            name='permissao',
            field=models.CharField(choices=[('GR', 'Gerente'), ('FUN', 'Funcionário'), ('EST', 'Estagiário'), ('VIS', 'Visitante')], default='Funcionário', max_length=45, verbose_name='Permissão'),
        ),
        migrations.AlterField(
            model_name='protocolo',
            name='situacao',
            field=models.CharField(choices=[('PEN', 'Pendente'), ('RET', 'Retirado'), ('CAN', 'Cancelado')], default='Pendente', max_length=45, verbose_name='Situação'),
        ),
    ]