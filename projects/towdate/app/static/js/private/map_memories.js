document.addEventListener('DOMContentLoaded', () => {
    const mapEl = document.getElementById('memoriesMap');
    if (!mapEl) return;

    const defaultCenter = [-15.7801, -47.9292]; // fallback coords (Brasília)
    const map = L.map('memoriesMap').setView(defaultCenter, 4);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    let markers = L.layerGroup().addTo(map);

    function fetchData() {
        const params = new URLSearchParams(window.location.search);
        return fetch(`/memorias/mapa/data?${params.toString()}`)
            .then(r => r.json());
    }

    function renderSummary(data) {
        document.getElementById('totalPlaces').textContent = new Set(data.map(d => d.location)).size;
        document.getElementById('totalMemories').textContent = data.length;
        const cities = Array.from(new Set(data.map(d => d.city).filter(Boolean)));
        document.getElementById('citiesList').textContent = cities.length ? cities.join(', ') : '—';
    }

    function renderList(data) {
        const list = document.getElementById('placesList');
        list.innerHTML = '';
        data.forEach(item => {
            const el = document.createElement('div');
            el.className = 'memory-card';
            el.innerHTML = `
                <h4>${item.title}</h4>
                <p>${item.location || ''}</p>
                <p>${item.memory_date ? new Date(item.memory_date).toLocaleDateString() : ''}</p>
                <a class="btn btn-outline" href="/memorias/${item.id}">Abrir memória</a>
            `;
            list.appendChild(el);
        });
    }

    function addMarkers(data) {
        markers.clearLayers();
        const latlngs = [];
        data.forEach(item => {
            if (item.latitude && item.longitude) {
                const marker = L.marker([item.latitude, item.longitude]);
                const popup = `
                    <div style="max-width:240px">
                        ${item.photo ? `<img src="${item.photo}" alt="" style="width:100%;height:auto;border-radius:6px;margin-bottom:6px">` : ''}
                        <strong>${item.title}</strong>
                        <div>${item.memory_date ? new Date(item.memory_date).toLocaleDateString() : ''}</div>
                        <div style="font-size:13px;color:#666">${item.category || ''} — ${item.location || ''}</div>
                        <p style="margin-top:6px">${item.description || ''}</p>
                        <a class="btn btn-outline" href="/memorias/${item.id}">Abrir memória</a>
                    </div>
                `;
                marker.bindPopup(popup);
                marker.addTo(markers);
                latlngs.push([item.latitude, item.longitude]);
            }
        });
        if (latlngs.length) {
            const bounds = L.latLngBounds(latlngs);
            map.fitBounds(bounds.pad(0.2));
        }
    }

    function refresh() {
        fetchData().then(data => {
            renderSummary(data);
            renderList(data);
            addMarkers(data);
        }).catch(err => console.error(err));
    }

    document.getElementById('centerMap')?.addEventListener('click', () => {
        map.setView(defaultCenter, 4);
    });

    document.getElementById('resetFilters')?.addEventListener('click', () => {
        window.location.href = window.location.pathname;
    });

    document.getElementById('clearFilters')?.addEventListener('click', () => {
        window.location.href = window.location.pathname;
    });

    refresh();
});
