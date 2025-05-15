from django.urls import path
from uniescolar.views import home, register_user, logout_user, add_aula, aula_detail
from . import views

urlpatterns=[
    path('', home, name='home'), # Utiliza-se name para chamar a rota através do link
    path('register/', register_user, name='register'),
    path('logout/',logout_user, name='logout'),
    path('add_aula/', add_aula, name='add_aula'),
    path('aula/<int:id>',aula_detail,name='aula'),
    #path('login/', views.login_view, name='login'),
    path('excluir-aula/<int:aula_id>/', views.excluir_aula, name='excluir_aula'),
    path('aula/<int:aula_id>/aprovar/', views.aprovar_aula_view, name='aprovar_aula'),
    path('aula/<int:aula_id>/rejeitar/', views.rejeitar_aula_view, name='rejeitar_aula'),
    path('aula/<int:aula_id>/editar-gestor/', views.editar_aprovar_aula_gestor, name='editar_aprovar_aula_gestor')

]