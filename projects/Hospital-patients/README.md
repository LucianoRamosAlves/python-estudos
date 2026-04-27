# 🏥 Hospital Queue System (Python)

Sistema de gerenciamento de fila hospitalar desenvolvido em Python, utilizando a biblioteca **Rich** para interface visual no terminal.

Este projeto simula o funcionamento de um atendimento hospitalar, separando pacientes por prioridade e organizando a ordem de atendimento.

---

## 📌 Funcionalidades

* ➕ Adicionar pacientes (normais ou prioritários)
* 🚑 Atendimento com prioridade automática
* 📋 Listagem de pacientes em fila
* 🔍 Busca de paciente pelo nome
* 🗂️ Registro de pacientes atendidos (em memória)
* 🎨 Interface visual estilizada no terminal

---

## 🛠️ Tecnologias Utilizadas

* Python 3
* Rich (interface no terminal)
* Biblioteca padrão:

  * `os`
  * `time`

---

## ▶️ Como executar

1. Instale o Rich (caso ainda não tenha):

```bash id="cmd1"
pip install rich
```

2. Execute o programa:

```bash id="cmd2"
python nome_do_arquivo.py
```

---

## 📂 Estrutura do Sistema

O sistema utiliza listas para simular filas:

* `pacientes_prioritarios` → fila de prioridade
* `pacientes_normal` → fila comum
* `pacientes_atendidos` → histórico de atendimentos

Cada paciente é representado como:

```python id="code1"
[nome, tempo_de_espera, prioridade]
```

Exemplo:

```python id="code2"
["João", 30, True]
```

---

## 🧠 Lógica de Atendimento

O sistema segue a regra:

1. Atende primeiro pacientes prioritários
2. Caso não haja, atende pacientes normais
3. Remove da fila e adiciona à lista de atendidos

---

## 🎮 Menu do Sistema

```text id="menu1"
1 - Adicionar paciente
2 - Atender paciente
3 - Listar pacientes
4 - Buscar paciente
0 - Sair
```

---

## 🎨 Interface

A interface é feita com a biblioteca Rich, incluindo:

* Painéis estilizados
* Cores no terminal
* Spinners de carregamento
* Emojis para melhorar a experiência

---

## ⚠️ Observações

* Os dados são armazenados apenas em memória (não persistem após fechar o programa)
* Não há uso de banco de dados
* Projeto focado em aprendizado de lógica e listas

---

## 🚧 Melhorias Futuras

* 💾 Salvar dados em arquivo ou banco de dados
* 🧱 Refatorar usando Programação Orientada a Objetos (POO)
* ⏱️ Ordenar pacientes por tempo de espera
* 🖥️ Criar interface gráfica (GUI)
* 📊 Gerar relatórios de atendimento

---

## 🎯 Objetivo do Projeto

Este projeto foi desenvolvido para:

* Praticar listas em Python
* Trabalhar com estruturas de fila
* Melhorar lógica de programação
* Aprender uso da biblioteca Rich
* Simular sistemas reais simples

---

## 👨‍💻 Autor

Luciano Ramos
📍 Brasil

---

## ⭐ Considerações

Projeto de estudo com foco em evolução prática.
Cada melhoria representa um passo rumo a sistemas mais complexos.

Se esse projeto evoluir, pode se tornar um sistema completo de gestão hospitalar 🚀
