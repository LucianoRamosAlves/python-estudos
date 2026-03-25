user = {'id': 1, 'nome': 'lucas', 'ano': 29, 'city': 'New eus'}

usar_str = {
     k: v.upper() #expressão #* temos sempre chave-valor(k e v)
     #* neste caso eu alterei/trasfmorei o valor .upper(), posso manipular também as chaves, colocar K.upper()
     for k, v in user.items() #loop #! começo por aqui, pecorro tudo
     if isinstance(v, str) #filtro #| aqui eu filtro tudo
}

print(f"${usar_str}")

usar_int = {
    k: v
    for k, v in user.items()
    if isinstance(v, int)
}

print(f"${usar_int}")