// Goatchi's service worker (ADR goatchi-full-game), for the Goatchi page only. It keeps what the page last loaded,
// so an installed Goatchi opens offline, and, only once the player has turned reminders on, it wakes when the browser
// lets it (periodic background sync), looks at the goat the page left for it in IndexedDB, and says so on this
// device when the goat sulks, at most once a day. It sends nothing anywhere: there is no server.
const CACHE = "goatchi-1";
const EMPTY_AFTER = 36 * 3600e3;
const SULK = 0.25;
const NEEDS = ["food", "play", "sleep"];
const DAY = 864e5;
const WANDER_AFTER = 3 * DAY;
const TAG = "goatchi-check";

// The needs and moods, worked out from the time passed exactly as the page does.
const level = (goat, n, now) => Math.max(0, Math.min(1, goat.needs[n][0] - (now - goat.needs[n][1]) / EMPTY_AFTER));
const wandered = (goat, now) => !!goat.challenge
  && now - Math.max(...NEEDS.map((n) => goat.needs[n][1] + goat.needs[n][0] * EMPTY_AFTER)) >= WANDER_AFTER;
// Tell the player only about a goat they asked to hear about, still theirs, sulking, and not told about in a day.
const shouldRemind = (goat, lastTold, now) => !!goat && goat.remind === true && !wandered(goat, now)
  && NEEDS.some((n) => level(goat, n, now) < SULK) && !(lastTold && now - lastTold < DAY);
const reminder = (goat) => ({
  title: `${goat.name} is sulking`,
  body: goat.challenge ? "Baaa… Feed it, play with it or let it sleep, before it wanders off to the hills." : "Baaa… Feed it, play with it or let it sleep.",
});

if (typeof module === "object") module.exports = { level, wandered, shouldRemind, reminder };

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
  if (!shouldRemind(goat, told, now)) return false;
  const { title, body } = reminder(goat);
  await self.registration.showNotification(title, { body, tag: TAG, icon: "img/goatchi-icon-192.png", badge: "img/goatchi-icon-192.png" });
  await store("readwrite", (kv) => kv.put(now, "told"));
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
