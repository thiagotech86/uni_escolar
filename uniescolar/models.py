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
    CPF = models.CharField(max_length=14, primary_key=True, default='') # CPF como PK
    user = models.ForeignKey( # Relação com o User do Django
        User, 
        on_delete=models.CASCADE, 
        default=None, 
        null=True, 
        blank=True, 
        related_name="responsavel_profiles" # Permite user.responsavel_profiles.all()
    )
    profissao = models.CharField(max_length=255)

    def __str__(self):
        if self.user:
            return f"Responsável: {self.user.username} ({self.CPF})"
        return f"Responsável: (Sem usuário Django associado) ({self.CPF})"


class Professor(models.Model):
    user = models.OneToOneField( # Relação OneToOne com User do Django, User é a PK de Professor
        User, 
        on_delete=models.CASCADE, 
        primary_key=True, 
        default=None, 
        related_name="professor_profile" # Permite user.professor_profile
    )
    materia = models.CharField(max_length=100)

    def __str__(self):
        return f"Professor: {self.user.username}"
    

class Gestor(models.Model):
    user = models.OneToOneField( # Relação OneToOne com User do Django, User é a PK de Gestor
        User, 
        on_delete=models.CASCADE, 
        primary_key=True,
        related_name="gestor_profile" # Permite user.gestor_profile
    )
    # Adicionar campos específicos do Gestor aqui, se necessário.
    # Ex: departamento = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Gestor: {self.user.username}"

    def save(self, *args, **kwargs):
        # Garante que o User associado ao Gestor seja superuser e staff.
        self.user.is_superuser = True
        self.user.is_staff = True 
        self.user.save() 
        super().save(*args, **kwargs)



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
    responsavel = models.ForeignKey( # Aluno tem um Responsavel
        Responsavel, 
        on_delete=models.CASCADE, 
        related_name="alunos_dependentes" # Permite responsavel.alunos_dependentes.all()
    )

    def horas_contratadas(self):
     if self.responsavel: # Garante que o aluno tem um responsável vinculado
        
        total_horas = sum(pacote.horas_contratadas for pacote in self.responsavel.pacotes_hora.all())
        return total_horas
     return 0 #

    def horas_utilizadas(self):
            total_segundos = 0
        # Filtra apenas aulas APROVADAS para o cálculo de horas utilizadas
            for aula in self.aulas.filter(status_aprovacao='aprovada'):
             if aula.hora_inicio and aula.hora_fim:
              data_referencia = aula.data_inicio if aula.data_inicio else date.today()
            try:
                inicio = datetime.combine(data_referencia, aula.hora_inicio)
                fim = datetime.combine(data_referencia, aula.hora_fim)
                if fim > inicio:
                    total_segundos += (fim - inicio).total_seconds()
            except TypeError: # Caso hora_inicio/fim não sejam objetos time válidos
                pass # Ignora esta aula no cálculo
                return round(total_segundos / 3600, 2)

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
    STATUS_APROVACAO_CHOICES = [
        ('pendente', 'Pendente'),
        ('aprovada', 'Aprovada'),
        ('rejeitada', 'Rejeitada'),
    ]

    id = models.AutoField(primary_key=True)
    local = models.CharField(max_length=100)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, related_name="aulas_disciplina")
    data_inicio = models.DateField(default=timezone.now)
    hora_inicio = models.TimeField(default=hora_inicio_padrao)
    hora_fim = models.TimeField(default=hora_fim_padrao)
    aluno = models.ForeignKey(
        Aluno, 
        on_delete=models.CASCADE, 
        related_name="aulas"
    )
    professor = models.ForeignKey(
        Professor, 
        on_delete=models.CASCADE, 
        related_name="aulas_ministradas"
    )
    descricao = models.CharField(max_length=200)
    status_aprovacao = models.CharField( # NOVO CAMPO
        max_length=10,
        choices=STATUS_APROVACAO_CHOICES,
        default='pendente' # Default para novas aulas
    )

    def __str__(self):
        return f"Aula de {self.disciplina} para {self.aluno.nome} ({self.get_status_aprovacao_display()})"
    
