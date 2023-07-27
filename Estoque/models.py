from datetime import date
from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    pass
# Create your models here.
class Entrada(models.Model):
    data = models.DateField(null=False, default=date.today)
    sku = models.CharField(max_length=100)
    nome_item = models.CharField(max_length=100)
    categoria = models.CharField(max_length=15)
    quantidade = models.IntegerField(null=False)
    data_vencimento = models.CharField(max_length=10, blank=True, null=True)
    valor_unitario = models.CharField(max_length=15, blank=True)
    preco_pago = models.CharField(max_length=15, blank=True)

class Saida(models.Model):
    data = models.DateField(null=False, default=date.today)
    sku = models.CharField(max_length=100)
    nome_item = models.CharField(max_length=100)
    quantidade = models.IntegerField(null=False)
    preco_venda = models.CharField(max_length=15)
    valor_venda = models.CharField(max_length=15, blank=True, null=True)

class Estoque(models.Model):
    situacoes = [("ESTOQUE CHEIO","ESTOQUE CHEIO"),("ESTOQUE RASOAVEL","ESTOQUE RASOAVEL"),("ESTOQUE CRITICO","ESTOQUE CRITICO"),("SEM ESTOQUE","SEM ESTOQUE")]
    sku = models.CharField(max_length=100)
    nome_item = models.CharField(max_length=100)
    categoria = models.CharField(max_length=15)
    quantidade = models.IntegerField(null=False)
    valor_vendido = models.CharField(max_length=15)
    valor_lote = models.CharField(max_length=15)
    situacao = models.CharField(max_length=15, blank=True, null=True)

class Iten(models.Model):
    categorias = [("ALIMENTOS","ALIMENTOS"),("BEBIDAS","BEBIDAS"),("CONSUMIVEIS","CONSUMIVEIS")]
    sku = models.CharField(max_length=100)
    nome = models.CharField(max_length=100)
    categoria = models.CharField(max_length=15, choices=categorias)
    valor_unitario = models.CharField(max_length=15)
    imagem = models.CharField(max_length=100, default='image/padrao.png')

    def __str__(self):
        return str(self.nome)

class Carrinho(models.Model):
    sku = models.CharField(max_length=100)
    nome_item = models.CharField(max_length=100)
    quantidade = models.IntegerField(null=False)
    preco_venda = models.CharField(max_length=15)
    valor_venda = models.CharField(max_length=15, blank=True, null=True)
    situacao = models.CharField(max_length=100, default='PENDENTE')
