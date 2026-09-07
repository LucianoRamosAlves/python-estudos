# Django — Migração do SQLite para PostgreSQL no CinePost

## Objetivo

O CinePost começou usando:

```text
SQLite
```

O banco ficava em:

```text
db.sqlite3
```

Depois decidimos migrar para:

```text
PostgreSQL
```

principalmente porque queremos utilizar recursos mais avançados, como:

```text
Full-Text Search
```

O objetivo final da migração foi:

```text
SQLite
↓
exportar os dados
↓
PostgreSQL
↓
recriar as tabelas
↓
importar os dados
```

Sem perder:

```text
usuários
posts
comentários
tags
```

---

# 1. SQLite x PostgreSQL

## SQLite

SQLite é um banco simples que fica basicamente em um arquivo:

```text
db.sqlite3
```

No Django:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
```

Fluxo:

```text
Django
↓
SQLite
↓
db.sqlite3
```

É muito prático para:

```text
estudos
projetos pequenos
desenvolvimento
testes
```

---

# PostgreSQL

PostgreSQL é um servidor de banco de dados mais completo.

Agora nosso fluxo é:

```text
Django
↓
psycopg
↓
PostgreSQL
↓
banco cinepost
```

Ele oferece recursos mais avançados, incluindo a busca textual que vamos estudar.

---

# 2. Instalando PostgreSQL

O livro utiliza Docker para executar PostgreSQL.

No nosso caso, Docker começou a exigir configuração de:

```text
WSL 2
virtualização
BIOS
```

Como nosso objetivo principal era aprender Django e PostgreSQL, escolhemos o caminho mais simples:

```text
instalar PostgreSQL diretamente no Windows
```

---

# Componentes instalados

Durante a instalação, utilizamos principalmente:

```text
PostgreSQL Server
pgAdmin 4
Command Line Tools
```

A porta padrão foi:

```text
5432
```

O usuário administrativo criado pelo PostgreSQL é:

```text
postgres
```

Também definimos uma senha durante a instalação.

---

# 3. O que é pgAdmin?

O pgAdmin é uma ferramenta gráfica para administrar PostgreSQL.

Com ele podemos:

```text
criar bancos
visualizar tabelas
consultar dados
executar SQL
gerenciar usuários
```

---

# 4. Criando o banco `cinepost`

No pgAdmin:

```text
Servers
↓
PostgreSQL
↓
Databases
↓
Create
↓
Database
```

Criamos:

```text
Database:
cinepost
```

Owner:

```text
postgres
```

Resultado:

```text
PostgreSQL
└── cinepost
```

Nesse momento o banco existia, mas estava vazio.

---

# 5. Instalando o driver PostgreSQL para Python

Django precisa de um driver para conversar com PostgreSQL.

Instalamos:

```powershell
pip install "psycopg[binary]"
```

---

# O que é `psycopg`?

É a ponte entre Python/Django e PostgreSQL.

```text
Django
↓
psycopg
↓
PostgreSQL
```

Sem o driver, Django não conseguiria abrir uma conexão com PostgreSQL.

---

# Testando o psycopg

Podemos testar com:

```powershell
python -c "import psycopg; print(psycopg.__version__)"
```

Se aparecer uma versão sem erro:

```text
psycopg funcionando ✅
```

---

# 6. Configurando as credenciais no `.env`

Não queremos deixar senha diretamente no `settings.py`.

Então colocamos os dados do banco no `.env`.

Exemplo:

```env
CINEPOST_DB_NAME=cinepost
CINEPOST_DB_USER=postgres
CINEPOST_DB_PASSWORD=SUA_SENHA
CINEPOST_DB_HOST=localhost
CINEPOST_DB_PORT=5432
```

Nunca envie ou publique a senha real.

---

# Por que usar `.env`?

Evita coisas assim:

```python
"PASSWORD": "minha_senha_secreta"
```

dentro do código.

Preferimos:

```python
"PASSWORD": os.getenv("CINEPOST_DB_PASSWORD")
```

---

# 7. Configurando PostgreSQL no Django

Antes tínhamos:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
```

Mudamos o banco padrão para:

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
use PostgreSQL
```

---

## `NAME`

```python
"NAME": os.getenv("CINEPOST_DB_NAME")
```

É o banco:

```text
cinepost
```

---

## `USER`

```python
"USER": os.getenv("CINEPOST_DB_USER")
```

É o usuário que acessará o PostgreSQL.

No nosso ambiente:

```text
postgres
```

---

## `PASSWORD`

```python
"PASSWORD": os.getenv("CINEPOST_DB_PASSWORD")
```

É a senha do usuário PostgreSQL.

---

## `HOST`

```python
"HOST": os.getenv("CINEPOST_DB_HOST")
```

Como PostgreSQL está instalado no nosso próprio computador:

```text
localhost
```

---

## `PORT`

```python
"PORT": os.getenv("CINEPOST_DB_PORT")
```

Usamos:

```text
5432
```

que é a porta padrão do PostgreSQL.

---

# 8. Testando a conexão

Podemos executar:

```powershell
python manage.py showmigrations
```

Se o Django conseguir acessar o banco e listar coisas como:

```text
admin
auth
contenttypes
filmes
sessions
sites
taggit
```

sem erro de conexão, significa:

```text
Django ✅
psycopg ✅
PostgreSQL ✅
cinepost ✅
```

---

# 9. O PostgreSQL ainda estava vazio

Nesse momento tínhamos:

```text
SQLite
├── tabelas
├── usuários
├── posts
├── comentários
└── tags
```

Enquanto o PostgreSQL tinha:

```text
PostgreSQL
└── cinepost
    └── vazio
```

Criar o banco no pgAdmin não cria automaticamente as tabelas do Django.

---

# 10. Usando `migrate`

Executamos:

```powershell
python manage.py migrate
```

Foi aqui que ficou muito claro para que migrations realmente servem.

---

# O que `migrate` fez?

O Django já possuía todo o histórico de migrations do projeto:

```text
0001_initial.py
0002_...
0003_...
...
```

Então:

```text
PostgreSQL vazio
↓
Django lê as migrations
↓
executa as instruções
↓
recria a estrutura
```

Depois:

```text
PostgreSQL
├── tabelas ✅
├── relacionamentos ✅
├── índices ✅
└── alguns dados internos do Django ✅
```

---

# Muito importante

`migrate` não levou nossos posts do SQLite para PostgreSQL.

Ele recriou principalmente:

```text
estrutura
```

Não:

```text
dados da aplicação
```

---

# Estrutura x Dados

## Estrutura

São coisas como:

```text
tabelas
colunas
ForeignKey
índices
restrições
```

## Dados

São coisas como:

```text
Luciano
Interestelar
comentário X
tag terror
```

---

# Depois do `migrate`

Tínhamos:

```text
SQLite
├── estrutura ✅
└── dados ✅
```

e:

```text
PostgreSQL
├── estrutura ✅
└── nossos dados ❌
```

---

# 11. `makemigrations` x `migrate`

Essa migração ajudou a entender a diferença.

## `makemigrations`

```powershell
python manage.py makemigrations
```

O Django:

```text
analisa os Models
↓
descobre alterações
↓
cria arquivos de migration
```

Mentalmente:

```text
makemigrations
= criar a planta
```

---

## `migrate`

```powershell
python manage.py migrate
```

O Django:

```text
lê as migrations
↓
executa no banco
↓
cria ou altera a estrutura
```

Mentalmente:

```text
migrate
= executar a planta
```

---

# Fluxo

```text
Models
↓
makemigrations
↓
arquivos de migration
↓
migrate
↓
banco de dados
```

---

# 12. Mantendo acesso ao SQLite antigo

Como já tínhamos mudado o banco `"default"` para PostgreSQL, adicionamos temporariamente o SQLite como um segundo banco.

No `settings.py`:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("CINEPOST_DB_NAME"),
        "USER": os.getenv("CINEPOST_DB_USER"),
        "PASSWORD": os.getenv("CINEPOST_DB_PASSWORD"),
        "HOST": os.getenv("CINEPOST_DB_HOST"),
        "PORT": os.getenv("CINEPOST_DB_PORT"),
    },

    "sqlite_antigo": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
}
```

Agora:

```text
default
→ PostgreSQL
```

e:

```text
sqlite_antigo
→ antigo db.sqlite3
```

---

# Por que fizemos isso?

Porque ainda precisávamos acessar os dados antigos.

O Django suporta múltiplos bancos.

Podemos selecionar qual banco usar através de:

```python
.using()
```

---

# Exemplo

```python
PostFilme.objects.count()
```

usa:

```text
default
→ PostgreSQL
```

Enquanto:

```python
PostFilme.objects.using("sqlite_antigo").count()
```

usa:

```text
SQLite antigo
```

---

# Mentalmente

```python
PostFilme.objects.count()
```

significa:

```text
Conte os posts no PostgreSQL
```

Enquanto:

```python
PostFilme.objects.using("sqlite_antigo").count()
```

significa:

```text
Conte os posts no SQLite
```

---

# 13. O que é `dumpdata`?

O Django possui um comando para exportar registros:

```powershell
python manage.py dumpdata
```

Ele transforma os dados do banco em um arquivo serializado.

Por padrão, utiliza:

```text
JSON
```

---

# Mentalmente

```text
Banco
↓
dumpdata
↓
arquivo JSON
```

---

# O que é uma Fixture?

O arquivo gerado pelo `dumpdata` é chamado de:

```text
fixture
```

É um arquivo contendo registros que o Django consegue importar posteriormente.

Exemplo conceitual:

```json
{
    "model": "filmes.postfilme",
    "pk": 1,
    "fields": {
        "titulo": "Interestelar",
        "nota": 10
    }
}
```

---

# 14. Primeiro problema — Codificação UTF-8

Inicialmente criamos o arquivo JSON normalmente.

Na hora de executar:

```powershell
python manage.py loaddata cinepost_data.json
```

recebemos:

```text
UnicodeDecodeError
```

Algo semelhante a:

```text
'utf-8' codec can't decode byte ...
```

---

# Por que aconteceu?

O arquivo continha caracteres como:

```text
á
é
í
ó
ú
ç
ã
```

e havia sido salvo com uma codificação diferente da esperada.

---

# Solução

Geramos novamente utilizando:

```text
-Xutf8
```

Exemplo:

```powershell
python -Xutf8 manage.py dumpdata ...
```

Isso força o Python a trabalhar em:

```text
UTF-8
```

---

# 15. Segundo problema — Dados internos duplicados

Ao tentar exportar absolutamente todo o banco SQLite, o JSON levou registros internos do Django, como:

```text
contenttypes
permissions
sites
```

Só que esses registros já tinham sido criados no PostgreSQL quando executamos:

```powershell
python manage.py migrate
```

Então o `loaddata` encontrou duplicação.

Recebemos um erro parecido com:

```text
IntegrityError

duplicar valor da chave viola a restrição de unicidade

(app_label, model)=(filmes, postfilme) já existe
```

---

# O que aconteceu?

O PostgreSQL já tinha:

```text
contenttypes:
filmes / postfilme
```

E o JSON tentou criar novamente:

```text
contenttypes:
filmes / postfilme
```

Resultado:

```text
duplicado ❌
```

---

# Solução

Em vez de exportar absolutamente tudo, exportamos somente os dados importantes para o CinePost:

```text
auth.user
filmes
taggit
```

---

# Comando final utilizado

```powershell
python -Xutf8 manage.py dumpdata auth.user filmes taggit --database=sqlite_antigo --natural-foreign --natural-primary --indent=2 --output=cinepost_data.json
```

---

# Entendendo esse comando

## `python -Xutf8`

```text
use UTF-8
```

Evita problemas com acentos e caracteres especiais.

---

## `manage.py dumpdata`

```text
exporte dados
```

---

## `auth.user`

Exporta:

```text
usuários
```

---

## `filmes`

Exporta os Models do nosso aplicativo.

Por exemplo:

```text
PostFilme
Comentario
```

---

## `taggit`

Exporta:

```text
tags
relações entre tags e posts
```

---

## `--database=sqlite_antigo`

Muito importante.

Significa:

```text
pegue os dados do SQLite antigo
```

e não do PostgreSQL.

---

## `--natural-foreign`

Ajuda o Django a representar algumas ForeignKeys utilizando chaves naturais.

É útil principalmente em fixtures e em relações com Models internos.

---

## `--natural-primary`

Utiliza chaves naturais para determinados Models que possuem esse recurso.

Ajuda a evitar conflitos durante a importação.

---

## `--indent=2`

Apenas deixa o JSON organizado:

```json
{
  "model": "...",
  "fields": {
    ...
  }
}
```

---

## `--output=cinepost_data.json`

Salva os dados em:

```text
cinepost_data.json
```

---

# Resultado

```text
SQLite
↓
dumpdata
↓
cinepost_data.json
```

---

# 16. O que é `loaddata`?

Depois usamos:

```powershell
python manage.py loaddata cinepost_data.json
```

Enquanto `dumpdata` faz:

```text
Banco
↓
arquivo
```

`loaddata` faz o contrário:

```text
arquivo
↓
Banco
```

---

# Como o Django sabia que deveria importar no PostgreSQL?

Porque PostgreSQL estava configurado como:

```python
"default"
```

Então:

```powershell
python manage.py loaddata cinepost_data.json
```

usa automaticamente:

```text
DATABASES["default"]
```

que agora era:

```text
PostgreSQL
```

---

# Fluxo da importação

```text
cinepost_data.json
↓
loaddata
↓
Django identifica os Models
↓
insere os registros
↓
PostgreSQL
```

---

# Resultado final

Depois que `loaddata` funcionou:

```text
PostgreSQL
├── usuários ✅
├── posts ✅
├── comentários ✅
├── tags ✅
└── relacionamentos ✅
```

---

# 17. Fluxo completo da migração

```text
SQLite
│
│ dados antigos
│
▼
dumpdata
│
▼
cinepost_data.json
│
│
│                PostgreSQL vazio
│                      │
│                      ▼
│                   migrate
│                      │
│                      ▼
│                 cria tabelas
│                      │
└──────────────► loaddata
                       │
                       ▼
                  PostgreSQL
                       │
                estrutura + dados
```

---

# Outra forma de visualizar

## Antes

```text
Django
↓
SQLite
↓
db.sqlite3
```

---

## Durante a migração

```text
SQLite
↓
dumpdata
↓
JSON

PostgreSQL
↓
migrate
↓
tabelas
```

Depois:

```text
JSON
↓
loaddata
↓
PostgreSQL
```

---

## Depois

```text
Django
↓
psycopg
↓
PostgreSQL
↓
cinepost
```

---

# 18. O antigo SQLite foi apagado?

Não.

Mantivemos:

```text
db.sqlite3
```

como segurança.

Isso é importante durante uma migração.

Não é uma boa ideia apagar imediatamente o banco antigo.

Primeiro verificamos:

```text
posts
comentários
tags
usuários
```

no novo banco.

Depois de confirmar que tudo está correto, podemos decidir se queremos manter o arquivo apenas como backup.

---

# 19. O JSON também pode ser mantido como backup?

Durante a migração, sim.

Temos:

```text
cinepost_data.json
```

contendo os dados exportados.

Porém, é importante lembrar que fixtures podem conter informações de usuários e outros dados.

Portanto, não devemos simplesmente publicar esse arquivo no GitHub sem verificar seu conteúdo.

---

# 20. Cuidados com Git

Arquivos que podem conter dados sensíveis não devem ser enviados para repositórios públicos.

Exemplos:

```text
.env
cinepost_data.json
```

O `.env` deve estar no:

```text
.gitignore
```

Por exemplo:

```gitignore
.env
```

Se decidir manter a fixture apenas localmente, também pode adicionar:

```gitignore
cinepost_data.json
```

---

# 21. Comandos principais aprendidos

## Criar migrations

```powershell
python manage.py makemigrations
```

---

## Aplicar migrations

```powershell
python manage.py migrate
```

---

## Mostrar migrations

```powershell
python manage.py showmigrations
```

---

## Exportar dados

```powershell
python manage.py dumpdata
```

---

## Importar dados

```powershell
python manage.py loaddata arquivo.json
```

---

# Comando de exportação usado no CinePost

```powershell
python -Xutf8 manage.py dumpdata auth.user filmes taggit --database=sqlite_antigo --natural-foreign --natural-primary --indent=2 --output=cinepost_data.json
```

---

# Comando de importação

```powershell
python manage.py loaddata cinepost_data.json
```

---

# 22. Principal diferença entre migration e fixture

Esse conceito é muito importante.

## Migration

Cuida principalmente da:

```text
ESTRUTURA
```

Exemplo:

```text
criar tabela
adicionar coluna
alterar campo
criar índice
```

---

## Fixture

Cuida dos:

```text
DADOS
```

Exemplo:

```text
Luciano
Interestelar
nota 10
tag ficção
comentário
```

---

# Mentalmente

```text
migration
= estrutura
```

```text
fixture
= registros
```

---

# Por isso usamos os dois

Primeiro:

```powershell
python manage.py migrate
```

Resultado:

```text
PostgreSQL
└── estrutura
```

Depois:

```powershell
python manage.py loaddata cinepost_data.json
```

Resultado:

```text
PostgreSQL
├── estrutura
└── dados
```

---

# 23. `dumpdata` x `loaddata`

Uma maneira fácil de lembrar:

```text
DUMP
= tirar
```

Então:

```text
dumpdata
= tirar os dados do banco e colocar em arquivo
```

Enquanto:

```text
load
= carregar
```

Então:

```text
loaddata
= carregar os dados do arquivo para o banco
```

---

# Resumo

```text
dumpdata
Banco → JSON
```

```text
loaddata
JSON → Banco
```

---

# 24. Grande aprendizado sobre o ORM

O nosso código Django praticamente não precisou mudar.

Por exemplo:

```python
PostFilme.publicados.all()
```

funcionava com SQLite.

E continua funcionando com PostgreSQL.

Isso acontece porque temos:

```text
nosso código
↓
Django ORM
↓
banco
```

O ORM abstrai grande parte das diferenças entre os bancos.

---

# Antes

```text
PostFilme.publicados.all()
↓
Django ORM
↓
SQLite
```

---

# Agora

```text
PostFilme.publicados.all()
↓
Django ORM
↓
PostgreSQL
```

---

# 25. Situação atual do CinePost

Agora estamos usando:

```text
Django
↓
psycopg
↓
PostgreSQL
↓
cinepost
```

E o banco possui:

```text
Models ✅
migrations ✅
usuários ✅
posts ✅
comentários ✅
tags ✅
```

O SQLite antigo ficou apenas como segurança.

---

# 26. Por que fizemos toda essa migração?

O principal motivo neste capítulo é poder utilizar recursos específicos do PostgreSQL.

Principalmente:

```text
Full-Text Search
```

Vamos poder trabalhar com recursos como:

```text
SearchVector
SearchQuery
SearchRank
```

para criar uma busca mais inteligente.

---

# Fluxo geral do capítulo

```text
Queremos busca avançada
↓
Full-Text Search
↓
precisamos de PostgreSQL
↓
instalamos PostgreSQL
↓
instalamos psycopg
↓
criamos cinepost
↓
configuramos DATABASES
↓
migrate
↓
exportamos dados do SQLite
↓
dumpdata
↓
fixture JSON
↓
loaddata
↓
dados no PostgreSQL
↓
CinePost migrado ✅
```

---

# Resumo mental final

```text
SQLite
= banco antigo
```

```text
PostgreSQL
= novo banco
```

```text
psycopg
= comunicação Django ↔ PostgreSQL
```

```text
migrate
= recria/aplica a estrutura
```

```text
dumpdata
= banco → arquivo
```

```text
fixture
= arquivo contendo registros
```

```text
loaddata
= arquivo → banco
```

```text
-Xutf8
= evita problemas de codificação
```

```text
--database=sqlite_antigo
= manda o Django buscar dados no SQLite antigo
```

```text
.using("sqlite_antigo")
= usa um banco específico através do ORM
```

---

# Principal aprendizado

Migrar um projeto Django de um banco para outro não significa recriar tudo manualmente.

Nós conseguimos aproveitar:

```text
Models
+
migrations
+
ORM
+
dumpdata
+
loaddata
```

para fazer:

```text
SQLite
↓
PostgreSQL
```

sem criar tabelas manualmente e sem reescrever os Models.

Esse processo mostrou na prática por que o sistema de migrations e o ORM são partes tão importantes do Django.