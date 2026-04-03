# Conceitos de Tuplas em Python

## O que é uma Tupla?
Uma tupla é uma coleção ordenada e **imutável** de elementos em Python. Uma vez criada, não pode ser modificada.

## Características Principais
- **Imutável**: Não pode ser alterada após criação
- **Ordenada**: Mantém a ordem dos elementos
- **Heterogênea**: Pode conter diferentes tipos de dados
- **Indexável**: Acesso por índice (começa em 0)
- **Iterável**: Pode ser percorrida em loop

## Criação de Tuplas

### Sintaxe Básica

```python
tupla = (1, 2, 3)
tupla_vazia = ()
tupla_um_elemento = (1,)  # Nota a vírgula
```

### Tuplas com Diferentes Tipos
```python
tupla_mista = (1, "texto", 3.14, True)
```

## Operações com Tuplas

### Indexação e Fatiamento
```python
tupla = (10, 20, 30, 40, 50)
print(tupla[0])      # 10
print(tupla[-1])     # 50
print(tupla[1:3])    # (20, 30)
```

### Concatenação e Repetição
```python
t1 = (1, 2)
t2 = (3, 4)
print(t1 + t2)       # (1, 2, 3, 4)
print(t1 * 3)        # (1, 2, 1, 2, 1, 2)
```

## Funções Úteis

### Funções Integradas
```python
tupla = (5, 2, 8, 2, 1)
len(tupla)           # 5
max(tupla)           # 8
min(tupla)           # 1
sum(tupla)           # 18
tupla.count(2)       # 2
tupla.index(8)       # 2
```

### Conversão
```python
lista = [1, 2, 3]
tupla = tuple(lista)  # (1, 2, 3)
```

## Operadores

| Operador | Descrição | Exemplo |
|----------|-----------|---------|
| `in` | Pertence à tupla | `2 in (1, 2, 3)` → `True` |
| `not in` | Não pertence | `4 not in (1, 2, 3)` → `True` |
| `+` | Concatenação | `(1, 2) + (3, 4)` |
| `*` | Repetição | `(1, 2) * 2` |
| `==` | Igualdade | `(1, 2) == (1, 2)` |
