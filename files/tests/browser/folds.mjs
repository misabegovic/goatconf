// The home page's sections that open and close, in a real browser (DESIGN.md, "Sections and lists that open and
// close"; sources/conversations/2026-11-22--org--every-section-collapsible-and-remembered.md): what a first visit
// shows, that the page's script finishes whatever is remembered, that a choice is kept across a reload, that a link
// opens what it lands in, and that the page is whole with storage blocked, with the script file missing and with
// script off.
//
//   python3 -m http.server 8765 --directory site &                      (from files/)
//   <chromium> --headless --remote-debugging-port=9222 about:blank &
//   node tests/browser/folds.mjs <the browser's ws:// address> http://127.0.0.1:8765
//
// It needs a Chromium and Node 22 or later (for WebSocket), so it is not part of the local CI; run it before shipping
// a change to the folds in site/album.js, tools/nav.py or the home page's sections. It talks to the browser's
// developer protocol directly and needs no package.
const [url, BASE = "http://127.0.0.1:8765"] = process.argv.slice(2);
if (!url) { console.error("usage: node tests/browser/folds.mjs <ws address of the browser> [base address of the site]"); process.exit(2); }
const ws = new WebSocket(url);
let id = 0, failed = 0;
const wait = new Map(), events = [];
const send = (method, params = {}, sessionId) => new Promise((res, rej) => { const i = ++id; wait.set(i, [res, rej]); ws.send(JSON.stringify({ id: i, method, params, sessionId })); });
ws.onmessage = (m) => {
  const d = JSON.parse(m.data);
  if (d.id && wait.has(d.id)) { const [res, rej] = wait.get(d.id); wait.delete(d.id); if (d.error) rej(new Error(d.error.message)); else res(d.result); } else if (d.method) events.push(d);
};
await new Promise((r) => { ws.onopen = r; });
const { targetInfos } = await send("Target.getTargets");
const { sessionId } = await send("Target.attachToTarget", { targetId: targetInfos.find((t) => t.type === "page").targetId, flatten: true });
const S = (m, p) => send(m, p, sessionId);
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const ev = async (expr) => { const r = await S("Runtime.evaluate", { expression: expr, returnByValue: true }); return r.exceptionDetails ? "EXCEPTION" : r.result.value; };
const check = (ok, what) => { console.log(`${ok ? "ok  " : "FAIL"} ${what}`); if (!ok) failed += 1; };
await S("Page.enable"); await S("Runtime.enable"); await S("Network.enable");
await S("Emulation.setFocusEmulationEnabled", { enabled: true }); await S("Page.bringToFront");
await S("Emulation.setDeviceMetricsOverride", { width: 390, height: 844, deviceScaleFactor: 1, mobile: false });
const nav = async (path, settle = 900) => {
  await S("Page.navigate", { url: "about:blank" }); await sleep(150);
  const n = events.length;
  await S("Page.navigate", { url: `${BASE}/${path}` });
  for (let i = 0; i < 80 && !events.slice(n).some((e) => e.method === "Page.loadEventFired"); i++) await sleep(100);
  await sleep(settle);
};
const errors = () => events.filter((e) => e.method === "Runtime.exceptionThrown").length;
const remember = (state) => ev(`localStorage.setItem("folds", JSON.stringify({ index: ${JSON.stringify(state)} })); 1`);
const forget = () => ev(`localStorage.removeItem("folds"); 1`);
const closed = () => ev(`[...document.querySelectorAll("[data-folds] > section.is-closed")].map((s) => s.id).join(",")`);
const alive = () => ev(`document.documentElement.classList.contains("folds-on") && document.documentElement.classList.contains("folds-ready") && document.querySelectorAll(".sec__toggle").length`);
const FOLDING = ["days", "speakers", "tuzla", "food", "talk", "add", "money", "the-goat", "conduct", "goatchi"];
const START_CLOSED = FOLDING;
const shut = Object.fromEntries(FOLDING.map((s) => [s, "closed"]));

await nav("index.html"); await forget(); await nav("index.html");
check(await closed() === START_CLOSED.join(","), "a first visit has every section that opens and closes closed, the speakers too");
check(await alive() === FOLDING.length, "every section that closes has its button; the hero and the free ticket have none");
check(await ev(`!document.querySelector("#ticket .sec__toggle") && !document.querySelector(".spread .sec__toggle") && !document.querySelector("#see-you .sec__toggle")`), "the hero, the free ticket and See you in Tuzla have no control");

// Whatever is remembered, the page's script runs to its end (it once stopped when the first section was remembered open).
for (const state of [{ days: "open" }, { days: "open", speakers: "closed" }, Object.fromEntries(FOLDING.map((s) => [s, "open"])), shut, { "see-you": "open" }, { days: "nonsense", nothing: "open" }]) {
  await remember(state); await nav("index.html");
  const want = FOLDING.filter((s) => (state[s] === "open" || state[s] === "closed" ? state[s] === "closed" : START_CLOSED.includes(s))).join(",");
  check(await alive() === FOLDING.length && await closed() === want, `remembered ${JSON.stringify(state).slice(0, 60)}: the script finishes and the page shows it`);
}
await ev(`localStorage.setItem("folds", "not json"); 1`); await nav("index.html");
check(await alive() === FOLDING.length && await closed() === START_CLOSED.join(","), "a damaged record gives the first-visit page");

await forget(); await nav("index.html");
await ev(`document.querySelector("#days-title .sec__toggle").click(); document.querySelector("#speakers-title .sec__toggle").click(); 1`);
await ev(`document.querySelector("#tuzla-title .sec__toggle").click(); document.querySelector("#tuzla-title .sec__toggle").click(); 1`);
check(await ev(`localStorage.getItem("folds")`) === JSON.stringify({ index: { days: "open", speakers: "open", tuzla: "closed" } }), "a press is kept under the key folds, one entry a page");
check(await ev(`document.querySelector("#days-title .sec__toggle").getAttribute("aria-expanded") + document.querySelector("#speakers-title .sec__toggle").getAttribute("aria-expanded") + document.querySelector("#tuzla-title .sec__toggle").getAttribute("aria-expanded")`) === "truetruefalse", "the button says whether its section is open");
await nav("index.html");
check(!(await closed()).split(",").includes("days") && !(await closed()).split(",").includes("speakers") && (await closed()).split(",").includes("tuzla"), "the choice is there after a reload");
await ev(`document.querySelector("#days [data-fold-end]").focus(); document.querySelector("#days [data-fold-end]").click(); 1`);
check((await closed()).split(",").includes("days") && await ev(`document.activeElement === document.querySelector("#days-title .sec__toggle") && JSON.parse(localStorage.getItem("folds")).index.days`) === "closed", "Show less at a section's end closes it, remembers it and puts the keyboard on its heading");
check(await ev(`document.querySelectorAll("[data-fold-end]").length`) === FOLDING.length, "every section that closes ends with Show less; the hero, the free ticket and See you in Tuzla have none");
await ev(`document.querySelector("[data-folds-all]").click(); 1`);
check(await closed() === "" && await ev(`document.querySelector("[data-folds-all]").textContent`) === "Close all sections", "Open all sections opens every one and then offers to close them");
await ev(`document.querySelector("[data-folds-all]").click(); 1`);
check(await closed() === FOLDING.join(","), "Close all sections closes every one");

// A link opens what it lands in and does not change what is remembered.
await remember(shut);
const ids = await ev(`[...document.querySelectorAll("[data-folds] > section[id], [data-folds] > section [id]")].map((e) => e.id).filter((i) => !/^theme-/.test(i)).join(",")`);
for (const target of ids.split(",")) {
  await nav(`index.html#${target}`, 300);
  const ok = await ev(`(() => { const t = document.getElementById(${JSON.stringify(target)}); const s = t.closest("[data-folds] > section"); return !s.classList.contains("is-closed") && !t.closest("[data-fold-part][hidden]") && JSON.parse(localStorage.getItem("folds")).index[s.id] !== "open"; })()`);
  check(ok === true, `a link to #${target} opens its section and remembers nothing`);
}
await nav("index.html#:~:text=Reports%20are%20confidential", 1200);
check(!(await closed()).split(",").includes("conduct"), "a link to a sentence inside a closed section opens it (where the browser can)");

// The goat and the rows (sources/conversations/2026-11-22--org--meals-section-weird-when-collapsed.md): a closed row
// holds still whatever the goat does, the goat has one place of one size on every row, a press on the goat and a
// press on the heading do not set each other off, and no goat is inside a closed section.
await forget(); await remember(shut); await nav("index.html");
await ev(`document.documentElement.style.scrollBehavior = "auto"; window.__shift = 0; new PerformanceObserver((l) => { for (const e of l.getEntries()) if (!e.hadRecentInput) window.__shift += e.value; }).observe({ type: "layout-shift" }); 1`);
const boxes = new Set(); let moved = 0, absent = 0, inside = 0;
// The section goats at a size that reads and never cut, nor what they say
// (sources/conversations/2026-11-22--org--section-goats-too-small-and-cut-off.md): whether the goat or its open speech
// bubble is clipped by anything it stands in, lies under the sticky top bar or leaves the window, and how wide it is.
const whole = `(() => { const st = document.querySelector(".goat-one__stage"), say = st.querySelector(".goat-say"), bar = document.querySelector(".topbar").getBoundingClientRect().bottom;
  const cut = (e) => { const b = e.getBoundingClientRect(); if (b.top < bar - 0.5 || b.left < 0 || b.right > document.documentElement.clientWidth) return true;
    for (let a = st.parentElement; a && a !== document.documentElement; a = a.parentElement) { const c = getComputedStyle(a), r = a.getBoundingClientRect(); if ((/hidden|clip|auto|scroll/.test(c.overflowX + c.overflowY) || c.clipPath !== "none") && (b.left < r.left - 0.5 || b.top < r.top - 0.5 || b.right > r.right + 0.5 || b.bottom > r.bottom + 0.5)) return true; } return false; };
  const said = parseFloat(getComputedStyle(say).opacity) > 0.5; const range = document.createRange(); range.selectNodeContents(say);
  return { on: st.parentElement.id, goat: cut(st.querySelector(".goat")), said, say: said && cut(say), lines: new Set([...range.getClientRects()].map((r) => Math.round(r.top))).size, width: Math.round(st.getBoundingClientRect().width) }; })()`;
// A press is a trick, and every second trick says a line: it is pressed until it speaks, five times at most, each
// press given the time of the longest trick.
// It is pressed only where it stands: while it flies to a row or ducks behind the edge the press would land on what
// is under it, a heading or a strip of pictures, and that would open a section.
const steady = async () => {
  const where = () => ev(`(() => { const st = document.querySelector(".goat-one__stage"), g = st.querySelector(".goat").getBoundingClientRect(), s = st.parentElement.getBoundingClientRect(); return Math.abs(g.bottom - s.top) < g.height * 0.25 && !st.classList.contains("is-tucked") ? [Math.round(g.left), Math.round(g.top)].join() : ""; })()`);
  for (let i = 0, last = "x"; i < 40; i++) { const now = await where(); if (now && now === last) return true; last = now; await sleep(120); }
  return false;
};
const press = async () => {
  for (let n = 0; n < 5; n++) {
    if (!await steady()) continue;
    await mouse(".goat-one__stage .goat-hit", 0.5, 0.5, true);
    for (let i = 0; i < 24; i++) { await sleep(100); const now = await ev(whole); if (now.said || now.goat) return now; }
  }
  return ev(whole);
};
const arrived = async (sid) => { for (let i = 0; i < 40; i++) { if (await ev(`(() => { const st = document.querySelector(".goat-one__stage"); return !!st && !!st.parentElement && st.parentElement.id === "${sid}"; })()`)) break; await sleep(100); } await sleep(1000); };
// A goat overlays what is above it, and a press on the goat is the goat's alone
// (sources/conversations/2026-11-22--org--goats-overlay-no-empty-room.md): what the page's address, its closed sections
// and its stored state are, to compare around a press; and, of the links, buttons, heading controls and linked cards
// the goat's picture lies over, how many have no point left that still takes a press.
const state = () => ev(`location.href + "|" + [...document.querySelectorAll("[data-folds] > section.is-closed")].map((s) => s.id).join(",") + "|" + localStorage.getItem("folds")`);
const beneath = `(() => { const st = document.querySelector(".goat-one__stage"), hit = st.querySelector(".goat-hit") || st.querySelector(".goat"), g = hit.getBoundingClientRect(); let over = 0, lost = 0;
  for (const el of document.querySelectorAll("main a, main button")) { if (st.contains(el) || !el.getClientRects().length || el.closest("[hidden]")) continue; const r = el.getBoundingClientRect();
    if (r.right <= g.left || r.left >= g.right || r.bottom <= g.top || r.top >= g.bottom) continue; over += 1; let free = false;
    for (let i = 1; i < 12 && !free; i++) for (let j = 1; j < 6 && !free; j++) { const x = r.left + r.width * i / 12, y = r.top + r.height * j / 6; if (y < 0 || y > innerHeight) continue; const t = document.elementFromPoint(x, y); free = !!t && !st.contains(t) && (t === el || el.contains(t) || !!t.closest("a, button") && t.closest("a, button") === el); }
    if (!free) lost += 1; }
  return { over, lost }; })()`;
let cutGoats = 0, cutWords = 0, mute = 0, small = 0, leaks = 0, overlaid = 0, unreachable = 0;
const look = async (sid, pressed = true) => {
  const at = await ev(whole);
  if (at.on !== sid || at.goat) cutGoats += 1;
  if (at.width < 80) small += 1;
  if (!pressed) return;
  await steady();
  const below = await ev(beneath); overlaid += below.over; unreachable += below.lost;
  const before = await state();
  const after = await press();
  if (before !== await state()) leaks += 1;
  if (!after.said) mute += 1; else if (after.say || after.goat || after.lines > 2) cutWords += 1;
  await sleep(900);
};
const point = (sel, fx = 0.5, fy = 0.5) => ev(`(() => { const r = document.querySelector(${JSON.stringify(sel)}).getBoundingClientRect(); return [Math.round(r.left + r.width * ${fx}), Math.round(r.top + r.height * ${fy})]; })()`);
const mouse = async (sel, fx, fy, press = false) => { const [x, y] = await point(sel, fx, fy); await S("Input.dispatchMouseEvent", { type: "mouseMoved", x, y }); if (press) for (const type of ["mousePressed", "mouseReleased"]) await S("Input.dispatchMouseEvent", { type, x, y, button: "left", clickCount: 1 }); };
for (const sid of FOLDING) {
  const tall = () => ev(`[document.getElementById("${sid}"), document.querySelector("#${sid} h2"), document.querySelector("#${sid} .sec__peek")].map((e) => Math.round(e.getBoundingClientRect().height * 10) / 10).join("/")`);
  await ev(`window.scrollTo(0, document.getElementById("${sid}").getBoundingClientRect().top + scrollY - innerHeight * 0.45); 1`); await sleep(500);
  const first = await tall();
  await S("Input.dispatchMouseEvent", { type: "mouseMoved", x: 5, y: 5 }); await mouse(`#${sid} h2`, 0.5, 0.5); await sleep(1800);
  const g = await ev(`(() => { const st = document.querySelector(".goat-one__stage"), s = st && st.parentElement; if (!s || s.id !== "${sid}") return null; const r = st.getBoundingClientRect(), b = s.getBoundingClientRect(); return [Math.round(r.width), Math.round(b.right - r.right), Math.round(r.bottom - b.top)].join(","); })()`);
  if (!g) absent += 1; else { boxes.add(g); await look(sid); }
  if (first !== await tall()) moved += 1;
  if (await ev(`!!document.querySelector("[data-fold-part][hidden] .goat-one__stage, .is-closed h2 .goat-one__stage")`)) inside += 1;
}
check(moved === 0, "no closed row, heading or line on it changes size as the goat arrives and leaves");
check(await ev(`window.__shift`) === 0, "no layout shift on the closed page while the goat goes from row to row");
check(absent === 0 && boxes.size === 1, `the goat stands on every closed row in one place of one size (${[...boxes].join(" | ")}${absent ? `; ${absent} rows without it` : ""})`);
check(inside === 0, "the goat is never inside a closed section");
check(small === 0, "the goat on a section is as wide as the goat on a slot of the cover, 80 pixels or more");
check(cutGoats === 0 && cutWords === 0 && mute === 0, `pressed on each closed row, the goat and what it says are whole: not clipped, not under the top bar, inside the window, on two lines at most (${cutGoats} goats cut, ${cutWords} bubbles cut, ${mute} said nothing)`);
check(await ev(`window.__shift`) === 0, "no layout shift on the closed page while a goat does its trick and says its line");
check(leaks === 0 && unreachable === 0, `a press on a closed row's goat follows no link, opens no section and stores nothing, and each of the ${overlaid} links and buttons its picture lies over can still be pressed beside it (${leaks} presses leaked, ${unreachable} out of reach)`);
await ev(`window.scrollTo(0, document.getElementById("food").getBoundingClientRect().top + scrollY - innerHeight * 0.45); 1`); await sleep(400);
await mouse("#food h2", 0.5, 0.5); await sleep(1800); await steady();
await mouse(".goat-one__stage .goat-hit", 0.5, 0.5, true); await sleep(700);
check((await closed()).split(",").includes("food") && await ev(`document.querySelector(".goat-one__stage").parentElement.id`) === "food", "a press on the row's goat is for the goat: the section stays closed");
await sleep(3200);
// What the goat does is counted in the page, in the 200 milliseconds after the press lands, so a slow answer from
// the browser cannot stretch that time into the goat's next move of its own (it picks its stop again 250
// milliseconds after a section opens).
await ev(`window.__moves = 0; window.__pressAt = 0; const animate = Element.prototype.animate; Element.prototype.animate = function (...a) { if (this.closest && this.closest(".goat-one__stage") && (!window.__pressAt || performance.now() - window.__pressAt < 200)) window.__moves += 1; return animate.apply(this, a); }; 1`);
// The heading is pressed directly under the goat, the nearest a press on a heading comes to it, with the pointer
// already at rest there and the press sent alone, with no move before it. A goat turns its head towards a pointer
// that moves to one side of it, which is its answer to the pointer and never to a press; straight under it there is
// no side to turn to, so anything the goat does after the press is the press's doing, and nothing is excused.
const [hx, hy] = await ev(`(() => { const g = document.querySelector(".goat-one__stage").getBoundingClientRect(), h = document.querySelector("#food-title .sec__toggle").getBoundingClientRect(); return [Math.round(g.left + g.width / 2), Math.round(h.top + h.height / 2)]; })()`);
await S("Input.dispatchMouseEvent", { type: "mouseMoved", x: hx, y: hy }); await sleep(1500);
await ev(`window.__moves = 0; document.addEventListener("pointerdown", () => { window.__pressAt = performance.now(); }, { capture: true, once: true }); 1`);
for (const type of ["mousePressed", "mouseReleased"]) await S("Input.dispatchMouseEvent", { type, x: hx, y: hy, button: "left", clickCount: 1 });
await sleep(450);
check(!(await closed()).split(",").includes("food") && await ev(`window.__pressAt > 0 && window.__moves`) === 0, "a press on the heading opens the section and does not set the goat off");
await sleep(900);
check(await ev(`(() => { const st = document.querySelector(".goat-one__stage"); if (st.parentElement.id !== "food") return true; const r = st.getBoundingClientRect(); return Math.abs(r.bottom - document.getElementById("food").getBoundingClientRect().top) < r.height * 0.2; })()`), "the section's own goat stays on the section's top edge when the section opens");
check(await ev(`document.querySelectorAll("[data-folds] details").length === 0 && document.getElementById("food-dishes").getClientRects().length > 0 && document.querySelectorAll("#food-dishes img").length >= 12`), "opening a section opens all of it: the twelve dishes are there, with no second fold");
await ev(`document.querySelector("#food-title .sec__toggle").click(); 1`); await sleep(1800);
check(await ev(`!document.querySelector("[data-fold-part][hidden] .goat-one__stage")`), "a goat inside a section that closes does not stay inside it");
await ev(`document.querySelector("#tuzla .sec__strip img").click(); 1`); await sleep(300);
check(!(await closed()).split(",").includes("tuzla") && await ev(`JSON.parse(localStorage.getItem("folds")).index.tuzla`) === "open", "a press on a closed row's strip of pictures opens the section");
check(await ev(`!document.querySelector("#see-you .sec__toggle") && !document.querySelector("#see-you [data-fold-end]") && !document.getElementById("see-you").classList.contains("is-closed")`), "See you in Tuzla has no control and is open whatever is remembered");
// The same with every section open, where the section's own page used to cut the goat standing on its top edge, and
// on a wide screen.
const everyOpen = Object.fromEntries(FOLDING.map((s) => [s, "open"]));
for (const [width, height, folds] of [[390, 844, everyOpen], [1440, 900, everyOpen], [1440, 900, shut]]) {
  await S("Emulation.setDeviceMetricsOverride", { width, height, deviceScaleFactor: 1, mobile: false });
  await forget(); await remember(folds); await nav("index.html");
  await ev(`document.documentElement.style.scrollBehavior = "auto"; 1`);
  cutGoats = cutWords = mute = small = leaks = overlaid = unreachable = 0;
  for (const sid of FOLDING) {
    await ev(`window.scrollTo(0, document.getElementById("${sid}").getBoundingClientRect().top + scrollY - innerHeight * 0.45); 1`); await sleep(400);
    await S("Input.dispatchMouseEvent", { type: "mouseMoved", x: 5, y: 5 }); await mouse(`#${sid} h2`, 0.5, 0.5); await sleep(1800); await arrived(sid);
    await look(sid);
  }
  check(cutGoats === 0 && cutWords === 0 && mute === 0 && small === 0, `at ${width} wide with every section ${folds === shut ? "closed" : "open"}, each section's goat and what it says are whole and the goat is 80 pixels wide or more (${cutGoats} goats cut, ${cutWords} bubbles cut, ${mute} said nothing, ${small} small)`);
  check(leaks === 0 && unreachable === 0, `at ${width} wide with every section ${folds === shut ? "closed" : "open"}, a press on a section's goat reaches nothing under it, and the ${overlaid} links and buttons under its picture can still be pressed (${leaks} leaked, ${unreachable} out of reach)`);
}
// Every goat on a top edge at its own size at the right end
// (sources/conversations/2026-11-22--org--goats-overlay-no-empty-room.md,
// sources/conversations/2026-11-22--org--speaker-goats-on-the-left-and-smaller.md): with everything open, the page's
// own rule seats every slot's goat at 100 percent at the right end, on every page that has slots and at five widths;
// a seat moved along the edge so a small link keeps 44 pixels to press is named. Then, visited one by one on a phone,
// the eight speakers' goats: each speaker's own, drawn at its own size at the right end, clear of every face, a press
// on it opening no card, and the card it stands over still pressed beside it.
const nudged = [];
for (const [width, height] of [[320, 700], [390, 844], [768, 900], [1024, 900], [1440, 900]]) {
  await S("Emulation.setDeviceMetricsOverride", { width, height, deviceScaleFactor: 1, mobile: false });
  let slotsSeen = 0; const off = [];
  for (const page of ["index.html", "speakers.html", "extend.html", "talk.html", "organising.html"]) {
    // The host page's sections fold too in the proposal: its slots are measured with every one of them open.
    await forget(); await ev(`localStorage.setItem("folds", JSON.stringify({ index: ${JSON.stringify(everyOpen)}, extend: { adding: "open", what: "open", where: "open", propose: "open" } })); 1`); await nav(page, 1200);
    const seats = JSON.parse(await ev(`JSON.stringify(window.goatSeats ? window.goatSeats() : [])`));
    slotsSeen += seats.length;
    for (const [goat, seat] of seats) { if (seat !== "own" && !seat.startsWith("1R")) off.push(`${page} ${goat} ${seat}`); if (seat.includes("moved")) nudged.push(`${width} ${page} ${goat} ${seat}`); }
    if (page === "index.html" || page === "speakers.html") { const faces = seats.filter(([goat]) => goat.startsWith("speaker-")); if (faces.length !== 8 || new Set(faces.map(([goat]) => goat)).size !== 8) off.push(`${page}: ${faces.length} speakers' goats`); }
  }
  check(slotsSeen > 40 && off.length === 0, `at ${width} wide every one of the ${slotsSeen} goats on a slot's top edge stands at its own size at the right end, each speaker with their own (${off.join(", ") || "none off"})`);
}
console.log(`     seats moved along the edge to leave a link 44 pixels: ${nudged.join("; ") || "none"}`);
await S("Emulation.setDeviceMetricsOverride", { width: 390, height: 844, deviceScaleFactor: 1, mobile: false });
await forget(); await remember(everyOpen); await nav("index.html");
await ev(`document.documentElement.style.scrollBehavior = "auto"; 1`);
const drawn = new Set(); let strangers = 0, faces = 0; leaks = overlaid = unreachable = 0;
const cards = await ev(`document.querySelectorAll("#speakers .sticker--speaker").length`);
for (let i = 0; i < cards; i++) {
  await ev(`(() => { const c = document.querySelectorAll("#speakers .sticker--speaker")[${i}]; window.scrollTo(0, c.getBoundingClientRect().top + scrollY - innerHeight * 0.45); })(); 1`); await sleep(400);
  await S("Input.dispatchMouseEvent", { type: "mouseMoved", x: 5, y: 5 });
  const [x, y] = await ev(`(() => { const r = document.querySelectorAll("#speakers .sticker--speaker")[${i}].getBoundingClientRect(); return [Math.round(r.left + r.width / 2), Math.round(r.top + r.height / 2)]; })()`);
  await S("Input.dispatchMouseEvent", { type: "mouseMoved", x, y }); await sleep(2200);
  const seen = await ev(`(() => { const st = document.querySelector(".goat-one__stage"), c = document.querySelectorAll("#speakers .sticker--speaker")[${i}]; if (st.parentElement !== c) return null; const own = c.querySelector(".peek"), g = st.getBoundingClientRect(), b = c.getBoundingClientRect(); const face = [...document.querySelectorAll("#speakers .sticker--speaker img")].some((im) => { if (c.contains(im)) return false; const r = im.getBoundingClientRect(); return r.left < g.right && r.right > g.left && r.top < g.bottom && r.bottom > g.top; }); return { same: st.querySelector(".goat").dataset.goat === own.dataset.goat, part: Math.round(g.width / parseFloat(getComputedStyle(own).width) * 100), end: Math.round(b.right - g.right), face }; })()`);
  if (seen && seen.face) faces += 1;
  if (seen) { await steady(); const below = await ev(beneath); overlaid += below.over; unreachable += below.lost; const before = await state(); await mouse(".goat-one__stage .goat-hit", 0.5, 0.5, true); await sleep(500); if (before !== await state()) leaks += 1; }
  // A card is tilted a degree or two, so the goat's box reads a few pixels wider than it is drawn and its distance
  // from the card's corner a few pixels either way: own size is within a twentieth, the right end within 2rem.
  if (!seen || !seen.same) strangers += 1; else drawn.add(`${Math.abs(seen.part - 100) <= 5 ? "its own size" : `${seen.part}%`} at the ${seen.end >= 0 && seen.end <= 32 ? "right" : `other (${seen.end}px)`} end`);
}
check(cards === 8 && strangers === 0 && drawn.size === 1 && [...drawn][0] === "its own size at the right end", `visited one by one on a phone, every speaker's card has that speaker's own goat at its own size and at the same end (${[...drawn].join(" | ")}${strangers ? `; ${strangers} cards without their goat` : ""})`);
check(faces === 0, "no speaker's goat lies over the photo of another speaker");
check(leaks === 0 && unreachable === 0, `a press on a speaker's goat opens no card and stores nothing, and the ${overlaid} cards and links under the goats' pictures can still be pressed beside them (${leaks} leaked, ${unreachable} out of reach)`);
// A row just under the sticky top bar is not a stop: the goat is never called where its head would be under the bar.
await forget(); await remember(shut); await nav("index.html");
await ev(`document.documentElement.style.scrollBehavior = "auto"; 1`);
let under = 0;
for (const sid of ["tuzla", "add", "conduct"]) {
  await ev(`window.scrollTo(0, document.getElementById("${sid}").getBoundingClientRect().top + scrollY - document.querySelector(".topbar").getBoundingClientRect().bottom - 30); 1`); await sleep(1900);
  if (await ev(`(() => { const st = document.querySelector(".goat-one__stage"); if (getComputedStyle(st).visibility === "hidden" || !st.parentElement) return false; return st.querySelector(".goat").getBoundingClientRect().top < document.querySelector(".topbar").getBoundingClientRect().bottom - 0.5 && st.getBoundingClientRect().bottom > 0; })()`)) under += 1;
}
check(under === 0, "when the page comes to rest with a row just under the top bar, the goat is not left under the bar");
const tops = [];
for (const target of ["days", "food", "the-goat", "conduct", "ticket"]) { await nav(`index.html#${target}`, 1600); tops.push(await ev(`Math.round(document.getElementById("${target}").getBoundingClientRect().top)`)); }
check(Math.max(...tops) - Math.min(...tops) <= 1, `a link to any section lands at one distance from the top, to the pixel's rounding (${tops.join(", ")})`);
// The phone menu on a phone held sideways, and the theme control in the footer.
await S("Emulation.setDeviceMetricsOverride", { width: 667, height: 375, deviceScaleFactor: 1, mobile: false }); await nav("index.html");
await ev(`document.querySelector(".topbar__phone summary, .topbar__phone [aria-controls], .topbar__phone button").click(); 1`); await sleep(400);
check(await ev(`(() => { const p = document.querySelector(".topbar__panel"); p.scrollTop = p.scrollHeight; const last = [...p.querySelectorAll("a, input, label")].pop().getBoundingClientRect(); return p.getBoundingClientRect().bottom <= innerHeight + 1 && last.bottom <= innerHeight + 1 && last.height > 0; })()`), "the open menu fits a sideways phone and scrolls to its last control");
await S("Emulation.setDeviceMetricsOverride", { width: 390, height: 844, deviceScaleFactor: 1, mobile: false }); await nav("index.html");
check(await ev(`(() => { const t = document.querySelector("footer .theme"); return !!t && t.getClientRects().length > 0 && [...t.querySelectorAll("label")].every((l) => l.getBoundingClientRect().height >= 44); })()`), "the footer shows the theme control on a phone, each choice at least 44 pixels tall");

// A proposal, to be shown (DESIGN.md, "A proposal: the travel page and the host page open and close";
// sources/conversations/2026-11-22--org--anything-left-lets-iterate.md): the same sections on the two other long
// pages. What a first visit shows on each, that a choice is kept under the page's own name and leaves the home
// page's alone, that a link into a closed section opens it, that each section that folds has its goat on its top
// edge and a press on it is the goat's alone, and that the page is whole with script off.
const LONG = {
  travel: { never: ["ways"], open: ["costs", "staying", "eating"], shut: ["getting-here", "good-to-know", "june"] },
  extend: { never: ["how"], open: ["adding", "propose"], shut: ["what", "where"] },
};
const stored = () => ev(`localStorage.getItem("folds")`);
for (const [name, want] of Object.entries(LONG)) {
  const page = `${name}.html`, folding = [...want.open, ...want.shut];
  const inOrder = (ids) => ev(`[...document.querySelectorAll("[data-folds] > section")].map((s) => s.id).filter((id) => ${JSON.stringify(ids)}.includes(id)).join(",")`);
  await S("Emulation.setDeviceMetricsOverride", { width: 390, height: 844, deviceScaleFactor: 1, mobile: false });
  await nav(page); await forget(); await nav(page);
  check(await closed() === await inOrder(want.shut), `${page}: a first visit shows ${want.shut.join(", ")} closed and every other section open`);
  check(await ev(`document.documentElement.classList.contains("folds-ready") && document.querySelectorAll(".sec__toggle").length`) === folding.length && await ev(`${JSON.stringify(want.never)}.every((id) => !document.querySelector("#" + id + " .sec__toggle") && !document.querySelector("#" + id + " > .peek") && !document.getElementById(id).classList.contains("is-closed"))`), `${page}: every section that folds has its control; ${want.never.join(", ")} has none, no goat of its own, and is open`);
  check(await ev(`${JSON.stringify(folding)}.every((id) => document.querySelectorAll("#" + id + " > .peek").length === 1 && document.querySelectorAll("#" + id + " [data-fold-end]").length === 1 && document.querySelectorAll("#" + id + " .sec__peek").length === 1)`), `${page}: every section that folds has one goat on its edge, one closed row and Show less at its end`);
  check(await ev(`[...document.querySelectorAll("[data-folds] > section.is-closed")].every((s) => [...s.children].every((c) => c.matches("h2, .sec__peek, .peek, .goat-one__stage") || !c.getClientRects().length || getComputedStyle(c).contentVisibility === "hidden"))`), `${page}: a closed section shows its heading and its row and nothing else`);
  // A press is kept under this page's name, survives a reload, and the home page's record is not touched.
  await ev(`localStorage.setItem("folds", JSON.stringify({ index: { days: "open" } })); 1`); await nav(page);
  await ev(`document.querySelector("#${want.shut[0]} .sec__toggle").click(); document.querySelector("#${want.open[0]} .sec__toggle").click(); 1`);
  check(await stored() === JSON.stringify({ index: { days: "open" }, [name]: { [want.shut[0]]: "open", [want.open[0]]: "closed" } }), `${page}: a press is kept under the page's own name and the home page's record stays as it was`);
  await nav(page);
  check((await closed()).split(",").includes(want.open[0]) && !(await closed()).split(",").includes(want.shut[0]), `${page}: the choice is there after a reload`);
  await ev(`document.querySelector("#${want.shut[0]} [data-fold-end]").click(); 1`); await sleep(200);
  check((await closed()).split(",").includes(want.shut[0]) && await ev(`document.activeElement === document.querySelector("#${want.shut[0]} .sec__toggle")`), `${page}: Show less closes the section and puts the keyboard on its heading`);
  // A link into a closed section opens it and remembers nothing.
  await forget(); await nav(page);
  if (name === "travel") {
    await ev(`document.querySelector('#ways a[href="#getting-here"]').click(); 1`); await sleep(700);
    check(!(await closed()).split(",").includes("getting-here") && await stored() === null, `${page}: "Every route in detail" opens the routes and remembers nothing`);
    await nav(`${page}#car`, 700);
    check(!(await closed()).split(",").includes("getting-here") && await ev(`document.getElementById("car").getClientRects().length > 0`), `${page}: a link to something inside a closed section opens it`);
    await forget(); await nav(page);
    await ev(`document.querySelector('.daynav a[href="#good-to-know"]').click(); 1`); await sleep(700);
    check(!(await closed()).split(",").includes("good-to-know"), `${page}: the jump row opens the section it jumps to`);
    check(await ev(`(() => { const n = document.querySelector(".daynav--page"); return n.getBoundingClientRect().height < 50 && [...n.querySelectorAll("a")].every((a) => a.getBoundingClientRect().height >= 44); })()`), `${page}: at 390 wide the jump row is one line and each link is 44 pixels tall`);
  } else {
    check(await ev(`document.querySelector(".finder").getClientRects().length`) === 0, `${page}: the closed places hide their finder too`);
    await ev(`document.querySelector("#what .sec__toggle").click(); 1`); await sleep(200);
    await ev(`document.querySelector('#what a[data-pick-kind="hike"]').click(); 1`); await sleep(900);
    check(!(await closed()).split(",").includes("where") && await ev(`document.getElementById("f-kind").value === "hike" && document.querySelector(".finder").getClientRects().length > 0 && document.querySelector("[data-places]").getClientRects().length > 0`), `${page}: a kind pressed in "What you could run" opens the places with that kind picked`);
  }
  // Each section's goat, closed and at both widths: on the top edge at the right end, 80 pixels wide or more, whole,
  // and a press on it changes neither the address, the closed sections nor what is stored.
  for (const [width, height] of [[390, 844], [1440, 900]]) {
    await S("Emulation.setDeviceMetricsOverride", { width, height, deviceScaleFactor: 1, mobile: false });
    await ev(`localStorage.setItem("folds", JSON.stringify({ ${JSON.stringify(name)}: ${JSON.stringify(Object.fromEntries(folding.map((s) => [s, "closed"])))} })); 1`); await nav(page);
    await ev(`document.documentElement.style.scrollBehavior = "auto"; 1`);
    cutGoats = 0; cutWords = 0; mute = 0; small = 0; leaks = 0; overlaid = 0; unreachable = 0;
    let away = 0; const seats = new Set();
    for (const sid of await (async () => (await inOrder(folding)).split(","))()) {
      await ev(`window.scrollTo(0, document.getElementById("${sid}").getBoundingClientRect().top + scrollY - innerHeight * 0.45); 1`); await sleep(500);
      await S("Input.dispatchMouseEvent", { type: "mouseMoved", x: 5, y: 5 }); await mouse(`#${sid} h2`, 0.3, 0.5); await arrived(sid);
      const g = await ev(`(() => { const st = document.querySelector(".goat-one__stage"), s = st && st.parentElement; if (!s || s.id !== "${sid}") return null; const r = st.getBoundingClientRect(), b = s.getBoundingClientRect(); return [Math.round(r.width), Math.round(b.right - r.right)].join(","); })()`);
      if (!g) away += 1; else { seats.add(g); await look(sid); }
    }
    check(away === 0 && seats.size === 1 && cutGoats === 0 && small === 0, `${page} at ${width} wide: the goat stands on every closed row in one place of one size, whole and 80 pixels wide or more (${[...seats].join(" | ")}; ${away} rows without it, ${cutGoats} cut, ${small} small)`);
    check(leaks === 0 && unreachable === 0 && cutWords === 0, `${page} at ${width} wide: a press on a row's goat follows no link, opens no section and stores nothing, what it says is whole, and the ${overlaid} links and buttons under its picture can still be pressed (${leaks} leaked, ${unreachable} out of reach, ${cutWords} bubbles cut)`);
  }
  await S("Emulation.setDeviceMetricsOverride", { width: 390, height: 844, deviceScaleFactor: 1, mobile: false });
  await forget();
  await S("Emulation.setScriptExecutionDisabled", { value: true }); await nav(page, 1200);
  check(await ev(`document.querySelectorAll("[data-folds] > section.is-closed, .sec__toggle").length === 0 && [...document.querySelectorAll(".sec__peek, .sec__end, .folds-all")].every((e) => getComputedStyle(e).display === "none") && ${JSON.stringify(want.shut)}.every((id) => document.querySelector("#" + id + " > :not(h2, .sec__peek, .sec__end, .peek, [hidden])").getClientRects().length > 0)`), `${page}: with script off everything is open and no control shows`);
  await S("Emulation.setScriptExecutionDisabled", { value: false });
}
await forget();

// The cover on a phone, as the organiser chose it (sources/conversations/2026-11-22--org--phone-hero-layout-and-trim-keep-the-six-cards.md): on a first visit the first screen shows the name, the date,
// the place, the promise and the whole Register button, at five phone sizes; of who it is for the cover shows "Any
// programming language, any stack." and the sentence before it is not displayed; the three links are one row, each 44
// pixels tall, on one line each from 21.5rem and on two lines each under it, never one left alone on a second row;
// the goat stands on the cover's rule, whole and clear of the top bar and of the name, and leaves once the page has
// moved its stop under the bar; "What is decided" shows its six stickers numbered 1 to 6; nothing is wider than the
// window. The window is a phone's here (mobile: true), so it is as wide as it says: with a desktop window the
// scrollbar takes 15 pixels of it. From 48rem up the cover has no goat stop, its date line is one run of words with
// its dot, its links keep their arrows and it says the whole of who it is for.
const phoneWindow = (width, height) => S("Emulation.setDeviceMetricsOverride", { width, height, deviceScaleFactor: 1, mobile: true });
const WHO = "Any programming language, any stack.";
const coverNow = `(() => { const b = (s) => document.querySelector(s).getBoundingClientRect(), bar = b(".topbar").bottom, wide = document.documentElement.clientWidth; const st = document.querySelector(".goat-one__stage"), on = st && st.parentElement, g = st ? st.getBoundingClientRect() : null; const links = [...document.querySelectorAll(".cover-links a")].map((a) => a.getBoundingClientRect()); const parts = [...document.querySelectorAll(".cover-when__part")].map((e) => e.getBoundingClientRect()); const shown = (e) => e.getClientRects().length > 0; return { wide, said: [".cover-title", ".cover-when", ".cover-lede strong", ".cover-lede__who", ".button--cover"].every((s) => b(s).top >= bar && b(s).bottom <= innerHeight), who: document.querySelector(".cover-lede__who").innerText.replace(/\\s+/g, " ").trim(), long: shown(document.querySelector(".cover-lede__long")), rows: new Set(links.map((r) => Math.round(r.top))).size, tall: links.every((r) => r.height >= 44 && r.left >= 0 && r.right <= wide), apart: links.slice(1).every((r, i) => r.left - links[i].right >= 8), lines: parts.length === 2 && parts[1].top >= parts[0].bottom - 1 && parts.every((r) => r.height < 30), goat: !!on && on.matches(".cover-perch") && getComputedStyle(st).visibility === "visible" && g.top >= bar && g.right <= wide && g.left >= b(".cover-title").right, fits: document.documentElement.scrollWidth <= wide, stickers: [...document.querySelectorAll(".slots--hero > *")].filter(shown).map((e) => e.querySelector(".num").textContent).join("") }; })()`;
for (const [width, height] of [[390, 844], [412, 915], [390, 700], [360, 780], [320, 640]]) {
  await phoneWindow(width, height);
  await forget(); await nav("index.html", 2600);
  const c = await ev(coverNow);
  check(c.wide === width && c.said && c.fits, `at ${width} by ${height} the first screen shows the name, the date and place, the promise, who it is for and the whole Register button, and nothing is wider than the window`);
  check(c.who === WHO && !c.long, `at ${width} wide the cover says "${WHO}" of who it is for, and the sentence before it is not displayed`);
  check(c.rows === 1 && c.tall && c.apart, `at ${width} wide the cover's three links are one row, each 44 pixels tall, 8 pixels or more apart (${c.rows} rows)`);
  check(c.lines, `at ${width} wide the date is one line and the place the next, neither wrapped`);
  check(c.goat, `at ${width} by ${height} the goat stands on the cover's rule, whole, clear of the top bar and of the name`);
  check(c.stickers === "123456", `at ${width} wide "What is decided" shows its six stickers, numbered 1 to 6 (${c.stickers})`);
}
// The goat leaves the cover's rule once its stop is under the top bar, and is back when the page is at its top.
await phoneWindow(390, 844);
await forget(); await nav("index.html", 2600);
await ev(`document.documentElement.style.scrollBehavior = "auto"; 1`);
const coverGoat = `(() => { const st = document.querySelector(".goat-one__stage"); return !!st && !!st.parentElement && st.parentElement.matches(".cover-perch") && getComputedStyle(st).visibility === "visible"; })()`;
let stayed = 0;
for (const y of [30, 90]) { await ev(`window.scrollTo(0, ${y}); 1`); for (let i = 0; i < 40 && await ev(coverGoat); i++) await sleep(150); if (await ev(coverGoat)) stayed += 1; }
check(stayed === 0, "scrolled so that the cover's rule is under the top bar, the goat does not stay there");
await ev(`window.scrollTo(0, 0); 1`); for (let i = 0; i < 40 && !await ev(coverGoat); i++) await sleep(150);
check(await ev(coverGoat), "back at the top of the page, the goat is on the cover's rule again");
await S("Emulation.setDeviceMetricsOverride", { width: 1440, height: 900, deviceScaleFactor: 1, mobile: false });
await forget(); await nav("index.html", 2600);
check(await ev(`document.querySelector(".cover-perch").getClientRects().length === 0 && !document.querySelector(".cover-perch .goat-one__stage") && getComputedStyle(document.querySelector(".cover-when__dot")).display === "inline" && [...document.querySelectorAll(".cover-when__part")].every((e) => getComputedStyle(e).display === "inline") && getComputedStyle(document.querySelector(".cover-links a"), "::after").content !== "none" && document.querySelector(".cover-lede__who").innerText.replace(/\\s+/g, " ").trim() === "Engineers, designers, product people, founders, and the incurably curious dreamers and visionaries. Any programming language, any stack." && [...document.querySelectorAll(".slots--hero > *")].filter((e) => e.getClientRects().length).length === 6`), "from 48rem up the cover has no goat stop, its date and place are one run of words with the dot, its links keep their arrows, and it says the whole of who it is for beside six stickers");
await S("Emulation.setDeviceMetricsOverride", { width: 390, height: 844, deviceScaleFactor: 1, mobile: false });

// Never a trap.
await forget();
const { identifier } = await S("Page.addScriptToEvaluateOnNewDocument", { source: `Object.defineProperty(window, "localStorage", { get() { throw new DOMException("denied", "SecurityError"); } });` });
const before = errors();
await nav("index.html");
check(await alive() === FOLDING.length && await closed() === START_CLOSED.join(","), "with storage blocked it is the first-visit page");
await ev(`document.querySelector("#days-title .sec__toggle").click(); 1`);
check(!(await closed()).split(",").includes("days") && errors() === before, "with storage blocked a section still opens and nothing throws");
await S("Page.removeScriptToEvaluateOnNewDocument", { identifier });
const open = `[...document.querySelectorAll("[data-folds] > section > *")].filter((e) => !e.matches(".sec__peek, .sec__end, .peek") && getComputedStyle(e).display === "none").length === 0 && [...document.querySelectorAll(".sec__peek, .sec__end, .folds-all")].every((e) => getComputedStyle(e).display === "none")`;
await S("Network.setBlockedURLs", { urls: ["*album.js*"] }); await nav("index.html", 1200);
check(await ev(open) === true, "if album.js never arrives, everything is open once the page has loaded");
await S("Network.setBlockedURLs", { urls: [] });
await S("Emulation.setScriptExecutionDisabled", { value: true }); await nav("index.html", 1200);
check(await ev(open) === true && await ev(`document.querySelectorAll(".sec__toggle").length`) === 0, "with script off everything is open and no control shows");
await S("Emulation.setScriptExecutionDisabled", { value: false });

console.log(failed ? `${failed} check(s) failed` : "every check passed");
ws.close();
process.exit(failed ? 1 : 0);
