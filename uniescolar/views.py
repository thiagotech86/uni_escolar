from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, AddAulaForm, CustomLoginForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Aula, Aluno, Professor 
from datetime import datetime, timedelta, date 
from django.http import JsonResponse # Para excluir_aula
from django.views.decorators.csrf import csrf_exempt # Para excluir_aula
from django.views.decorators.http import require_POST # Para excluir_aula

# Create your views here.

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Usuário ou senha inválidos')
        else:
            form.add_error(None, 'Erro no formulário. Tente novamente!')
    else:
        form = CustomLoginForm()

    return render(request, 'login.html', {'form': form})


# Tela Home / Login
def home(request):
    # Lógica de autenticação para requisições POST
    if request.method == "POST":
        username_from_form = request.POST.get('username')
        password_from_form = request.POST.get('password')
        user_type_selected = request.POST.get('user_type') # Captura o tipo de usuário selecionado no formulário

        user = authenticate(request, username=username_from_form, password=password_from_form)

        if user is not None:
            auth_login(request, user) # Realiza o login

            
            if user_type_selected:
                request.session['view_as_type'] = user_type_selected
            
            messages.success(request, "Login realizado com sucesso!")
            return redirect('home') # Redireciona para a própria home (será uma requisição GET)
        else:
            messages.error(request, "Usuário ou senha inválidos.")
            return redirect('home') # Redireciona para a home para mostrar o erro e o formulário novamente

    
    
    processed_aulas = []
    total_acumulado_timedelta = timedelta()
    horas_contratadas_por_aluno = {}
    total_contratado_geral = 0.0
    total_geral_em_horas = 0.0 # Inicializa para o caso de usuário não autenticado

    if request.user.is_authenticated:
        aulas_queryset = Aula.objects.all() # Ou filtre as aulas conforme sua necessidade (ex: por usuário)
        
        for aula_instance in aulas_queryset:
            aula_instance.duracao = 0.0 # Inicializa o atributo para o template
            if aula_instance.hora_inicio and aula_instance.hora_fim:
                # Use a data da aula se disponível e relevante para a duração.
                dia_para_calculo = aula_instance.data_inicio if aula_instance.data_inicio else date.today()

                try:
                    datetime_inicio = datetime.combine(dia_para_calculo, aula_instance.hora_inicio)
                    datetime_fim = datetime.combine(dia_para_calculo, aula_instance.hora_fim)

                    if datetime_fim > datetime_inicio:
                        duracao_aula_timedelta = datetime_fim - datetime_inicio
                        total_acumulado_timedelta += duracao_aula_timedelta
                        aula_instance.duracao = round(duracao_aula_timedelta.total_seconds() / 3600, 2)
                except TypeError:
                    # Lida com casos onde hora_inicio/fim podem não ser objetos time válidos
                    aula_instance.duracao = 0.0
            
            processed_aulas.append(aula_instance)

        total_geral_em_horas = round(total_acumulado_timedelta.total_seconds() / 3600, 2)

        # Calcula horas contratadas (apenas se usuário autenticado)
        for aluno_obj in Aluno.objects.all(): # Adapte este queryset se necessário
            try:
                horas_aluno = aluno_obj.horas_contratadas() # Método deve existir no modelo Aluno
                horas_contratadas_por_aluno[aluno_obj.nome] = float(horas_aluno if horas_aluno is not None else 0.0)
            except (ValueError, TypeError, AttributeError): 
                horas_contratadas_por_aluno[aluno_obj.nome] = 0.0
                
        total_contratado_geral = sum(horas_contratadas_por_aluno.values())



    context = {
        'aulas': processed_aulas,
        'total': total_geral_em_horas, # Total de horas/aula dadas
        'horas_contratadas_aluno': horas_contratadas_por_aluno,
        'total_contratado_todos': total_contratado_geral,
    }
    return render(request, 'home.html', context)


def logout_user(request):
    logout(request)
    messages.success(request, "Logout com sucesso!")
    return redirect('home')


def total_aulas(request,id):
    if request.user.is_authenticated:
        total=Aula.objects.count()

        return render (request,'home.html',{'total':total})
    else:
        messages.error(request,'Você precisa estar logado')
        return redirect('home')


def register_user(request):
    if request.method == 'POST': 
        user_form = SignUpForm(request.POST)
        if user_form.is_valid(): 
            user = user_form.save(commit=False)
            user.senha = make_password(user_form.cleaned_data['senha'])
            user.save()

            cpf = user_form.cleaned_data['cpf']
            senha = user_form.cleaned_data['senha']
            user = authenticate(
                request,
                username=cpf,  # cuidado: precisa adaptar para seu authenticate aceitar CPF
                password=senha
            )
            if user is not None:
                login(request, user)
                messages.success(request, 'Login realizado com sucesso')
                return redirect('home')
            else:
                messages.error(request, 'Erro ao autenticar. Tente novamente.')

    else:
        user_form = SignUpForm()

    return render(request, "register.html", {'user_form': user_form})

def book_detail(request,id):
    if request.user.is_authenticated:
        book=Aula.objects.get(id=id) # Buscar objeto pelo id
        return render (request,'book.html',{'book':book})
    else:
        messages.error(request,'Você precisa estar logado')
        return redirect('home')


@login_required
def add_aula(request): # Mude este nome se sua view se chamar diferente
    is_professor = Professor.objects.filter(pk=request.user.pk).exists()
    if not (request.user.is_superuser or is_professor):
        raise PermissionDenied("Você não tem permissão para acessar esta página.")

    if request.method == 'POST':
        form = AddAulaForm(request.POST) # Use seu formulário de adicionar aula
        if form.is_valid():
            
            form.save() 
            messages.success(request, "Aula cadastrada com sucesso!")
            return redirect('home') 
        
    else:
        form = AddAulaForm() # Formulário para GET

    # A variável 'can_add_aula_permission' já estará no contexto devido ao context processor
    return render(request, 'uniescolar/add_aula.html', {'form': form})

def aula_detail(request,id):
    if request.user.is_authenticated:
        aula=Aula.objects.get(id=id) # Buscar objeto pelo id
        return render (request,'aula.html',{'aula':aula})
    else:
        messages.error(request,'Você precisa estar logado')
        return redirect('home')

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

@require_POST
@csrf_exempt  # se não quiser usar isso, certifique-se de que o CSRF token está presente no JS
def excluir_aula(request, aula_id):
    if request.user.is_authenticated:
        try:
            aula = Aula.objects.get(id=aula_id)
            aula.delete()
            return JsonResponse({'status': 'ok'})
        except Aula.DoesNotExist:
            return JsonResponse({'status': 'erro', 'mensagem': 'Aula não encontrada'}, status=404)
    else:
        return JsonResponse({'status': 'erro', 'mensagem': 'Usuário não autenticado'}, status=401)
