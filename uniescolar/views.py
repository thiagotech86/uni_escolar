from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import Aula
from .forms import SignUpForm, AddAulaForm, CustomLoginForm
from django.contrib.auth.hashers import make_password

# Create your views here.

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "Login realizado com sucesso!")

                # Obtém o tipo de usuário do formulário
                user_type = request.POST.get('userType')

                if user_type == 'cliente':
                    # Redireciona para a home (que lista aulas para autenticados)
                    return redirect('home')

                elif user_type == 'professor':
                    # Redireciona para a página de adicionar aula
                    return redirect('add_aula') # Redireciona para a URL nomeada 'add_aula'

                else:
                    # Redirecionamento padrão caso o tipo de usuário não seja reconhecido
                    return redirect('home')

            else:
                messages.error(request, 'Usuário ou senha inválidos')
                form = CustomLoginForm(request.POST)
                return render(request, 'login.html', {'form': form})

        else:
            messages.error(request, 'Erro no formulário. Verifique os campos.')
            form = CustomLoginForm(request.POST)
            return render(request, 'login.html', {'form': form})

    else:
        form = CustomLoginForm()
        return render(request, 'login.html', {'form': form})


# Tela Home / Login
def home(request):

    aulas=Aula.objects.all() 

    if request.method=="POST": # Se o método request for post, valide login e senha, se não retorne a página home.
        username=request.POST['usuario']
        password=request.POST['senha']
        #Autenticação
        user=authenticate(
            request,
            username=username,
            password=password
        )
        if user is not None: # condição após a validação
            login(request,user)
            messages.success(request,"Login realizado com sucesso!") # mensagem de confirmação de login
            return redirect('home')
        else:
            messages.error(request,"Erro na autenticação. Tente novamente!") # mensagem de erro de login
            return redirect('home')

    else:
        return render(request,'home.html',{'aulas':aulas}) 


def logout_user(request):
    logout(request)
    messages.success(request, "Logout com sucesso!")
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
    

def add_aula(request):
    form = AddAulaForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, 'Livro adicionado com sucesso!')
                return redirect('home')
        return render(request, 'add_aula.html', {'form':form})
    else:
        messages.error(request, 'Você deve estar autenticado para adicionar livro')
        return redirect('home')
    
def aula_detail(request,id):
    if request.user.is_authenticated:
        aula=Aula.objects.get(id=id) # Buscar objeto pelo id
        return render (request,'aula.html',{'aula':aula})
    else:
        messages.error(request,'Você precisa estar logado')
        return redirect('home')





