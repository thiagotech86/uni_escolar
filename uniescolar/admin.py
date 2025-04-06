from django.contrib import admin
from .models import  Aula, Materia, Aluno, Professor # importando o model 
from django.contrib.auth.models import User
# Register your models here.

admin.site.register(Materia)
admin.site.register(Aluno)
admin.site.register(Aula)
admin.site.register(Professor)