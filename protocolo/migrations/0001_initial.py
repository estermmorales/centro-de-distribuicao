# Generated by Django 2.2.5 on 2023-10-06 02:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmitenteDestinatario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=45)),
                ('documento', models.CharField(max_length=11)),
                ('telefone', models.CharField(max_length=11)),
                ('email', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='Funcionario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=45)),
                ('documento', models.CharField(max_length=11)),
                ('contato', models.CharField(max_length=45)),
                ('email', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='Permissao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(choices=[('GR', 'Gerente'), ('FUN', 'Funcionário'), ('EST', 'Estagiário'), ('VIS', 'Visitante')], max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='Situacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(choices=[('PEN', 'PENDENTE'), ('RET', 'RETIRADO'), ('CAN', 'CANCELADO')], max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=45)),
                ('senha', models.CharField(max_length=30)),
                ('id_funcionario', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='protocolo.Funcionario')),
                ('id_perfil', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='protocolo.Perfil')),
            ],
        ),
        migrations.CreateModel(
            name='Protocolo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_entrega', models.DateField()),
                ('data_retirada', models.DateField()),
                ('qtd_volumes', models.IntegerField()),
                ('id_destinatario', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='id_destinatario', to='protocolo.EmitenteDestinatario')),
                ('id_emitente', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='id_emitente', to='protocolo.EmitenteDestinatario')),
                ('id_situacao', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='protocolo.Situacao')),
                ('id_usuario', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='protocolo.Usuario')),
            ],
        ),
        migrations.AddField(
            model_name='perfil',
            name='id_perimssao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='protocolo.Permissao'),
        ),
    ]
