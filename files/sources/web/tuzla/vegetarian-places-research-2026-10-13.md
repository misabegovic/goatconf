---
title: "Vegetarian and vegan food near IPI Academy, Tuzla: research notes"
date: 2026-10-13
kind: web
---

Research by an agent on 2026-10-13, recorded as written: what was searched, what each source said, and short quotes of menu items. Follows on from places-research-2026-10-12.md and vegetarian-places-search-2026-10-12.md in this folder. Nothing here changes files/places/places.yml; the organiser decides what to add.

Reference points (same as places.yml): IPI 44.5404, 18.6738; Trg slobode 44.5393, 18.6746. Distances are straight-line, from IPI, computed from the coordinates given. No place was contacted, no form was submitted, no account was used.

Menu text below is quoted as shown on the page on 2026-10-13 (Bosnian, prices in KM). "Meat-free by the listed ingredients" means the menu lists the ingredients and none is meat or fish; it does not mean the place labels the dish vegetarian.

## 1. Searches that found nothing useful

Web searches (2026-10-13): "vegan Tuzla restaurant"; "vegetarijanski restoran Tuzla"; "posna jela Tuzla restoran meni"; "krompiruša zeljanica sirnica Tuzla pekara buregdžinica"; "falafel Tuzla"; "salata bar Tuzla"; "Tuzla pekara krompiruša cijena meni"; "Tuzla veganska hrana zdrava hrana prodavnica"; "restaurantguru Tuzla vegetarian friendly"; "happycow Tuzla Bosnia vegan"; "happycow.net reviews tuzla"; "Don Papa Tuzla meni sushi wok povrće"; "Barok Tuzla pizzeria meni jelovnik"; "\"Lijepa priča\" Tuzla palačinke slane meni"; "MamaMia Origins Tuzla menu vegetarian dish"; "Casper kebab Tuzla falafel". None found a vegetarian or vegan restaurant, a salad bar, or a falafel place in Tuzla (Bosnia). Results for "Tuzla" falafel and vegan were mostly about Tuzla in Istanbul. No menus were found for Barok, Don Papa, MamaMia Origins or Lijepa priča.

## 2. Sources that could not be read

- HappyCow, https://www.happycow.net/europe/bosnia_and_herzegovina/tuzla/ (also /print and the /widget/ page): Imperva "Additional security check is required" page with a CAPTCHA. Not bypassed. A search result says the HappyCow country page lists "Tuzla (2)", so HappyCow has two Tuzla listings that we could not see. The 2026-10-12 notes already record that "Darkwood - Craft Beer Garden" moved from Tuzla to Mostar.
- Restaurant Guru: the Tuzla list page loaded once (https://restaurantguru.com/Tuzla), then venue pages returned HTTP 503 "Suspicious activity detected" after about ten requests. Pages that did load are in section 5.
- Glovo: every Tuzla URL (for example https://glovoapp.com/en/ba/tuzla/ and https://glovoapp.com/bs/ba/tuzla/stores/restoran-mir-tzl) now redirects to the Glovo home page or "Not Found". Glovo seems to no longer serve Tuzla. Search engines still show old Glovo snippets (see section 6), which we could not check.
- Wolt: https://wolt.com/en/bih returns 404. Wolt does not appear to operate in Bosnia and Herzegovina.
- buregdzinicaoldstory.com: DNS lookup failed (EAI_AGAIN) on 2026-10-13.
- Tourism BiH pages: bot check for plain fetches; one page (Zdravljak Bosna) loaded in a browser but has no coordinates.

## 3. OpenStreetMap (Overpass)

Query run 2026-10-13 on https://overpass-api.de/api/interpreter, data timestamp 2026-10-13T11:57:40Z:

```
[out:json][timeout:60];(nwr["amenity"~"restaurant|fast_food|cafe|bar|pub|ice_cream|food_court"](44.533,18.662,44.546,18.685);nwr["shop"~"bakery|pastry|health_food|greengrocer|deli|convenience|supermarket|organic|nutrition_supplements"](44.533,18.662,44.546,18.685);nwr[~"^diet:"~"."](44.50,18.60,44.58,18.75););out center tags;
```

Result: no element inside the 44.533,18.662 to 44.546,18.685 box has diet:vegetarian or diet:vegan. No shop=health_food anywhere in the box. In the wider box (44.50,18.60 to 44.58,18.75) only four elements carry any diet:* tag, all about 2.4 km east of IPI on Ismeta Mujezinovića (Sjenjak):

- node 11069795149 "Favoris", amenity=restaurant, 44.5325555, 18.7029046: diet:vegetarian=yes, diet:vegan=yes (plus diet:meat=yes, diet:halal=yes), opening_hours Mo-Su 07:00-22:00. About 2466 m from IPI.
- node 11069795150 "café café kafeterija", amenity=fast_food (cafeteria), 44.5326458, 18.7024805: diet:vegetarian=yes, diet:vegan=yes, opening_hours Mo-Su 07:00-22:00, Instagram cafecafe.tuzla, website https://cafe-cafe-kafeterija.business.site/ (not checked). About 2431 m.
- node 11069795147 "CITY STEAK HOUSE", restaurant, steak_house, 44.5325871, 18.7021228: diet:vegan=yes and diet:non-vegetarian=yes (contradictory). About 2407 m.
- node 11447389082 "Donerhana", kebab: diet:non-vegetarian=yes (already known).

OSM tags are added by mappers, not by the venues, so they are leads, not proof.

Other OSM food points inside 800 m that are not in places.yml and have no menu source: node 4305976616 Antalya (turkish, Solni trg), node 1350032534 TNT (fast_food, sandwich, Solni trg), node 4336624291 London (fast_food, Solni trg 16), way 431402283 Žuta kuća (fast_food), node 3764956136 Fresh (fast_food, "regional,pizza,burger", about 416 m), node 4086383308 Sezam 2 (Turalibegova 22), node 4086765196 Sezam 7, node 6024615121 Fast food Pazar, node 4923509100 Lovac, bakeries node 2849418604 Breza and node 2849418605 Vrapče (about 480 to 540 m, Slatina), node 2314344030 Pekara Šaćir and node 3772291160 Pekara Tusanj (about 800 to 900 m), node 13614247063 Taco Bell (about 755 m, Univerzitetska 16), node 5302551721 "Old Story Pub" (Turalibegova 34, about 611 m).

## 4. Korpa.ba (delivery app), the main new source

Korpa.ba home page, city tab "Tuzla" (https://korpa.ba/), read in a browser on 2026-10-13. It showed 63 Tuzla partners. Each partner page (https://korpa.ba/partner/<slug>) shows the address and the full menu with ingredients. A keyword scan over all 63 menus for vegan, vegetar, posn, falafel, tofu, humus found the items below. No partner was labelled vegan or vegetarian as a whole, and no buregdžinica appears in the Tuzla list. "Trenutno nedostupno" means "currently unavailable" at the time of reading.

### Existing places in places.yml

- Pizza Bar, https://korpa.ba/partner/pizza-bar, "Trg žrtava genocida u Srebrenici, Tuzla". Pizza: "Margarita / Sir, paradajz sos / 10 KM"; "Fungi / Sir, šampinjoni, paradajz sos / 10 KM"; "Špinat pizza / Sir, špinat, jaje, paradajz sos / 13 KM"; "Vegetarijana / Sir, šampinjoni, paprika, luk, maslina, svježI paradajz, paradajz sos / 14 KM"; "Četiri sira / Edamer, mocarela, gorgonzola, parmezan, paradajz sos / 17 KM". Also "Omlet sa povrćem 9 KM", "Classic sendvič I / Domaće pecivo, sir, kajmak, salata / 4 KM", "Uštipci 2 / Sir, kajmak, suhi sir / 10 KM", "Šopska salata / Svježi sir, feta sir, ribanac, sezonsko povrće, domaće povrće / 8 KM", sweet pancakes. No item labelled vegan.
- Pizzeria Mozaik, https://korpa.ba/partner/pizzeria-mozaik, "Trgovačka 2-4, Tuzla 75000". "Pizza Vegetariana / Tijesto, sos, sir, šampinjoni, kukuruz, paprika, paradajz, luk, masline, origano / 14 KM"; "Pizza Margherita / Tijesto, sos, sir, origano / 14 KM"; "Pizza Funghi"; "Pasta funghi / Pasta, sos od gljiva / 11 KM"; "Vegetarijanski obrok / Pohovane pljeskavice od povrća, pomfrit, salata, pecivo / 12 KM"; "Vegetarijanski obrok sa povrćem / Carsko povrće, paprika, tikvica, riža / 9 KM"; and pita by weight: "Sirnica / 100gr / 1.7 KM", "Krompiruša / 100gr / 1.7 KM", "Zeljanica / 100gr / 1.7 KM".
- Pekara Hukić, https://korpa.ba/partner/pekara-hukic, "Gradska 59 Tuzla 75000". "Margherita (Paradajz sos i sir) 11 KM"; "Funghi (Paradajz sos, sir i gljive) 13 KM"; "Vegetariana (Paradajz sos, sir, gljive, paprika, kukuruz i cherry paradajz) 15 KM"; "Napolitana (Paradajz sos, mozzarella i bosiljak) 15 KM"; "Quattro formaggi" 15 KM; "Lisnato pecivo sa sirom 1.5 KM"; "Integralno pecivo sa sirom 1.5 KM"; bread, strudels, doughnuts. No pita (krompiruša, sirnica, zeljanica) on the Korpa menu. Confirms OSM house number 59.
- Palačinkara kod Bagija, https://korpa.ba/partner/palacinkara-kod-bagija, "Patriotske lige, Tuzla". Only sweet pancakes on Korpa, for example "Šumsko Voće & Jogurt (Klasični palačinak, jogurt krema, šumsko voće ...) 9 KM" and "Orah (Klasični palačinak, orah krema ...) 9.5 KM". No savoury pancakes listed.
- Ćevabdžinica Sarajka Korzo, https://korpa.ba/partner/cevabdzinica-sarajka-korzo, "Jevrejska 6". Menu is ćevapi and meat dishes; the only meat-free items are sides ("Pomfrit 4.5 KM", "Cheedar pomfrit 6 KM", "Jogurt", "Kajmak").
- Ćevabdžinica Limenka, https://korpa.ba/partner/cevabdzinica-limenka, "Patriotske lige 24". Ćevapi portions plus "Pomfrit (200g) 4.5 KM" and "Salata (Kupus, paradajz, 200g) 4.5 KM". No meat-free main.

### New places within about 800 m

- Zdravljak Bosna, https://korpa.ba/partner/zdravljak-bosna, "Muhameda Hevaija Uskufija 9, Tuzla 75000", rating 4.85. Items: "Sendvič - Veganski / 7 KM" (no ingredients listed); "Veggie wrap / 7 KM"; "Rižoto sa povrćem / 11 KM"; "Grilovano povrće / 6 KM"; pizzas "Margherita 9 KM", "Vegetariana 10 KM", "Funghi pizza 10 KM", "Pizza 4 vrste sira 11 KM"; "4 vrste sira pasta 12 KM"; "Omlet sa sirom 6 KM"; "Pohovani sir 7 KM". This is the only item in the walking radius that a source labels vegan. Tourism BiH (https://www.tourismbih.com/location/zdravljak-bosna/, published 2024-08-21) says it is "located on Muhameda Hevaija Uskufija in Tuzla". Location: Nominatim has the street "Muhameda Hevaije Uskufija" in Slatina as OSM way 27690968 (centroid 44.5398844, 18.6668112, the street runs from about 440 m to 670 m from IPI); house 9 is not in OSM. A second Nominatim street of the same name (way 33283346) is in Lukavac and is not this place.
- Caffe Pizzeria Old School Pub, https://korpa.ba/partner/caffe-pizzeria-old-school-pub, "Turalibegova 34, Tuzla", rating 4.41. "Veggi omlet 6.5 KM"; "Kajgana s mozzarella sirom 8 KM"; "Margarita Pizza" (described as pelat, melted cheese and oregano) 10 KM; "Quattro formaggi pizza 13 KM"; "Pohovani Sir" 10 KM; "Sirna Plata" (domestic cheeses with walnuts, olives and honey) 20 KM; "Sezonska salata 6 KM". In OSM the same address is node 5302551721 "Old Story Pub" (Mo-Su 08:00-00:00), and In Your Pocket lists "Old Story" at Turalibegova 34 as a pub. The names differ; it may have been renamed.
- Restoran barČina, https://korpa.ba/partner/restoran-barcina, "Turalibegova 64, Tuzla", rating 4.67. "Pizza vegeteriana / Paradajz sos, povrće / 13 KM" (no cheese listed); "Pizza Margherita / Paradajz sos, sir, origano, maslina / 12 KM"; "Domaća krompirčina / Punomasni kajmak, krompir, maslac, dimljeni suhi sir, prilog po izboru / 8 KM". Restaurant Guru (https://restaurantguru.com/barCina-Restaurant-and-Bar-Tuzla) gives "Turalibegova 46", coordinates 44.5351368, 18.6810344 (about 819 m) and hours Mo-Sa 07:00-23:00, Su 08:00-22:00. House number differs (64 vs 46).
- Casper Kebab, https://korpa.ba/partner/casper-kebab, "Univerzitetska bb, Tuzla Grad 75000", rating 4.80. Falafel section: "Falafel tortilja / Tortilja, svježa salata, falafel, sos / 7.5 KM"; "Falafel salata / Svježa salata, falafel, sos / 7 KM"; also falafel combined with beef or chicken doner. The falafel section was marked "Trenutno nedostupno" when read. In Your Pocket (https://www.inyourpocket.com/bosnia-herzegovina/tuzla/venues/casper-kebab-shop) gives "Turalibegova 22 (TC Pasaž)", "Open 08:00 - 23:30. Closed Sun.", and does not mention falafel. So there may be two branches; the falafel menu belongs to the Korpa listing at Univerzitetska bb. Not in OSM.
- Aljina kafana, https://korpa.ba/partner/aljina-kafana, "Gradska 1" (about 128 m). Meat menu; meat-free items are only salads ("Šopska salata porcija 5 KM", "Miješana salata 4 KM") and "Pomfrit 5 KM". Not a vegetarian option.
- Taco Bell Tuzla, https://korpa.ba/partner/taco-bell-tuzla, "Univerzitetska 16" (OSM node 13614247063, about 755 m). Burritos say "proteinom po izboru" (protein of your choice) but the choices are not shown in the page text; no meat-free item could be confirmed.

### Places further away with explicit vegetarian or vegan items (Korpa)

- Ali Baba Doner, https://korpa.ba/partner/ali-baba-doner, address given only as plus code "GMHV+8X2, Tuzla 75000" (decodes to about 44.5283, 18.6949, about 2.1 km from IPI). "Pizza Vegan / 10 KM" and "Pizza Vegetariana / 9 KM", no ingredients listed.
- Restoran Favoris, https://korpa.ba/partner/restoran-favoris, "Ismeta Mujezinovića 48, Tuzla" (matches OSM node 11069795149, about 2.47 km). "Vegetarijanska plata 10 KM", "Punjeni palačinci sa povrćem i sirom 12 KM", "Gratinirani palačinci sa povrćem 12 KM", "Rižoto sa povrćem i kurkumom 14 KM", "Vegetariana 9 KM", "Povrće sa žara 6 KM", "Omlet sa povrćem 7.5 KM". Nothing labelled vegan on Korpa, although OSM tags it diet:vegan=yes.
- En Vie, https://korpa.ba/partner/en-vie, "Mitra Trifunovića Uče bb" (about 1.96 km). "Vegeterijanski wrap / Kukuruz, grah, sir edamer, namaz, zelena salata, paradajz ... / 8 KM", "Omlet sa povrćem 8 KM", "Granola Power bowl" and "Granola protein bowl" (with Greek yoghurt), "Grčka salata". See section 5 for reviews.
- Other Korpa partners with a vegetarian pizza or dish, all outside the walking radius: Nota Bene ("Vegetarijana", "Vegetarijana od heljde"), Old Story Caffe Restaurant, Rudarska 68 ("Vegetariana", "Maslenjak sa sirom 13 KM"), La Linea, Stupine ("Omlet vegetarijanski", "Vegetarijana"), Pizza Trkačica, Nesiba Malkića 20 ("Vegetariana mala/srednja"), San Marco, Stupine ("Pica vegetarijana"), Pizzeria TNT krušna peć, 1. tuzlanske brigade 21 ("Vegetariana").
- Health-food shop: "Orašnica prodavnica zdrave hrane", https://korpa.ba/partner/orasnica-prodavnica-zdrave-hrane, "Univerzitetska 16, Tuzla 75000" (same building as Taco Bell and Mamamia, about 750 m). Its Korpa list is mostly herbal drops ("Biljne kapi ... 50 ml") and similar products; it is a health-food shop, not a place to eat.

## 5. Restaurant Guru pages that loaded

All fetched 2026-10-13 before the site started blocking. Coordinates from the page JSON-LD.

- TNT Mini Pizzerija, https://restaurantguru.com/TNT-mini-pizzerija-Tuzla, "Prve Tuzlanske 21", 44.5342874, 18.7032434 (about 2.4 km). Cuisine line "Pizza , Vegetarian options". A Google review quoted on the page: "Vegetarijanska pizza je odlična i bogata."
- En Vie coffee & snack, https://restaurantguru.com/En-Vie-Coffee-and-snack-Tuzla, "Mitra Trifunovića Uče bb", 44.5314028, 18.6525451 (about 1.96 km), Mo-Fr 07:00-22:00, Sa 07:00-21:00. Google reviews quoted on the page: "multiple, diverse, delicious vegetarian and vegan options" and, under "Vegetarian options", "one of the best places in Tuzla for yummy plant-based meals". Another review says they offer plant-based milk. These are customer reviews, not the menu.
- Arka Food - Coffee & Restaurant, https://restaurantguru.com/Arka-Food-Coffee-and-Restaurant-Tuzla, Mehmedalije Maka Dizdara b2 (about 1.8 km): one review answers "Vegetarian options: Ima." (there are). No dishes named.
- Sezam, https://restaurantguru.com/Sezam-Tuzla, "Turalibegova 22", 44.5370664, 18.6779742 (about 497 m), 07:00-00:00 daily. No vegetarian mention.
- Buregdžinica Tepsija, https://restaurantguru.com/Buregdzinica-Tepsija-Tuzla, "Rudarska 67", 44.536467, 18.6536753 (about 1.65 km), Mo-Fr 06:00-17:00, Sa 07:00-15:00. A review mentions burek "with cheese". No pita list.
- Pekara Maha (Hudeč, about 4 km), Delicija, MN FOOD, Quadro (all about 1.7 to 2.1 km, Stupine): no vegetarian information beyond generic dish tags.

## 6. Other sources

- tanjir.ba (delivery directory), https://www.tanjir.ba/tuzla: lists only five Tuzla places. Zmaj od Bosne, https://www.tanjir.ba/tuzla/zmaj-od-bosne, "Klosterska 11", working hours Mo-Fr 08:15-22:00, Sa-Su 10:00-22:00. Under "Jela po narudžbi": "Vegeterijanska plata / sezonsko povrće, gljive, kajmak / od 4,50 KM" and "Šampinjoni \"Indija\" sa pavlakom na riži (kari) / 5,00 KM". Also "Placka sir i kajmak 3,50 KM", "Uštipci sir i kajmak od 3,00 KM", "Pohovani sir ... od 3,00 KM". The prices (for example "Pljeskavica ... 2,50 KM") look many years old, so the page may be stale; the restaurant was shown as not open for delivery. Nominatim puts Klosterska 11 at OSM way 406368672, 44.5371419, 18.6798222 (about 599 m). No OSM POI there.
- In Your Pocket, Tuzla restaurants list, https://www.inyourpocket.com/tuzla/restaurants: 20 venues, no vegetarian or vegan text in the list. IYP "Royal", https://www.inyourpocket.com/bosnia-herzegovina/tuzla/venues/royal, "Bosne Srebrene 105/a", "open daily", says the menu has "some of the best vegetarian options in the city" (no dishes named). Nominatim puts Bosne Srebrene 105 at about 1.3 km from IPI. IYP "Coffee Zone", Fra Grge Martića 30, 07:00-23:00: sandwiches, no vegetarian mention.
- Search snippets only (pages not readable): a Glovo page titled "Buregdžinica Kipovi delivery in Tuzla" (https://glovoapp.com/ba/en/tuzla/buregdzinica-kipovi/) was summarised by the search tool as listing sirnica (KM 5,50), zeljanica (KM 5,50) and krompiruša (KM 5,00) with the store shown as closed; a later search for the same page did not return it, and the URL now redirects to the Glovo home page. A Glovo page "Buregdžinica Old Story" (https://glovoapp.com/hr/ba/tuzla/stores/pite-by-old-story) was summarised as listing krompiruša at KM 3.60 and sirnica; a search summary of buregdzinicaoldstory.com gave "Rudarska 17" (Nominatim: about 1.1 km from IPI). None of these could be confirmed.
- A search snippet of an older Glovo Mozaik page described "Vegeterijanski sendvič / Lepina, sir, kajmak, sezonska salata". Not on the current Korpa menu; not confirmed.

## 7. Summary

- Inside 800 m, the menus now confirm meat-free dishes at Pizza Bar, Mozaik (including vegetarian meals and sirnica, krompiruša, zeljanica), Pekara Hukić, Palačinkara kod Bagija (sweet pancakes only), Zdravljak Bosna, Caffe Pizzeria Old School Pub, Casper Kebab (falafel, Univerzitetska branch) and, just outside, barČina (about 819 m). Zmaj od Bosne (about 599 m) has a vegetarian plate on a possibly stale tanjir.ba menu.
- The only explicit "vegan" items found in Tuzla are "Sendvič - Veganski" at Zdravljak Bosna and "Pizza Vegan" at Ali Baba Doner (about 2.1 km), both on Korpa, both without ingredients. OSM tags Favoris, café café kafeterija and City Steak House (about 2.4 km) diet:vegan=yes. Reviews on Restaurant Guru call En Vie (about 2 km) good for vegan and plant-based food.
- No dedicated vegetarian or vegan restaurant, salad bar or Asian place with a confirmed meat-free dish was found in Tuzla.
