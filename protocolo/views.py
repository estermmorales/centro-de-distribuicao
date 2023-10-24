from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from django.db.models.functions import TruncDate
from .models import Protocolo

# Create your views here.


def protocolo(request):
    hoje = timezone.now()
    ultimos_30_dias = hoje - timedelta(days=30)

    protocolos_hoje = Protocolo.objects.annotate(
        data_trunc=TruncDate('data_entrega')).filter(data_trunc=hoje.date())
    protocolos_ultimos_30_dias = Protocolo.objects.annotate(data_trunc=TruncDate(
        'data_entrega')).filter(data_trunc__gte=ultimos_30_dias.date())
    todos_protocolos = Protocolo.objects.all()

    context = {
        'protocolos_hoje': protocolos_hoje,
        'protocolos_ultimos_30_dias': protocolos_ultimos_30_dias,
        'todos_protocolos': todos_protocolos,
    }

    return render(request, 'protocolo.html', context)


def historico(request):
    return render(request, 'historico.html')


def usuarios(request):
    return render(request, 'usuarios.html')


def funcionarios(request):
    return render(request, 'funcionarios.html')
