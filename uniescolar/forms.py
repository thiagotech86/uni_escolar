from django import forms
from .models import Aula, Aluno, Professor, Usuario

from django.contrib.auth.forms import AuthenticationForm

class CustomLoginForm(AuthenticationForm):
    cpf = forms.CharField(label='cpf', max_length=100)
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)


class SignUpForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['cpf', 'nome', 'email', 'telefone', 'senha']


class AddAulaForm(forms.ModelForm):
    numero = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(
            attrs={"placeholder": "Número da aula", "class": "form-control"}
        ),
        label=""
    )

    local = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={"placeholder": "Local da aula", "class": "form-control"}
        ),
        label=""
    )

    disciplina = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={"placeholder": "Disciplina", "class": "form-control"}
        ),
        label=""
    )

    data_inicio = forms.DateField(
        required=True,
        widget=forms.DateInput(
            attrs={"placeholder": "Data de início", "class": "form-control", "type": "date"}
        ),
        label=""
    )

    hora_inicio = forms.TimeField(
        required=True,
        widget=forms.TimeInput(
            attrs={"placeholder": "Hora de início", "class": "form-control", "type": "time"}
        ),
        label=""
    )

    hora_fim = forms.TimeField(
        required=True,
        widget=forms.TimeInput(
            attrs={"placeholder": "Hora de fim", "class": "form-control", "type": "time"}
        ),
        label=""
    )

    aluno = forms.ModelChoiceField(
        queryset=Aluno.objects.all(),
        widget=forms.Select(
            attrs={"class": "form-control"}
        ),
        label="Aluno"
    )

    professor = forms.ModelChoiceField(
        queryset=Professor.objects.all(),
        widget=forms.Select(
            attrs={"class": "form-control"}
        ),
        label="Professor"
    )

    class Meta:
        model = Aula
        fields = ['numero', 'local', 'disciplina', 'data_inicio', 'hora_inicio', 'hora_fim', 'aluno', 'professor']
