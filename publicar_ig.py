"""Publica en el Instagram de Pronto Estudio el posteo del día (ig/<AAAA-MM-DD>/post.json) con la API oficial.

Corre en GitHub Actions (.github/workflows/publicar-ig.yml), así que no depende de ninguna PC prendida.
Las imágenes se sirven desde GitHub Pages: la API de Instagram necesita una URL pública.

Secrets del repo (los carga el operador, nunca van en un archivo):
  IG_TOKEN    token del usuario del sistema del portfolio de Pronto Estudio (instagram_content_publish)
  IG_USER_ID  id de la cuenta de Instagram profesional

Sin secrets o sin posteo del día, no hace nada y sale bien. Un posteo ya publicado no se repite.
  python publicar_ig.py [--fecha AAAA-MM-DD] [--seco]
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
BASE = "https://bigdaddy69-crypto.github.io/prontoestudio/ig"
AQUI = Path(__file__).resolve().parent


def llamar(metodo, ruta, token, **params):
    params["access_token"] = token
    datos = urllib.parse.urlencode(params).encode()
    url = f"{API}/{ruta}"
    if metodo == "GET":
        req = urllib.request.Request(f"{url}?{datos.decode()}")
    else:
        req = urllib.request.Request(url, data=datos, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        cuerpo = e.read().decode(errors="replace")
        sys.exit(f"❌ Meta respondió {e.code} en {ruta}: {cuerpo[:400]}")


def esperar(cid, token):
    for _ in range(30):
        st = llamar("GET", cid, token, fields="status_code").get("status_code")
        if st == "FINISHED":
            return
        if st in ("ERROR", "EXPIRED"):
            sys.exit(f"❌ el contenedor {cid} quedó en {st}")
        time.sleep(5)
    sys.exit(f"❌ el contenedor {cid} no terminó de procesarse")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--fecha", default=(datetime.now(timezone.utc) - timedelta(hours=3)).date().isoformat())
    ap.add_argument("--seco", action="store_true", help="muestra qué publicaría, sin llamar a Meta")
    a = ap.parse_args()
    carpeta = AQUI / "ig" / a.fecha
    archivo = carpeta / "post.json"
    if not archivo.exists():
        print(f"Sin posteo para {a.fecha}.")
        return
    post = json.loads(archivo.read_text(encoding="utf-8"))
    if post.get("estado") == "publicado":
        print(f"{a.fecha} ya está publicado.")
        return
    urls = [f"{BASE}/{a.fecha}/{i}" for i in post["imagenes"]]
    historias = [f"{BASE}/{a.fecha}/{h}" for h in post.get("historias", [])]
    if a.seco:
        print(json.dumps({"carrusel": urls, "historias": historias, "caption": post["caption"]}, ensure_ascii=False, indent=1))
        return
    token, ig = os.environ.get("IG_TOKEN"), os.environ.get("IG_USER_ID")
    if not token or not ig:
        print("Faltan los secrets IG_TOKEN / IG_USER_ID: no publico nada (el posteo queda listo).")
        return
    for u in urls + historias:  # GitHub Pages tiene que estar sirviendo las imágenes
        try:
            urllib.request.urlopen(urllib.request.Request(u, method="HEAD"), timeout=30)
        except Exception as e:  # noqa: BLE001
            sys.exit(f"❌ la imagen no está publicada todavía: {u} ({e})")

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
    print(f"✅ feed publicado: {feed_id}")

    ids_hist = []
    for u in historias:
        hid = llamar("POST", f"{ig}/media", token, image_url=u, media_type="STORIES")["id"]
        esperar(hid, token)
        ids_hist.append(llamar("POST", f"{ig}/media_publish", token, creation_id=hid)["id"])
    print(f"✅ historias: {len(ids_hist)}")

    post.update(estado="publicado", publicado=datetime.now(timezone.utc).isoformat(timespec="seconds"),
                id_feed=feed_id, ids_historias=ids_hist)
    archivo.write_text(json.dumps(post, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
