# Exemplo 1: Classe simples
class Pessoa:  # Define uma classe chamada Pessoa
    def __init__(self, nome, idade):  # Construtor que inicializa os atributos
        self.nome = nome  # Armazena o nome do objeto
        self.idade = idade  # Armazena a idade do objeto
    
    def apresentar(self):  # Método que retorna uma apresentação
        return f"Olá, meu nome é {self.nome} e tenho {self.idade} anos"

# Criando objetos
pessoa1 = Pessoa("João", 30)  # Cria primeira instância da classe Pessoa
pessoa2 = Pessoa("Maria", 25)  # Cria segunda instância da classe Pessoa

print(pessoa1.apresentar())  # Chama o método apresentar de pessoa1
print(pessoa2.apresentar())  # Chama o método apresentar de pessoa2


# Exemplo 2: Classe com mais métodos
class Carro:  # Define uma classe chamada Carro
    def __init__(self, marca, modelo, ano):  # Construtor da classe
        self.marca = marca  # Atributo: marca do carro
        self.modelo = modelo  # Atributo: modelo do carro
        self.ano = ano  # Atributo: ano de fabricação
        self.velocidade = 0  # Atributo: velocidade inicial é zero

    def acelerar(self, incremento):  # Método que aumenta a velocidade
        self.velocidade += incremento  # Adiciona o incremento à velocidade
        return f"{self.marca} acelerou para {self.velocidade} km/h"
    
    def frear(self):  # Método que reduz a velocidade para zero
        self.velocidade = 0  # Reseta a velocidade
        return "Carro parou"
    
    def info(self):  # Método que retorna informações do carro
        return f"{self.ano} - {self.marca} {self.modelo}"

# Usando a classe
meu_carro = Carro("Toyota", "Corolla", 2022)  # Cria uma instância da classe Carro
print(meu_carro.info())  # Exibe as informações do carro
print(meu_carro.acelerar(50))  # Aumenta velocidade em 50 km/h
print(meu_carro.frear())  # Para o carro