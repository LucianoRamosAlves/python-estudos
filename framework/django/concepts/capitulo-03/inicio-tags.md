Django Taggit — Resumo até aqui
Instalação
Instalamos o pacote:
python -m pip install django-taggit==6.1.0
Depois adicionamos no settings.py:
INSTALLED_APPS = [
    # apps do Django...

    "taggit",

    "filmes.apps.FilmesConfig",
]
Boa prática:
Apps do Django
↓
Apps de terceiros
↓
Apps do projeto
Adicionando tags ao model
No models.py:
from taggit.managers import TaggableManager
E dentro de PostFilme:
tags = TaggableManager()
Isso permite usar:
post.tags
Relação entre posts e tags
Um post pode ter várias tags:
Corra
├── Terror
├── Suspense
└── Psicologico
E uma mesma tag pode estar em vários posts:
Corra ─── Terror
Nós ───── Terror
Isso é uma relação:
muitos-para-muitos
Migrations
Depois da mudança no model:
python manage.py makemigrations filmes
python manage.py migrate
O migrate também cria as tabelas internas do django-taggit.
Usando tags no shell
Abrir:
python manage.py shell
Importar:
from filmes.models import PostFilme
Pegar um post:
post = PostFilme.objects.get(id=1)
ou:
post = PostFilme.objects.first()
Adicionar tags
post.tags.add(
    "terror",
    "suspense",
    "psicologico",
)
Não precisa executar post.save() depois.
Ver tags
post.tags.all()
Remover tag
post.tags.remove("terror")
Remover todas
post.tags.clear()
Buscar posts por tag
PostFilme.objects.filter(tags__name="terror")
Isso significa:
PostFilme
↓
tags
↓
campo name
↓
"terror"
Ideia principal
O django-taggit nos dá um TaggableManager, que facilita:
post.tags.add()
post.tags.all()
post.tags.remove()
post.tags.clear()
Agora o próximo passo é começar a mostrar as tags nos templates e permitir clicar nelas para filtrar os posts.