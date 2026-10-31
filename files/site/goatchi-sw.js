// Goatchi's service worker (ADR goatchi-full-game), for the Goatchi page only. It keeps what the page last loaded,
// so an installed Goatchi opens offline, and, only once the player has turned reminders on, it wakes when the browser
// lets it (periodic background sync), looks at the goat the page left for it in IndexedDB, and says so on this
// device when the goat needs it, at most once a day, and once if a challenge goat wanders off. It sends nothing
// anywhere: there is no server.
const CACHE = "goatchi-1";
const EMPTY_AFTER = 36 * 3600e3;
const SULK = 0.25;
const NEEDS = ["food", "play", "sleep"];
const DAY = 864e5;
const WANDER_AFTER = 3 * DAY;
const TAG = "goatchi-check";

// The needs, worked out from the time passed exactly as the page does.
const level = (goat, n, now) => Math.max(0, Math.min(1, goat.needs[n][0] - (now - goat.needs[n][1]) / EMPTY_AFTER));
const lowest = (goat, now) => NEEDS.reduce((a, b) => (level(goat, b, now) < level(goat, a, now) ? b : a));
// A challenge goat leaves three days after its last need ran out.
const leftAt = (goat) => (goat.challenge
  ? Math.max(...NEEDS.map((n) => goat.needs[n][1] + goat.needs[n][0] * EMPTY_AFTER)) + WANDER_AFTER : Infinity);
const wandered = (goat, now) => now >= leftAt(goat);
// What to tell the player, if anything, about a goat they asked to hear about: once, that a challenge goat has
// wandered off; otherwise that it needs them, naming the need it lacks most, when it sulks and not within a day of
// the last time.
const remindOf = (goat, lastTold, toldGone, now) => {
  if (!goat || goat.remind !== true) return null;
  if (wandered(goat, now)) return toldGone ? null : "left";
  if (!NEEDS.some((n) => level(goat, n, now) < SULK)) return null;
  return lastTold && now - lastTold < DAY ? null : "need";
};
const shouldRemind = (goat, lastTold, now, toldGone = false) => remindOf(goat, lastTold, toldGone, now) !== null;
const NEEDING = {
  food: ["is hungry", "Baaa… Come and feed it."],
  play: ["wants to play", "Baaa… Come and play with it."],
  sleep: ["is sleepy", "Baaa… Come and let it sleep."],
};
const reminder = (goat, kind = "need", now = Date.now()) => {
  if (kind === "left") {
    const days = Math.max(0, Math.floor((leftAt(goat) - goat.since) / DAY));
    return { title: `${goat.name} went exploring`,
      body: `It set off for the hills above Tuzla. You kept ${goat.name.startsWith("The ") ? "it" : "them"} for ${days} day${days === 1 ? "" : "s"}.` };
  }
  const [what, body] = NEEDING[lowest(goat, now)];
  return { title: `${goat.name} ${what}`,
    body: goat.challenge ? `${body} Three days with every need empty and it wanders off to the hills.` : body };
};

if (typeof module === "object") module.exports = { level, wandered, remindOf, shouldRemind, reminder };

// What the page left for the worker: the goat, and when the worker last told the player about it.
const store = (mode, run) => new Promise((resolve, reject) => {
  const open = indexedDB.open("goatchi", 1);
  open.onupgradeneeded = () => open.result.createObjectStore("kv");
  open.onerror = () => reject(open.error);
  open.onsuccess = () => {
    const tx = open.result.transaction("kv", mode);
    const req = run(tx.objectStore("kv"));
    tx.oncomplete = () => { open.result.close(); resolve(req && req.result); };
    tx.onerror = () => reject(tx.error);
  };
});

async function check(now = Date.now()) {
  const goat = await store("readonly", (kv) => kv.get("goat"));
  const told = await store("readonly", (kv) => kv.get("told"));
  const toldGone = await store("readonly", (kv) => kv.get("toldGone"));
  const kind = remindOf(goat, told, toldGone, now);
  if (!kind) return false;
  const { title, body } = reminder(goat, kind, now);
  await self.registration.showNotification(title, { body, tag: TAG, icon: "img/goatchi-icon-192.png", badge: "img/goatchi-icon-192.png" });
  await store("readwrite", (kv) => kv.put(now, "told"));
  if (kind === "left") await store("readwrite", (kv) => kv.put(true, "toldGone"));
  return true;
}

if (typeof self === "object" && typeof self.addEventListener === "function" && typeof module !== "object") {
  self.addEventListener("install", () => self.skipWaiting());
  self.addEventListener("activate", (e) => e.waitUntil(
    caches.keys().then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))).then(() => self.clients.claim())));
  // The network first, so Goatchi is always the newest build when online; what it last loaded when offline.
  self.addEventListener("fetch", (e) => {
    const url = new URL(e.request.url);
    if (e.request.method !== "GET" || url.origin !== self.location.origin) return;
    e.respondWith(fetch(e.request).then((res) => {
      if (res.ok) { const copy = res.clone(); caches.open(CACHE).then((c) => c.put(e.request, copy)); }
      return res;
    }).catch(() => caches.match(e.request, { ignoreSearch: true })));
  });
  self.addEventListener("periodicsync", (e) => { if (e.tag === TAG) e.waitUntil(check()); });
  self.addEventListener("notificationclick", (e) => {
    e.notification.close();
    e.waitUntil(self.clients.matchAll({ type: "window" }).then((open) => {
      const page = open.find((c) => new URL(c.url).pathname.includes("goatchi"));
      return page ? page.focus() : self.clients.openWindow("goatchi.html");
    }));
  });
}
