# 💰 Sistema de Controle de Caixa (Python)

Este projeto é um sistema simples de **controle de caixa via terminal**, desenvolvido em Python com o objetivo de praticar lógica de programação, funções e manipulação de dados.

---

## 📌 Funcionalidades

* 🔍 Verificar saldo atual
* 📉 Registrar dívidas (saídas)
* 💸 Registrar troco (saídas)
* 📈 Registrar entradas (ganhos)
* 🧾 Fechamento de caixa com registro em arquivo
* 📄 Salvamento automático em `caixa.txt`

---

## 🛠️ Tecnologias Utilizadas

* Python 3
* Biblioteca padrão:

  * `datetime`

---

## ▶️ Como executar

1. Certifique-se de ter o Python instalado
2. Execute o arquivo no terminal:

```bash
python nome_do_arquivo.py
```

---

## 📋 Menu do Sistema

O sistema apresenta as seguintes opções:

```
[0] Verificar saldo
[1] Registrar dívida
[2] Registrar troco
[3] Registrar entrada
[4] Fechar caixa
[5] Encerrar programa
```

---

## 🧠 Lógica do Sistema

O programa utiliza uma variável global chamada `caixa`, que representa o saldo atual.

### Funções principais:

* `entrada(valor)` → adiciona dinheiro ao caixa
* `divida(valor)` → remove dinheiro do caixa
* `troco(valor)` → remove dinheiro do caixa

⚠️ Observação:
O uso de `global` foi aplicado para fins didáticos. Em projetos maiores, isso não é recomendado.

---

## 📊 Fechamento de Caixa

Ao fechar o caixa, o sistema:

* Avalia o saldo final
* Classifica a situação:

  * 💚 **BOM** → saldo > 1000
  * 🟡 **REGULAR** → saldo > 500
  * 🔴 **RUIM** → saldo ≤ 500
* Salva os dados no arquivo `caixa.txt`

Exemplo de saída:

```
Responsável: João
Data: 2026-04-26
Saldo: R$ 850.00
Situação: REGULAR
```

---

## ⚠️ Tratamento de Erros

O sistema possui tratamento básico para:

* Entradas inválidas (`ValueError`)
* Valores negativos
* Saldo insuficiente

---

## 🚧 Melhorias Futuras

* ❌ Remover uso de variável global
* ✅ Criar estrutura com classes (POO)
* ✅ Melhorar validações
* ✅ Interface gráfica (GUI)
* ✅ Relatórios mais detalhados

---

## 🎯 Objetivo do Projeto

Este projeto foi desenvolvido para:

* Praticar lógica em Python
* Trabalhar com funções
* Entender fluxo de controle (`if`, `while`)
* Manipular arquivos (`.txt`)

---

## 👨‍💻 Autor

Luciano Ramos
📍 Brasil

---

## ⭐ Considerações

Este é um projeto de estudo, focado em aprendizado.
Sugestões e melhorias são sempre bem-vindas!
