from flask import render_template
from flask_login import login_required

from app.private.routes import private


@private.route("/memorias/colecao/<collection_slug>")
@login_required
def colecao(collection_slug):
    collections = {
        "cinema": {
            "slug": "cinema",
            "icon": "🎬",
            "title": "Cinema",
            "description": "Todos os momentos especiais que vocês viveram juntos no cinema.",
            "memory_count": 32,
            "photo_count": 148,
            "background_image": "https://images.unsplash.com/photo-1544078751-58fee2d8a03b?w=1200&h=800&fit=crop",
            "category": "Cinema",
            "featured": {
                "title": "Maratona de clássicos e abraço no final",
                "date": "22 de Julho, 2025",
                "details": "4 memórias · 12 fotos · 4.9",
                "image": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?w=900&h=600&fit=crop",
            },
            "summary": {
                "average_rating": "4.7",
                "total_memories": "32",
            },
            "memories": [
                {
                    "title": "Noite de estreia",
                    "description": "Veio o primeiro beijo na entrada do cinema, aquele frio na barriga gostoso.",
                    "subtitle": "A primeira vez que assistimos juntos.",
                    "rating": 4.8,
                    "tags": ["Romance", "Noite", "Primeiro filme"],
                    "date": "07 Jul",
                    "image": "https://images.unsplash.com/photo-1497032628192-86f99bcd76bc?w=500&h=400&fit=crop",
                },
                {
                    "title": "Pipoca compartilhada",
                    "description": "Rimos de cada cena e dividimos a pipoca até o final do filme.",
                    "subtitle": "Risos, spoilers e escolha de filme.",
                    "rating": 4.6,
                    "tags": ["Pipoca", "Risos", "Parede cinza"],
                    "date": "13 Jul",
                    "image": "https://images.unsplash.com/photo-1517256064527-09c73fc73e66?w=500&h=400&fit=crop",
                },
                {
                    "title": "Noite de terror",
                    "description": "Abraçamos forte na cadeira escura enquanto o filme aterrorizava tudo.",
                    "subtitle": "Pulamos de susto e abraços no escuro.",
                    "rating": 4.4,
                    "tags": ["Medo", "Abraço", "Cinema"],
                    "date": "19 Jul",
                    "image": "https://images.unsplash.com/photo-1519677100203-a0e668c92439?w=500&h=400&fit=crop",
                },
                {
                    "title": "Clássicos do domingo",
                    "description": "Repassamos filmes antigos e lembramos de outros momentos juntos.",
                    "subtitle": "Redescobrimos filmes favoritos.",
                    "rating": 4.7,
                    "tags": ["Clássicos", "Domingo", "Romance"],
                    "date": "26 Jul",
                    "image": "https://images.unsplash.com/photo-1515378791036-0648a3ef77b2?w=500&h=400&fit=crop",
                },
            ],
        },
        "parques": {
            "slug": "parques",
            "icon": "🌳",
            "title": "Parques",
            "description": "Caminhadas, pôr do sol e momentos de paz em verde.",
            "memory_count": 27,
            "photo_count": 114,
            "background_image": "https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?w=1200&h=800&fit=crop",
            "category": "Parques",
            "featured": {
                "title": "Piquenique sob as árvores douradas",
                "date": "09 Maio, 2025",
                "details": "5 memórias · 18 fotos · 4.8",
                "image": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?w=900&h=600&fit=crop",
            },
            "summary": {
                "average_rating": "4.8",
                "total_memories": "27",
            },
            "memories": [
                {
                    "title": "Manhã de domingo",
                    "description": "Sentamos no banco da praça, com o mapa das rotas e o café na mão.",
                    "subtitle": "Brisa fresca e sorrisos cuidadosos.",
                    "rating": 4.9,
                    "tags": ["Manhã", "Café", "Verde"],
                    "date": "03 Maio",
                    "image": "https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?w=500&h=400&fit=crop",
                },
                {
                    "title": "Entardecer silencioso",
                    "description": "O crepúsculo desenhou tons dourados enquanto caminhávamos sem pressa.",
                    "subtitle": "Palavras suaves entre árvores.",
                    "rating": 4.7,
                    "tags": ["Entardecer", "Caminhada", "Silêncio"],
                    "date": "16 Maio",
                    "image": "https://images.unsplash.com/photo-1441829266145-bcd7b6f9cb27?w=500&h=400&fit=crop",
                },
                {
                    "title": "Piquenique inesperado",
                    "description": "A toalha estendida, o vento suave e a risada que ficou guardada como lembrança.",
                    "subtitle": "Sanduíches, risos e fotografia espontânea.",
                    "rating": 4.7,
                    "tags": ["Piquenique", "Verde", "Tarde"],
                    "date": "21 Maio",
                    "image": "https://images.unsplash.com/photo-1493246507139-91e8fad9978e?w=500&h=400&fit=crop",
                },
                {
                    "title": "Noite de lanternas",
                    "description": "O céu ficou colorido enquanto caminhávamos de mãos dadas sob as luzes.",
                    "subtitle": "Luzes delicadas sob o céu azul escuro.",
                    "rating": 4.9,
                    "tags": ["Luzes", "Caminhada", "Noite"],
                    "date": "30 Maio",
                    "image": "https://images.unsplash.com/photo-1445820134882-9a2e07a0c25c?w=500&h=400&fit=crop",
                },
            ],
        },
    }

    collection = collections.get(collection_slug, collections["cinema"])

    return render_template("private/memorias/colecao.html", collection=collection)
