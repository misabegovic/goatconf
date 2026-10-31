// Goatchi's reminders in a real browser (ADR wiki/org/adrs/goatchi-full-game.md): headless Chromium, with notifications
// and periodic background sync allowed as an installed Goatchi has them, fires the worker's periodic sync through the
// browser's developer protocol and reads back the notifications the worker shows.
//
//   python3 -m http.server 8765 --directory site &      (from files/)
//   NODE_PATH=<dir with playwright-core> CHROMIUM=<chrome binary> node tests/browser/goatchi-reminders.mjs
//
// It needs playwright-core and a Chromium, so it is not part of the local CI; run it before shipping a change to
// goatchi.js or goatchi-sw.js, and by hand on a phone as the ADR asks.
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const { chromium } = require("playwright-core");
const BASE = process.env.BASE || "http://localhost:8765";
const H = 3600e3;
let failed = 0;
const check = (ok, what) => { console.log(`${ok ? "ok  " : "FAIL"} ${what}`); if (!ok) failed += 1; };

// A persistent context is the browser's default one, where the developer protocol's permissions apply.
const { mkdtempSync } = await import("node:fs");
const { tmpdir } = await import("node:os");
const ctx = await chromium.launchPersistentContext(mkdtempSync(`${tmpdir()}/goatchi-`), { executablePath: process.env.CHROMIUM, args: ["--enable-features=PeriodicBackgroundSync"] });
const browser = ctx;
const page = ctx.pages()[0] || await ctx.newPage();
const errors = [];
page.on("pageerror", (e) => errors.push(e.message));
page.on("console", (m) => { if (m.type() === "error") errors.push(m.text()); });
const cdp = await ctx.newCDPSession(page);
await cdp.send("Browser.grantPermissions", { origin: BASE, permissions: ["notifications", "periodicBackgroundSync", "backgroundSync"] });
const regs = new Map();
await cdp.send("ServiceWorker.enable");
cdp.on("ServiceWorker.workerRegistrationUpdated", ({ registrations }) => registrations.forEach((r) => regs.set(r.scopeURL, r.registrationId)));

// A goat kept a day and a half ago, every need run low: it is sulking.
const sulking = (hoursAgo) => {
  const then = Date.now() - hoursAgo * H;
  return { pose: "sitting", name: "The goat", src: "img/goat/sitting.webp", speaker: "", since: then, cheered: [], challenge: false,
    needs: { food: [1, then], play: [1, then], sleep: [1, then] } };
};
const shown = () => page.evaluate(async () => (await (await navigator.serviceWorker.ready).getNotifications()).map((n) => ({ title: n.title, body: n.body })));
const clear = () => page.evaluate(async () => (await (await navigator.serviceWorker.ready).getNotifications()).forEach((n) => n.close()));
const fire = async () => {
  const id = [...regs.entries()].find(([scope]) => scope.includes("/goatchi"))?.[1];
  await cdp.send("ServiceWorker.dispatchPeriodicSyncEvent", { origin: BASE, registrationId: id, tag: "goatchi-check" });
  await page.waitForTimeout(800);
};

// Before a goat is picked nothing is registered and nothing is offered.
await page.goto(`${BASE}/goatchi.html`, { waitUntil: "networkidle" });
check(await page.evaluate(async () => (await navigator.serviceWorker.getRegistrations()).length === 0), "no worker before a goat is picked");
check(await page.locator(".goatchi__remind").isHidden(), "no reminder switch before a goat is picked");

// A kept goat: the worker registers, and where periodic sync is allowed the switch appears, off.
await page.evaluate((g) => localStorage.setItem("goatconf-goatchi", JSON.stringify(g)), sulking(30));
await page.reload({ waitUntil: "networkidle" });
await page.waitForFunction(() => !document.querySelector(".goatchi__remind").hidden, null, { timeout: 5000 }).catch(() => {});
check(await page.locator(".goatchi__remind").isVisible(), "the switch appears for a kept goat where periodic sync is allowed");
check(!(await page.locator(".goatchi__remind input").isChecked()), "the switch starts off");

// Off: the worker wakes, and says nothing.
await fire();
check((await shown()).length === 0, "with reminders off, a sulking goat brings no notification");

// On: one notification, naming the goat; then none again within the day.
await page.locator(".goatchi__remind input").check();
await page.waitForTimeout(500);
check(await page.evaluate(async () => (await (await navigator.serviceWorker.ready).periodicSync.getTags()).includes("goatchi-check")), "turning it on registers the check");
await fire();
const first = await shown();
check(first.length === 1 && first[0].title === "The goat is hungry", `a sulking goat brings one notification, naming its need (${JSON.stringify(first)})`);
await clear();
await fire();
check((await shown()).length === 0, "no second notification within the day");

// A happy goat: fed and played with, the told time cleared, the worker wakes and says nothing.
await page.evaluate(() => new Promise((r) => { const o = indexedDB.open("goatchi", 1); o.onsuccess = () => { const t = o.result.transaction("kv", "readwrite"); t.objectStore("kv").delete("told"); t.oncomplete = r; }; }));
for (const act of ["feed", "play", "sleep"]) { await page.click(`[data-act="${act}"]`); await page.waitForTimeout(300); }
await fire();
check((await shown()).length === 0, "a happy goat brings no notification");

// Off again: the check and the copy are gone.
await page.locator(".goatchi__remind input").uncheck();
await page.waitForTimeout(500);
check(await page.evaluate(async () => !(await (await navigator.serviceWorker.ready).periodicSync.getTags()).includes("goatchi-check")), "turning it off removes the check");
check(await page.evaluate(() => new Promise((r) => { const o = indexedDB.open("goatchi", 1); o.onsuccess = () => { const q = o.result.transaction("kv").objectStore("kv").get("goat"); q.onsuccess = () => r(q.result === undefined); }; })), "turning it off removes the goat's copy");

// A challenge goat that wandered off: told once, with how long it was kept, and not again.
await page.evaluate(() => new Promise((r) => { const o = indexedDB.open("goatchi", 1); o.onsuccess = () => { const t = o.result.transaction("kv", "readwrite"); t.objectStore("kv").delete("told"); t.oncomplete = r; }; }));
await page.locator(".goatchi__remind input").check();
await page.waitForTimeout(500);
await page.evaluate((g) => new Promise((r) => { const o = indexedDB.open("goatchi", 1); o.onsuccess = () => { const t = o.result.transaction("kv", "readwrite"); t.objectStore("kv").put(g, "goat"); t.oncomplete = r; }; }),
  { ...sulking(24 * 6), challenge: true, remind: true, since: Date.now() - 9 * 24 * H });
await clear();
await fire();
const left = await shown();
check(left.length === 1 && left[0].title === "The goat went exploring" && /kept it for 7 days/.test(left[0].body), `a challenge goat that wandered off is told once (${JSON.stringify(left)})`);
await clear();
await fire();
check((await shown()).length === 0, "and not told again");

check(errors.length === 0, `no console errors (${errors.join(" | ")})`);
await browser.close();
process.exit(failed ? 1 : 0);
