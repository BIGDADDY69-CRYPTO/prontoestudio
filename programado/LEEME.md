# Programación de Instagram (@prontoestudio.ar)

El contenido está en `programado/AAAA-MM-DD/`, del 18/10 al 4/11. Se programa en Meta Business Suite → Planificador (Instagram web no programa ni sube historias). En cada post o historia, **desmarcá la página de Facebook**.
Esta carpeta **no la publica nadie solo**: el publicador automático (`publicar_ig.py`) lee `ig/`, no `programado/`.

## Qué hay en cada día
| Archivo | Qué es | Lunes a viernes | Sábado y domingo |
|---|---|---|---|
| `h1.png` | Historia «Nuevo posteo» | 9:30 | 10:00 |
| `1.png`… + `post.json` → `caption` | Carrusel del feed | 12:30 | 11:00 |
| `s1.png`, `s2.png`… + `historias.json` | Historias interactivas (desde el 22/10) | la hora de cada una en `historias.json` (13:00 / 17:30) | ídem |
| `h2.png` | Historia «Respondé con PALABRA» | 20:00 | 20:00 |
| `reel.mp4` + `reel.json` → `caption` | Reel (7 en total) | 21:00 | 19:00 |

**Historias interactivas:** cada `s*.png` deja libre el centro (recuadro punteado) para el sticker. Al subirla, agregá el sticker que dice `historias.json` (`encuesta`, `quiz`, `pregunta`, `cuenta` = cuenta regresiva, `slider`) con el texto y las opciones de ahí, encima del recuadro. Business Suite no pone stickers: esas se suben desde el celular (o se programan sin sticker y se pierde lo interactivo).
**Reels:** subilos desde la app, portada = el cuadro del segundo 1, y apenas sale **compartilo en historias** («Reel nuevo 👇»).

## Calendario 22/10 → 4/11
| Día | Carrusel 12:30 | Reel | Historias interactivas | Palabra |
|---|---|---|---|---|
| jue 22 | Presupuestos (empresas) | **La pregunta Nº 40** (ropa) 21:00 | encuesta envíos · pregunta | WHATSAPP |
| vie 23 | ⚠ usar `reemplazo/` (merch) en vez del de «la IA no te reemplaza» | — | encuesta domingo · lock · CTA | WHATSAPP |
| sáb 24 | Este Instagram se publica solo | **Peluquería 22:47** 19:00 | cuenta regresiva · encuesta · slider | MUESTRA |
| dom 25 | ¿Usás IA? (encuesta) | — | quiz · respuesta · pregunta | DIAGNOSTICO |
| lun 26 | Turnos que se agendan solos | **Merch: el domingo** 21:00 | encuesta · chat · CTA | WHATSAPP |
| mar 27 | ¿Alguien persigue cobros? (empresas) | — | slider · lista · pregunta | DIAGNOSTICO |
| mié 28 | ⚠ usar `reemplazo/` (inmobiliaria) en vez de «La IA es cara» | **Inmobiliaria: ¿sigue disponible?** 21:00 | encuesta · chat · CTA | MUESTRA |
| jue 29 | Del «¿precio?» al pedido | — | quiz 72 h · lista · pregunta | AUTOMATIZACION |
| vie 30 | ¿Cuántas de estas hacés a mano? | **Desafío concesionaria** 21:00 | cuenta regresiva · encuesta · chat · CTA | WHATSAPP |
| sáb 31 | Por dónde empezás | — | encuesta · lock · pregunta | DIAGNOSTICO |
| dom 1/11 | 5 mensajes que tu WhatsApp tendría que contestar solo (11:00) | **Salón: antes/después** 19:00 | encuesta · lista · CTA | WHATSAPP / MUESTRA |
| lun 2/11 | Si tenés peluquería, guardá esto | — | quiz · lock · CTA | MUESTRA |
| mar 3/11 | El WhatsApp de una tienda, antes y después | **Lo que te preguntan a las 23 h** 21:00 | cuenta regresiva · encuesta · pregunta | AUTOMATIZACION / WHATSAPP |
| mié 4/11 | ¿Cuánto te lleva contestar el precio? | — | pregunta · cuenta · CTA | DIAGNOSTICO |

Los carruseles del 22 al 31/10 son los que ya estaban (no se tocaron). Los del 23 y 28/10 hablan de «IA» en abstracto, que el operador pidió evitar: por eso está la alternativa en `2026-10-23/reemplazo/` y `2026-10-28/reemplazo/` (mismo formato). Si esos días ya están cargados en Business Suite, se cambian ahí.
Sistema completo, series y cómo medir: `cashflow-hq/docs/organico-viral.md`.

## Destacadas
Las portadas están en `marca/perfil/destacada-*.png` y las historias en `marca/destacadas/<nombre>/`:
- Casos (4)
- Cómo funciona (3)
- Precios (2)
- Preguntas (3)
- Diagnóstico (2)
- Armá el tuyo (2)

Se suben como historias y se guardan en su destacada.

## Palabras clave (respuesta automática por mensaje privado)
AUTOMATIZACION · PRECIOS · SEMANA · AUDITORIA · DIAGNOSTICO · CASO · **WHATSAPP** · **MUESTRA** (las dos últimas son nuevas del 18/10 y **hay que cargarlas** en ManyChat o en Business Suite antes del 22/10). Los textos están en `marca/perfil/automatizaciones.txt`.
