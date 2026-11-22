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
const START_CLOSED = FOLDING.filter((s) => s !== "speakers");
const shut = Object.fromEntries(FOLDING.map((s) => [s, "closed"]));

await nav("index.html"); await forget(); await nav("index.html");
check(await closed() === START_CLOSED.join(","), "a first visit has the speakers open and every other section closed");
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
check(await ev(`localStorage.getItem("folds")`) === JSON.stringify({ index: { days: "open", speakers: "closed" } }), "a press is kept under the key folds, one entry a page");
check(await ev(`document.querySelector("#days-title .sec__toggle").getAttribute("aria-expanded") + document.querySelector("#speakers-title .sec__toggle").getAttribute("aria-expanded")`) === "truefalse", "the button says whether its section is open");
await nav("index.html");
check(!(await closed()).split(",").includes("days") && (await closed()).split(",").includes("speakers"), "the choice is there after a reload");
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
const point = (sel, fx = 0.5, fy = 0.5) => ev(`(() => { const r = document.querySelector(${JSON.stringify(sel)}).getBoundingClientRect(); return [Math.round(r.left + r.width * ${fx}), Math.round(r.top + r.height * ${fy})]; })()`);
const mouse = async (sel, fx, fy, press = false) => { const [x, y] = await point(sel, fx, fy); await S("Input.dispatchMouseEvent", { type: "mouseMoved", x, y }); if (press) for (const type of ["mousePressed", "mouseReleased"]) await S("Input.dispatchMouseEvent", { type, x, y, button: "left", clickCount: 1 }); };
for (const sid of FOLDING) {
  const tall = () => ev(`[document.getElementById("${sid}"), document.querySelector("#${sid} h2"), document.querySelector("#${sid} .sec__peek")].map((e) => Math.round(e.getBoundingClientRect().height * 10) / 10).join("/")`);
  await ev(`window.scrollTo(0, document.getElementById("${sid}").getBoundingClientRect().top + scrollY - innerHeight * 0.45); 1`); await sleep(500);
  const first = await tall();
  await S("Input.dispatchMouseEvent", { type: "mouseMoved", x: 5, y: 5 }); await mouse(`#${sid} h2`, 0.5, 0.5); await sleep(1800);
  const g = await ev(`(() => { const st = document.querySelector(".goat-one__stage"), s = st && st.parentElement; if (!s || s.id !== "${sid}") return null; const r = st.getBoundingClientRect(), b = s.getBoundingClientRect(); return [Math.round(r.width), Math.round(b.right - r.right), Math.round(r.bottom - b.top)].join(","); })()`);
  if (!g) absent += 1; else boxes.add(g);
  if (first !== await tall()) moved += 1;
  if (await ev(`!!document.querySelector("[data-fold-part][hidden] .goat-one__stage, .is-closed h2 .goat-one__stage")`)) inside += 1;
}
check(moved === 0, "no closed row, heading or line on it changes size as the goat arrives and leaves");
check(await ev(`window.__shift`) === 0, "no layout shift on the closed page while the goat goes from row to row");
check(absent === 0 && boxes.size === 1, `the goat stands on every closed row in one place of one size (${[...boxes].join(" | ")}${absent ? `; ${absent} rows without it` : ""})`);
check(inside === 0, "the goat is never inside a closed section");
await ev(`window.scrollTo(0, document.getElementById("food").getBoundingClientRect().top + scrollY - innerHeight * 0.45); 1`); await sleep(400);
await mouse("#food h2", 0.5, 0.5); await sleep(1800);
await mouse(".goat-one__stage .goat", 0.5, 0.4, true); await sleep(700);
check((await closed()).split(",").includes("food") && await ev(`document.querySelector(".goat-one__stage").parentElement.id`) === "food", "a press on the row's goat is for the goat: the section stays closed");
await sleep(1200);
await ev(`window.__moves = 0; const animate = Element.prototype.animate; Element.prototype.animate = function (...a) { if (this.closest && this.closest(".goat-one__stage")) window.__moves += 1; return animate.apply(this, a); }; 1`);
await mouse("#food-title .sec__toggle", 0.2, 0.5, true); await sleep(250);
check(!(await closed()).split(",").includes("food") && await ev(`window.__moves`) === 0, "a press on the heading opens the section and does not set the goat off");
await sleep(900);
check(await ev(`(() => { const st = document.querySelector(".goat-one__stage"); if (st.parentElement.id !== "food") return true; return Math.abs(st.getBoundingClientRect().bottom - document.getElementById("food").getBoundingClientRect().top) < 12; })()`), "the section's own goat stays on the section's top edge when the section opens");
check(await ev(`document.querySelectorAll("[data-folds] details").length === 0 && document.getElementById("food-dishes").getClientRects().length > 0 && document.querySelectorAll("#food-dishes img").length >= 12`), "opening a section opens all of it: the twelve dishes are there, with no second fold");
await ev(`document.querySelector("#food-title .sec__toggle").click(); 1`); await sleep(1800);
check(await ev(`!document.querySelector("[data-fold-part][hidden] .goat-one__stage")`), "a goat inside a section that closes does not stay inside it");
await ev(`document.querySelector("#tuzla .sec__strip img").click(); 1`); await sleep(300);
check(!(await closed()).split(",").includes("tuzla") && await ev(`JSON.parse(localStorage.getItem("folds")).index.tuzla`) === "open", "a press on a closed row's strip of pictures opens the section");
check(await ev(`!document.querySelector("#see-you .sec__toggle") && !document.querySelector("#see-you [data-fold-end]") && !document.getElementById("see-you").classList.contains("is-closed")`), "See you in Tuzla has no control and is open whatever is remembered");
const tops = [];
for (const target of ["days", "food", "the-goat", "conduct", "ticket"]) { await nav(`index.html#${target}`, 1600); tops.push(await ev(`Math.round(document.getElementById("${target}").getBoundingClientRect().top)`)); }
check(new Set(tops).size === 1, `a link to any section lands at one distance from the top (${tops.join(", ")})`);
// The phone menu on a phone held sideways, and the theme control in the footer.
await S("Emulation.setDeviceMetricsOverride", { width: 667, height: 375, deviceScaleFactor: 1, mobile: false }); await nav("index.html");
await ev(`document.querySelector(".topbar__phone summary, .topbar__phone [aria-controls], .topbar__phone button").click(); 1`); await sleep(400);
check(await ev(`(() => { const p = document.querySelector(".topbar__panel"); p.scrollTop = p.scrollHeight; const last = [...p.querySelectorAll("a, input, label")].pop().getBoundingClientRect(); return p.getBoundingClientRect().bottom <= innerHeight + 1 && last.bottom <= innerHeight + 1 && last.height > 0; })()`), "the open menu fits a sideways phone and scrolls to its last control");
await S("Emulation.setDeviceMetricsOverride", { width: 390, height: 844, deviceScaleFactor: 1, mobile: false }); await nav("index.html");
check(await ev(`(() => { const t = document.querySelector("footer .theme"); return !!t && t.getClientRects().length > 0 && [...t.querySelectorAll("label")].every((l) => l.getBoundingClientRect().height >= 44); })()`), "the footer shows the theme control on a phone, each choice at least 44 pixels tall");

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
