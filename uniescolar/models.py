from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

# Create your models here.

#criando e vendo a nova branch

class Materia(models.Model):
    id=models.AutoField(primary_key=True)
    nome=models.CharField(max_length=50)
    def __str__(self): # Função para retornar uma mensagem espefícia ao inves de mensagens da memória.
        return (f'{self.nome}') 

class Aluno(models.Model):
    id=models.AutoField(primary_key=True)
    nome=models.CharField(max_length=50)
    def __str__(self): # Função para retornar uma mensagem espefícia ao inves de mensagens da memória.
        return (f'{self.nome}') 
    
class Professor(models.Model):
    id=models.AutoField(primary_key=True)
    nome=models.CharField(max_length=50)
    def __str__(self): # Função para retornar uma mensagem espefícia ao inves de mensagens da memória.
        return (f'{self.nome}') 
    
class Aula(models.Model):
    
    created_at=models.DateTimeField(auto_now_add=True) # data de criação do casdastro.
    disciplina=models.ForeignKey(Materia, on_delete=models.PROTECT, related_name="aula_disciplina")
    descricao=models.CharField(max_length=200)
    data=models.DateField()
    inicio=models.TimeField(max_length=30)
    termino=models.TimeField()
    aluno=models.ForeignKey(Aluno,on_delete=models.SET_NULL, null=True, blank=True )
    professor=models.ForeignKey(Professor,on_delete=models.SET_NULL, null=True, blank=True )
    criado_por=models.ForeignKey(User,on_delete=models.SET_NULL, null=True, blank=True ) # Chave estrangeira 
    def __str__(self): # Função para retornar uma mensagem espefícia ao inves de mensagens da memória.
        return (f'Aula de {self.disciplina}- {self.data}') 
    

