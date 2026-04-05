

#** boas praticas para o sql
email = ""
print(email != "") # até aqui dar false, validado

# porem se não for fornecido nada, None, esse passa, dar True
# ou seja não fica validado

email1 = None
print(email1 != "")

#vamos resolver
print(email1 != None and email1 != "" )
# agora foi validado

#** porem essa validação tem uma pratica melhor, usando o is
print(email1 is not None and email1 != "" )
# troco o != pelo is not