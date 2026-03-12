
senha = input('Por Favor! crie sua senha:')
if senha.islower():
    print('❌ ERRO !, Use pelo menos uma letra maiúscula')
elif senha.isupper():
    print('❌ ERRO !, Use pelo menos uma letra minuscula')
elif senha.isnumeric():
    print('❌ ERRO !, Use pelo menos uma letra')
elif senha.isspace():
    print('❌ \033[31;40mERRO \033[m!,Use pelo menos uma letra e numero')
elif senha.isalpha():
    print('❌ ERRO !, A senha precisa ter numeros')

else:
    print(' ✅ \033[32;40mok sua senha está salva\033[m Sua senha será :{:>8}'.format(senha))
