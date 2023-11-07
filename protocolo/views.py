from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from datetime import timedelta
from django.db.models.functions import TruncDate
from .models import Funcionario, Protocolo, EmitenteDestinatario, Endereco
from .forms import ProtocoloForm, EmitenteDestinatarioEnderecoForm, FuncionarioForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


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
            protocolo = form.save(commit=False)
            # Associe o funcionário logado ao protocolo
            # protocolo.id_funcionario = Funcionario.objects.get(
            #     user=request.user)
            protocolo.save() 
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

def excluir_protocolo(request):
    protocolo_id = request.POST.get('protocolo_id')
    protocolo = Protocolo.objects.get(id=protocolo_id)
    protocolo.delete()
    return redirect('/')


def usuarios(request):
    usuarios = EmitenteDestinatario.objects.all().order_by('-id')
    nome_pesquisado = request.GET.get('nome-usuario') 
    if nome_pesquisado:
        usuarios = usuarios.filter(nome=nome_pesquisado)

    # Paginação
    paginator = Paginator(usuarios, 10)
    page = request.GET.get('page')
    usuarios = paginator.get_page(page)

    context = {
        "usuarios": usuarios,
    }
    return render(request, 'usuarios.html', context)


def cadastrar_usuarios(request):
    if request.method == 'POST':
        form = EmitenteDestinatarioEnderecoForm(request.POST)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            email = form.cleaned_data['email']
            documento = form.cleaned_data['documento']
            telefone = form.cleaned_data['telefone']
            cep = form.cleaned_data['cep']
            rua = form.cleaned_data['rua']
            bairro = form.cleaned_data['bairro']
            cidade = form.cleaned_data['cidade']
            estado = form.cleaned_data['estado']

            endereco = Endereco(cep=cep, rua=rua, bairro=bairro, cidade=cidade, estado=estado)
            endereco.save()
            endereco_object = Endereco.objects.filter(cep=cep)

            usuario = EmitenteDestinatario(nome=nome, email=email, documento=documento, telefone=telefone, id_endereco_id=endereco_object[0].id)
            usuario.save()

            return redirect('usuarios')
        else:
            print(form.errors)

    else:
        return JsonResponse({'success': False, 'errors': form.errors})

    return redirect('usuarios')

def editar_usuario(request):
    usuario = EmitenteDestinatario.objects.get(id=request.POST.get('usuario_id'))
    nome = request.POST.get('nome_editar')
    email = request.POST.get('email_editar')
    telefone = request.POST.get('telefone_editar')
    documento = request.POST.get('documento_editar')

    cep = request.POST.get('cep_editar')
    rua = request.POST.get('rua_editar')
    bairro = request.POST.get('bairro_editar')
    cidade = request.POST.get('cidade_editar')
    estado = request.POST.get('estado_editar')

    if(nome != usuario.nome):
        usuario.nome = nome
    if(email != usuario.email):
        usuario.email = email
    if(telefone != usuario.telefone):
        usuario.telefone = telefone
    if (documento != usuario.documento):
        usuario.documento = documento
    
    if(cep != usuario.id_endereco.cep):
        usuario.id_endereco.cep = cep
    if (rua != usuario.id_endereco.rua):
        usuario.id_endereco.rua = rua
    if (bairro != usuario.id_endereco.bairro):
        usuario.id_endereco.bairro = bairro
    if (cidade != usuario.id_endereco.cidade):
        usuario.id_endereco.cidade = cidade
    if (estado != usuario.id_endereco.estado):
        usuario.id_endereco.estado = estado

    usuario.save()
    return redirect('usuarios')
    

def excluir_usuario(request):
    usuario_id = request.POST.get('usuario_id')
    usuario = EmitenteDestinatario.objects.get(id=usuario_id)
    usuario.delete()
    return redirect('/usuarios')

def funcionarios(request):
    funcionarios = Funcionario.objects.all().order_by('-id')
    nome_pesquisado = request.GET.get('nome-usuario') 
    if nome_pesquisado:
        funcionarios = funcionarios.filter(nome=nome_pesquisado)

    # Paginação
    paginator = Paginator(funcionarios, 10)
    page = request.GET.get('page')
    funcionarios = paginator.get_page(page)

    context = {
        "funcionarios": funcionarios,
    }
    return render(request, 'funcionarios.html', context)

def cadastrar_funcionario(request):
    if request.method == 'POST':
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('funcionarios')
        else:
            print(form.errors)
    else:
        return JsonResponse({'success': False, 'errors': form.errors})
    return redirect('funcionarios')

def editar_funcionario(request):
    funcionario = Funcionario.objects.get(id=request.POST.get('funcionario_id'))
    nome = request.POST.get('nome_editar')
    email = request.POST.get('email_editar')
    telefone = request.POST.get('telefone_editar')
    documento = request.POST.get('documento_editar')
    permissao = request.POST.get('permissao_editar')

    if(nome != funcionario.nome):
        funcionario.nome = nome
    if(email != funcionario.email):
        funcionario.email = email
    if(telefone != funcionario.telefone):
        funcionario.telefone = telefone
    if (documento != funcionario.documento):
        funcionario.documento = documento
    if (permissao != funcionario.permissao):
        funcionario.permissao = permissao

    funcionario.save()
    return redirect('funcionarios')

def excluir_funcionario(request):
    funcionario_id = request.POST.get('funcionario_id')
    funcionario = Funcionario.objects.get(id=funcionario_id)
    user = User.objects.get(username=funcionario.email)
    funcionario.delete()
    user.delete()
    return redirect('funcionarios')

def autocomplete_usuarios(request):
    termo_pesquisa = request.GET.get('term', '')
    tabela_pesquisa = request.GET.get('tabela', '')

    if tabela_pesquisa == 'funcionario':
        usuarios = Funcionario.objects.filter(nome__icontains=termo_pesquisa)
    else:
        usuarios = EmitenteDestinatario.objects.filter(nome__icontains=termo_pesquisa)  
    
    # Crie uma lista de nomes de usuários correspondentes
    resultados = [usuario.nome for usuario in usuarios]
    
    return JsonResponse(resultados, safe=False)

def historico(request):
    return render(request, 'historico.html')

def configuracoes(request):
    return render(request, 'configuracoes.html')

def handler404(request, exception):
    context = {}
    response = render(request, "errors/404.html", context=context)
    response.status_code = 404
    return response


def handler500(request):
    context = {}
    response = render(request, "errors/500.html", context=context)
    response.status_code = 500
    return response

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('protocolos')
        else:
            error_message = "Nome de usuário ou senha incorretos."
        return render(request, 'login.html', {'error_message': error_message})
    
    return render(request, 'login.html')