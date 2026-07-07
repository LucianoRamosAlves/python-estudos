import urllib.request, urllib.error, sys

urls = [
    "http://127.0.0.1:5000/memorias/mapa",
    "http://127.0.0.1:5000/memorias/mapa/data",
    "http://127.0.0.1:5000/static/js/private/map_memories.js",
    "http://127.0.0.1:5000/static/css/private/desejos.css",
]
for url in urls:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "TowDate-Test/1.0"})
        with urllib.request.urlopen(req, timeout=5) as r:
            print("URL:", url)
            print("Status:", r.status)
            print("Content-Type:", r.headers.get("Content-Type"))
            data = r.read(800)
            try:
                print("Body snippet:", data.decode("utf-8", errors="replace")[:600])
            except Exception as e:
                print("Body bytes:", data[:200])
    except urllib.error.HTTPError as e:
        print("URL:", url)
        print("HTTPError:", e.code)
        loc = e.headers.get("Location")
        if loc:
            print("Location header:", loc)
        body = e.read(400).decode("utf-8", errors="replace")
        print("Body snippet:", body[:400])
    except Exception as e:
        print("URL:", url)
        print("Error:", repr(e))
print("done")
