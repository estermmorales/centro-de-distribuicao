# Generated by Django 4.2.6 on 2023-11-16 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('protocolo', '0011_alter_protocolo_id_destinatario_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='funcionario',
            name='user',
        ),
        migrations.AddField(
            model_name='funcionario',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='funcionario',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='funcionario',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
        migrations.AddField(
            model_name='funcionario',
            name='password',
            field=models.CharField(default=123, max_length=128, verbose_name='password'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='funcionario',
            name='documento',
            field=models.CharField(max_length=11, unique=True, verbose_name='Documento'),
        ),
        migrations.AlterField(
            model_name='funcionario',
            name='email',
            field=models.EmailField(max_length=45, unique=True, verbose_name='E-mail'),
        ),
    ]
