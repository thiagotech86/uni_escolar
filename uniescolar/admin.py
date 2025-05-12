from django.contrib import admin
from .models import Aula, Disciplina, Aluno, Professor
from django.contrib.auth.models import User
# Register your models here.

admin.site.register(Disciplina)
admin.site.register(Aluno)
admin.site.register(Aula)
admin.site.register(Professor)