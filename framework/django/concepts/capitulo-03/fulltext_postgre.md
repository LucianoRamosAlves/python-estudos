# Django — Full-Text Search, PostgreSQL e Migrações no CinePost

## Onde chegamos

Até aqui, o CinePost estava usando:

```text
Django
↓
SQLite
```

Agora começamos a parte de busca mais avançada.

O objetivo é chegar em algo assim:

```text
Usuário pesquisa:
"terror psicológico"

↓
CinePost analisa os textos
↓
retorna os posts mais relevantes
```

Para isso, o livro introduz:

```text
Full-Text Search
```

e vamos usar:

```text
PostgreSQL
```

---

# 1. Busca simples com `icontains`

O Django já permite fazer buscas simples usando o ORM.

Exemplo:

```python
PostFilme.objects.filter(
    titulo__icontains="terror"
)
```

Também podemos pesquisar no comentário:

```python
PostFilme.objects.filter(
    comentario__icontains="terror"
)
```

---

## O que significa `icontains`?

```text
i
→ ignora maiúsculas e minúsculas

contains
→ contém
```

Então:

```text
terror
Terror
TERROR
```

podem ser encontrados.

---

# Exemplo

```python
PostFilme.objects.filter(
    titulo__icontains="batman"
)
```

Pode encontrar:

```text
Batman Begins
The Batman
Batman Forever
```

---

# Limitação do `icontains`

O `icontains` basicamente pergunta:

```text
Este texto contém essa palavra?
```

É uma busca simples.

Ele não calcula muito bem coisas como:

```text
qual resultado é mais relevante?
```

ou:

```text
encontrar a palavra no título é mais importante do que no texto?
```

---

# 2. O que é Full-Text Search?

Full-Text Search significa:

```text
busca de texto completo
```

Em vez de simplesmente procurar uma sequência de caracteres, o sistema consegue analisar melhor as palavras de um texto.

Pode fazer coisas como:

```text
buscar palavras
↓
calcular relevância
↓
ordenar resultados
↓
dar pesos diferentes para campos
```

---

# Exemplo

Usuário pesquisa:

```text
ficção científica espacial
```

O sistema pode retornar:

```text
1. Interestelar
2. Duna
3. Alien
```

ordenando os resultados de acordo com a relevância.

---

# `icontains` x Full-Text Search

## Busca simples

```text
icontains
↓
"Esse texto contém esta palavra?"
```

## Full-Text Search

```text
Full-Text Search
↓
"Quais textos são mais relevantes para esta pesquisa?"
```

---

# Exemplo de peso

Imagine que o usuário pesquise:

```text
Batman
```

Resultado A:

```text
Título:
Batman
```

Resultado B:

```text
Comentário:
"...esse personagem lembra um pouco o Batman..."
```

Podemos configurar a busca para entender que:

```text
Batman no título
→ mais importante
```

do que:

```text
Batman no comentário
→ menos importante
```

---

# 3. Por que PostgreSQL?

O Django possui ferramentas específicas para Full-Text Search através de:

```python
django.contrib.postgres
```

Esse módulo aproveita recursos que existem no:

```text
PostgreSQL
```

---

# Nosso banco antigo

Até agora usamos:

```text
SQLite
```

Que ficava no arquivo:

```text
db.sqlite3
```

---

# Novo banco

Agora vamos usar:

```text
PostgreSQL
```

Então o projeto ficará:

```text
Django
↓
PostgreSQL
```

---

# O Django muda completamente?

Não.

Essa é uma das vantagens do ORM.

Antes:

```python
PostFilme.publicados.all()
```

funcionava com:

```text
SQLite
```

Agora o mesmo código pode funcionar com:

```text
PostgreSQL
```

Porque o Django ORM fica no meio:

```text
nosso código Python
↓
Django ORM
↓
banco de dados
```

---

# Antes

```text
Python
↓
Django ORM
↓
SQLite
```

# Agora

```text
Python
↓
Django ORM
↓
PostgreSQL
```

---

# 4. Docker

O livro sugeriu utilizar:

```text
Docker
```

para executar PostgreSQL.

A ideia seria:

```text
Windows
│
├── Django
│
└── Docker
    └── PostgreSQL
```

---

# O que é Docker?

Docker permite executar programas em ambientes isolados chamados:

```text
containers
```

Exemplo:

```text
Container
└── PostgreSQL
```

---

# Por que não continuamos com Docker?

No nosso computador o Docker encontrou um problema com:

```text
WSL 2
```

porque a virtualização do processador estava desabilitada.

O caminho começou a ficar:

```text
Docker
↓
WSL
↓
virtualização
↓
BIOS
↓
PostgreSQL
```

Como nosso objetivo principal é aprender Django e PostgreSQL, decidimos usar um caminho mais simples:

```text
instalar PostgreSQL diretamente no Windows
```

---

# 5. Instalando PostgreSQL no Windows

Instalamos:

```text
PostgreSQL 16
```

junto com:

```text
PostgreSQL Server
pgAdmin 4
Command Line Tools
```

---

# Porta

Mantivemos a porta padrão:

```text
5432
```

Então:

```text
PostgreSQL
→ localhost:5432
```

---

# Usuário principal

O PostgreSQL criou o usuário administrativo:

```text
postgres
```

Durante a instalação definimos uma senha para esse usuário.

---

# Importante

A senha do PostgreSQL não deve ficar exposta diretamente no código.

Vamos guardar no:

```text
.env
```

---

# 6. O que é pgAdmin?

O:

```text
pgAdmin 4
```

é uma ferramenta visual para administrar PostgreSQL.

Com ele podemos:

```text
criar bancos
ver tabelas
executar SQL
ver dados
gerenciar usuários
```

---

# 7. Criamos o banco do CinePost

No pgAdmin fomos em:

```text
Servers
↓
PostgreSQL 16
↓
Databases
↓
Create
↓
Database
```

Criamos:

```text
cinepost
```

Owner:

```text
postgres
```

Agora temos:

```text
PostgreSQL
└── banco cinepost
```

---

# 8. Driver `psycopg`

O Django precisa de um driver para conversar com PostgreSQL.

Instalamos:

```powershell
pip install "psycopg[binary]"
```

---

# O que é `psycopg`?

Ele funciona como uma ponte:

```text
Django
↓
psycopg
↓
PostgreSQL
```

Sem ele, o Django não conseguiria conversar com PostgreSQL.

---

# Testando `psycopg`

Podemos verificar com:

```powershell
python -c "import psycopg; print(psycopg.__version__)"
```

Se aparecer a versão:

```text
psycopg instalado corretamente
```

---

# 9. Configuração do `.env`

Adicionamos informações do banco no `.env`.

Exemplo:

```env
CINEPOST_DB_NAME=cinepost
CINEPOST_DB_USER=postgres
CINEPOST_DB_PASSWORD=SUA_SENHA
CINEPOST_DB_HOST=localhost
CINEPOST_DB_PORT=5432
```

---

# Por que usar `.env`?

Para evitar colocar coisas sensíveis diretamente no código.

Evitar:

```python
"PASSWORD": "minha_senha"
```

Preferir:

```python
"PASSWORD": os.getenv("CINEPOST_DB_PASSWORD")
```

---

# 10. Alterando o `DATABASES`

Antes o `settings.py` usava SQLite:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
```

Alteramos para PostgreSQL:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("CINEPOST_DB_NAME"),
        "USER": os.getenv("CINEPOST_DB_USER"),
        "PASSWORD": os.getenv("CINEPOST_DB_PASSWORD"),
        "HOST": os.getenv("CINEPOST_DB_HOST"),
        "PORT": os.getenv("CINEPOST_DB_PORT"),
    }
}
```

---

# Entendendo cada configuração

## `ENGINE`

```python
"ENGINE": "django.db.backends.postgresql"
```

Significa:

```text
Use PostgreSQL.
```

---

## `NAME`

```python
"NAME": os.getenv("CINEPOST_DB_NAME")
```

Nome do banco:

```text
cinepost
```

---

## `USER`

```python
"USER": os.getenv("CINEPOST_DB_USER")
```

Usuário do PostgreSQL:

```text
postgres
```

---

## `PASSWORD`

```python
"PASSWORD": os.getenv("CINEPOST_DB_PASSWORD")
```

Senha do usuário PostgreSQL.

---

## `HOST`

```python
"HOST": os.getenv("CINEPOST_DB_HOST")
```

Nosso banco está no próprio computador:

```text
localhost
```

---

## `PORT`

```python
"PORT": os.getenv("CINEPOST_DB_PORT")
```

Porta:

```text
5432
```

---

# Fluxo atual

Agora temos:

```text
CinePost
↓
Django
↓
psycopg
↓
localhost:5432
↓
PostgreSQL
↓
cinepost
```

---

# 11. Testando a conexão

Antes de criar qualquer tabela, usamos:

```powershell
python manage.py showmigrations
```

Se o Django consegue listar as migrations sem erro de conexão:

```text
admin
auth
contenttypes
filmes
sessions
sites
taggit
...
```

significa que:

```text
Django ✅
psycopg ✅
PostgreSQL ✅
banco cinepost ✅
```

---

# 12. O PostgreSQL novo estava vazio

Quando criamos:

```text
cinepost
```

ele não possuía nossas tabelas.

Tínhamos algo assim:

```text
SQLite
├── tabelas
└── dados
```

Enquanto o PostgreSQL estava:

```text
PostgreSQL
└── vazio
```

---

# Então usamos `migrate`

Executamos:

```powershell
python manage.py migrate
```

---

# O que `migrate` realmente faz?

Esse ponto é muito importante.

Durante todo o projeto nós fomos criando migrations.

Exemplo:

```text
0001_initial
0002_...
0003_...
```

Essas migrations são como um:

```text
histórico de construção do banco
```

---

# Analogia

Imagine que as migrations sejam plantas de construção:

```text
Migration 1
→ crie a tabela PostFilme

Migration 2
→ adicione um campo

Migration 3
→ altere alguma configuração
```

Quando executamos:

```powershell
python manage.py migrate
```

o Django lê essas instruções e aplica no banco atual.

---

# No SQLite

As migrations já tinham sido aplicadas anteriormente:

```text
SQLite
↓
tabelas já criadas
```

---

# No PostgreSQL

Como o banco era novo:

```text
PostgreSQL
↓
nenhuma tabela
```

Então:

```powershell
python manage.py migrate
```

fez:

```text
Django lê as migrations
↓
executa novamente no PostgreSQL
↓
cria todas as tabelas
```

---

# Resultado

Depois do `migrate`:

```text
SQLite
├── estrutura
└── dados antigos
```

e:

```text
PostgreSQL
├── estrutura
└── ainda sem nossos dados antigos
```

---

# Essa é uma das grandes utilidades das migrations

As migrations não servem apenas para atualizar o banco que já existe.

Elas também permitem:

```text
criar um banco novo do zero
```

seguindo todo o histórico do projeto.

---

# Exemplo

Se amanhã apagássemos o banco e criássemos outro vazio:

```text
novo banco
```

bastaria executar:

```powershell
python manage.py migrate
```

e o Django conseguiria reconstruir a estrutura.

---

# `makemigrations` x `migrate`

Essa diferença é muito importante.

## `makemigrations`

```powershell
python manage.py makemigrations
```

Significa:

```text
Olhe os Models
↓
descubra o que mudou
↓
crie instruções de migration
```

Mentalmente:

```text
makemigrations
= criar a planta
```

---

# `migrate`

```powershell
python manage.py migrate
```

Significa:

```text
pegue as migrations existentes
↓
execute no banco
↓
crie/alterar tabelas
```

Mentalmente:

```text
migrate
= executar a planta
```

---

# Exemplo completo

Alteramos o Model:

```python
class PostFilme(models.Model):
    genero = models.CharField(...)
```

Primeiro:

```powershell
python manage.py makemigrations
```

O Django cria algo como:

```text
0005_postfilme_genero.py
```

Depois:

```powershell
python manage.py migrate
```

O Django aplica isso no banco.

---

# Resumo

```text
Models
↓
makemigrations
↓
arquivo de migration
↓
migrate
↓
banco de dados
```

---

# Por que isso foi tão útil agora?

Porque mudamos de:

```text
SQLite
```

para:

```text
PostgreSQL
```

Mas não precisamos criar as tabelas manualmente.

Não precisamos abrir pgAdmin e fazer:

```sql
CREATE TABLE ...
```

uma por uma.

O Django já tinha o histórico.

Então:

```text
migrations antigas
↓
PostgreSQL novo
↓
python manage.py migrate
↓
estrutura reconstruída
```

---

# Atenção: estrutura não é a mesma coisa que dados

O `migrate` recriou:

```text
tabelas
campos
relacionamentos
índices
```

Mas não levou automaticamente:

```text
posts
comentários
usuários
tags
```

do SQLite antigo.

---

# Situação atual

Temos:

```text
db.sqlite3
```

com os dados antigos.

E temos:

```text
PostgreSQL
└── cinepost
```

com as tabelas novas.

---

# Importante

Não apagamos:

```text
db.sqlite3
```

porque ainda vamos precisar dele para recuperar os dados antigos.

---

# Próximo passo

O próximo objetivo será:

```text
SQLite
↓
exportar dados
↓
PostgreSQL
↓
importar dados
```

Para chegarmos a:

```text
PostgreSQL
├── tabelas ✅
├── posts ✅
├── comentários ✅
├── tags ✅
├── usuários ✅
└── demais dados ✅
```

---

# Resumo mental de tudo até aqui

```text
Queremos busca avançada
↓
Full-Text Search
↓
PostgreSQL
↓
instalamos PostgreSQL
↓
criamos banco cinepost
↓
instalamos psycopg
↓
configuramos .env
↓
alteramos DATABASES
↓
Django conecta no PostgreSQL
↓
migrate
↓
Django recria toda a estrutura do banco
```

---

# Conceitos principais

```text
icontains
= busca simples por texto
```

```text
Full-Text Search
= busca avançada com relevância
```

```text
PostgreSQL
= banco que vamos usar para Full-Text Search
```

```text
psycopg
= ponte entre Django e PostgreSQL
```

```text
pgAdmin
= ferramenta visual para administrar PostgreSQL
```

```text
makemigrations
= cria as instruções das mudanças
```

```text
migrate
= executa essas instruções no banco
```

---

# A grande sacada sobre migrations

Antes podia parecer que rodávamos:

```powershell
python manage.py migrate
```

apenas porque o Django mandava.

Agora fica mais claro o motivo.

As migrations permitem que o Django mantenha um histórico da estrutura do banco.

Por isso conseguimos trocar:

```text
SQLite
```

por:

```text
PostgreSQL
```

e reconstruir as tabelas simplesmente executando:

```powershell
python manage.py migrate
```

Essa é uma das grandes vantagens do sistema de migrations do Django.