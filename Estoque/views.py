from .models import *
from django.views.generic import *
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

class HomePage(TemplateView):
    template_name = 'homepage.html'

class NovoItem(TemplateView):
    template_name = 'novo_item.html'

    @method_decorator(csrf_exempt, name='dispatch')
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            cod = request.POST.get('novoItemCod')
            nome = request.POST.get('novoItemNome')
            categoria = request.POST.get('novoItemCategoria')
            valor_unitario = request.POST.get('novoItemValor')
            cadastrar(request, cod, nome, categoria, valor_unitario)
        return render(request, 'novo_item.html')

# Registrar no Banco de Dados
def cadastrar(request, cod, nome, categoria, valor_unitario):
    valor_unitario = str(valor_unitario).replace(',', '.')
    if Iten.objects.filter(sku=str(cod)).exists() or Iten.objects.filter(nome=str(nome)).exists() and Iten.objects.filter(categoria=str(categoria)).exists():
        pass
    else:
        registro = Iten(sku=str(cod), nome=str(nome), categoria=str(categoria), valor_unitario=str(valor_unitario))
        registro.save()
        return redirect('Estoque:novo_item')
    return render(request, 'novo_item.html')

def entradas(request):
    # Bancos de dados que se conectará com o HMTL através de dicionários
    Itens = Iten.objects.all()

    # Cadastrar em no banco de dados de entradas
    if request.method == 'POST':
        cod = request.POST.get('entradaCod')
        nome = request.POST.get('entradaNome')
        categoria = request.POST.get('entradaCategoria')
        quantidade = request.POST.get('entradaQuantidade')
        validade = request.POST.get('entradaValidade')

        if validade == '':
            validade = None

        valor_unitario = request.POST.get('entradaValorUnitario')
        valor_total = request.POST.get('entradaValorTotal')

        valor_unitario = str(valor_unitario).replace(',', '.')
        valor_total = str(valor_total).replace(',', '.')

        registro = Entrada(sku=str(cod), nome_item=str(nome), categoria=str(categoria), quantidade=quantidade, data_vencimento=validade, valor_unitario=valor_unitario, preco_pago=valor_total)
        registro.save()

        # Verificar se o item que está entrando já existe no estoque
        if Estoque.objects.filter(sku=cod).exists():
            # Caso exista, apenas fazer uma atualização
            estoque = Estoque.objects.filter(sku=cod).all()
            for campo in estoque:
                quantidade_antiga = campo.quantidade
                valor_lote_antigo = campo.valor_lote

            status = situacao(int(quantidade_antiga) + int(quantidade))

            estoque.update(quantidade=int(quantidade_antiga) + int(quantidade), valor_vendido=float(valor_unitario) * 0.20 + float(valor_unitario), valor_lote=float(valor_lote_antigo) + float(valor_total) + float(valor_total) * 0.20, situacao=status)
        else:
            # Caso não exista, cadastrar e salvar o mesmo.

            status = situacao(int(quantidade))

            estoque = Estoque(sku=str(cod), nome_item=str(nome), categoria=str(categoria), quantidade=quantidade, valor_vendido=float(valor_unitario) * 0.20 + float(valor_unitario), valor_lote=float(valor_total) + float(valor_total) * 0.20, situacao=status)
            estoque.save()
        return redirect('Estoque:entradas')

    return render(request, 'entradas.html', {'Itens': Itens})



def saidas(request):
    # Bancos de dados que se conectará com o HMTL através de dicionários
    itens = Iten.objects.all()
    estoque = Estoque.objects.all()
    carrinho = Carrinho.objects.all()
    pendencias = Carrinho.objects.filter(situacao='PENDENTE').count()

    # Cadastrar em no banco de dados de saidas
    if request.method == 'POST':
        # Campos HTML
        ids = request.POST.get('ids')
        idrest = request.POST.get('idrest')
        range1 = request.POST.get('range1')
        range2 = request.POST.get('range2')

        cod = request.POST.get('saidaCod')
        nome = request.POST.get('saidaNome')
        quantidade = request.POST.get('saidaQuantidade')
        validade = request.POST.get('saidaValidade')

        valor_unitario = request.POST.get('saidaValorUnitario')
        valor_total = request.POST.get('saidaValorTotal')

        valor_unitario = str(valor_unitario).replace(',', '.')
        valor_total = str(valor_total).replace(',', '.')

        # Verificar se a quantidade de id informado é diferente de vazio.
        if str(range1) != 'None':
            for i in range(int(range1)):
                # Pegar os id separados por vírgulas
                id = str(ids).split(',')[i]
                # Puxar o banco de carrinho
                compras = Carrinho.objects.filter(id=id).all()
                # Pegar as informações do Banco Carrinho, percorre-las e subtrair do estoque no estoque
                for campo in compras:
                    sku = campo.sku
                    nome1 = campo.nome_item
                    quantidade = campo.quantidade
                    unitario1 = campo.preco_venda
                    total1 = campo.valor_venda
                    estoque1 = Estoque.objects.filter(sku=sku).all()
                    # Pegar a quantidade vendida e subtrair da quantidade que tinha em estoque
                    for campo_e in estoque1:
                        quantidade_antiga = campo_e.quantidade
                        valor_antigo = campo_e.valor_lote
                        status = situacao(int(quantidade_antiga) - int(quantidade))

                        estoque1.update(quantidade=int(quantidade_antiga) - int(quantidade), valor_lote=float(valor_antigo) - float(total1), situacao=status)
                    # Cadastrar no banco de saídas
                    saida1 = Saida(sku=str(sku), nome_item=str(nome1), quantidade=quantidade, preco_venda=unitario1, valor_venda=total1)
                    saida1.save()
                    # Apagar os Id restantes do Banco Carrinho
                    compras = Carrinho.objects.filter(id=id).all()
                    compras.delete()

        # Verificar se a quantidade de id restante informado é diferente de vazio.
        if str(range2) != 'None':
            for i in range(int(range2)):
                # Separar os Id
                id = str(idrest).split(',')[i]
                # Apagar do Banco Carrinho os Id que não foram selecionados
                compras = Carrinho.objects.filter(id=id).all()
                compras.delete()

        # Cadastrar no banco carrinho se as variaveis no if for diferente de None
        if cod != None and nome != None and quantidade != None:
            pre_compra = Carrinho(sku=str(cod), nome_item=str(nome), quantidade=quantidade, preco_venda=valor_unitario, valor_venda=valor_total, situacao='PENDENTE')
            pre_compra.save()
        return redirect('Estoque:saidas')

    return render(request, 'saidas.html', {'Itens': itens, 'Estoque': estoque, 'Carrinho': carrinho, 'Pendencias': pendencias})

def estoque(request):
    # Banco de dados para se conectar com HTML
    estoque = Estoque.objects.all()

    # Contadores
    alimentos = 0
    preco_ali = 0
    bebidas = 0
    preco_beb = 0
    consumiveis = 0
    preco_con = 0

    # For para percorrer as informações do banco
    for categoria in estoque:
        if categoria.categoria == 'ALIMENTOS':
            alimentos += 1
            preco_ali += precos(float(categoria.valor_lote))

        if categoria.categoria == 'BEBIDAS':
            bebidas += 1
            preco_beb += precos(float(categoria.valor_lote))
        if categoria.categoria == 'CONSUMIVEIS':
            consumiveis += 1
            preco_con += precos(float(categoria.valor_lote))


    # Somar o valor do estoque
    soma_total = float(preco_ali) + float(preco_beb) + float(preco_con)

    # Substituir o "." por uma ","
    preco_ali = str(preco_ali).replace('.', ',')
    preco_beb = str(preco_beb).replace('.', ',')
    preco_con = str(preco_con).replace('.', ',')

    # Quantidade de itens vendidos
    vendas = Saida.objects.all()
    quantidade_antiga = 0
    for ext in vendas:
        quantidade_antiga += ext.quantidade

    # Investimento
    entradas = Entrada.objects.all()
    investimento = 0
    for inv in entradas:
        investimento += float(inv.preco_pago)

    return render(request, 'estoque.html', {'alimentos': alimentos, 'preco_ali': preco_ali, 'bebidas': bebidas, 'preco_beb': preco_beb, 'consumiveis': consumiveis, 'preco_con': preco_con, 'soma_total': soma_total,'vendas': quantidade_antiga, 'investimento': investimento})

def status(request):
    estoque = Estoque.objects.all()
    return render(request, 'status.html', {'estoque': estoque})

def situacao(qnty):
    situacao = ""

    if qnty == 0:
        situacao = 'Estoque Vazio'
    elif qnty > 0 and qnty <= 10:
        situacao = 'Estoque Crítico'
    elif qnty > 10 and qnty <= 20:
        situacao = 'Estoque Regular'
    elif qnty > 20:
        situacao = 'Estoque Seguro'
    return situacao

def precos(preco):
    if preco < 0:
        novo_preco = 0
    else:
        novo_preco = preco
    return novo_preco