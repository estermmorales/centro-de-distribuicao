from django.shortcuts import redirect, render
from django.utils import timezone
from datetime import timedelta
from django.db.models.functions import TruncDate
from .models import Funcionario, Protocolo
from .forms import ProtocoloForm, ProtocoloEditForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

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


# @login_required
def cadastrar_protocolo(request):
    if request.method == 'POST':
        form = ProtocoloForm(request.POST)
        if form.is_valid():
            # Crie o protocolo a partir do formulário, mas não o salve ainda
            protocolo = form.save(commit=False)
            # Associe o funcionário logado ao protocolo
            protocolo.id_funcionario = Funcionario.objects.get(
                user=request.user)
            protocolo.save()  # Agora, salve o protocolo no banco de dados
            return redirect('/')
        else:
            print(form.errors)
    else:
        return JsonResponse({'success': False, 'errors': form.errors})
    return redirect('/')


@login_required
def editar_protocolo(request, protocolo_id):
    protocolo = Protocolo.objects.get(pk=protocolo_id)

    if request.method == 'POST':
        form = ProtocoloEditForm(request.POST, instance=protocolo)
        if form.is_valid():
            protocolo = form.save(commit=False)
            protocolo.id_funcionario = request.user
            protocolo.save()
            return redirect('lista_protocolos')
    else:
        form = ProtocoloEditForm(instance=protocolo)
    return render(request, 'protocolos/editar_protocolo.html', {'form': form})


def historico(request):
    return render(request, 'historico.html')


def usuarios(request):
    return render(request, 'usuarios.html')


def funcionarios(request):
    return render(request, 'funcionarios.html')
