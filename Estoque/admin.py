from .models import *
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.

admin.site.register(Entrada)
admin.site.register(Saida)
admin.site.register(Estoque)
admin.site.register(Iten)
admin.site.register(Carrinho)
admin.site.register(Usuario, UserAdmin)