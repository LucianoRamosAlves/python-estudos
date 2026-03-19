a = float(input("digite o lado a"))
b = float(input("digite o lado b"))
c = float(input("digite o lado c"))

if (a < b + c) and (b < a + c) and ( c < a + b):
    if (a == b ) and (b == c):
        lado = "equilatero"

    elif (a == b) or (b==c) or (c==a):
        lado = "isosceles"

    else:
        lado = "escaleno"

    if (a**2 == b**2 + c**2):
        angulo = "retangulo"


    elif (a**2 > b**2 + c**2):
        angulo = "obtusangulo"


    elif (a**2 < b**2 + c**2):
        angulo = "acutangulo"

    print(f"seu triangulo é do tipo {lado}\n e tem o angulo {angulo}")


else:
    print("opss, triangulo inesxistente")