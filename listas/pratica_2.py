idades_sujo = ['24', '38', '47', '29', '49', '50', '35', '24','24', '38', '47', '27', '', '51', False, '21','2', '18', '41', '9', '', '50', '35', '24',True,'24', '38', '47', '', '21', '5', '', '2', '24', '38', '47', '29', '38', '50', '', 'true','24', '38', '47', 'a', '49', '15', '35', '24','24', '38', '47', '29', '18', '50', '35', '24','24', '38', '47', '29', 'brasil', '50', '35', '','24', '38', '', '9', '49', '50', '35', '24','24', '38', '47', '29', '49', 'thh', '35', '24','24', '68', '47', '29', '49', '50', '35', '24','24', '21', '47', '29', '49', '', '35', '24' ,'24', '38', '7', '29', '4', '50', '35', '24','14', '38', '27', '39', '29', '50', '30', 'abc', True, '8'] 


#print(len(idades_sujo))

idades_sujo_copia = idades_sujo.copy()
#for index, value in enumerate(idades_Copia):
#    print(index, value)

idades_limpa = []


for idade in idades_sujo_copia:
    if  isinstance(idade,str) and idade.isnumeric():
        idades_limpa.append(int(idade))
#print(idades_limpa)
idades_limpa_ordenada = sorted(idades_limpa)
#print(idades_limpa_ordenada)

media = sum(idades_limpa) /len(idades_limpa)
print(f' a media das idades é {media:.1f} anos')

print(f' a maior idade é: {max(idades_limpa)}')
print(f' a menor idade é: {min(idades_limpa)}')

print(f'a quantidades de idades registradas: {len(idades_limpa)}')


criancas = []
adultos = []
idosos = []



for idade in idades_limpa:
    if idade < 18:
        criancas.append(idade)
    elif idade < 60:
        adultos.append(idade)
    else:
        idosos.append(idade)

print(f'esses dados possui {len(criancas)} crianças')
print(f'esses dados possui {len(adultos)} adultos')
print(f'esses dados possui {len(idosos)} idosos')

de_maior = adultos + idosos
de_menor = len(idades_limpa) - len(de_maior)
print(f'quantidades de maior {len(de_maior)}')
print(f'quantidades de menor {de_menor}')

porcent_criancas = len(criancas) * 100 / len(idades_limpa)
porcent_adultos = len(adultos) * 100 / len(idades_limpa)
porcent_idosos = len(idosos) * 100 / len(idades_limpa)
porcent_de_maior = len(de_maior) * 100 / len(idades_limpa)
porcent_de_menor = de_menor * 100 / len(idades_limpa)
print(f'porcentagem de crianças {porcent_criancas:.1f}%')
print(f'porcentagem de adultos {porcent_adultos:.1f}%')
print(f'porcentagem de idosos {porcent_idosos:.1f}%')
print(f'porcentagem de de maior {porcent_de_maior:.1f}%')
print(f'porcentagem de de menor {porcent_de_menor:.1f}%')

#idade_digitada= int(input('digite a idade'))
#contador = idades_limpa.count(idade_digitada)
#print(f'a idade {idade_digitada} tem no banco {contador} vezes')

idades_unicas = []
for idade in idades_limpa:
    if idade not in idades_unicas:
        idades_unicas.append(idade)
idades_unicas.sort()
#print(idades_unicas)


