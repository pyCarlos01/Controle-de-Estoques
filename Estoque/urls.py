from django.urls import path, include
from .views import *

app_name = 'Estoque'

urlpatterns = [
    path('', HomePage.as_view(), name='homepage'),
    path('novoitem/', NovoItem.as_view(), name='novo_item'),
    path('entradas/', entradas, name='entradas'),
    path('saidas/', saidas, name='saidas'),
    path('statusestoque/', status, name='status'),
    path('estoques/', estoque, name='estoques'),
]
