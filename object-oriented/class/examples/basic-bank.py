from rich import print

class ContaBancaria: # Definição da classe ContaBancaria
    
    
    #| abaixo eu faço a documentação da minha classe, isso é importante para que outros programadores possam entender o que a classe faz e como usá-la.
    """A classe ContaBancaria representa uma conta bancária com funcionalidades básicas como depósito, saque e consulta de saldo.""" 
    
    
    
    def __init__(self, id, nome, saldo=0):
        self.id = id
        self.titular = nome
        self.saldo = saldo 
        
        
    def __str__(self): #| O método __str__ é um método especial em Python que é chamado quando você tenta imprimir um objeto ou convertê-lo para uma string. Ele deve retornar uma representação legível do objeto.
        
        
        return f"ContaBancaria(id={self.id}, titular='{self.titular}', saldo={self.saldo:.2f})"
    
    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            return f"Depósito de R${valor:.2f} [green]realizado com sucesso.[/green] Saldo atual: R${self.saldo:.2f}"
        else:
            return "[green]Valor de depósito deve ser positivo.[/green]"
        
        
    def sacar(self, valor):
        try:
            if valor > 0:
                if self.saldo >= valor:
                   self.saldo -= valor
                   return f"Saque de R${valor:.2f} [green]realizado com sucesso.[/green] Saldo atual: R${self.saldo:.2f}"
                else:
                    return "[red]Saldo insuficiente.[/red]"
            else:
               return "[red]Valor de saque deve ser positivo.[/red]"
           
        except:
            return f"Ocorreu um erro:"

    
c1 = ContaBancaria(1, "João", 1000)
print(c1.depositar(500))
print(c1.sacar(-900))
print(c1)
    