meu_projeto/
│
├── venv/                  # Ambiente virtual
│
├── app/                   # Aplicação principal
│   ├── __init__.py        # Cria a aplicação Flask
│   ├── routes.py          # Rotas
│   ├── models.py          # Modelos do banco
│   ├── forms.py           # Formulários (opcional)
│   │
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   ├── img/
│   │   └── fonts/
│   │
│   └── templates/
│       ├── base.html
│       ├── index.html
│       ├── login.html
│       └── cadastro.html
│
├── instance/              # Configurações locais e banco SQLite
│
├── migrations/            # Migrações do banco (Flask-Migrate)
│
├── tests/                 # Testes automatizados
│
├── config.py              # Configurações
├── run.py                 # Arquivo para iniciar a aplicação
├── requirements.txt       # Dependências
├── .env                   # Variáveis de ambiente
├── .gitignore             # Arquivos ignorados pelo Git
└── README.md              # Documentação