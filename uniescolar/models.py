from django.db import models
import datetime


class Usuario(models.Model):
    cpf = models.CharField(max_length=11, primary_key=True)
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    telefone = models.CharField(max_length=20)

    class Meta:
        abstract = True  


class Responsavel(Usuario):
    profissao = models.CharField(max_length=100)


class Professor(Usuario):
    materia = models.CharField(max_length=100)


class Aluno(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    sexo = models.CharField(max_length=10)
    data_nascimento = models.DateField(default=datetime.date(2000, 1, 1))  # Valor padrão
    responsavel = models.ForeignKey(
        Responsavel, on_delete=models.CASCADE, related_name="alunos"
    )

# PacoteHora
class PacoteHora(models.Model):
    id = models.AutoField(primary_key=True)
    horas_contratadas = models.IntegerField()
    valor_hora = models.IntegerField()
    saldo = models.IntegerField()
    responsavel = models.ForeignKey(
        Responsavel, on_delete=models.CASCADE, related_name="pacotes_hora"
    )

# Aula
class Aula(models.Model):
    id = models.AutoField(primary_key=True)
    numero = models.IntegerField()
    local = models.CharField(max_length=100)
    disciplina = models.CharField(max_length=100)
    data_inicio = models.DateField(default=datetime.date.today)  # Data atual como padrão
    hora_inicio = models.TimeField(default=datetime.time(8, 0))  # Horário padrão 08:00
    hora_fim = models.TimeField(default=datetime.time(9, 0))  # Horário padrão 09:00
    aluno = models.ForeignKey(
        Aluno, on_delete=models.CASCADE, related_name="aulas"
    )
    professor = models.ForeignKey(
        Professor, on_delete=models.CASCADE, related_name="aulas"
    )