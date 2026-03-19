email = "sdfsd@gmail.com "
email_valido = True

email = email.strip() #| junto tudo

if email == "":
    print("email vazio!")
    email_valido = False

elif not ("." in email and "@" in email):
    print("adcione @ ou .")
    email_valido = False

elif email.count("@") != 1 :
    print("deve conter pelo menos 1 @")
    email_valido = False

elif not email.endswith((".com", ".org", ".net")):
    print("adicione .com, .org ou .net")
    email_valido = False

elif len(email) > 200:
    print("email muito grande")
    email_valido = False

elif not(email[0].isalnum() and email[-1].isalnum() ):
    email[0].isalnum("email nao deve comecar e nem terminar com caracteres especias")
    email_valido = False

elif email_valido:
    print("email valido")

# NOTE se eu quiser um relatorio de todos os erros, troco todos os elif por if