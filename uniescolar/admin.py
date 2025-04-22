from django.contrib import admin
from .models import  Usuario, Professor, Responsavel, Aluno, PacoteHora, Aula
from django.contrib.auth.models import User
# Register your models here.

admin.site.register(Aluno)
admin.site.register(Aula)
admin.site.register(Professor)
admin.site.register(Responsavel)