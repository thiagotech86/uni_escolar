from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib import admin
from datetime import datetime, date

def hora_inicio_padrao():
    return timezone.datetime.strptime("08:00", "%H:%M").time()

def hora_fim_padrao():
    return timezone.datetime.strptime("09:00", "%H:%M").time()

class Usuario(models.Model):
    cpf = models.CharField(max_length=14, primary_key=True)
    nome = models.CharField(max_length=255)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    senha = models.CharField(max_length=255, default='default_password')

    def __str__(self):
        return f"{self.nome} ({self.cpf})"

class Responsavel(models.Model):
    CPF = models.CharField(max_length=14, primary_key=True, default='')
    user=models.ForeignKey(
        User, on_delete=models.CASCADE, default='', related_name="alunos"
    )
    profissao = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user}"


class Professor(models.Model):
    nome = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, default='')
    materia = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nome}"

class Disciplina(models.Model):
    nome = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.nome}"
    
class Aluno(models.Model):
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
    ]
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=200)
    sexo = models.CharField(max_length=30, choices=SEXO_CHOICES)
    data_nascimento = models.DateField(default=timezone.now)
    responsavel = models.ForeignKey(
        Responsavel, on_delete=models.CASCADE, related_name="responsavel"
    )

    def horas_contratadas(self):
        return sum(pacote.horas_contratadas for pacote in self.responsavel.pacotes_hora.all())

    def horas_utilizadas(self):
        total = 0
        for aula in self.aulas.all():  # usa related_name="aulas" em Aula.aluno
            if aula.hora_inicio and aula.hora_fim:
                inicio = datetime.combine(date.today(), aula.hora_inicio)
                fim = datetime.combine(date.today(), aula.hora_fim)
                total += (fim - inicio).total_seconds() / 3600
        return round(total, 2)

    def __str__(self):
        return self.nome

class PacoteHora(models.Model):
    id = models.AutoField(primary_key=True)
    horas_contratadas = models.IntegerField()
    valor_hora = models.DecimalField(max_digits=8, decimal_places=2)
    data_contrato = models.DateField(default=timezone.now)
    responsavel = models.ForeignKey(
        Responsavel, on_delete=models.CASCADE, related_name="pacotes_hora"
    )

    def __str__(self):
        return f"{self.responsavel} - Data: {self.data_contrato} - {self.horas_contratadas} h "

class Aula(models.Model):
    id = models.AutoField(primary_key=True)
    
    local = models.CharField(max_length=100)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, related_name="disciplina")
    data_inicio = models.DateField(default=timezone.now)
    hora_inicio = models.TimeField(default=hora_inicio_padrao)
    hora_fim = models.TimeField(default=hora_fim_padrao)
    aluno = models.ForeignKey(
        Aluno, on_delete=models.CASCADE, related_name="aulas"
    )
    professor = models.ForeignKey(
        Professor, on_delete=models.CASCADE, related_name="professor"
    )
    descricao=models.CharField(max_length=200)

    def __str__(self):
        return f"Aula {self.disciplina}"
    
