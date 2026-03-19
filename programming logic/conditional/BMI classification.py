print("IMC")


idade = int(input("digite sua idade"))
altura = float(input("digite sua altura em centimetros (cm)"))
peso = float(input("digite seu peso em Kg"))

if not any([altura, peso, idade]):
    print("opss! prenncha todos")


elif isinstance(altura, str) or isinstance(peso, str) or isinstance(idade, str) :
    print("digite um numero, voce digitou texto em uma das opções")

else:
    altura = altura / 100
    imc = peso / altura ** 2


# classificação para adultos
if idade >= 60:
    
    if imc >= 27 :
        print("sobrepeso")

    elif imc > 22 :
        print("adequado ou eutrófico")

    else:
        print("baixo peso")

#clasificação para adultos
elif idade >= 20:

    if imc >= 40 :
        print("obesidade de classe 3")

    elif imc >= 35 :
        print("obesidade de classe 2")

    elif imc >= 30 :
        print("obesidade de classe 1")

    elif imc >= 25 :
        print("excesso de peso")


    elif imc >= 18.5 :
        print("peso normal")

    else:
        print("baixo peso")

else:
    print(""" sua idade não é compativel com esse programa
              
              a crianças ou adolescente é aferido outro tipo
              de medição, a massa corporea""")
