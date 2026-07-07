import re
import unicodedata
from datetime import date, datetime

from flask import url_for
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models.memory import Memory
from app.models.memory_collection import MemoryCollection
from app.models.memory_photo import MemoryPhoto
from app.models.memory_tag import MemoryTag
from app.models.tag import Tag
from app.services.relationship_service import get_active_relationship_member
from app.services.upload_services import remover_imagem, salvar_imagem

COLLECTION_PRESETS = {
    "cinema": {
        "title": "Cinema",
        "icon": "CM",
        "description": "Todos os momentos especiais que voces viveram juntos no cinema.",
        "background_image": "https://images.unsplash.com/photo-1544078751-58fee2d8a03b?w=1200&h=800&fit=crop",
    },
    "parques": {
        "title": "Parques",
        "icon": "PK",
        "description": "Caminhadas, por do sol e momentos de paz em verde.",
        "background_image": "https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?w=1200&h=800&fit=crop",
    },
    "restaurante": {
        "title": "Restaurantes",
        "icon": "RS",
        "description": "Jantares, cafes e encontros especiais.",
        "background_image": "https://images.unsplash.com/photo-1504674900152-b8b0cb6f3f61?w=1200&h=800&fit=crop",
    },
    "romance": {
        "title": "Romance",
        "icon": "RM",
        "description": "Momentos romanticos e historias marcantes.",
        "background_image": "https://images.unsplash.com/photo-1516589178581-6cd7833ae3b2?w=1200&h=800&fit=crop",
    },
    "viagem": {
        "title": "Viagens",
        "icon": "VG",
        "description": "Roteiros, descobertas e aventuras em casal.",
        "background_image": "https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=1200&h=800&fit=crop",
    },
    "datas-especiais": {
        "title": "Datas especiais",
        "icon": "DT",
        "description": "Celebracoes e momentos unicos da relacao.",
        "background_image": "https://images.unsplash.com/photo-1478759509037-27186f19749a?w=1200&h=800&fit=crop",
    },
    "aleatorias": {
        "title": "Aleatorias",
        "icon": "AL",
        "description": "Lembrancas espontaneas do dia a dia.",
        "background_image": "https://images.unsplash.com/photo-1516321318423-f06140bcbcc0?w=1200&h=800&fit=crop",
    },
}

COLLECTION_ALIASES = {
    "parks": "parques",
    "park": "parques",
    "parque": "parques",
    "restaurants": "restaurante",
    "restaurant": "restaurante",
    "restaurantes": "restaurante",
    "travels": "viagem",
    "travel": "viagem",
    "special": "datas-especiais",
    "datas": "datas-especiais",
    "random": "aleatorias",
    "nova": "nova",
}


class MemoryServiceError(Exception):
    """Erro de negocio para operacoes do modulo de memorias."""


def normalize_slug(value):
    """Normaliza texto para uso como slug."""

    normalized = unicodedata.normalize("NFKD", (value or "").strip().lower())
    without_accents = "".join(ch for ch in normalized if not unicodedata.combining(ch))
    slug = re.sub(r"[^a-z0-9]+", "-", without_accents).strip("-")
    return slug


def canonical_collection_slug(raw_slug):
    """Converte aliases para o slug canonico de colecao."""

    slug = normalize_slug(raw_slug)
    if not slug:
        return ""
    return COLLECTION_ALIASES.get(slug, slug)


def parse_tags(raw_tags):
    """Converte string de tags em lista de tags unicas e normalizadas."""

    if not raw_tags:
        return []

    items = []
    for piece in raw_tags.split(","):
        cleaned = piece.strip().lstrip("#").strip().lower()
        if not cleaned:
            continue
        cleaned = re.sub(r"\s+", "-", cleaned)
        cleaned = re.sub(r"[^a-z0-9\-]", "", normalize_slug(cleaned))
        if not cleaned:
            continue
        if cleaned not in items:
            items.append(cleaned)

    return items[:10]


def _resolve_collection_identity(collection_slug, custom_collection_name):
    slug = canonical_collection_slug(collection_slug)

    if not slug:
        raise MemoryServiceError("Escolha uma colecao para a memoria.")

    if slug == "nova":
        custom_name = (custom_collection_name or "").strip()
        if not custom_name:
            raise MemoryServiceError("Informe o nome da nova colecao.")

        generated_slug = normalize_slug(custom_name)
        if not generated_slug:
            raise MemoryServiceError("O nome da nova colecao e invalido.")

        return generated_slug, custom_name

    preset = COLLECTION_PRESETS.get(slug)
    if preset:
        return slug, preset["title"]

    human_name = slug.replace("-", " ").title()
    return slug, human_name


def _get_or_create_collection(relationship_id, collection_slug, custom_collection_name):
    slug, name = _resolve_collection_identity(collection_slug, custom_collection_name)

    collection = MemoryCollection.query.filter_by(
        relationship_id=relationship_id,
        slug=slug,
    ).first()

    if collection:
        if collection.name != name:
            collection.name = name
            db.session.add(collection)
            db.session.flush()
        return collection

    collection = MemoryCollection(
        relationship_id=relationship_id,
        slug=slug,
        name=name,
    )

    try:
        db.session.add(collection)
        db.session.flush()
    except IntegrityError:
        db.session.rollback()
        collection = MemoryCollection.query.filter_by(
            relationship_id=relationship_id,
            slug=slug,
        ).first()
        if collection is None:
            raise

        if collection.name != name:
            collection.name = name
            db.session.add(collection)
            db.session.flush()

    return collection


def _image_to_static_url(image_path):
    if not image_path:
        return ""
    return url_for("static", filename=f"uploads/{image_path}")


def _format_short_date(value):
    months = {
        1: "Jan",
        2: "Fev",
        3: "Mar",
        4: "Abr",
        5: "Mai",
        6: "Jun",
        7: "Jul",
        8: "Ago",
        9: "Set",
        10: "Out",
        11: "Nov",
        12: "Dez",
    }
    return f"{value.day:02d} {months[value.month]}"


def _format_long_date(value):
    months = {
        1: "Janeiro",
        2: "Fevereiro",
        3: "Marco",
        4: "Abril",
        5: "Maio",
        6: "Junho",
        7: "Julho",
        8: "Agosto",
        9: "Setembro",
        10: "Outubro",
        11: "Novembro",
        12: "Dezembro",
    }
    return f"{value.day} de {months[value.month]}, {value.year}"


def _days_since(memory_date):
    if memory_date is None:
        return 0
    delta = (date.today() - memory_date).days
    return max(0, delta)


def _get_active_relationship_for_user(user):
    """Retorna o relacionamento ativo do usuário autenticado."""

    member = get_active_relationship_member(user)
    if member is None or member.relationship is None:
        return None

    return member.relationship


def _get_active_relationship_id_for_user(user):
    """Retorna o id do relacionamento ativo do usuário autenticado."""

    relationship = _get_active_relationship_for_user(user)
    if relationship is None:
        return None

    return relationship.id


def _require_active_relationship_id_for_user(user):
    """Garante que o usuário tenha um relacionamento ativo para a operação."""

    relationship_id = _get_active_relationship_id_for_user(user)
    if relationship_id is None:
        raise MemoryServiceError(
            "Voce precisa ter um relacionamento ativo para registrar memorias."
        )

    return relationship_id


def create_memory_for_user(user, form):
    """Cria uma memoria para o relacionamento ativo do usuario."""

    relationship_id = _require_active_relationship_id_for_user(user)

    collection = _get_or_create_collection(
        relationship_id=relationship_id,
        collection_slug=form.collection_slug.data,
        custom_collection_name=form.custom_collection_name.data,
    )

    photos = [
        photo for photo in (form.photos.data or []) if getattr(photo, "filename", "")
    ]
    if not photos:
        raise MemoryServiceError(
            "Adicione pelo menos uma foto para registrar a memoria."
        )

    tags = parse_tags(form.tags.data)

    saved_file_names = []

    try:
        memory = Memory(
            relationship_id=relationship_id,
            collection_id=collection.id,
            title=form.title.data.strip(),
            description=form.description.data.strip(),
            memory_date=form.memory_date.data,
            location=(form.location.data or "").strip() or None,
            rating=form.rating.data,
            is_favorite=bool(form.favorite.data),
        )
        db.session.add(memory)
        db.session.flush()

        for index, photo in enumerate(photos):
            file_name = salvar_imagem(
                photo,
                pasta="memories",
                largura=1600,
                altura=1600,
                qualidade=88,
            )

            if not file_name:
                raise MemoryServiceError(
                    "Uma das fotos e invalida ou excede o limite permitido."
                )

            saved_file_names.append(file_name)

            db.session.add(
                MemoryPhoto(
                    memory_id=memory.id,
                    image_path=f"memories/{file_name}",
                    display_order=index,
                )
            )

        for tag_name in tags:
            tag = Tag.query.filter_by(name=tag_name).first()
            if tag is None:
                tag = Tag(name=tag_name)
                db.session.add(tag)
                db.session.flush()

            db.session.add(MemoryTag(memory_id=memory.id, tag_id=tag.id))

        db.session.commit()
    except MemoryServiceError:
        db.session.rollback()
        for file_name in saved_file_names:
            remover_imagem(file_name, "memories")
        raise
    except Exception as error:
        db.session.rollback()
        for file_name in saved_file_names:
            remover_imagem(file_name, "memories")
        raise MemoryServiceError(
            "Nao foi possivel salvar a memoria neste momento."
        ) from error


def get_collection_context_for_user(user, collection_slug):
    """Monta o contexto da pagina de colecao de memorias para o usuario."""

    relationship_id = _get_active_relationship_id_for_user(user)

    canonical_slug = canonical_collection_slug(collection_slug)
    if not canonical_slug:
        canonical_slug = "cinema"

    preset = COLLECTION_PRESETS.get(canonical_slug, COLLECTION_PRESETS["cinema"])

    if relationship_id is None:
        return {
            "slug": canonical_slug,
            "icon": preset["icon"],
            "title": preset["title"],
            "description": preset["description"],
            "memory_count": 0,
            "photo_count": 0,
            "background_image": preset["background_image"],
            "category": preset["title"],
            "featured": None,
            "summary": {
                "average_rating": "0.0",
                "total_memories": "0",
            },
            "memories": [],
        }

    collection = MemoryCollection.query.filter_by(
        relationship_id=relationship_id,
        slug=canonical_slug,
    ).first()

    if collection is None:
        return {
            "slug": canonical_slug,
            "icon": preset["icon"],
            "title": preset["title"],
            "description": preset["description"],
            "memory_count": 0,
            "photo_count": 0,
            "background_image": preset["background_image"],
            "category": preset["title"],
            "featured": None,
            "summary": {
                "average_rating": "0.0",
                "total_memories": "0",
            },
            "memories": [],
        }

    ordered_memories = sorted(
        collection.memories,
        key=lambda memory: (memory.memory_date, memory.created_at),
        reverse=True,
    )

    photo_count = sum(len(memory.photos or []) for memory in ordered_memories)

    average_rating = (
        sum(memory.rating for memory in ordered_memories) / len(ordered_memories)
        if ordered_memories
        else 0
    )

    memory_items = []
    for memory in ordered_memories:
        subtitle = memory.location or "Memoria registrada"
        image_path = memory.photos[0].image_path if memory.photos else ""

        memory_items.append(
            {
                "id": memory.id,
                "collection_slug": collection.slug,
                "title": memory.title,
                "description": memory.description,
                "subtitle": subtitle,
                "rating": float(memory.rating),
                "tags": [f"#{item.tag.name}" for item in memory.memory_tags],
                "date": _format_short_date(memory.memory_date),
                "image": _image_to_static_url(image_path),
            }
        )

    featured = None
    if memory_items:
        featured_memory = memory_items[0]
        featured = {
            "title": featured_memory["title"],
            "date": featured_memory["date"],
            "details": (
                f"{len(ordered_memories)} memorias | "
                f"{photo_count} fotos | {average_rating:.1f}"
            ),
            "image": featured_memory["image"],
        }

    return {
        "slug": collection.slug,
        "icon": preset["icon"],
        "title": collection.name,
        "description": preset["description"],
        "memory_count": len(ordered_memories),
        "photo_count": photo_count,
        "background_image": preset["background_image"],
        "category": collection.name,
        "featured": featured,
        "summary": {
            "average_rating": f"{average_rating:.1f}",
            "total_memories": str(len(ordered_memories)),
        },
        "memories": memory_items,
    }


def _matches_search(memory, query):
    if not query:
        return True

    needle = query.strip().lower()
    if not needle:
        return True

    text_parts = [
        memory.title or "",
        memory.description or "",
        memory.location or "",
    ]
    text_parts.extend(item.tag.name for item in memory.memory_tags)

    haystack = " ".join(text_parts).lower()
    return needle in haystack


def _matches_date_filter(memory, date_filter):
    if not date_filter or date_filter == "all":
        return True

    today = date.today()
    memory_date = memory.memory_date

    if date_filter == "7d":
        return (today - memory_date).days <= 7

    if date_filter == "30d":
        return (today - memory_date).days <= 30

    if date_filter == "this_month":
        return memory_date.year == today.year and memory_date.month == today.month

    return True


def _sort_memories(memories, sort_key):
    if sort_key == "oldest":
        return sorted(
            memories,
            key=lambda memory: (memory.memory_date, memory.created_at),
        )

    if sort_key == "best_rating":
        return sorted(
            memories,
            key=lambda memory: (
                memory.rating,
                memory.memory_date,
                memory.created_at,
            ),
            reverse=True,
        )

    return sorted(
        memories,
        key=lambda memory: (memory.memory_date, memory.created_at),
        reverse=True,
    )


def get_collection_context_for_user_filtered(
    user,
    collection_slug,
    query="",
    date_filter="all",
    sort="recent",
):
    """Monta contexto da colecao com filtros e ordenacao aplicados."""

    context = get_collection_context_for_user(user, collection_slug)

    relationship_id = _get_active_relationship_id_for_user(user)
    if relationship_id is None:
        context["filter_state"] = {
            "query": query,
            "date_filter": date_filter,
            "sort": sort,
        }
        return context

    collection = MemoryCollection.query.filter_by(
        relationship_id=relationship_id,
        slug=context["slug"],
    ).first()

    if collection is None:
        context["filter_state"] = {
            "query": query,
            "date_filter": date_filter,
            "sort": sort,
        }
        return context

    filtered_memories = [
        memory
        for memory in collection.memories
        if _matches_search(memory, query) and _matches_date_filter(memory, date_filter)
    ]

    ordered_memories = _sort_memories(filtered_memories, sort)

    memory_items = []
    for memory in ordered_memories:
        subtitle = memory.location or "Memoria registrada"
        image_path = memory.photos[0].image_path if memory.photos else ""

        memory_items.append(
            {
                "id": memory.id,
                "collection_slug": collection.slug,
                "title": memory.title,
                "description": memory.description,
                "subtitle": subtitle,
                "rating": float(memory.rating),
                "tags": [f"#{item.tag.name}" for item in memory.memory_tags],
                "date": _format_short_date(memory.memory_date),
                "image": _image_to_static_url(image_path),
            }
        )

    filtered_photo_count = sum(len(memory.photos or []) for memory in ordered_memories)
    filtered_average_rating = (
        sum(memory.rating for memory in ordered_memories) / len(ordered_memories)
        if ordered_memories
        else 0
    )

    context["memories"] = memory_items
    context["memory_count"] = len(memory_items)
    context["photo_count"] = filtered_photo_count
    context["summary"] = {
        "average_rating": f"{filtered_average_rating:.1f}",
        "total_memories": str(len(memory_items)),
    }

    if memory_items:
        context["featured"] = {
            "title": memory_items[0]["title"],
            "date": memory_items[0]["date"],
            "details": (
                f"{len(memory_items)} memorias | "
                f"{filtered_photo_count} fotos | {filtered_average_rating:.1f}"
            ),
            "image": memory_items[0]["image"],
        }

    context["filter_state"] = {
        "query": query,
        "date_filter": date_filter,
        "sort": sort,
    }

    return context


def apply_memory_form_defaults(form):
    """Aplica valores iniciais para o formulario de memoria."""

    if not form.memory_date.data:
        form.memory_date.data = date.today()


def get_memories_dashboard_context_for_user(user):
    """Monta o contexto da pagina principal de memorias do usuario."""

    default_collection_order = [
        "cinema",
        "parques",
        "restaurante",
        "viagem",
        "datas-especiais",
        "aleatorias",
    ]

    relationship = _get_active_relationship_for_user(user)

    empty_dashboard = {
        "stats": {
            "photos": 0,
            "memories": 0,
            "collections": len(default_collection_order),
            "last_label": "ha 0 dias",
        },
        "featured": {
            "title": "Nenhuma memoria registrada",
            "date": "",
            "description": "Comece registrando a primeira memoria de voces.",
            "image": COLLECTION_PRESETS["cinema"]["background_image"],
            "category": "Memorias",
        },
        "collections": [],
        "latest_memories": [],
    }

    if relationship is None:
        for slug in default_collection_order:
            preset = COLLECTION_PRESETS[slug]
            empty_dashboard["collections"].append(
                {
                    "slug": slug,
                    "title": preset["title"],
                    "image": preset["background_image"],
                    "average_rating": 0.0,
                    "memory_count": 0,
                    "days_since_last": 0,
                    "is_featured": False,
                }
            )
        return empty_dashboard

    all_memories = sorted(
        relationship.memories,
        key=lambda memory: (memory.memory_date, memory.created_at),
        reverse=True,
    )

    total_photos = sum(len(memory.photos or []) for memory in all_memories)
    last_memory = all_memories[0] if all_memories else None

    collections_payload = []
    for collection in relationship.memory_collections:
        collection_memories = sorted(
            collection.memories,
            key=lambda memory: (memory.memory_date, memory.created_at),
            reverse=True,
        )

        rating = (
            sum(memory.rating for memory in collection_memories)
            / len(collection_memories)
            if collection_memories
            else 0
        )

        last_collection_memory = collection_memories[0] if collection_memories else None
        days_since_last = (
            _days_since(last_collection_memory.memory_date)
            if last_collection_memory
            else 0
        )

        canonical_slug = canonical_collection_slug(collection.slug)
        preset = COLLECTION_PRESETS.get(canonical_slug, COLLECTION_PRESETS["cinema"])

        collections_payload.append(
            {
                "slug": collection.slug,
                "title": collection.name,
                "image": preset["background_image"],
                "average_rating": float(rating),
                "memory_count": len(collection_memories),
                "days_since_last": days_since_last,
                "is_featured": False,
                "updated_at": collection.updated_at or datetime.min,
            }
        )

    collections_payload.sort(
        key=lambda item: (
            item["memory_count"],
            item["updated_at"],
        ),
        reverse=True,
    )

    existing_slugs = {item["slug"] for item in collections_payload}
    for slug in default_collection_order:
        if slug in existing_slugs:
            continue
        preset = COLLECTION_PRESETS[slug]
        collections_payload.append(
            {
                "slug": slug,
                "title": preset["title"],
                "image": preset["background_image"],
                "average_rating": 0.0,
                "memory_count": 0,
                "days_since_last": 0,
                "is_featured": False,
                "updated_at": datetime.min,
            }
        )

    collections_payload = collections_payload[:6]
    if collections_payload:
        collections_payload[0]["is_featured"] = True

    latest_memories = []
    for memory in all_memories[:4]:
        latest_memories.append(
            {
                "title": memory.title,
                "category": memory.collection.name if memory.collection else "Memorias",
                "date": _format_short_date(memory.memory_date),
                "image": (
                    _image_to_static_url(memory.photos[0].image_path)
                    if memory.photos
                    else COLLECTION_PRESETS["cinema"]["background_image"]
                ),
            }
        )

    featured = empty_dashboard["featured"]
    if last_memory:
        featured = {
            "title": last_memory.title,
            "date": _format_long_date(last_memory.memory_date),
            "description": last_memory.description,
            "image": (
                _image_to_static_url(last_memory.photos[0].image_path)
                if last_memory.photos
                else COLLECTION_PRESETS["cinema"]["background_image"]
            ),
            "category": (
                last_memory.collection.name if last_memory.collection else "Memorias"
            ),
        }

    return {
        "stats": {
            "photos": total_photos,
            "memories": len(all_memories),
            "collections": len(collections_payload),
            "last_label": (
                f"ha {_days_since(last_memory.memory_date)} dias"
                if last_memory
                else "ha 0 dias"
            ),
        },
        "featured": featured,
        "collections": collections_payload,
        "latest_memories": latest_memories,
    }


def get_memory_for_user(user, memory_id):
    """Retorna memoria do relacionamento ativo do usuario."""

    relationship_id = _get_active_relationship_id_for_user(user)
    if relationship_id is None:
        return None

    return Memory.query.filter_by(
        id=memory_id,
        relationship_id=relationship_id,
    ).first()


def update_memory_for_user(user, memory_id, form):
    """Atualiza dados de uma memoria existente do usuario."""

    memory = get_memory_for_user(user, memory_id)
    if memory is None:
        raise MemoryServiceError("Memoria nao encontrada.")

    relationship_id = memory.relationship_id

    collection = _get_or_create_collection(
        relationship_id=relationship_id,
        collection_slug=form.collection_slug.data,
        custom_collection_name=form.custom_collection_name.data,
    )

    memory.title = form.title.data.strip()
    memory.description = form.description.data.strip()
    memory.memory_date = form.memory_date.data
    memory.location = (form.location.data or "").strip() or None
    memory.rating = form.rating.data
    memory.is_favorite = bool(form.favorite.data)
    memory.collection_id = collection.id

    tags = parse_tags(form.tags.data)
    previous_tag_ids = [item.tag_id for item in memory.memory_tags]

    try:
        MemoryTag.query.filter_by(memory_id=memory.id).delete()

        for tag_name in tags:
            tag = Tag.query.filter_by(name=tag_name).first()
            if tag is None:
                tag = Tag(name=tag_name)
                db.session.add(tag)
                db.session.flush()

            db.session.add(MemoryTag(memory_id=memory.id, tag_id=tag.id))

        db.session.commit()
    except Exception as error:
        db.session.rollback()
        raise MemoryServiceError("Nao foi possivel atualizar a memoria.") from error

    _delete_unused_tags(previous_tag_ids)
    return memory


def delete_memory_for_user(user, memory_id):
    """Remove memoria do relacionamento ativo do usuario."""

    memory = get_memory_for_user(user, memory_id)
    if memory is None:
        raise MemoryServiceError("Memoria nao encontrada.")

    stored_paths = [photo.image_path for photo in memory.photos]
    previous_tag_ids = [item.tag_id for item in memory.memory_tags]

    try:
        db.session.delete(memory)
        db.session.commit()
    except Exception as error:
        db.session.rollback()
        raise MemoryServiceError("Nao foi possivel excluir a memoria.") from error

    for path in stored_paths:
        if path.startswith("memories/"):
            remover_imagem(path.split("/", 1)[1], "memories")

    _delete_unused_tags(previous_tag_ids)


def _delete_unused_tags(tag_ids):
    """Remove tags sem vinculacao com memorias."""

    if not tag_ids:
        return

    for tag_id in set(tag_ids):
        exists = MemoryTag.query.filter_by(tag_id=tag_id).first()
        if exists:
            continue

        orphan_tag = Tag.query.get(tag_id)
        if orphan_tag:
            db.session.delete(orphan_tag)

    db.session.commit()
