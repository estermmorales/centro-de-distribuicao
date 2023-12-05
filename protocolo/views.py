import datetime
from django.shortcuts import redirect, render
from django.utils import timezone
from datetime import timedelta
from .models import Funcionario, Protocolo, EmitenteDestinatario, Endereco, Historico
from .forms import ProtocoloForm, EmitenteDestinatarioEnderecoForm, LoginForm, FuncionarioForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseServerError, JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa

@login_required(login_url='/login')
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



@login_required(login_url='/login')
def cadastrar_protocolo(request):
    if request.method == 'POST':
        form = ProtocoloForm(request.POST)
        if form.is_valid():
            protocolo = form.save(commit=False)

            protocolo.id_funcionario = request.user
            protocolo.save() 

            Historico.objects.create(protocolo=protocolo, operacao='Pendente', funcionario=protocolo.id_funcionario)
            return redirect('/')
        else:
            print(form.errors)
    else:
        return JsonResponse({'success': False, 'errors': form.errors})
    return redirect('/')


@login_required(login_url='/login')
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
            Historico.objects.create(protocolo=protocolo, operacao='Retirado', funcionario=request.user)
        if (nova_situacao == 'Cancelado'):
            Historico.objects.create(protocolo=protocolo, operacao='Cancelado', funcionario=request.user)
        protocolo.situacao = nova_situacao

        
    protocolo.save()
    return redirect('/')

@login_required(login_url='/login')
def excluir_protocolo(request):
    protocolo_id = request.POST.get('protocolo_id')
    protocolo = Protocolo.objects.get(id=protocolo_id)
    protocolo.delete()
    return redirect('/')


@login_required(login_url='/login')
def pegar_protocolo_por_id(request, protocolo_id):
    protocolo = Protocolo.objects.filter(id=protocolo_id)

    total_retirado = protocolo.filter(situacao='retirado').count()
    total_pendente = protocolo.filter(situacao='pendente').count()
    total_cancelado = protocolo.filter(situacao='cancelado').count()

    paginator = Paginator(protocolo, 1)
    page = request.GET.get('page')
    protocolo = paginator.get_page(page)

    context = {
        'protocolos': protocolo,
        'total_retirado': total_retirado,
        'total_pendente': total_pendente,
        'total_cancelado': total_cancelado,
    }

    return render(request, 'protocolo.html', context)


@login_required(login_url='/login')
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

@login_required(login_url='/login')
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

@login_required(login_url='/login')
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
    
@login_required(login_url='/login')
def excluir_usuario(request):
    usuario_id = request.POST.get('usuario_id')
    usuario = EmitenteDestinatario.objects.get(id=usuario_id)
    usuario.delete()
    return redirect('/usuarios')

@login_required(login_url='/login')
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

@login_required(login_url='/login')
def cadastrar_funcionario(request):
    if request.method == 'POST':
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            login(request, user)
            return redirect('funcionarios')  
    else:
        form = FuncionarioForm()
    return redirect('funcionarios')

@login_required(login_url='/login')
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

@login_required(login_url='/login')
def excluir_funcionario(request):
    funcionario_id = request.POST.get('funcionario_id')
    funcionario = Funcionario.objects.get(id=funcionario_id)
    funcionario.delete()
    return redirect('funcionarios')


def autocomplete_usuarios(request):
    termo_pesquisa = request.GET.get('term', '')
    tabela_pesquisa = request.GET.get('tabela', '')

    if tabela_pesquisa == 'funcionario':
        usuarios = Funcionario.objects.filter(nome__icontains=termo_pesquisa)
    else:
        usuarios = EmitenteDestinatario.objects.filter(nome__icontains=termo_pesquisa)  
    
    resultados = [usuario.nome for usuario in usuarios]
    
    return JsonResponse(resultados, safe=False)

@login_required(login_url='/login')
def historico(request):
    historico = Historico.objects.all().order_by('-id')

    # Paginação
    paginator = Paginator(historico, 10)
    page = request.GET.get('page')
    historico = paginator.get_page(page)

    return render(request, 'historico.html', {'historico': historico})

class RelatorioPDF(View):
    def get(self, request, *args, **kwargs):

        protocolos = Protocolo.objects.all().order_by('-id')[:10]

        template_path = 'relatorio.html'
        context = {'protocolos': protocolos}

        # Renderiza o template HTML
        template = get_template(template_path)
        html = template.render(context)

        # Criação do PDF usando xhtml2pdf
        response = HttpResponse(content_type='application/pdf')
        
        # Define o nome do arquivo com "Protocolos" + data atual
        nome_arquivo = f"Protocolos_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{nome_arquivo}"'

        pisa_status = pisa.CreatePDF(
            html, dest=response, encoding='utf-8')

        if pisa_status.err:
            return HttpResponse('Erro ao gerar o PDF', status=500)

        return response

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


def login_view(request):
    if request.method == 'POST':
        try:
            form = LoginForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                user = authenticate(request, email=email, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('protocolo') 
        except Exception as e:
            print(f"Erro durante o login: {e}")
            return HttpResponseServerError("Erro interno do servidor")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')