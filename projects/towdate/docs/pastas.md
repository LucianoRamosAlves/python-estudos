todate/
│
├── app/
│   │
│   ├── auth/
│   │   ├── routes.py
│   │   └── __init__.py
│   │
│   ├── public/
│   │   ├── routes.py
│   │   └── __init__.py
│   │
│   ├── private/
│   │   ├── routes.py
│   │   └── __init__.py
│   │
│   ├── static/
│   │
│   ├── templates/
│   │   │
│   │   ├── public/
│   │   │   ├── index.html
│   │   │   ├── about.html
│   │   │   └── pricing.html
│   │   │
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   │
│   │   ├── private/
│   │   │   ├── home.html
│   │   │   ├── dashboard.html
│   │   │   └── profile.html
│   │   │
│   │   ├── base_public.html
│   │   └── base_private.html
│   │
│   ├── db.py
│   ├── config.py
│   └── __init__.py
│
├── run.py
└── requirements.txt


svg 

            success: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><polyline points="20 6 9 17 4 12"></polyline></svg>',
            error: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>',
            warning: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.1"><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>',
            info: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.1"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>'