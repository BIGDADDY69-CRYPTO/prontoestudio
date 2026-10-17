"""Publica en Instagram el posteo del día con la API oficial: el de Pronto Estudio y el de cada cliente.

  ig/<AAAA-MM-DD>/post.json                     → Instagram de Pronto Estudio (secrets IG_TOKEN, IG_USER_ID)
  clientes/<slug>/ig/<AAAA-MM-DD>/post.json     → Instagram del cliente (secrets IG_TOKEN_<SLUG>, IG_USER_ID_<SLUG>;
                                                  slug en mayúsculas y con _ en vez de -)

Corre en GitHub Actions (.github/workflows/publicar-ig.yml), así que no depende de ninguna PC prendida.
Las imágenes se sirven desde GitHub Pages: la API de Instagram necesita una URL pública.
Los tokens los carga el operador como secrets del repo; nunca van en un archivo.
Sin secrets o sin posteo del día, esa cuenta se saltea. Un posteo ya publicado no se repite.
Un cliente con clientes/<slug>/PAUSA no publica (se frena con un mensaje: «frenar»).

  python publicar_ig.py [--fecha AAAA-MM-DD] [--seco] [--solo <slug>|propio]
"""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

API = "https://graph.facebook.com/v23.0"
PAGES = "https://bigdaddy69-crypto.github.io/prontoestudio"
AQUI = Path(__file__).resolve().parent


class ErrorMeta(Exception):
    pass


def secretos():
    """Todos los secrets llegan juntos en SECRETS (toJSON(secrets)); IG_TOKEN/IG_USER_ID sueltos también sirven."""
    try:
        s = json.loads(os.environ.get("SECRETS") or "{}")
    except ValueError:
        s = {}
    for k in ("IG_TOKEN", "IG_USER_ID"):
        if os.environ.get(k):
            s[k] = os.environ[k]
    return s


def llamar(metodo, ruta, token, **params):
    params["access_token"] = token
    datos = urllib.parse.urlencode(params).encode()
    url = f"{API}/{ruta}"
    req = (urllib.request.Request(f"{url}?{datos.decode()}") if metodo == "GET"
           else urllib.request.Request(url, data=datos, method="POST"))
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise ErrorMeta(f"Meta respondió {e.code} en {ruta}: {e.read().decode(errors='replace')[:400]}") from e


def esperar(cid, token):
    for _ in range(30):
        st = llamar("GET", cid, token, fields="status_code").get("status_code")
        if st == "FINISHED":
            return
        if st in ("ERROR", "EXPIRED"):
            raise ErrorMeta(f"el contenedor {cid} quedó en {st}")
        time.sleep(5)
    raise ErrorMeta(f"el contenedor {cid} no terminó de procesarse")


def cuentas():
    """[(nombre, carpeta ig, prefijo de URL, sufijo de secrets)]"""
    out = [("propio", AQUI / "ig", f"{PAGES}/ig", "")]
    for d in sorted((AQUI / "clientes").glob("*/ig")):
        slug = d.parent.name
        if (d.parent / "PAUSA").exists():
            print(f"⏸ {slug}: en pausa")
            continue
        out.append((slug, d, f"{PAGES}/clientes/{slug}/ig", "_" + slug.upper().replace("-", "_")))
    return out


def publicar(nombre, carpeta, base, sufijo, fecha, seco, sec):
    archivo = carpeta / fecha / "post.json"
    if not archivo.exists():
        print(f"· {nombre}: sin posteo para {fecha}")
        return False
    post = json.loads(archivo.read_text(encoding="utf-8"))
    if post.get("estado") == "publicado":
        print(f"· {nombre}: {fecha} ya está publicado")
        return False
    urls = [f"{base}/{fecha}/{i}" for i in post["imagenes"]]
    historias = [f"{base}/{fecha}/{h}" for h in post.get("historias", [])]
    if seco:
        print(json.dumps({"cuenta": nombre, "carrusel": urls, "historias": historias}, ensure_ascii=False, indent=1))
        return False
    token, ig = sec.get("IG_TOKEN" + sufijo), sec.get("IG_USER_ID" + sufijo)
    if not token or not ig:
        print(f"· {nombre}: faltan los secrets IG_TOKEN{sufijo} / IG_USER_ID{sufijo}; el posteo queda listo")
        return False
    for u in urls + historias:  # GitHub Pages tiene que estar sirviendo las imágenes
        urllib.request.urlopen(urllib.request.Request(u, method="HEAD"), timeout=30)
    if len(urls) == 1:
        cid = llamar("POST", f"{ig}/media", token, image_url=urls[0], caption=post["caption"])["id"]
    else:
        hijos = [llamar("POST", f"{ig}/media", token, image_url=u, is_carousel_item="true")["id"] for u in urls]
        for h in hijos:
            esperar(h, token)
        cid = llamar("POST", f"{ig}/media", token, media_type="CAROUSEL", children=",".join(hijos),
                     caption=post["caption"])["id"]
    esperar(cid, token)
    feed_id = llamar("POST", f"{ig}/media_publish", token, creation_id=cid)["id"]
    ids_hist = []
    for u in historias:
        hid = llamar("POST", f"{ig}/media", token, image_url=u, media_type="STORIES")["id"]
        esperar(hid, token)
        ids_hist.append(llamar("POST", f"{ig}/media_publish", token, creation_id=hid)["id"])
    post.update(estado="publicado", publicado=datetime.now(timezone.utc).isoformat(timespec="seconds"),
                id_feed=feed_id, ids_historias=ids_hist)
    archivo.write_text(json.dumps(post, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"✅ {nombre}: feed {feed_id} + {len(ids_hist)} historias")
    return True


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--fecha", default=(datetime.now(timezone.utc) - timedelta(hours=3)).date().isoformat())
    ap.add_argument("--seco", action="store_true", help="muestra qué publicaría, sin llamar a Meta")
    ap.add_argument("--solo")
    a = ap.parse_args()
    sec, errores = secretos(), []
    for nombre, carpeta, base, sufijo in cuentas():
        if a.solo and a.solo != nombre:
            continue
        try:
            publicar(nombre, carpeta, base, sufijo, a.fecha, a.seco, sec)
        except Exception as e:  # noqa: BLE001  (una cuenta que falla no frena a las demás)
            errores.append(f"{nombre}: {e}")
            print(f"❌ {nombre}: {e}")
    if errores:
        sys.exit("Fallaron: " + " · ".join(errores))


if __name__ == "__main__":
    main()
