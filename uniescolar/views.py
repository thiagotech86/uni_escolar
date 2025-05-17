from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from .forms import SignUpForm, AddAulaForm 
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from .models import Aula, Aluno, Professor, Responsavel, Gestor, Disciplina
from datetime import datetime, timedelta, date 
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django import forms 
import json

# Create your views here.

# Função auxiliar para verificar se o usuário é Gestor
def is_gestor_check(user):
    return user.is_authenticated and hasattr(user, 'gestor_profile')

# Tela Home / Login
def home(request):
    if request.method == "POST": # Tentativa de Login
        username_from_form = request.POST.get('username')
        password_from_form = request.POST.get('password')
        user_type_selected = request.POST.get('user_type')

        user = authenticate(request, username=username_from_form, password=password_from_form)

        if user is not None:
            actual_user_type_matches = False
            is_responsavel = hasattr(user, 'responsavel_profiles') and user.responsavel_profiles.exists()
            is_professor = hasattr(user, 'professor_profile')
            is_gestor = is_gestor_check(user) # Usa a função auxiliar

            if user_type_selected == 'aluno_responsavel' and is_responsavel:
                actual_user_type_matches = True
            elif user_type_selected == 'professor' and is_professor:
                actual_user_type_matches = True
            elif user_type_selected == 'gestor' and is_gestor:
                actual_user_type_matches = True
            
            if actual_user_type_matches:
                auth_login(request, user)
                messages.success(request, "Login realizado com sucesso!")
                return redirect('home') 
            else:
                logout(request)
                type_display_name_selected = user_type_selected.replace('_', ' ').title()
                correct_roles = []
                if is_responsavel: correct_roles.append("Responsável")
                if is_professor: correct_roles.append("Professor")
                if is_gestor: correct_roles.append("Gestor")
                error_msg = f"Login falhou. Você selecionou '{type_display_name_selected}', mas seu perfil é: {', '.join(correct_roles) if correct_roles else 'não identificado'}. Por favor, selecione o tipo correto."
                messages.error(request, error_msg)
                return redirect('home')
        else:
            messages.error(request, "Usuário ou senha inválidos.")
            return redirect('home')

    # GET request: Exibir página
    aulas_list = []
    total_horas_aulas_filtradas = timedelta() 
    
    # Dados para o JavaScript (filtros de aluno/professor)
    horas_contratadas_por_aluno_dict = {}
    total_contratado_todos_alunos_val = 0.0 # Soma de todas as horas contratadas de todos os alunos (para JS)

    # Variáveis para o contexto específico do Responsável logado
    total_contratado_responsavel_logado = 0
    total_utilizado_pelo_responsavel_logado = 0
    saldo_total_horas_responsavel = 0
    
    # Determina os perfis do usuário logado uma vez
    user_is_gestor_profile = False
    user_is_professor_profile = False
    user_is_responsavel_profile = False

    if request.user.is_authenticated:
        user_is_gestor_profile = is_gestor_check(request.user)
        user_is_professor_profile = hasattr(request.user, 'professor_profile')
        user_is_responsavel_profile = hasattr(request.user, 'responsavel_profiles') and request.user.responsavel_profiles.exists()

        aulas_queryset = Aula.objects.none()

        if user_is_gestor_profile:
            aulas_queryset = Aula.objects.all().select_related('disciplina', 'aluno', 'professor__user').order_by('-data_inicio', '-hora_inicio')
        elif user_is_professor_profile:
            try:
                aulas_queryset = Aula.objects.filter(professor=request.user.professor_profile).select_related('disciplina', 'aluno', 'professor__user').order_by('-data_inicio', '-hora_inicio')
            except Professor.DoesNotExist:
                messages.error(request, "Perfil de professor não encontrado.")
        elif user_is_responsavel_profile:
            responsavel_instances = request.user.responsavel_profiles.all()
            aulas_queryset = Aula.objects.filter(
                aluno__responsavel__in=responsavel_instances,
                status_aprovacao='aprovada'
            ).select_related('disciplina', 'aluno', 'professor__user').distinct().order_by('-data_inicio', '-hora_inicio')

        for aula_instance in aulas_queryset:
            aula_instance.duracao_calculada = 0.0
            if aula_instance.hora_inicio and aula_instance.hora_fim:
                dia_para_calculo = aula_instance.data_inicio if aula_instance.data_inicio else date.today()
                try:
                    datetime_inicio = datetime.combine(dia_para_calculo, aula_instance.hora_inicio)
                    datetime_fim = datetime.combine(dia_para_calculo, aula_instance.hora_fim)
                    if datetime_fim > datetime_inicio:
                        duracao_aula_timedelta = datetime_fim - datetime_inicio
                        if aula_instance.status_aprovacao == 'aprovada' or \
                           user_is_gestor_profile or \
                           (user_is_professor_profile and aula_instance.professor == request.user.professor_profile):
                            total_horas_aulas_filtradas += duracao_aula_timedelta
                        aula_instance.duracao_calculada = round(duracao_aula_timedelta.total_seconds() / 3600, 2)
                except TypeError:
                    aula_instance.duracao_calculada = 0.0
            aulas_list.append(aula_instance)

        for aluno_obj in Aluno.objects.all(): 
            try:
                horas_aluno_contratadas = aluno_obj.horas_contratadas() 
                horas_contratadas_por_aluno_dict[aluno_obj.nome] = float(horas_aluno_contratadas if horas_aluno_contratadas is not None else 0.0)
            except Exception: 
                horas_contratadas_por_aluno_dict[aluno_obj.nome] = 0.0
        total_contratado_todos_alunos_val = sum(horas_contratadas_por_aluno_dict.values())
        
        if user_is_responsavel_profile:
            responsavel_instances = request.user.responsavel_profiles.all()
            
            for resp_instance in responsavel_instances:
                # Garante que horas_contratadas seja um número antes de somar
                soma_pacotes_resp = sum(pacote.horas_contratadas for pacote in resp_instance.pacotes_hora.all() if isinstance(pacote.horas_contratadas, (int, float)))
                total_contratado_responsavel_logado += soma_pacotes_resp
            
            alunos_do_responsavel_logado = Aluno.objects.filter(responsavel__in=responsavel_instances)
            for aluno_resp in alunos_do_responsavel_logado:
                horas_usadas_aluno = aluno_resp.horas_utilizadas() 
                if isinstance(horas_usadas_aluno, (int, float)): # CORREÇÃO APLICADA AQUI
                    total_utilizado_pelo_responsavel_logado += horas_usadas_aluno
                else:
                    # Opcional: Logar que horas_utilizadas() retornou um tipo inesperado (None)
                    print(f"AVISO: Aluno ID {aluno_resp.id} - horas_utilizadas() retornou {type(horas_usadas_aluno)} em vez de um número.")
            
            saldo_total_horas_responsavel = total_contratado_responsavel_logado - total_utilizado_pelo_responsavel_logado

    context = {
        'aulas': aulas_list,
        'total_horas_aulas_filtradas': round(total_horas_aulas_filtradas.total_seconds() / 3600, 2),
        'horas_contratadas_por_aluno_json': json.dumps(horas_contratadas_por_aluno_dict),
        'total_contratado_todos_alunos_json': json.dumps(total_contratado_todos_alunos_val),
        'user_is_gestor': user_is_gestor_profile,
        'total_contratado_responsavel': total_contratado_responsavel_logado if user_is_responsavel_profile else None,
        'total_utilizado_responsavel': total_utilizado_pelo_responsavel_logado if user_is_responsavel_profile else None,
        'saldo_horas_responsavel': saldo_total_horas_responsavel if user_is_responsavel_profile else None,
    }
    return render(request, 'home.html', context)

@login_required
def add_aula(request):
    is_logged_user_gestor = is_gestor_check(request.user)
    is_logged_user_professor = hasattr(request.user, 'professor_profile')

    if not (is_logged_user_gestor or is_logged_user_professor):
        raise PermissionDenied("Você não tem permissão para adicionar aulas.")

    if request.method == 'POST':
        form = AddAulaForm(request.POST)
        
        if is_logged_user_professor and not is_logged_user_gestor:
            post_data = request.POST.copy()
            post_data['professor'] = request.user.pk
            form = AddAulaForm(post_data)

        if form.is_valid():
            aula_instance = form.save(commit=False)
            
            if is_logged_user_gestor:
                aula_instance.status_aprovacao = 'aprovada'
            else: 
                aula_instance.status_aprovacao = 'pendente'
            
            # Se for professor não-gestor, garante que ele seja o professor da aula
            if is_logged_user_professor and not is_logged_user_gestor:
                aula_instance.professor = request.user.professor_profile

            aula_instance.save()
            form.save_m2m() 
            messages.success(request, f"Aula cadastrada com status '{aula_instance.get_status_aprovacao_display()}'!")
            return redirect('home')
        else:
            messages.error(request, "Erro ao cadastrar aula. Verifique os dados do formulário.")
    else: 
        form = AddAulaForm()
        if is_logged_user_professor and not is_logged_user_gestor:
            form.fields['professor'].initial = request.user.professor_profile
            form.fields['professor'].widget = forms.HiddenInput()
            form.fields['professor'].required = False # Torna não obrigatório no HTML, pois será preenchido

    return render(request, 'uniescolar/add_aula.html', {'form': form})


@login_required
@user_passes_test(is_gestor_check, login_url='home')
def editar_aprovar_aula_gestor(request, aula_id):
    aula = get_object_or_404(Aula, id=aula_id)

    if aula.status_aprovacao != 'pendente':
        messages.error(request, "Apenas aulas com status 'Pendente' podem ser editadas desta forma.")
        return redirect('home')

    if request.method == 'POST':
        form = AddAulaForm(request.POST, instance=aula)
        if form.is_valid():
            aula_editada = form.save(commit=False)

            if 'salvar_e_aprovar' in request.POST:
                aula_editada.status_aprovacao = 'aprovada'
                messages.success(request, f"Aula ID {aula_editada.id} ({aula_editada.disciplina}) foi editada e APROVADA com sucesso!")
            elif 'salvar_pendente' in request.POST:
                aula_editada.status_aprovacao = 'pendente' 
                messages.success(request, f"Aula ID {aula_editada.id} ({aula_editada.disciplina}) foi editada e mantida como PENDENTE.")
            else:
                messages.warning(request, "Ação não especificada. Alterações salvas, mas o status da aula permanece Pendente.")
                aula_editada.status_aprovacao = 'pendente'

            aula_editada.save()
            form.save_m2m()
            return redirect('home')
        else:
            messages.error(request, "Não foi possível salvar as alterações. Por favor, verifique os erros no formulário.")
    else: 
        form = AddAulaForm(instance=aula)

    context = {
        'form': form,
        'aula': aula,
        'page_title': f"Editar Aula Pendente (ID: {aula.id})",
    }
    return render(request, 'uniescolar/editar_aula_gestor.html', context)


@login_required
@user_passes_test(is_gestor_check, login_url='home') 
@require_POST 
def aprovar_aula_view(request, aula_id): # Certifique-se que esta view existe
    aula = get_object_or_404(Aula, id=aula_id)
    if aula.status_aprovacao == 'pendente':
        aula.status_aprovacao = 'aprovada'
        aula.save()
        messages.success(request, f"Aula ID {aula.id} ({aula.disciplina}) APROVADA com sucesso.")
    else:
        messages.warning(request, f"Aula ID {aula.id} não estava pendente ou já foi processada.")
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
@user_passes_test(is_gestor_check, login_url='home')
@require_POST
def rejeitar_aula_view(request, aula_id):
    aula = get_object_or_404(Aula, id=aula_id)
    if aula.status_aprovacao == 'pendente':
        aula.status_aprovacao = 'rejeitada'
        aula.save()
        messages.success(request, f"Aula ID {aula.id} ({aula.disciplina}) REJEITADA com sucesso.")
    else:
        messages.warning(request, f"Aula ID {aula.id} não estava pendente ou já foi processada.")
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
def aula_detail(request, id):
    aula_instance = get_object_or_404(Aula.objects.select_related('disciplina', 'aluno', 'professor__user'), id=id)
    
    user_can_view = False
    user_is_gestor = is_gestor_check(request.user)
    user_is_professor_of_aula = hasattr(request.user, 'professor_profile') and aula_instance.professor == request.user.professor_profile
    user_is_responsavel_of_aluno = False
    if hasattr(request.user, 'responsavel_profiles'):
        if aula_instance.aluno.responsavel in request.user.responsavel_profiles.all():
            user_is_responsavel_of_aluno = True

    if user_is_gestor:
        user_can_view = True
    elif user_is_professor_of_aula:
        user_can_view = True
    elif user_is_responsavel_of_aluno and aula_instance.status_aprovacao == 'aprovada':
        user_can_view = True
    
    if not user_can_view:
        messages.error(request, "Você não tem permissão para ver detalhes desta aula ou a aula não está aprovada.")
        return redirect('home')

    if not hasattr(aula_instance, 'duracao_calculada'):
        aula_instance.duracao_calculada = 0.0
        if aula_instance.hora_inicio and aula_instance.hora_fim:
            dia_para_calculo = aula_instance.data_inicio if aula_instance.data_inicio else date.today()
            try:
                datetime_inicio = datetime.combine(dia_para_calculo, aula_instance.hora_inicio)
                datetime_fim = datetime.combine(dia_para_calculo, aula_instance.hora_fim)
                if datetime_fim > datetime_inicio:
                    aula_instance.duracao_calculada = round((datetime_fim - datetime_inicio).total_seconds() / 3600, 2)
            except TypeError:
                pass
            
    return render(request,'aula.html',{'aula':aula_instance})


@login_required
@require_POST

def excluir_aula(request, aula_id):
    aula = get_object_or_404(Aula, id=aula_id)
    can_delete = False
    user_is_gestor = is_gestor_check(request.user)
    user_is_professor_of_aula = hasattr(request.user, 'professor_profile') and aula.professor == request.user.professor_profile

    if user_is_gestor:
        can_delete = True
    elif user_is_professor_of_aula and aula.status_aprovacao == 'pendente':
        can_delete = True
    
    if not can_delete:
        return JsonResponse({'status': 'erro', 'mensagem': 'Você não tem permissão para excluir esta aula ou o status não permite.'}, status=403)

    aula.delete()
    messages.success(request, "Aula excluída com sucesso!") # Mensagem para o backend
    return JsonResponse({'status': 'ok', 'mensagem': 'Aula excluída com sucesso!'})


def logout_user(request):
    logout(request)
    messages.success(request, "Logout realizado com sucesso!")
    return redirect('home')


def register_user(request):
    if request.method == 'POST': 
        user_form = SignUpForm(request.POST)
        if user_form.is_valid(): 
            usuario_instance = user_form.save(commit=False)
            usuario_instance.senha = make_password(user_form.cleaned_data['senha']) 
            usuario_instance.save()
            messages.success(request, 'Cadastro (modelo Usuário) realizado. Para login com perfis, um admin precisa criar seu usuário Django e vincular o perfil.')
            return redirect('home') 
        else:
            # Passar o formulário com erros de volta para o template
            messages.error(request, 'Erro no formulário de cadastro. Verifique os dados.')
            return render(request, "register.html", {'user_form': user_form})
    else:
        user_form = SignUpForm()
    return render(request, "register.html", {'user_form': user_form})

def aula_detail(request,id):
    if request.user.is_authenticated:
        aulas=Aula.objects.get(id=id) # Buscar objeto pelo id
        return render (request,'aula_detail.html',{'aula_detail':aulas})
    else:
        messages.error(request,'Você precisa estar logado')
        return redirect('home')