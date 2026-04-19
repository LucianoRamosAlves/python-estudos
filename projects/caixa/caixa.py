from datetime import datetime
data = datetime.now()
caixa = 500

def divida(valor):
    global caixa #! não é recomendado usar global, mas para esse exemplo simples, vamos usar para modificar a variável caixa dentro da função
    if valor <= caixa:
        caixa -= valor
    else:
        return print("saldo no caixa insuficiente.")
    return caixa

def troco(valor): #! essa função é praticamente igual a divida, mas para esse exemplo, vamos deixar assim para ilustrar a ideia de funções diferentes para cada tipo de operação, mesmo que a lógica seja similar.
    global caixa
    if valor <= caixa:
        caixa -= valor
    else:
        return print("saldo no caixa insuficiente.")
    return caixa

def entrada(valor):
    global caixa
    if valor > 0:
        caixa += valor
    else:
        return print("numero invalido.")
    return caixa

opcao = ''
status = ''


nome = input('Nome do operador: ').capitalize()
while opcao != "5":

    print(""" =-=-= CAIXA =-=-
    [0]. Verificar saldo
    [1]. Registrar dívida
    [2]. Registrar troco
    [3]. Registrar entrada
    [4]. Fechar caixa
    [5]. Fechar Programa
    """)
    
    try:
        opcao = str(input("Digite uma opção (0-5) ou 'fechar' para encerrar: ").lower())
    except:
        print('opção invalida')
        print('tente novamente')
        continue

    if opcao == '4':
            opcao_fechar = input('Deseja realmente fechar o caixa? (s/n) ').lower()
            if opcao_fechar == 's':
                if caixa > 1000:
                    status = 'BOM'
                elif caixa > 500:
                    status = 'REGULAR'
                else:
                    status = 'RUIM'
                with open("caixa.txt", "a") as saldo_caixa:
                    saldo_caixa.write(f"Responsavél: {nome}\n data: {data} saldo: R$: {caixa:.2f}\n situação {status}\n\n")
                    print('Caixa finalizado')
                    print(f'Responsavél {nome}')
                    break
            else:
                print('Caixa ainda aberto!')
                continue
    try:
        if opcao == '0':
            print(f'Saldo atual: R$: {caixa}')
        elif opcao == '1':
            divida(valor := float(input('valor da divida: ')))
            print('Aplicação da dívida registrada com sucesso!')
        elif opcao == '2':
            troco(valor := float(input('valor do troco : ')))
            print('Aplicação do troco registrada com sucesso!')
        elif opcao == '3':
            entrada(valor := float(input('valor da entrada : ')))
            print('Aplicação da entrada registrada com sucesso!')
        else:
            print('opção invalida')
            print('tente novamente')
            continue
    except:
        print('opss: Numero invalido')
        print('tente novamente')
else:
    print('Caixa ainda aberto!')

# TODO: FAZER MELHORAR O CODIGO COM TRATAMENTO DE ERROS,

