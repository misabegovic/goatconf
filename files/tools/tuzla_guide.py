#!/usr/bin/env python3
"""The "Introduction to Tuzla" guide: five A4 pages for visitors, in GoatConf's
look, after the EuRuKo 2024 "Introduction to Sarajevo" guide. Every fact comes
from the brain's sources (listed in
sources/conversations/2026-10-27--org--tuzla-guide.md); every photo is Grad
Tuzla's, credited on the photo; the food is shown with the sticker drawings.

  render   write site/guides/introduction-to-tuzla.pdf (needs Chrome)

Usage: python3 tools/tuzla_guide.py render
"""
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import brand  # noqa: E402

SITE = Path(__file__).resolve().parent.parent / "site"
OUT = SITE / "guides" / "introduction-to-tuzla.pdf"
F = (SITE / "fonts").as_uri()
IMG = lambda n: (SITE / "img" / n).as_uri()
ST = lambda n: (SITE / "stickers" / f"{n}.png").as_uri()
SEAL = (SITE / "brand" / "seal.svg").as_uri()

css = f"""
@font-face {{ font-family: "Bricolage Grotesque"; src: url("{F}/bricolage-wdth-latin.woff2") format("woff2"); font-weight: 200 800; font-stretch: 75% 100%; }}
@font-face {{ font-family: "Bricolage Grotesque"; src: url("{F}/bricolage-wdth-latin-ext.woff2") format("woff2"); font-weight: 200 800; font-stretch: 75% 100%; unicode-range: U+0100-02BA; }}
@font-face {{ font-family: "Atkinson Hyperlegible Next"; src: url("{F}/atkinson-latin.woff2") format("woff2"); font-weight: 200 800; }}
@font-face {{ font-family: "Atkinson Hyperlegible Next"; src: url("{F}/atkinson-latin-ext.woff2") format("woff2"); font-weight: 200 800; unicode-range: U+0100-02BA; }}
@page {{ size: A4; margin: 0; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: "Atkinson Hyperlegible Next", sans-serif; color: #12204a; font-size: 9.6pt; line-height: 1.38; }}
.page {{ width: 210mm; height: 297mm; padding: 13mm 14mm 11mm; position: relative; overflow: hidden; page-break-after: always; background: #fff; }}
.page::before {{ content: ""; position: absolute; left: 0; right: 0; top: 0; height: 4mm; background: #0b3d91; border-bottom: 1.2mm solid #ffd400; }}
header {{ display: flex; justify-content: space-between; align-items: center; padding: 3mm 0 4mm; border-bottom: 0.4mm solid #c9d7f5; margin-bottom: 5mm; }}
header .kick {{ font-family: "Bricolage Grotesque"; font-weight: 400; font-size: 21pt; color: #0b3d91; line-height: 1.05; }}
header h1 {{ font-family: "Bricolage Grotesque"; font-weight: 800; font-stretch: 78%; text-transform: uppercase; font-size: 30pt; line-height: .95; color: #051d47; }}
header img {{ width: 26mm; }}
h2 {{ font-family: "Bricolage Grotesque"; font-weight: 800; font-stretch: 85%; text-transform: uppercase; font-size: 11pt; letter-spacing: .02em; color: #0b3d91; margin: 0 0 3mm; display: inline-block; background: #ffd400; padding: .6mm 2.4mm .4mm; border-radius: 1mm; }}
.row {{ display: grid; grid-template-columns: 1fr 58mm; gap: 6mm; align-items: start; margin-bottom: 5mm; }}
.row.flip {{ grid-template-columns: 58mm 1fr; }}
.row.flip .pic, .row.flip .sticker {{ order: -1; }}
.row.text {{ grid-template-columns: 1fr; }}
.row.st {{ grid-template-columns: 1fr 34mm; }}
.row.st.flip {{ grid-template-columns: 34mm 1fr; }}
h3 {{ font-family: "Bricolage Grotesque"; font-weight: 700; font-stretch: 90%; font-size: 12pt; color: #051d47; margin-bottom: 1.6mm; text-decoration: underline; text-decoration-color: #ffd400; text-decoration-thickness: 1mm; text-underline-offset: .6mm; }}
ul {{ list-style: none; }}
li {{ position: relative; padding-left: 4.2mm; margin-bottom: 1.4mm; text-align: left; }}
li::before {{ content: ""; position: absolute; left: .4mm; top: 1.6mm; width: 1.8mm; height: 1.8mm; border-radius: 50%; background: #0b3d91; }}
.pic {{ position: relative; border-radius: 2mm; overflow: hidden; border: 1mm solid #fff; box-shadow: 0 .6mm 1.4mm rgb(0 0 0 / .25); }}
.pic img {{ display: block; width: 100%; height: 44mm; object-fit: cover; }}
.pic span {{ position: absolute; left: 2mm; bottom: 1.4mm; color: #fff; font-size: 7pt; font-weight: 700; text-shadow: 0 .3mm 1mm rgb(0 0 0 / .8); }}
.sticker {{ width: 34mm; }}
.note {{ background: #edf2fb; border-radius: 2mm; padding: 3mm 4mm; margin-top: 2mm; font-size: 8.8pt; }}
footer {{ position: absolute; left: 14mm; right: 14mm; bottom: 7mm; display: flex; justify-content: space-between; font-size: 7.5pt; color: #46557a; border-top: .3mm solid #c9d7f5; padding-top: 2mm; }}
.cols {{ display: grid; grid-template-columns: 1fr 1fr; gap: 6mm; }}
b {{ color: #051d47; }}
"""

def head(kick, title):
    return f'<header><div><div class="kick">Introduction to Tuzla:</div><h1>{title}</h1></div><img src="{SEAL}" alt=""></header>'

def foot(n):
    return f'<footer><span>GoatConf 2027 · Tuzla · 3–5 June 2027 · goatconf.com</span><span>{n} / 5</span></footer>'

def pic(name, h=44):
    return f'<div class="pic"><img src="{IMG(name)}" style="height:{h}mm"><span>Photo: Grad Tuzla</span></div>'

def entry(title, items):
    return f'<div><h3>{title}</h3><ul>' + "".join(f"<li>{i}</li>" for i in items) + "</ul></div>"

def row(body, side, flip=False, kind=""):
    return f'<div class="row {kind} {"flip" if flip else ""}">{body}{side}</div>'

def stk(n):
    return f'<img class="sticker" src="{ST(n)}" alt="">'

p1 = head("", "The town of salt") + '<h2>Top places to visit</h2>' + \
 row(entry("Freedom Square (Trg slobode)", [
   "About 8,000 m², called the largest square in Bosnia and Herzegovina.",
   "In the middle is a large fountain shaped like a salt-boiling dish.",
   "Around it stand the 16th-century Bazaar Mosque, the Ruždija (1883), the Čaršijska česma drinking fountain (1888) and the Baroque building (1900).",
   "The first Neolithic finds came up here in 1903, when it was called Appel Platz."]), pic("city-square-mosque-summer.jpg")) + \
 row(entry("Salt Square (Solni trg)", [
   "An open-air salt museum in the old town.",
   "It has an Ottoman salt well, a fountain given by Ravenna in the shape of a Neolithic salt dish, and a replica of how salt was boiled.",
   "A salt well here was dug or modernised in 1476, and up to 80 pans boiled brine on this spot."]), pic("city-old-town-aerial-paving.jpg"), flip=True) + \
 row(entry("The Korzo, and “at Meša and Ismet”", [
   "The Korzo is Turali Bey's Street, from the Kapija to the statues of Meša and Ismet.",
   "The statues are of the writer Meša Selimović and the painter Ismet Mujezinović, both from Tuzla.",
   "They are the city's meeting point: “kod Meše i Ismeta” is all you need to say.",
   "The Tourist Information Center is beside the Korzo, at Turalibegova 5."]), pic("city-korzo-clock.jpg")) + \
 row(entry("The Kapija", [
   "At one end of the Korzo. On 25 May 1995 a shell hit the Kapija, the centre of the city's nightlife, and killed 71 people, most of them young.",
   "A memorial carries every name. Pass it quietly."]), "", kind="text") + foot(1)

p2 = head("", "Salt, the goat and the past") + '<h2>A city on a grain of salt</h2>' + \
 row(entry("The name", [
   "Tuzla comes from the Turkish <i>tuz</i>, salt.",
   "Its older names are about salt too: Ad Salinas in Latin, Soli in South Slavic.",
   "Locals call it “the city on a grain of salt”: rock salt and salt water left by the Pannonian Sea."]), pic("city-aerial-summer.jpg", 40)) + \
 row(entry("Older than Rome", [
   "Neolithic pile dwellings stood in what is now the centre.",
   "Two reconstructed salt-boiling pots date to about 5,000 and 3,500 BC.",
   "An archaeological park of pile dwellings opened at the lakes in summer 2006.",
   "Louis XIV bought Tuzla salt in the 17th century."]), pic("city-archaeological-park.jpg", 40), flip=True) + \
 row(entry("The goat", [
   "Under Austro-Hungarian rule, goats were banned to protect the forests.",
   "One man in Mosnik kept his goat, and the saying was born: “Cijela Tuzla jednu kozu muzla”, all of Tuzla milked one goat.",
   "In GoatConf's telling, that one goat fed the whole town with milk and cheese.",
   "The tourist board makes Tuzla's goat a photo stop, and the city has a goat statue."]), stk("goat-statue"), kind="st") + \
 row(entry("Museums and the park", [
   "The Museum of Eastern Bosnia holds about 30,000 objects, some over 7,000 years old.",
   "The International Portrait Gallery (1964) holds more than 5,000 works.",
   "The Pannonica exhibition shows tuzlaite, a mineral found only in Tuzla's salt.",
   "The City Park has granite paths, free Wi-Fi and a footbridge to the salt lakes."]), stk("salt"), flip=True, kind="st") + foot(2)

p3 = head("", "Food and coffee") + '<h2>What to eat</h2>' + \
 row(entry("Ćevapi", [
   "Small rolls of minced meat with onion, served in lepinja or somun with chopped onion, often with kajmak or yoghurt.",
   "Tuzla's own: mutton, beef and lamb, in a lepinja first dipped in poljev, a beef-bone broth.",
   "About 7 to 10 KM for five, 12 to 15 KM for ten (Tuzla menus, October 2026)."]), stk("cevapi"), kind="st") + \
 row(entry("Pita", [
   "Burek, zeljanica, sirnica and krompiruša: thin pastry with meat, greens, cheese or potato.",
   "About 3 to 5.5 KM for 250 g (menus, October 2026)."]), stk("burek"), flip=True, kind="st") + \
 row(entry("Cooked dishes", [
   "Sarma (stuffed rolls) and punjene paprike (stuffed peppers): 6 to 14 KM on Tuzla menus.",
   "Grah, a bean stew: 6 to 13 KM. Begova čorba, the bey's soup: 6 to 9 KM.",
   "Meat-free dishes are on the menus at Pizza Bar, Pekara Hukić, Mozaik, Caffe Pizzeria Old School Pub and Zmaj od Bosne."]), "", kind="text") + \
 row(entry("Sweets, coffee and beer", [
   "Tufahija (3.5 to 5 KM) and hurmašice (1.7 to 4 KM).",
   "A cappuccino is about 3.25 KM (about 1.66 €).",
   "Pivara Tuzla has brewed since 1884, with water piped from Konjuh. Its own pub, Pivnica Taverna, pours unfiltered beer at Maršala Tita 163.",
   "Sloboda caffe bar sits on Salt Square, at Solni trg 10.",
   "The central market has sold fruit, vegetables and local products since 1952."]), stk("fildzan"), kind="st") + \
 '<div class="note">Prices were read on menus in October 2026 and will change. 1 € is 1.95583 KM, a fixed rate.</div>' + foot(3)

p4 = head("", "Getting around") + '<h2>Around IPI Academy</h2>' + \
 row(entry("Where GoatConf is", [
   "The talks are in English, at IPI Academy, Kulina bana 2, in the centre of Tuzla.",
   "Coffee and lunch are in the cafés on Freedom Square, under five minutes' walk away."]), pic("city-square-fountain-summer.jpg", 38)) + \
 '<div class="cols">' + \
 entry("Getting about", [
   "A tourist train runs from Freedom Square to the salt lakes.",
   "Nextbike bike share: 20 KM a year to register, the first 30 minutes free, then 1.5 KM an hour.",
   "Free city Wi-Fi, “Tuzla Wireless City”, covers the old town in 30-minute sessions.",
   "A city bus ticket is 2.50 KM.",
   "Taxis start at 3 KM.",
   "From the airport, a private transfer is about 12 minutes."]) + \
 entry("Good to know", [
   "Money: the convertible mark (KM). 1 € is 1.95583 KM.",
   "The airport has ATMs and an exchange office.",
   "Foreigners register with the police within 72 hours. Hotels usually do it for you.",
   "EHIC and GHIC cards do not cover Bosnia and Herzegovina: bring travel insurance.",
   "June is warm and the wettest month: highs about 26 °C, about 11 rain days.",
   "Emergency: ambulance 124, fire 123, police 122.",
   "Maps and event news: Tourist Information Center, Turalibegova 5."]) + '</div>' + \
 f'<div style="position:absolute; right:16mm; bottom:20mm; display:flex; gap:4mm">{stk("goat-host")}{stk("goat-coder")}{stk("goat-pirate")}</div>' + foot(4)

p5 = head("", "In and around Tuzla") + '<h2>Things to do</h2>' + \
 row(entry("The Pannonian salt lakes (Panonika)", [
   "Three salt-water lakes in the city centre, filled from underground salt wells.",
   "They opened in 2003, 2008 and 2012, with salt waterfalls, an archaeological park and water slides.",
   "They won the UNWTO Ulysses award in 2012.",
   "The season opens on 1 June, so they are open during GoatConf.",
   "In 2026 an adult ticket was 7 KM on weekdays and 9 KM at weekends."]), pic("city-lakes-aerial-summer.jpg", 46)) + \
 row(entry("Slana banja park", [
   "Next to the lakes: paths, sports courts, cafés, views, war memorials and the Peace Flame House."]), stk("salt-lakes"), flip=True, kind="st") + \
 '<div class="cols">' + \
 entry("Konjuh mountain", [
   "Averages 1,000 m and peaks at 1,328 m, with conifer and beech forest.",
   "Stećak necropolises and the old caravan road that carried Tuzla's salt.",
   "Hike with a local guide: landmines remain in rural areas, so stay on roads and paths."]) + \
 entry("Srebrenik Fortress", [
   "First recorded in 1333, a national monument since 2004.",
   "It stands on a rock about 5 km from Srebrenik's centre, entered by a small bridge."]) + \
 entry("Gradačac", [
   "A fort with 18 m walls and a 22 m tower, built by Husein-kapetan Gradaščević, the “Dragon of Bosnia”.",
   "A spa on thermal springs since 1882, and the lakes Hazna and Vidara."]) + \
 entry("Husino", [
   "The village of the 1920 miners' rebellion, with Ivan Sabolić's monument and the victims' steles in its park."]) + \
 '</div>' + foot(5)

html = f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>' + \
  "".join(f'<section class="page">{p}</section>' for p in (p1, p2, p3, p4, p5)) + "</body></html>"


def render() -> int:
    OUT.parent.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        page = Path(tmp) / "guide.html"
        page.write_text(html, encoding="utf-8")
        subprocess.run([brand.chrome(), "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=4000",
                        f"--print-to-pdf={OUT}", page.as_uri()], check=True, capture_output=True, timeout=120)
    print(f"wrote site/guides/{OUT.name}")
    return 0


if __name__ == "__main__":
    if sys.argv[1:] != ["render"]:
        print(__doc__)
        sys.exit(2)
    sys.exit(render())
