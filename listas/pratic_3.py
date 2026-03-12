banco_fit = ['R$ 30','R$ -60','R$ 3','R$ 28']


#* tiro a copia
saldos_copia_string = banco_fit.copy()

#* removo os R$
saldos_sem_simbolos = []

for valor in saldos_copia_string:
     if  isinstance(valor,(int,float)) and not isinstance(valor,bool):
        saldos_sem_simbolos.append(float(valor))

for saldo in saldos_copia_string:
    if isinstance(saldo,str):
           saldo_limpo = saldo.replace("R$", "")
           saldos_sem_simbolos.append(saldo_limpo)
#print(f"${saldos_sem_simbolos}")

#* removendo os espaços
saldos_sem_spacos = []
for saldo in saldos_sem_simbolos:
    saldo_limpo = saldo.strip()
    saldos_sem_spacos.append(saldo_limpo)

#print(f"${saldos_sem_spacos}")

#* trasnformando em float
saldos = []
for saldo in saldos_sem_spacos:
    saldo_int = float(saldo)
    saldos.append(saldo_int)



#* pego o total
saldos_tamnaho = len(saldos)
print(f"O banco possui cerca de: {saldos_tamnaho} clientes")
print('-'*40)

#* pegando os negatios e positivos
saldos_negativos = []
saldos_positivos = []



for saldo in saldos:
    if saldo < 0:
        saldos_negativos.append(saldo)
    else:
        saldos_positivos.append(saldo)

qtd_negativados = len(saldos_negativos)
qtd_positivos = len(saldos_positivos)





print(f"Esse banco possui {qtd_negativados} NEGATIVADOS")
print(f"Esse banco possui {qtd_positivos} POSITIVOS")
print('-'*40)

#* porcentagem dos negativados
pocent_negativos = len(saldos_negativos) * 100 / saldos_tamnaho
print(f"Cerca de: {pocent_negativos:.2f}% dos usuarios são negativados")

#* porcentagem dos positivos
pocent_positivos = len(saldos_positivos) * 100 / saldos_tamnaho
print(f"Cerca de: {pocent_positivos:.2f}% dos usuarios são positivos")
print('-'*40)


#*status de recomendação
recomendacao = ''
if pocent_positivos > 89:
    recomendacao = 'RECOMENDAVEL'
elif pocent_positivos > 70:
    recomendacao = 'AGRADAVEL'
elif pocent_positivos > 50:
    recomendacao = 'usual'
elif pocent_positivos < pocent_negativos:
    recomendacao = 'não recomendado'
else:
    recomendacao = ' EM ALERT'

print(f"Nivél de Recomendação: {recomendacao}")
print('-'*40)

print(f"O maior saldo do Banco Fit R$:{max(saldos)}")
print(f"O menor saldo do Banco Fit R$:{min(saldos)}")
print('-'*40)

#* media geral
media = sum(saldos) / len(saldos)
print(f"A média geral do banco é: R$:{media:.2f}")

#* status do banco
status = ''
if media > 0:
    status = 'POSITIVO'
elif media == 0:
    status = 'NEUTRO'
else:
    status = 'NEGATIVO'
print(f"Status do Banco: {status}")

#* media dos negativos
if saldos_negativos:
    media_negativos = sum(saldos_negativos) / len(saldos_negativos)
    print(f"A media das dividas dos negativados R$:{media_negativos:.2f}")
else:
    print('não HÁ negativados')

#* media dos positivos
if saldos_positivos:
    media_positivos = sum(saldos_positivos) / len(saldos_positivos)
    print(f"A media das dividas dos positivos R$:{media_positivos:.2f}")
else:
    print('não HÁ positivos')
print('-'*40)

#* pegando o indice do maior
indice_maior = saldos.index(max(saldos)) + 1
print(f"O cliente com o maior saldo esta na posição :{indice_maior}")

#* pegando o indice do menor
indice_menor = saldos.index(min(saldos)) + 1
print(f"O cliente com o saldo mais devedor esta na posição :{indice_menor}")
print('-'*40)

#* qualificaçao dos clientes
clientes_vip = []
clientes_premium = []
clientes_normais = []
clientes_restritos = []

for saldo in saldos:
    if saldo > 900000:
        clientes_vip.append(saldo)
    elif saldo > 50000:
        clientes_premium.append(saldo)
    elif saldo > 0:
        clientes_normais.append(saldo)
    elif saldo < -2000:
        clientes_restritos.append(saldo)

qtd_vip = len(clientes_vip)
qtd_premium = len(clientes_premium)
qtd_normais = len(clientes_normais)
qtd_restritos = len(clientes_restritos)



print(f"O banco possui: {qtd_vip} clientes VIP")
print(f"O banco possui: {qtd_premium} clientes PREMIUM")
print(f"O banco possui: {qtd_normais} clientes NORMAIS")
print(f"O banco possui: {qtd_restritos} clientes RESTRITOS")
print('-'*40)


#* pegando o indice e o valor, não  foca na formatação!
posicao_vip = []
posicao_premium = []
posicao_normal = []
posicao_restritos = []


for i, saldo in enumerate(saldos):
    if saldo in clientes_vip:
        valor =  f'{saldo:,.2f}'.replace(',','x').replace('.',',').replace('x','.')
        posicao_vip.append((i,saldo))
        print(f"VEJA os indices {i+1} e o saldo dos VIP R$:{valor}") 

for i, saldo in enumerate(saldos):
    if saldo in clientes_premium:
        valor =  f'{saldo:,.2f}'.replace(',','x').replace('.',',').replace('x','.')
        posicao_premium.append((i,saldo))
        print(f"VEJA os indices {i+1} e o saldo dos PREMUIM R$:{valor}")

for i, saldo in enumerate(saldos):
    if saldo in clientes_normais:
        valor =  f'{saldo:,.2f}'.replace(',','x').replace('.',',').replace('x','.')
        posicao_normal.append((i,saldo))
        #print(f"VEJA os indices{i+1} e o saldo dos NORMAIS {valor}")

for i, saldo in enumerate(saldos):
    if saldo in clientes_restritos:
        valor =  f'{saldo:,.2f}'.replace(',','x').replace('.',',').replace('x','.')
        posicao_restritos.append((i,saldo))
       # print(f"VEJA os indices {i+1} e o saldo dos RESTRITIOS R$:{valor}")
print('-'*40)

#* porcentagem dos vips/premium/normais/rrestritos
porcent_vip = qtd_vip * 100 / saldos_tamnaho
porcent_premium = qtd_premium * 100 / saldos_tamnaho
porcent_normal = qtd_normais * 100 / saldos_tamnaho
porcent_restritos = qtd_restritos * 100 / saldos_tamnaho


import plotly.graph_objects as go

clients = ["vip", "premium", "normais", "restritos"]
valor = [qtd_vip, qtd_premium, qtd_normais, qtd_restritos]

fig = go.Figure(data = go.Bar(x = clients, y = valor))
fig.show()

fig = go.Figure(go.Bar(y = clients, x = valor, orientation="h"))
fig.show()

porcent_valor = [ porcent_vip, porcent_premium, porcent_normal, porcent_restritos]

fig = go.Figure(data = go.Pie(labels = clients, values = porcent_valor))
fig.show()

print(f"O percentual de vip: {porcent_vip:.2f}%")
print(f"O percentual de premuim: {porcent_premium:.2f}%")
print(f"O percentual de normal: {porcent_normal:.2f}%")
print(f"O percentual de restrito: {porcent_restritos:.2f}%")
print('-'*40)


#* todas as dividas
total_dividas = sum(saldos_negativos)
print(f"A divida total negativos: R$:{total_dividas:.2f}")

#* todas as ganhos
total_ganhos = sum(saldos_positivos)
print(f"A divida total de ganhos: R$:{total_ganhos:.2f}")
print('-'*40)

#*total de lucro
lucros_bruto = total_ganhos + total_dividas
print(f"Lucro bruto do banco R$:{lucros_bruto:.2f}")

#* lucro liquido
lucro_sem_imposto = lucros_bruto * 0.85
lucro_desconto_funciorio = lucro_sem_imposto * 0.90
lucro_dispesas = lucro_desconto_funciorio * 0.95
lucro_liquido  = lucro_dispesas

print(f"Retirando o imposto de 15% fica: R${lucro_sem_imposto:.2f}")
print(f"Retirando gastos com funcionarios, cerca de 10% fica:R$:{lucro_desconto_funciorio:.2f}")
print(f"Retirando as dispesas cerca de 5% fica:R$:{lucro_dispesas:.2f}")
print(f"O banco possui lucro liquido de: R$:{lucro_liquido:.2f}")

#* status do pratimonio
pratimonio = ""
if lucro_liquido > 100000:
    pratimonio = 'EXELENTE'
elif lucro_liquido > 50000:
    pratimonio = 'SAUDAVEL'
elif lucro_liquido > 10000:
    pratimonio = 'ESTAVEL'
elif lucro_liquido > 0:
    pratimonio = 'EM RISCO'
elif lucro_liquido < -50000:
    pratimonio = 'FALENCIA'
elif lucro_liquido < -10000:
    pratimonio = 'RECUPERAÇÃO'
elif lucro_liquido < 0:
    pratimonio = 'PREJUIZO'

print(f"O status do patrimonio do banco: {pratimonio}")










    


