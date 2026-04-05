#| devo usar o cache para armazenar os resultados de funções que são chamadas com frequência e que têm um custo computacional alto. O cache pode ajudar a melhorar o desempenho do programa, evitando a
# necessidade de recalcular os resultados para entradas já processadas.

#| O cache é especialmente útil em situações onde a função é chamada repetidamente com os mesmos argumentos, como em algoritmos de programação dinâmica, onde os resultados de subproblemas são armazenados para evitar cálculos redundantes. Além disso, o cache pode ser benéfico em casos de funções recursivas, onde a mesma função é chamada várias vezes com os mesmos parâmetros.

#@ quando usar o cache:
#| 1. Funções com alto custo computacional: Se a função realiza cálculos complexos ou operações demoradas, o cache pode ajudar a reduzir o tempo de execução.

#| 2. Funções chamadas com frequência: Se a função é chamada repetidamente com os mesmos argumentos, o cache pode evitar cálculos redundantes e melhorar o desempenho.

from functools import lru_cache
@lru_cache
def calcular_fatorial(n):
    if n == 0:
        return 1
    else:
        return n * calcular_fatorial(n - 1)
    
calcular_fatorial(5)  # Calcula o fatorial de 5 e armazena o resultado no cache

lru_cache
def buscar_usuario(id):
    # Simula uma consulta a um banco de dados para buscar informações do usuário
    print(f"Buscando informações do usuário com ID {id}...")
    return {"id": id, "nome": f"Usuário{id}"}