---
url: https://balkantransfer.com/api/public/destinations/all?langCode=en
pulled: 2026-11-02
fetched_via: The booking form on balkantransfer.com fills its "From" and "To" lists from a public JSON API (seen in the browser with Playwright); the agent then read the same API with curl. Names and prices verbatim from the JSON; the agent's summary of each list below.
source_kind: vendor-site
title: "Balkan Transfer: which routes its booking form offers to and from Tuzla, and the listed prices, read 2026-11-02"
---

Read on 2026-11-02 after the organiser asked whether people can use services such as Balkan Transfer (sources/conversations/2026-11-02--org--balkan-transfer-routes.md).

## Destination ids (https://balkantransfer.com/api/public/destinations/all?langCode=en)

53 "Banja Luka Airport (BNX)" (is_airport true); 54 "Tuzla Airport (TZL)" (is_airport true); 55 "Sarajevo Airport (SJJ)" (is_airport true); 35 "Banja Luka"; 31 "Doboj"; 23 "Tuzla"; 22 "Živinice"; 56 "Sarajevo". 71 destinations in all.

## Where each place's "To" list goes (https://balkantransfer.com/api/public/destinations/{id}/to?langCode=en)

- From 55 Sarajevo Airport (SJJ): Banja Luka, Blagaj, Čapljina, Doboj, Gračanica, Gradačac, Jablanica, Jelah, Kakanj, Kladanj, Konjic, Ljubuški, Lukavac, Maglaj, Medjugorje, Mostar, Nemila, Olovo, Široki Brijeg, Srebrenik, Stolac, Tešanj, Teslić, Tuzla, Zenica, Žepče, Živinice
- From 23 Tuzla: Sarajevo Airport (SJJ), Sarajevo
- From 54 Tuzla Airport (TZL): Kladanj, Olovo, Sarajevo
- From 53 Banja Luka Airport (BNX): Doboj, Ilijaš, Kakanj, Maglaj, Nemila, Sarajevo, Visoko, Zenica, Žepče
- From 35 Banja Luka: Sarajevo Airport (SJJ), Sarajevo
- From 31 Doboj: Banja Luka Airport (BNX), Sarajevo Airport (SJJ), Sarajevo
- From 22 Živinice: Sarajevo Airport (SJJ), Sarajevo

## Listed prices (https://balkantransfer.com/api/public/transfers/popular-articles?currency=EUR&langCode=en&limit=100), entries naming Tuzla, Banja Luka or Doboj

- "from_name":"Tuzla Airport (TZL)","to_name":"Sarajevo","article_price":"17","article_travel_time":"120","currency":"EUR"
- "from_name":"Sarajevo Airport (SJJ)","to_name":"Tuzla","article_price":"19","article_travel_time":"124","currency":"EUR"
- "from_name":"Doboj","to_name":"Tuzla Airport (TZL)","article_price":"21","article_travel_time":"90","currency":"EUR"
- "from_name":"Banja Luka","to_name":"Tuzla Airport (TZL)","article_price":"23","article_travel_time":"165","currency":"EUR"

## Agent's notes

- Balkan Transfer takes people from Sarajevo airport to Tuzla and from Tuzla back to Sarajevo airport, listed from 19 EUR, about 2 hours. It offers no route from Tuzla airport into Tuzla and none from Banja Luka airport to Tuzla.
- The Doboj and Banja Luka to Tuzla airport articles have pages and prices, but neither place's live "To" list offers Tuzla airport on 2026-11-02, so the agent treats them as not bookable now.
- The price is the article's "from" price per seat in a shared van; the real price shows only in the booking form for a date, which the agent did not use.
