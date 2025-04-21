from django.db import models
from django.utils import timezone

def hora_inicio_padrao():
    return timezone.datetime.strptime("08:00", "%H:%M").time()

def hora_fim_padrao():
    return timezone.datetime.strptime("09:00", "%H:%M").time()

class Usuario(models.Model):
    cpf = models.CharField(max_length=11, primary_key=True)
    nome = models.CharField(max_length=255)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    senha = models.CharField(max_length=255, default='default_password')

    def __str__(self):
        return f"{self.nome} ({self.cpf})"

class Responsavel(models.Model):
    cpf = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    profissao = models.CharField(max_length=255)

    def __str__(self):
        return f"Responsável: {self.cpf.nome}"


class Professor(models.Model):
    cpf = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    materia = models.CharField(max_length=100)

    def __str__(self):
        return f"Professor: {self.cpf.nome} - {self.materia}"



class Aluno(models.Model):
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
    ]

    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    data_nascimento = models.DateField(default=timezone.now)
    responsavel = models.ForeignKey(
        Responsavel, on_delete=models.CASCADE, related_name="alunos"
    )

    def __str__(self):
        return self.nome

class PacoteHora(models.Model):
    id = models.AutoField(primary_key=True)
    horas_contratadas = models.IntegerField()
    valor_hora = models.DecimalField(max_digits=8, decimal_places=2)
    saldo = models.IntegerField()
    responsavel = models.ForeignKey(
        Responsavel, on_delete=models.CASCADE, related_name="pacotes_hora"
    )

    def __str__(self):
        return f"Pacote #{self.id} - Saldo: {self.saldo}h"

class Aula(models.Model):
    id = models.AutoField(primary_key=True)
    numero = models.IntegerField()
    local = models.CharField(max_length=100)
    disciplina = models.CharField(max_length=100)
    data_inicio = models.DateField(default=timezone.now)
    hora_inicio = models.TimeField(default=hora_inicio_padrao)
    hora_fim = models.TimeField(default=hora_fim_padrao)
    aluno = models.ForeignKey(
        Aluno, on_delete=models.CASCADE, related_name="aulas"
    )
    professor = models.ForeignKey(
        Professor, on_delete=models.CASCADE, related_name="aulas"
    )

    def __str__(self):
        return f"Aula {self.numero} - {self.disciplina}"
    
