from datetime import datetime
import time
import urllib.parse
import urllib.request
import json

from app.extensions import db
from app.models.memory import Memory
from app.services.relationship_service import ensure_user_active_relationship


class MemoryMapServiceError(Exception):
    pass


def _ensure_relationship_for_user(user):
    relationship_member = ensure_user_active_relationship(user)
    if relationship_member is None or relationship_member.relationship is None:
        raise MemoryMapServiceError(
            "Você precisa de um relacionamento ativo para acessar o mapa de memórias."
        )

    return relationship_member.relationship


def _geocode_location(location):
    """Geocode a location string using Nominatim (OpenStreetMap).

    Returns (lat, lon, city) or (None, None, None) on failure.
    """
    try:
        base = "https://nominatim.openstreetmap.org/search"
        params = {"q": location, "format": "json", "addressdetails": 1, "limit": 1}
        url = f"{base}?{urllib.parse.urlencode(params)}"
        req = urllib.request.Request(
            url, headers={"User-Agent": "TowDate/1.0 (memory-map)"}
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            if not data:
                return None, None, None
            item = data[0]
            lat = float(item.get("lat"))
            lon = float(item.get("lon"))
            address = item.get("address", {})
            city = (
                address.get("city")
                or address.get("town")
                or address.get("village")
                or address.get("state")
            )
            return lat, lon, city
    except Exception:
        return None, None, None


def get_memories_for_map(
    user, category=None, date_from=None, date_to=None, city=None, favorites_only=False
):
    """Return memories with coordinates for the user's relationship, applying filters.

    If a memory has a textual location but no coordinates, attempt geocoding and persist results.
    """
    relationship = _ensure_relationship_for_user(user)

    query = Memory.query.filter(Memory.relationship_id == relationship.id)
    query = query.filter(Memory.location.isnot(None))

    if category:
        # category represented by collection slug
        from app.models.memory_collection import MemoryCollection

        query = query.join(Memory.collection).filter(MemoryCollection.slug == category)

    if date_from:
        query = query.filter(Memory.memory_date >= date_from)
    if date_to:
        query = query.filter(Memory.memory_date <= date_to)
    if city:
        query = query.filter(Memory.city.ilike(f"%{city}%"))
    if favorites_only:
        query = query.filter(Memory.is_favorite == True)

    memories = query.order_by(Memory.memory_date.desc()).all()

    results = []
    for m in memories:
        if m.latitude is None or m.longitude is None:
            lat, lon, resolved_city = _geocode_location(m.location)
            if lat and lon:
                m.latitude = lat
                m.longitude = lon
                if resolved_city and not m.city:
                    m.city = resolved_city
                try:
                    db.session.add(m)
                    db.session.commit()
                except Exception:
                    db.session.rollback()
            else:
                # skip if geocoding failed
                continue
            # small pause to be polite to Nominatim
            time.sleep(0.5)

        photo_url = None
        if m.photos:
            # memory photos ordered by id, take first
            first = m.photos[0]
            photo_url = getattr(first, "image_path", None)

        results.append(
            {
                "id": m.id,
                "title": m.title,
                "description": m.description[:200] if m.description else "",
                "memory_date": m.memory_date.isoformat() if m.memory_date else None,
                "category": m.collection.slug if m.collection else None,
                "location": m.location,
                "city": m.city,
                "latitude": float(m.latitude) if m.latitude is not None else None,
                "longitude": float(m.longitude) if m.longitude is not None else None,
                "photo": photo_url,
                "favorite": bool(m.is_favorite),
            }
        )

    return results
