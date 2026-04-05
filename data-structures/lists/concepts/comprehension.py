
#** basicamente , eu  percorro, filtro se eu quizer, e tramformo, quero tranformar e filtrar

#quero tranformar e filtrrar, deixar tudo padrão
dominios = [
    'www.itc.com',
    'Open.com',
    'localhost',
    'WWW.BASE.COM'
]
# 1 - nova list
#limpo = [
    # tranformo - 2- eu tranformo, #| i.lower().replace('www.', '')
    # for loop - comeco por aqui -- #| for i in dominios
    # filtro-- opcional, #| if '.' in d

limpo = [
    i.lower().replace('www.', '')
    for i in dominios
    if '.' in i
]

print(limpo)