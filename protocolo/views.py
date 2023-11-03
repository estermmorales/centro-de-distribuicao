from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from datetime import timedelta
from django.db.models.functions import TruncDate
from .models import Funcionario, Protocolo, EmitenteDestinatario
from .forms import ProtocoloForm, ProtocoloEditForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.db.models import Q


def protocolo(request):
    protocolos = Protocolo.objects.all().order_by('-id')

    total_retirado = protocolos.filter(situacao='retirado').count()
    total_pendente = protocolos.filter(situacao='pendente').count()
    total_cancelado = protocolos.filter(situacao='cancelado').count()

    situacao = request.GET.get('situacao')
    periodo = request.GET.get('periodo')
    nome_pesquisado = request.GET.get('nome-usuario') 
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
            total_retirado = protocolos.filter(situacao='retirado', data_entrega__range=(data_inicio, data_fim)).count()
            total_pendente = protocolos.filter(situacao='pendente', data_entrega__range=(data_inicio, data_fim)).count()
            total_cancelado = protocolos.filter(situacao='cancelado', data_entrega__range=(data_inicio, data_fim)).count()
        elif periodo == '30dias':
            data_fim = hoje.date()
            data_inicio = hoje - timedelta(days=30)
            protocolos = protocolos.filter(data_entrega__range=(data_inicio, data_fim))
            total_retirado = protocolos.filter(situacao='retirado', data_entrega__range=(data_inicio, data_fim)).count()
            total_pendente = protocolos.filter(situacao='pendente', data_entrega__range=(data_inicio, data_fim)).count()
            total_cancelado = protocolos.filter(situacao='cancelado', data_entrega__range=(data_inicio, data_fim)).count()


    if nome_pesquisado:
        usuario = EmitenteDestinatario.objects.get(nome=nome_pesquisado)
        protocolos = protocolos.filter(Q(id_emitente_id=usuario.id) | Q(id_destinatario_id=usuario.id))
        total_retirado = protocolos.filter(situacao='retirado').count()
        total_pendente = protocolos.filter(situacao='pendente').count()
        total_cancelado = protocolos.filter(situacao='cancelado').count()


    # Paginação
    paginator = Paginator(protocolos, 10)
    page = request.GET.get('page')
    protocolos = paginator.get_page(page)

    context = {
        'protocolos': protocolos,
        'situacao_selecionada': situacao,
        'periodo_selecionado': periodo,
        'total_retirado': total_retirado,
        'total_pendente': total_pendente,
        'total_cancelado': total_cancelado,
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
def editar_protocolo(request):
    protocolo = Protocolo.objects.get(id=request.POST.get('protocolo_id'))

    id_emitente = protocolo.id_emitente_id
    get_emitente = EmitenteDestinatario.objects.get(id=id_emitente)

    id_destinatario = protocolo.id_destinatario_id
    get_destinatario = EmitenteDestinatario.objects.get(id=id_destinatario)
    
    novo_emitente = request.POST.get('nome_emitente_editar')
    get_novo_emitente = EmitenteDestinatario.objects.get(nome=novo_emitente)
    if (get_novo_emitente.nome != get_emitente.nome):
        protocolo.id_emitente_id = get_novo_emitente.id

    novo_destinatario = request.POST.get('nome_destinatario_editar')
    get_novo_destinatario = EmitenteDestinatario.objects.get(nome=novo_destinatario)
    if (get_novo_destinatario.nome != get_destinatario.nome):
        protocolo.id_destinatario_id = get_novo_destinatario.id

    novo_qtd_volumes = request.POST.get('qtd_volumes_editar')
    if (novo_qtd_volumes != protocolo.qtd_volumes):
        protocolo.qtd_volumes = int(str(novo_qtd_volumes))

    nova_situacao = request.POST.get('situacao_editar')
    if(nova_situacao != protocolo.situacao):
        if (nova_situacao == 'Retirado'):
            protocolo.data_retirada = timezone.now()
        protocolo.situacao = nova_situacao

        
    protocolo.save()
    return redirect('/')

def autocomplete_usuarios(request):
    termo_pesquisa = request.GET.get('term', '')  # Obtenha o termo de pesquisa da solicitação
    usuarios = EmitenteDestinatario.objects.filter(nome__icontains=termo_pesquisa)  # Realize a pesquisa no banco de dados
    
    # Crie uma lista de nomes de usuários correspondentes
    resultados = [usuario.nome for usuario in usuarios]
    
    return JsonResponse(resultados, safe=False)

def historico(request):
    return render(request, 'historico.html')


def usuarios(request):
    return render(request, 'usuarios.html')


def funcionarios(request):
    return render(request, 'funcionarios.html')
