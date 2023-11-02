from django.shortcuts import redirect, render
from django.utils import timezone
from datetime import timedelta
from django.db.models.functions import TruncDate
from .models import Funcionario, Protocolo
from .forms import ProtocoloForm, ProtocoloEditForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView

def protocolo(request):
    protocolos = Protocolo.objects.all().order_by('-data_entrega')

    situacao = request.GET.get('situacao')
    periodo = request.GET.get('periodo')
    hoje = timezone.now()
    data_inicio = None
    data_fim = None

    if situacao:
        protocolos = protocolos.filter(situacao=situacao)

    if periodo:
        if periodo == 'hoje':
            data_inicio = hoje.date()
            data_fim = hoje.date()
            protocolos = protocolos.filter(data_entrega__range=(data_inicio, data_fim))
        elif periodo == '30dias':
            data_fim = hoje.date()
            data_inicio = hoje - timedelta(days=30)
            protocolos = protocolos.filter(data_entrega__range=(data_inicio, data_fim))

    # Paginação
    paginator = Paginator(protocolos, 10)
    page = request.GET.get('page')
    protocolos = paginator.get_page(page)

    context = {
        'protocolos': protocolos,
        'situacao_selecionada': situacao,
        'periodo_selecionado': periodo,
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
            # protocolo.id_funcionario = Funcionario.objects.get(
            #     user=request.user)
            protocolo.save()  # Agora, salve o protocolo no banco de dados
            return redirect('/')
        else:
            print(form.errors)
    else:
        return JsonResponse({'success': False, 'errors': form.errors})
    return redirect('/')


#@login_required
def editar_protocolo(request, protocolo_id):
    protocolo = Protocolo.objects.get(id=protocolo_id)

    if request.method == 'POST':
        form = ProtocoloEditForm(request.POST, instance=protocolo)
        if form.is_valid():
            protocolo = form.save(commit=False)
            #protocolo.id_funcionario = request.user
            protocolo.save()
            return redirect('/')
        else:
            print(form.errors)
    
    


def historico(request):
    return render(request, 'historico.html')


def usuarios(request):
    return render(request, 'usuarios.html')


def funcionarios(request):
    return render(request, 'funcionarios.html')
