//Função para puxar dados do banco de Itens e preecher os campos de acordo com o Cod digitado

function pesquisa(tela){
//  Pegar valor do campo cód
    limpar(tela)
    let cod = document.querySelector('#' + tela + 'Cod');
    let valorCod = cod.value;

//  Percorrer a lista do banco de dados
    items.forEach(item => {
//  Verificar se o cód digitado é igual o que tem no banco
        if(valorCod == item.cod){
//  Atribuir os valores conforme a pesquisa
            document.getElementById(tela + 'Nome').value = item.nome;
            document.getElementById(tela + 'ValorUnitario').value = item.valor_unitario;
            document.getElementById(tela + 'img').src = '/static/' + item.imagem;
            document.getElementById(tela + 'labelpreco').innerHTML = 'R$' + ' ' + item.valor_unitario;
            document.getElementById(tela + 'Quantidade').value = 1;
            document.getElementById(tela + 'Categoria').value = item.categoria;
//   Calcular o valor da Compra
            valorTotal(tela)
        }
    })
}

//  Mesmo código de cima, porém com adaptações para saídas
function pesquisaSaida(tela){
    limpar(tela)
    let cod = document.querySelector('#' + tela + 'Cod');
    let valorCod = cod.value;
//  Banco de dados do estoque
    estoque.forEach(item=> {
        if(valorCod == item.sku){
            if(item.quantidade == 0){
                document.getElementById('addcarrinho').style.display = 'none'
                document.getElementById('carrinho1').style.display = 'none'
                document.getElementById(tela + 'QuantidadeMaxima').value = 0;
                const mensagem = 'O Item acima está zerado no estoque!';
                exibirMensagemErro(mensagem);
            }
            else{
                document.getElementById(tela + 'Nome').value = item.nome;
                document.getElementById(tela + 'ValorUnitario').value = item.valor_vendido.toFixed(2);
                document.getElementById(tela + 'labelpreco').innerHTML = 'R$' + ' ' + item.valor_vendido.toFixed(2);
                document.getElementById('addcarrinho').style.display = 'inline'
                document.getElementById('carrinho1').style.display = 'inline'
//  Tirar a quantidade já inclusa no carrinho
                if(document.getElementById('pends').innerText[0]== 0){
                    document.getElementById(tela + 'QuantidadeMaxima').value = item.quantidade;
                }
                else{
                    carrin.forEach(item2 =>{
                        if(item2.sku == valorCod){
                            soma = parseInt(item.quantidade) - parseInt(item2.quantidade)
                            document.getElementById(tela + 'QuantidadeMaxima').value = soma;
                        }
                        else if(document.getElementById(tela + 'QuantidadeMaxima').value == ''){
                            document.getElementById(tela + 'QuantidadeMaxima').value = item.quantidade;

                        }
                    })
                }
//  Banco de dados dos itens
                items.forEach(item1=>{
                    if(valorCod == item1.cod){
                        document.getElementById(tela + 'img').src = '/static/' + item1.imagem;
                        document.getElementById(tela + 'Quantidade').value = 1
                    }
                })
//  Calcular o valor da Venda
                valorTotal(tela)
            }
        }
    })
}

//  Calcular valor total
function valorTotal(tela){
//  Pegar campo de quantidade * valor unitário
    let unitario = document.querySelector('#' + tela + 'ValorUnitario');
    let valorUnitario = parseFloat(unitario.value);
    let quantidade = document.querySelector('#' + tela + 'Quantidade');
    let valorQuantidade = parseInt(quantidade.value);
    let multiplicacao = valorUnitario * valorQuantidade

//  Verificar se a tela se chama saida, para criar uma variavel do campo quantidade maxima

    document.getElementById(tela + 'ValorTotal').value = multiplicacao.toFixed(2) ;

    let total = document.querySelector('#' + tela + 'ValorTotal');
    let valorTotal1 = total.value;

    if(valorTotal1 == 'NaN' || valorTotal1 == 0){
        document.getElementById(tela + 'ValorTotal').value = ""
    };
        if(tela == 'saida'){
        let quantidade_maxima = document.querySelector('#' + tela + 'QuantidadeMaxima');
        let valorQuantidadeMaxima = quantidade_maxima.value;
//  Verificar se a quantidade é maior do que a maxima
        if(valorQuantidade > valorQuantidadeMaxima){
            document.getElementById(tela + 'Cod').value = ""
            document.getElementById(tela + 'Cod').focus()
            limpar(tela)
            document.getElementById(tela + 'ValorTotal').value = ""
            const mensagem = 'A quantidade digitada é maior que a disponível no estoque!';
            exibirMensagemErro(mensagem);
        }
    }
}

//  Limpar os campos caso o valor digitado no cod não exista
function limpar(tela){
    document.getElementById(tela + 'Nome').value = ""
    document.getElementById(tela + 'Quantidade').value = ""
    document.getElementById(tela + 'ValorUnitario').value = ""
    document.getElementById(tela + 'ValorTotal').value = ""
    document.getElementById(tela + 'img').src = '/static/image/padrao.png'
    document.getElementById(tela + 'labelpreco').innerHTML = "R$ 0,00"
    if(tela == 'entrada'){
        document.getElementById(tela + 'Validade').value = ""
        document.getElementById(tela + 'Categoria').value = ""
    }
    else{
       document.getElementById(tela + 'QuantidadeMaxima').value = ""
    }
}

//  Itens do carrinho
function carrinho(){
    document.getElementById('saidaCod').value = ""
    limpar('saida')
    const lis = document.getElementById('confirmarCompras')
    lis.innerHTML = ''

    let lit = document.createElement('li')
    let ul = document.getElementById('confirmarCompras')
    let lsku = document.createElement('label')
    let litem = document.createElement('label')
    let lqnty = document.createElement('label')
    let ltotal = document.createElement('label')

    lsku.innerHTML = 'ID'
    lsku.id = 'sku'
    litem.innerHTML = 'Item'
    litem.id = 'item'
    lqnty.innerHTML = 'Qnty'
    lqnty.id = 'qnty'
    ltotal.innerHTML = 'Total'
    ltotal.id = 'total'

    lit.appendChild(lsku)
    lit.appendChild(litem)
    lit.appendChild(lqnty)
    lit.appendChild(ltotal)
    ul.appendChild(lit)

    carrin.forEach(item => {
        if(item.situacao == 'PENDENTE'){
//  Criar os elementos de ul
            let check = document.createElement('input')
            let label_sku = document.createElement('label')
            let label_nome = document.createElement('label')
            let label_quantidade = document.createElement('label')
            let label_total = document.createElement('label')
            let li = document.createElement('li')
            const ul = document.getElementById('confirmarCompras')

            check.type = 'checkbox'
            check.textContent = item.id
            check.id = 'check1'
            li.name = 'lils'

            label_sku.innerHTML = item.id
            label_sku.id = 'lbsku'
            label_nome.innerHTML = item.nome
            label_nome.id = 'lbnome'
            label_quantidade.innerHTML = item.quantidade
            label_quantidade.id = 'lbqnty'
            label_total.innerHTML = item.valor_total
            label_total.id = 'lbtotal'
            const valores = []

//  Somar os o valor da compra de acordo com os itens selecionados
            check.addEventListener('click', function(){
                let total1 = document.querySelector('#compra_total');
                let valorTotal2 = total1.innerText;
                if(check.checked == true){
                    if(valorTotal2 == ''){
                        valorTotal2 = 0
                    }
                    document.getElementById('compra_total').innerText = parseFloat(label_total.innerText) + parseFloat(valorTotal2)
                }
                else{
                    document.getElementById('compra_total').innerText = parseFloat(valorTotal2) - parseFloat(label_total.innerText)
                }
            })

            li.appendChild(check)
            li.appendChild(label_sku)
            li.appendChild(label_nome)
            li.appendChild(label_quantidade)
            li.appendChild(label_total)
            ul.appendChild(li)
        }
    })
}

function confirmar(){
    let pend = document.querySelector('#pendencias1');
    let valorPend = pend.value;
    const ul = document.getElementById('confirmarCompras')
    const checks = ul.getElementsByTagName('input')
    const valores = []
    const restante = []
    for (let i = 0; i < valorPend; i++){
        if(checks[i].checked == true){
            valores.push(checks[i].textContent);
        }
        else{
            restante.push(checks[i].textContent)
        }
    }
    document.getElementById('ids').value = valores
    document.getElementById('idrest').value = restante
    document.getElementById('range1').value = valores.length
    document.getElementById('range2').value = restante.length
}

//  Modificar a cor da fonte da coluna situação da tabela de status de estoque
function verificarSituacao(){
    const table = document.querySelector('#tbodyest');
    const itens = table.getElementsByTagName('td');

    for(let i = 5; i <= itens.length; i+= 6){
        if(itens[i].innerText == 'Estoque Crítico'){
            itens[i].style.color = 'orange'
        }
        else if(itens[i].innerText == 'Estoque Vazio'){
            itens[i].style.color = 'red'
        }
        else if(itens[i].innerText == 'Estoque Regular'){
            itens[i].style.color = 'yellow'
        }
        else if(itens[i].innerText == 'Estoque Seguro'){
            itens[i].style.color = 'green'
        }
    }
}

// Função para exibir a mensagem de erro
function exibirMensagemErro(mensagem) {
    const elementoMensagem = document.getElementById('mensagemErro');
    elementoMensagem.innerText = mensagem;
    elementoMensagem.style.display = 'block';
    setTimeout(ocultarMensagemErro, 4000);
}

// Função para ocultar a mensagem de erro
function ocultarMensagemErro() {
    const elementoMensagem = document.getElementById('mensagemErro');
    elementoMensagem.style.display = 'none';
}
//


