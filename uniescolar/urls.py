from django.urls import path
from uniescolar.views import home, register_user, logout_user, add_aula, aula_detail

urlpatterns=[
    path('', home, name='home'), # Utiliza-se name para chamar a rota através do link
    path('register/', register_user, name='register'),
    path('logout/',logout_user, name='logout'),
    path('add_aula/', add_aula, name='add_aula'),
    path('aula/<int:id>',aula_detail,name='aula')
]