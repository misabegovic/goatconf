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
const FOLDING = ["days", "speakers", "tuzla", "food", "talk", "add", "money", "the-goat", "conduct", "goatchi", "see-you"];
const START_CLOSED = FOLDING.filter((s) => s !== "speakers");
const shut = Object.fromEntries(FOLDING.map((s) => [s, "closed"]));

await nav("index.html"); await forget(); await nav("index.html");
check(await closed() === START_CLOSED.join(","), "a first visit has the speakers open and every other section closed");
check(await alive() === FOLDING.length, "every section that closes has its button; the hero and the free ticket have none");
check(await ev(`!document.querySelector("#ticket .sec__toggle") && !document.querySelector(".spread .sec__toggle")`), "the hero and the free ticket have no control");

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

// Never a trap.
await forget();
const { identifier } = await S("Page.addScriptToEvaluateOnNewDocument", { source: `Object.defineProperty(window, "localStorage", { get() { throw new DOMException("denied", "SecurityError"); } });` });
const before = errors();
await nav("index.html");
check(await alive() === FOLDING.length && await closed() === START_CLOSED.join(","), "with storage blocked it is the first-visit page");
await ev(`document.querySelector("#days-title .sec__toggle").click(); 1`);
check(!(await closed()).split(",").includes("days") && errors() === before, "with storage blocked a section still opens and nothing throws");
await S("Page.removeScriptToEvaluateOnNewDocument", { identifier });
const open = `[...document.querySelectorAll("[data-folds] > section > *")].filter((e) => !e.matches(".sec__peek") && getComputedStyle(e).display === "none").length === 0 && [...document.querySelectorAll(".sec__peek, .folds-all")].every((e) => getComputedStyle(e).display === "none")`;
await S("Network.setBlockedURLs", { urls: ["*album.js*"] }); await nav("index.html", 1200);
check(await ev(open) === true, "if album.js never arrives, everything is open once the page has loaded");
await S("Network.setBlockedURLs", { urls: [] });
await S("Emulation.setScriptExecutionDisabled", { value: true }); await nav("index.html", 1200);
check(await ev(open) === true && await ev(`document.querySelectorAll(".sec__toggle").length`) === 0, "with script off everything is open and no control shows");
await S("Emulation.setScriptExecutionDisabled", { value: false });

console.log(failed ? `${failed} check(s) failed` : "every check passed");
ws.close();
process.exit(failed ? 1 : 0);
