from django import forms
<<<<<<< HEAD
from .models import Aula, Aluno, Professor, Usuario, Disciplina
=======
from .models import  Aula, Disciplina, Aluno
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Aula, Disciplina, Aluno, Professor, Usuario 
import datetime
>>>>>>> main

from django.contrib.auth.forms import AuthenticationForm

import datetime

class CustomTimeSelect(forms.Select):
    def __init__(self, *args, **kwargs):
        # Agora usamos o objeto datetime.time como chave
        times = [
            (datetime.time(hour, minute), f'{hour:02d}:{minute:02d}')
            for hour in range(6, 23)  # De 06:00 até 22:30
            for minute in (0, 30)
        ]
        super().__init__(choices=times, *args, **kwargs)


<<<<<<< HEAD
class CustomLoginForm(AuthenticationForm):
    cpf = forms.CharField(label='cpf', max_length=100)
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)


class SignUpForm(forms.ModelForm):
=======
>>>>>>> main
    class Meta:
        model = Usuario
        fields = ['cpf', 'nome', 'email', 'telefone', 'senha']


class AddAulaForm(forms.ModelForm):
<<<<<<< HEAD
    local = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={"placeholder": "Local da aula", "class": "form-control"}
        ),
        label=""
    )
=======
    
    disciplina=forms.ModelChoiceField(Disciplina.objects.all()),
>>>>>>> main

    disciplina = forms.ModelChoiceField(
        queryset=Disciplina.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Disciplina"
    )

    data_inicio = forms.DateField(
        required=True,
        widget=forms.DateInput(
            attrs={"placeholder": "Data de início", "class": "form-control", "type": "date"}
        ),
        label="Data da Aula"
    )

    hora_inicio = forms.TimeField(
        required=True,
        initial=datetime.time(6, 0),
        widget=CustomTimeSelect(attrs={"class": "form-control"}),
        label="Hora de início"
    )

    hora_fim = forms.TimeField(
        required=True,
        initial=datetime.time(22, 0),
        widget=CustomTimeSelect(attrs={"class": "form-control"}),
        label="Hora de fim"
    )

    aluno = forms.ModelChoiceField(
        queryset=Aluno.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Aluno"
    )

    professor = forms.ModelChoiceField(
        queryset=Professor.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Professor"
    )

    descricao = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={"placeholder": "Descrição", "class": "form-control"}
        ),
        label="Descrição da aula"
    )

    class Meta:
<<<<<<< HEAD
=======
        model=Aula
        fields=('disciplina','aluno','descricao', 'data','inicio','termino',)

class CustomLoginForm(AuthenticationForm):
    user_type = forms.ChoiceField(
        label="Eu sou", # O label que aparecerá
        choices=[
            ('aluno_responsavel', 'Aluno/Responsável'),
            ('professor', 'Professor'),
        ],
        required=True, # Defina como True se a seleção for obrigatória
        widget=forms.Select(attrs={
            
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        
class CustomTimeSelect(forms.Select):
    """
    Widget personalizado para selecionar horários em intervalos de 30 minutos.
    Gera opções de horários das 06:00 às 22:30.
    """
    def __init__(self, *args, **kwargs):
        
        choices = [
            (datetime.time(hour, minute), f'{hour:02d}:{minute:02d}')
            for hour in range(6, 23)  
            for minute in (0, 30)   
        ]
        super().__init__(choices=choices, *args, **kwargs)


# Formulário de Login Atualizado
class CustomLoginForm(AuthenticationForm):
   
    user_type = forms.ChoiceField(
        label="Eu sou",
        choices=[
            ('aluno_responsavel', 'Aluno/Responsável'),
            ('professor', 'Professor'),
        ],
        required=True,
        widget=forms.Select(attrs={'class': 'form-control mb-3'}) # Estilização e margem
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Personaliza o campo 'username' (para CPF)
        self.fields['username'].label = "" # Remove o label padrão
        self.fields['username'].widget = forms.TextInput(attrs={
            'class': 'form-control mb-2',       # Classe Bootstrap para estilização
            'placeholder': 'CPF',               # Placeholder para indicar o que é esperado
            'name': 'username'                  # Garante que o nome do campo seja 'username'
        })

        # Personaliza o campo 'password'
        self.fields['password'].label = "" # Remove o label padrão
        self.fields['password'].widget.attrs.update({
            'class': 'form-control mb-2',       # Classe Bootstrap
            'placeholder': 'Senha'              # Placeholder
        })
        
        # Define a ordem dos campos, se desejado (opcional)
        # self.order_fields(['username', 'password', 'user_type'])


# Formulário de Cadastro Atualizado (para o modelo Usuario)
class SignUpForm(forms.ModelForm):
   
    cpf = forms.CharField(
        label="", 
        max_length=14, # Ex: "000.000.000-00"
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CPF'})
    )
    nome = forms.CharField(
        label="", 
        max_length=150, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome Completo'})
    )
    email = forms.EmailField(
        label="", 
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'})
    )
    telefone = forms.CharField(
        label="", 
        max_length=20, # Ex: "(XX) XXXXX-XXXX"
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefone (com DDD)'})
    )
    senha = forms.CharField(
        label="", 
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha'})
    )
    

    class Meta:
        model = Usuario
        fields = ['cpf', 'nome', 'email', 'telefone', 'senha'] # Adicionar 'senha2' se usar confirmação

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adiciona help_text similar ao UserCreationForm original, adaptado para os novos campos.
        self.fields['cpf'].help_text = '''
            <span class="form-text text-muted"><small>
                Obrigatório. Formato esperado: 000.000.000-00 (apenas números também podem ser aceitos dependendo da validação no backend).
            </small></span>
        '''
        self.fields['senha'].help_text = '''
            <ul class="form-text text-muted small">
                <li>Sua senha não pode ser muito parecida com suas outras informações pessoais.</li>
                <li>Sua senha deve conter pelo menos 8 caracteres.</li>
                <li>Sua senha não pode ser uma senha comumente usada.</li>
                <li>Sua senha não pode ser totalmente numérica.</li>
            </ul>
        '''
   

# Formulário para Adicionar/Editar Aula (Atualizado e Mesclado)
class AddAulaForm(forms.ModelForm):
  
    local = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={"placeholder": "Local da aula", "class": "form-control"}
        ),
        label="Local da Aula"
    )
    disciplina = forms.ModelChoiceField(
        queryset=Disciplina.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Disciplina"
    )
    data_inicio = forms.DateField(
        required=True,
        widget=forms.DateInput(
            attrs={"placeholder": "Data da aula", "class": "form-control", "type": "date"}
        ),
        label="Data da Aula"
    )
    hora_inicio = forms.TimeField(
        required=True,
        widget=CustomTimeSelect(attrs={"class": "form-control"}),
        label="Hora de Início"
    )
    hora_fim = forms.TimeField(
        required=True,
        widget=CustomTimeSelect(attrs={"class": "form-control"}),
        label="Hora de Fim"
    )
    aluno = forms.ModelChoiceField(
        queryset=Aluno.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Aluno"
    )
    professor = forms.ModelChoiceField(
        queryset=Professor.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Professor"
    )
    descricao = forms.CharField(
        required=True, # Conforme o novo snippet; ajuste para False se a descrição for opcional.
        widget=forms.Textarea(
            attrs={"placeholder": "Descrição detalhada da aula", "class": "form-control", "rows": 3}
        ),
        label="Descrição da Aula"
    )

    class Meta:
>>>>>>> main
        model = Aula
        fields = [
            'local', 'disciplina', 'aluno', 'professor',
            'data_inicio', 'hora_inicio', 'hora_fim', 'descricao'
        ]

    def clean(self):
<<<<<<< HEAD
        cleaned_data = super().clean()

=======
        """
        Validações personalizadas para o formulário AddAulaForm.
        - Garante que a hora de fim seja após a hora de início.
        - Verifica campos obrigatórios (embora 'required=True' nos campos já faça isso).
        """
        cleaned_data = super().clean()
>>>>>>> main
        data_inicio = cleaned_data.get("data_inicio")
        hora_inicio = cleaned_data.get("hora_inicio")
        hora_fim = cleaned_data.get("hora_fim")

<<<<<<< HEAD
        # Validação dos campos obrigatórios
=======
        # Validações de campos obrigatórios (redundantes se required=True está nos campos, mas mantidas do snippet)
>>>>>>> main
        if not data_inicio:
            self.add_error('data_inicio', "A data da aula é obrigatória.")
        if not hora_inicio:
            self.add_error('hora_inicio', "A hora de início é obrigatória.")
        if not hora_fim:
            self.add_error('hora_fim', "A hora de fim é obrigatória.")

<<<<<<< HEAD
        # Validação de lógica: hora fim deve ser após hora início
        if hora_inicio and hora_fim and hora_inicio >= hora_fim:
            self.add_error('hora_fim', "A hora de fim deve ser após a hora de início.")
=======
        # Validação de lógica: hora_fim deve ser posterior a hora_inicio
        if data_inicio and hora_inicio and hora_fim:  # Checa se todos os campos relevantes estão presentes
            if hora_inicio >= hora_fim:
                self.add_error('hora_fim', "A hora de fim deve ser após a hora de início.")
        
        return cleaned_data
>>>>>>> main
