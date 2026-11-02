---
url: https://zrs-rs.com/red-voznje
pulled: 2026-11-02
fetched_via: The ŽRS site only renders in a browser (Blazor), so the agent drove it with Playwright, filled the homepage's "Red vožnje" search (Jedan smijer; Početna stanica, Krajnja stanica, Datum polaska 04.11.2026) and copied the result text verbatim. The fare PDF was fetched with curl and read with pdftotext.
source_kind: official-site
title: "ŽRS (Railways of Republika Srpska): passenger trains Banja Luka to Doboj and back, and the fare, read 2026-11-02"
---

Read on 2026-11-02 after the organiser asked whether the Banja Luka train leaves in the morning or the afternoon, and whether it is a passenger train (sources/conversations/2026-11-02--org--banja-luka-train-two-a-day.md). This corrects the "1 polazak dnevno" of the aggregator quoted in sources/web/travel/trains-to-tuzla-2026-11-02.md.

## https://zrs-rs.com/red-voznje, Banja Luka to Doboj, Datum polaska : 04.11.2026

Pocetna stanica | Vrijeme polaska | Krajnja stanica | Vrijeme dolaska
Banja Luka | 04:32 | Doboj | 06:38
Banja Luka | 15:38 | Doboj | 17:45

## https://zrs-rs.com/red-voznje, Doboj to Banja Luka, Datum polaska : 04.11.2026

Pocetna stanica | Vrijeme polaska | Krajnja stanica | Vrijeme dolaska
Doboj | 04:15 | Banja Luka | 06:18
Doboj | 15:30 | Banja Luka | 17:27

## https://zrs-rs.com/putnicki-saobracaj/opsti-uslovi (ŽRS, "PUTNIČKI SAOBRAĆAJ")

The section lists: Opšti uslovi, Cijene, Cijene po relacijama, Specijalne ponude, Knjiga žalbi, Daljinar putnički saobraćaj.
IZVOD IZ OPŠTIH USLOVA ZA PREVOZ PUTNIKA U UNUTRAŠNJEM SAOBRAĆAJU
Napomena: Svi podaci su informativnog karaktera, a za uslove prevoza i cijene važe odredbe objavljene u tarifama ŽRS.

## https://zrs-rs.com/files/putnicki_saobracaj/Cijene%20po%20relacijama.pdf (ŽRS passenger fares by route, "konv. markama")

Row "B.Luka", column "Doboj": 10,40
Row "Doboj", column "B.Luka": 10,40

## Agent's notes

- The search sits on ŽRS's own site next to its passenger fares and conditions of carriage; ŽRS publishes no freight times there. The agent reads both trains as passenger trains, which the fare table supports.
- The timetable shown is the 2025/2026 one, valid from 14 December 2025 to 12 December 2026 (search-engine extracts of the ŽRS announcement, 2026-11-02; not fetched). June 2027 falls under the next timetable, which is (unknown, needs source).
- Doboj to Tuzla buses, by redvoznje.ba (sources/web/travel/trains-to-tuzla-2026-11-02.md): 00:17 to 01:28, 12:25 to 14:12, 13:10 to 14:57, 18:25 to 19:45. The 15:38 train (Doboj 17:45) meets the 18:25 bus (Tuzla 19:45): about 4 hours 10 minutes from Banja Luka. The 04:32 train (Doboj 06:38) waits until 12:25 for the next listed bus.
