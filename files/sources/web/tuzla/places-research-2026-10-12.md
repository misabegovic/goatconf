---
title: "Places to eat and stay near IPI Academy and Freedom Square: research notes"
date: 2026-10-12
kind: web
---

Research by an agent on 2026-10-12, recorded as written: the queries, the pages used and short excerpts. The list it produced is in files/places/places.yml, each place unapproved until the organiser approves it.

# GoatConf 2027 places research: sources log

All queries and fetches were made on 2026-10-12. Raw responses that could be saved are in raw/ and raw/pages/. Excerpts below are verbatim unless marked "paraphrase" (some fetch tools only return short quotes).

## 1. Locating IPI Academy and Trg slobode

- Nominatim: https://nominatim.openstreetmap.org/search?q=Kulina+bana+2,+Tuzla&format=json (raw/nom_ipi.json). Returned only the street (OSM way 721130379), no house number 2.
- Nominatim: q=Trg slobode, Tuzla (raw/nom_trg.json). Relation 6079776, centroid 44.5393328, 18.6745945. Used as the Trg slobode point.
- Nominatim: q=IPI Akademija Tuzla, and q=Internacionalna poslovno-informaciona akademija: no result. OSM has no IPI object.
- Overpass mirror https://overpass.kumi.systems/api/interpreter, query `nwr(around:400,44.5389,18.6772)["addr:street"];out center tags;` (raw/ipi_addr.json, data timestamp 2026-07-28). Found "Hotel Vertigos", addr:street Kulina bana, addr:housenumber 4, node 8795554146 at 44.5405057, 18.6738737, and an unnumbered Kulina bana building (way 366022989) at 44.5403687, 18.673779.
- https://hotelvertigos.com: hotel gives its own address as "Kulina Bana 2, 75000 Tuzla".
- uniRank (search snippet), https://www.unirank.org/ba/uni/internacionalna-poslovno-informaciona-akademija/: "Address Kulina bana br. 2 Tuzla 75000".
- Read only, not edited: the goatconf repo's image notes (files/assets/images/ipi/ipi-building.jpg.json) say "The front of IPI Academy beside Hotel Vertigos, Kulina bana 2".
- Conclusion: IPI point set to 44.5404, 18.6738 (beside Vertigos). Approximate, about 10 to 20 m.
- First attempts at overpass-api.de: one 406 error and one timeout. The main query then ran fine.

## 2. Overpass main query (overpass.json)

Endpoint https://overpass-api.de/api/interpreter, data timestamp 2026-10-12T16:43:51Z, centre 44.5398,18.6742 (between IPI and the square):

```
[out:json][timeout:120];(nwr["amenity"~"^(cafe|restaurant|fast_food|bar|pub|ice_cream)$"](around:1000,44.5398,18.6742);nwr["shop"~"^(bakery|pastry)$"](around:1000,44.5398,18.6742);nwr["tourism"~"^(hotel|hostel|guest_house|apartment|motel)$"](around:2000,44.5398,18.6742););out center tags;
```

114 elements. No element had diet:vegetarian or diet:vegan. One (Donerhana) has diet:non-vegetarian=yes. Many cafés have no name. Hotel Tuzla, Heartland and So i Sol are not tagged as tourism=* in OSM.

Extra geocoding (raw/nominatim_geocodes.json): ZAVNOBiH-a 13, Patriotske lige 24, Tabašnice 2, Đorđa Mihajlovića, Univerzitetska 16, Jevrejska 5/6, Turalibegova 18, Kazan mahala 10, Goli brijeg 8, Obala Zmaja od Bosne 24, Franjevačka 4, Tabašnice 19, Trg Stara tržnica 8, Aleja Alije Izetbegovića 3, "Hotel Tuzla", "Hotel Mellain Tuzla".

## 3. Vegetarian and vegan evidence

Web searches run: "vegan vegetarian restaurant Tuzla Bosnia HappyCow"; "vegetarijanski veganski restoran Tuzla centar"; "tripadvisor Tuzla restaurants vegetarian friendly"; "happycow Tuzla"; "Tuzla vegetarijanska pizza meni Trg slobode"; "wolt Tuzla restaurant vegetarian"; "Tuzla vegan hrana restoran veganska" (extended); "Tuzla Bosnia vegan cafe OR bistro OR salad bar" (extended).

Result: no dedicated vegetarian or vegan place found in Tuzla.

- HappyCow https://www.happycow.net/europe/bosnia_and_herzegovina/tuzla/: blocked (Incapsula "Request unsuccessful"). A search snippet says the vegan-friendly "Darkwood - Craft Beer Garden" was relocated from Tuzla to Mostar.
- In Your Pocket, "Vegan and vegetarian eating in Bosnia & Herzegovina", https://test.inyourpocket.com/vegan-and-vegetarian-eating-in-bosnia-herzegovina_77487f (undated, "more than a year ago"). Under "Options and logic" it argues pizzerias are a reliable vegetarian choice: "Pizza Bar (Tuzla), Mozart (Foča) and Palazzo (Bosanska Krupa) all deserve attention." It also says (paraphrase) that outside Sarajevo and Banja Luka vegetarian-focused restaurants are hard to find. House of Taste (Tuzla) also appears in its listings: "Waffles, pancakes, toast and more, House of Taste is a smashing spot to stop for the most important meal of the day".
- Restaurant Guru, https://restaurantguru.com/Tuzla and venue pages (raw/pages/*.html). Cuisine line on MamaMia Origins: "European , Mediterranean , Central European , Barbecue , Vegetarian options" ... "Price range per person BAM 17-BAM 44". On Mamamia (Univerzitetska 16): "European , International , Vegetarian options" ... "Price range per person BAM 10-BAM 35". No vegan tag anywhere.
- TripAdvisor vegetarian list, https://www.tripadvisor.com/Restaurants-g303197-zfz10665-Tuzla_Tuzla_Canton_Federation_of_Bosnia_and_Herzegovina.html: 403 when fetched. Search snippet only (paraphrase): the list includes "Mama Mia" and "MamaMia Origins", and one entry gives "Univerzitetska 16".
- In Your Pocket "Royal" (search snippet): the hotel restaurant opposite the bus and train stations (Bosne Srebrene 105/a) has "some of the best vegetarian options in the city". Not included: about 1.3 km from IPI, outside the 1 km eating radius, and not verified further.

## 4. Eat: venue sources

- In Your Pocket Tuzla restaurants list: https://www.inyourpocket.com/tuzla/restaurants (20 names, no dates).
- IYP Barok: "A pizzeria, cafe and bar all in one"; "some of the best pizza in town"; breakfast "pretty decent". Address Trg Slobode bb. Website pizzeriabarok.com: DNS failure on 2026-10-12.
- IYP Cafe Sloboda: Solni Trg 10, 07:00-01:00, "The centre of social life in Tuzla". caffesloboda.ba: MySQL error page.
- IYP Mama Mia Origins: Trg slobode bb, 09:00-23:00, "might just be the best restaurant in town". mamamiaorigins.com: steak/wine page full of unrelated gambling links.
- IYP Pizza Bar: Trg žrtava genocida u Srebrenici 6, "all the classic pizzas", "The location on the main square cannot be beaten".
- IYP Limenka: Patriotske lige 24, 07:00-22:00, "grilled meat is king". limenka.ba: "Monday to Sunday 07:00 to 22:00", founded 1967.
- IYP Čaršijska Česma: Trg Žrtava srebrenice 2, 07:00-22:00, "famous throughout the city for its ćevapi, pljeskavica".
- IYP Sarajka: Džemala Bijedića 2 (other branch), 08:00-22:00, "A good old fashioned aščinica with a couple of locations across town".
- IYP Mozaik: Trgovačka 4, "A chain of primarily pizza spots around Tuzla".
- IYP House of Taste: Đorđa Mihajlovića bb, "Open 08:00 - 22:00", "Ice creams, sandwiches and salads are also available". house-of-taste.net: DNS failure.
- IYP Caffe Bar Central: Trg Slobode bb, Zgrada Barok, 07:00-23:00; Tuzlansko on tap and espresso, terrace on the main square (paraphrase).
- putujte.ba, "Gdje jesti u Tuzli", published 2025-04-08, https://putujte.ba/gdje-jesti-u-tuzli-najbolja-mjesta-za-hranu-i-kafu/. Excerpts: Pizza bar "nudi raznovrsne pizze, svježe salate i sendviče"; Barok "razne vrste pizza, sendviča, burgera i salata"; Buregdžinica Kipovi, Tabašnice 2, "širok izbor ostalih tradicionalnih pita"; Lijepa priča, Turalibegova 18, "Miris svježe pečenih palačinaka, bogat izbor nadjeva"; Čaršijska česma "razne vrste tradicionalnih bosanskih jela, popiti kafu ili bozu"; MamaMia Origins "najkvalitetnijim specijalitetima od ribe i morskih plodova". No vegetarian or vegan mentions.
- Hotel Dorrah local guide, https://sites.google.com/view/hotel-dorrah/local-guide/restaurants: Don Papa (sushi, wok, fusion), Hukić Bakery (fresh pizza), Sarajka, Palačinkara kod Bagija, Donerhana. No vegetarian mentions.
- Guest House Pasha blog, https://guest-house-pasha.hotelrunner.com/en-US/blog/restaurants-in-tuzla: MamaMia "PREMIUM restaurant, placed on the big square SLOBODA, across from Barok Building".
- Restaurant Guru JSON-LD (address, coordinates, hours): Don Papa (Trg slobode, 44.5395713, 18.6758676, 10:00-23:00), Hukić Bakery (Gradska 57, 06:00-22:00), Pekara Mućaj (Tabašnice 1, 05:00-12:00, looks unreliable), Pekara Kabil (Klosterska 40), Mozaik Pizza (Turalibegova 2, 08:00-23:00, Sun 10:00), Sarajka (Jevrejska 6, 07:00-22:00), Mamamia (4. sprat, Univerzitetska 16, Mon-Sat 08:00-21:30).
- Tourism BiH (bot check, search snippets only): Palačinkara kod Bagija "located at Patriotske lige 10"; Lijepa priča "located at Turalibegova 18"; Buregdžinica Kipovi "Tabašnice 2", "known for its delicious burek".
- fabrikacoffee.com: roaster site, no branch addresses.

## 5. Stay: sources

- Tourist Board of the City of Tuzla (official), https://tztz.ba/en/hotels/, /moteli-i-pansion/, /sobe-i-apartmani/ and the venue pages (raw/pages/hotels_*.html, sobe-i-apartmani_*.html):
  - Heartland City Hotel, Kazan mahala 10: "situated only 200 metres from the hotel" (the lakes); "Price list: Overnight stay with breakfast in a double room with a double bed – 75.00 BAM Overnight stay with breakfast in a twin room – 125.00 BAM Overnight stay with breakfast in a triple room – 155.00 BAM". Page undated (footer "Copyright© 2026").
  - Hotel Golden Star, Jevrejska 5: "provides a rich buffet breakfast, free Wi-Fi". goldenstarhotel.ba (paraphrase): breakfast included; free parking in an enclosed garage two streets away.
  - Pansion Kipovi, Franjevačka bb: "The on-site dining area is basic and serves breakfast only, offered in a buffet style."
  - Pansion Centar, Trg Stara Tržnica 8: "located in the very heart of the city, on Solni Trg".
  - Hotel Miris Dunja 88, Goli brijeg 8: "total capacity of 70 beds"; "on-site restaurant as well as a meeting and seminar hall with a capacity of up to 100 guests".
  - Hotel Mellain, Aleja Alije Izetbegovića br. 3: "130 luxuriously furnished and spacious rooms"; "swimming pool with saunas, a fitness centre".
  - Hotel Tuzla: "comprises 12 floors"; "a 25-metre indoor swimming pool". No address on page; Nominatim puts OSM building "Hotel Tuzla" on ZAVNOBiH-a.
  - So i Sol Hotel, Obala Zmaja od Bosne (prije broja 24): "7 modern equipped rooms"; "The price of the bed and breakfast service includes tourist tax, insurance, parking and VAT."
  - Prenoćište Stari Grad, Franjevačka 4: "single, double, triple, quadruple, and quintuple rooms"; "large shared terrace".
  - Apartman Tabašnice, Tabašnice 19: "three accommodation units with 4, 3, and 2 beds"; "parking, and access to a shared kitchen".
  - Banja Residence Apt.: "approximately 30 m², ideal for 2 to 4 guests"; "private garage".
- Kayak:
  - Hotel Vertigos, https://www.es.kayak.com/Tuzla-Hoteles-Hotel-Vertigos.7520733.ksp: "2 Kulina bana Tuzla"; lowest "$54" "por noche con tasas", deluxe room, dates "lun. 19/10" to "mar. 20/10", 2 guests; "Hotel Vertigos ofrece estacionamiento gratis".
  - Pansion Kipovi, https://www.kayak.com/Tuzla-Hotels-Pansion-Kipovi.3555297.ksp: "Franjevacka 10, Tuzla 75000"; "9.1" from "407 reviews"; "$42" "nightly with fees", Deluxe room, Mon 10/19 to Tue 10/20, 2 guests.
  - Tuzla hotels, https://www.kayak.com/Tuzla-Hotels.23605.hotel.ksp: Heartland City Hotel "$100+", Hotel Mellain "$186+", "best prices for Oct 10 - 11"; "April is the most expensive month, with prices at $151/night." (a separate search snippet said May at $148, so the seasonal figures vary).
  - Hotel Miris Dunja 88: "Goli brijeg 8", rating "8,7", no price shown.
- hotelvertigos.com: "Kulina Bana 2"; breakfast options (continental, Bosnian traditional, etc.); "Ponedjeljak - Nedjelja 00-24h".
- Hotel Soni Lux (search snippets from Kayak, routard/Booking white-label, 2023 UNTZ accommodation PDF which returned HTTP 530 when fetched): "8 Kulina bana", "A buffet breakfast is available each morning", "free private parking with video surveillance".
- Hotel Tuzla / Grand Hotel Tuzla (search snippets: priceline, mappy): "Zavno BiH-a 13, 75000 Tuzla"; one listing says 43 rooms. Conflicts with the tourist board's 12-floor, 220+ room description.
- Pansion Centar Booking.com page: redirect, then empty content. Snippet only: free parking, breakfast buffet, lakes about 200 m.
- Not confirmed and left out: "Panonska oaza" (OSM hotel at Džindić mahala 19, no web evidence found); Hotel Dorrah (University hotel, Mitra Trifunovića Uče, about 2 km+ west, not geocoded).
