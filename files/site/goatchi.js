// Goatchi: keep a GoatConf goat (ADR goat-tamagotchi-on-the-site). The goat lives in this browser's storage only:
// which goat, and for each need its value and when it was last set. A need's value now is worked out from the time
// passed, so nothing runs while you are away. Food empties over a day, play over a day and a half and sleep over
// two days (ADR goatchi-full-game, organiser 2026-10-31); below a quarter the goat
// sulks and says so; it never dies. Picking, swapping and letting go all happen on this page, and nothing is sent
// anywhere.
(() => {
  const root = document.getElementById("goatchi");
  if (!root) return;
  const KEY = "goatconf-goatchi";
  const EMPTY_AFTER = { food: 24 * 3600e3, play: 36 * 3600e3, sleep: 48 * 3600e3 };
  const SULK = 0.25;
  const NEEDS = ["food", "play", "sleep"];
  const still = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const $ = (s) => root.querySelector(s);
  const playing = $(".goatchi__play"), empty = $(".goatchi__empty"), goat = $(".goatchi__goat"), say = $(".goatchi__say");
  const confirmRow = $(".goatchi__confirm");
  const picks = [...document.querySelectorAll(".goatchi__pick-goat")];
  const food = root.dataset.food.split("|"), sleepSrc = root.dataset.sleep;
  const dayOne = new Date(`${root.dataset.day}T09:00:00+02:00`);
  const stage = $(".goatchi__stage"), hike = $(".goatchi__hike"), hikeSrc = hike.getAttribute("src");
  const cards = [...root.querySelectorAll(".goatchi__card")];
  // A goat's own poses (ADR goatchi-full-game), from its pick: each a list of pictures. A goat without a pose shows
  // itself, or, for eating and sleep, the plain goat's food and sleep.
  const posesOf = (pose) => {
    const b = picks.find((p) => p.dataset.pose === pose);
    try { return JSON.parse((b && b.dataset.poses) || "{}"); } catch (e) { return {}; }
  };
  const look = (name) => {
    const list = goatState ? posesOf(goatState.pose)[name] : null;
    return list && list.length ? list[Math.floor(Math.random() * list.length)] : null;
  };

  // Nothing is written until a goat is picked: the page only reads whether one is kept. A browser that keeps
  // nothing (storage off, or a private window that refuses it) gets a note when a goat is picked.
  let store = null;
  try { store = window.localStorage; } catch (e) { store = null; }
  const canKeep = () => {
    try { store.setItem(`${KEY}-test`, "1"); store.removeItem(`${KEY}-test`); return true; } catch (e) { return false; }
  };
  const load = () => {
    try {
      const s = JSON.parse(store.getItem(KEY));
      if (!(s && s.pose && s.src && s.needs && NEEDS.every((n) => Array.isArray(s.needs[n])))) return null;
      // A goat kept before the postcards came starts with none, and earns at once what its days already have.
      if (!Array.isArray(s.cards)) s.cards = [];
      return s;
    } catch (e) { return null; }
  };
  let goatState = store ? load() : null;
  // With reminders on, the goat is also copied into IndexedDB, the one store the service worker can read.
  const mirror = (goat) => new Promise((resolve) => {
    if (!window.indexedDB) { resolve(); return; }
    const open = indexedDB.open("goatchi", 1);
    open.onupgradeneeded = () => open.result.createObjectStore("kv");
    open.onerror = () => resolve();
    open.onsuccess = () => {
      const tx = open.result.transaction("kv", "readwrite");
      if (goat) tx.objectStore("kv").put(goat, "goat"); else tx.objectStore("kv").clear();
      tx.oncomplete = tx.onerror = () => { open.result.close(); resolve(); };
    };
  });
  const save = () => {
    if (goatState) store.setItem(KEY, JSON.stringify(goatState)); else store.removeItem(KEY);
    if (goatState && goatState.remind) mirror(goatState);
  };
  const level = (n) => Math.max(0, Math.min(1, goatState.needs[n][0] - (Date.now() - goatState.needs[n][1]) / EMPTY_AFTER[n]));
  const fill = (n, by) => { goatState.needs[n] = [Math.min(1, (by === 1 ? 0 : level(n)) + by), Date.now()]; };
  const sulking = () => NEEDS.some((n) => level(n) < SULK);
  // Challenge mode: a goat left with every need empty for three days wanders off. Every need is empty from the
  // latest of the moments each one ran out; the goat leaves three days after that.
  const WANDER_AFTER = 3 * 864e5;
  const leftAt = () => {
    if (!goatState.challenge) return 0;
    const allEmpty = Math.max(...NEEDS.map((n) => goatState.needs[n][1] + goatState.needs[n][0] * EMPTY_AFTER[n]));
    return Date.now() - allEmpty >= WANDER_AFTER ? allEmpty + WANDER_AFTER : 0;
  };
  const daysKept = (until) => Math.max(0, Math.floor((until - goatState.since) / 864e5));
  const keptLine = (days) => (days === 0 ? "Kept since today" : `Kept for ${days} day${days === 1 ? "" : "s"}`);
  // Each need as a bar, full to empty, and the goat sulking when any runs low.
  // How long until it starts sulking, from the need that runs low first.
  const WANTS = { food: "food", play: "to play", sleep: "a nap" };
  const lasts = () => {
    if (sulking()) return goatState.challenge ? "It is sulking: feed it, play with it or let it sleep. In challenge mode, three days with every need empty and it wanders off." : "It is sulking: feed it, play with it or let it sleep.";
    // the need that reaches a quarter first, at its own speed
    const until = (k) => (level(k) - SULK) * EMPTY_AFTER[k];
    const n = NEEDS.reduce((a, b) => (until(b) < until(a) ? b : a));
    const hours = until(n) / 3600e3;
    const when = hours < 1 ? "less than an hour" : `about ${Math.round(hours)} hour${Math.round(hours) === 1 ? "" : "s"}`;
    return `Happy for ${when} more, then it wants ${WANTS[n]}.`;
  };
  const showNeeds = () => {
    root.querySelectorAll("[data-need]").forEach((bar) => {
      const v = level(bar.dataset.need);
      const pct = `${Math.round(v * 100)}%`;
      bar.setAttribute("aria-valuenow", String(Math.round(v * 100)));
      bar.setAttribute("aria-valuetext", pct);
      root.querySelector(`[data-pct="${bar.dataset.need}"]`).textContent = pct;
      bar.style.setProperty("--level", v.toFixed(3));
      bar.classList.toggle("is-low", v < SULK);
    });
    root.classList.toggle("is-sulking", sulking());
    $(".goatchi__lasts").textContent = lasts();
  };

  const daysToTuzla = () => Math.ceil((dayOne - Date.now()) / 864e5);
  // The goat's look at rest: sulking, then hungry, packing in the last week before Tuzla, happy at GoatConf and when
  // every need is nearly full, and otherwise itself.
  const mood = () => {
    if (sulking()) return "sulking";
    if (level("food") < 0.5 && level("food") <= Math.min(level("play"), level("sleep"))) return "hungry";
    const d = daysToTuzla();
    if (d >= 1 && d <= 7) return "packing";
    if ((d <= 0 && d > -3) || NEEDS.every((n) => level(n) >= 0.9)) return "happy";
    return "rest";
  };
  const restLook = () => (mood() !== "rest" && look(mood())) || goatState.src;
  // Postcards from Tuzla at so many days kept: earned once each, kept with the goat.
  const earn = () => {
    const days = daysKept(Date.now());
    const fresh = cards.map((c) => +c.dataset.day).filter((d) => days >= d && !goatState.cards.includes(d));
    if (!fresh.length) return false;
    goatState.cards.push(...fresh);
    save();
    return true;
  };
  const showCards = () => cards.forEach((c) => {
    const got = goatState.cards.includes(+c.dataset.day);
    c.querySelector("figure").hidden = !got;
    c.querySelector(".goatchi__card-lock").hidden = got;
  });
  let preloaded = "";
  const preload = () => {
    if (preloaded === goatState.pose) return;
    preloaded = goatState.pose;
    Object.values(posesOf(goatState.pose)).flat().forEach((src) => { const i = new Image(); i.decoding = "async"; i.src = src; });
  };

  // What the goat says when nothing has just happened: sulking, or the days to Tuzla.
  const trip = () => {
    const days = daysToTuzla();
    if (days > 1) return `${days} days to Tuzla!`;
    if (days === 1) return "Tuzla tomorrow!";
    if (days > -3) return "It's GoatConf!";
    return "Back from Tuzla. Baaa!";
  };
  let holding = 0;
  const speak = (text, ms = 0) => {
    say.textContent = text;
    clearTimeout(holding);
    holding = ms ? setTimeout(() => { holding = 0; render(); }, ms) : 0;
  };
  const gone = $(".goatchi__gone");
  const render = () => {
    const left = goatState ? leftAt() : 0;
    const kept = !!goatState && !left;
    document.documentElement.classList.toggle("goatchi-kept", kept);
    playing.hidden = !kept;
    empty.hidden = !!goatState;
    gone.hidden = !left;
    if (left) {
      const days = daysKept(left);
      hike.src = look("hiking") || hikeSrc;
      $(".goatchi__gone-line").textContent = `${goatState.name} went exploring the hills above Tuzla. You kept ${goatState.name.startsWith("The ") ? "it" : "them"} for ${days} day${days === 1 ? "" : "s"}.`;
      picks.forEach((b) => b.setAttribute("aria-pressed", "false"));
      return;
    }
    picks.forEach((b) => b.setAttribute("aria-pressed", String(kept && b.dataset.pose === goatState.pose)));
    if (!kept) return;
    preload();
    goat.src = restLook();
    goat.style.scale = "";
    stage.dataset.mood = mood();
    goat.alt = goatState.name;
    $(".goatchi__name").textContent = goatState.name;
    $(".goatchi__kept").textContent = `${keptLine(daysKept(Date.now()))}${goatState.challenge ? ", in challenge mode" : ""}`;
    showNeeds();
    const speaker = $('[data-cheer="speaker"]');
    if (goatState.speaker) { speaker.href = goatState.speaker; speaker.textContent = `Read about ${goatState.name.replace(/'s goat$/, "")}`; }
    root.querySelectorAll("[data-cheer]").forEach((a) => a.classList.toggle("is-done", goatState.cheered.includes(a.dataset.cheer)));
    $(".goatchi__trip").textContent = trip().replace("!", ".");
    const news = earn();
    showCards();
    if (news) speak("A postcard from Tuzla!", 3200);
    else speak(sulking() ? "Baaa…" : trip());
  };

  // A small move for the goat, by transform only; with reduced motion it stays where it is.
  const hop = () => still ? null : goat.animate([
    { transform: "none", easing: "cubic-bezier(.4,0,.6,1)" },
    { transform: "translateY(4%) scale(1.06, 0.9)", offset: 0.18, easing: "cubic-bezier(.2,.6,.4,1)" },
    { transform: "translateY(-22%) scale(0.95, 1.06) rotate(-4deg)", offset: 0.5, easing: "cubic-bezier(.5,0,.8,.4)" },
    { transform: "translateY(3%) scale(1.06, 0.92)", offset: 0.8, easing: "ease-out" },
    { transform: "none" },
  ], { duration: 760 });
  // For a moment the goat is shown eating, playing or asleep, moving as it does, then it is itself again.
  let showing = 0;
  // A frame painted on a larger canvas says how much larger after #s=, and is shown that much larger, from its
  // bottom middle, so the goat stays its own size.
  const show = (src, ms, act) => {
    goat.src = src;
    goat.style.scale = (src.split("#s=")[1]) || "";
    stage.classList.remove("is-eating", "is-playing", "is-sleeping", "is-petted", "is-fidget");
    stage.classList.add(act);
    clearTimeout(showing);
    showing = setTimeout(() => { stage.classList.remove(act); goat.style.scale = ""; if (goatState) goat.src = restLook(); }, ms);
  };
  const acts = {
    feed: () => { fill("food", 1); show(look("eating") || food[Math.floor(Math.random() * food.length)], 2600, "is-eating"); speak("Yum! Baaa!", 2600); },
    play: () => { fill("play", 1); const p = look("playing"); if (p) show(p, 2200, "is-playing"); hop(); speak("Baaa! Again!", 2200); },
    sleep: () => { fill("sleep", 1); show(look("sleeping") || sleepSrc, 3200, "is-sleeping"); speak("Zzz…", 3200); },
  };

  // Petting (ADR goat-animations): a tap on the goat shows a heart, a happy hop and a line, and lifts play a little,
  // at most three times an hour.
  const heart = document.createElement("b");
  heart.className = "goat-heart";
  heart.setAttribute("aria-hidden", "true");
  heart.textContent = "\u2665";
  stage.append(heart);
  let pets = [];
  goat.addEventListener("click", () => {
    if (!goatState || leftAt()) return;
    heart.getAnimations().forEach((a) => a.cancel());
    if (!still) heart.animate([
      { opacity: 0, transform: "translate(-50%, 0) scale(.4)" },
      { opacity: 1, transform: "translate(-50%, -40%) scale(1.1)", offset: 0.25 },
      { opacity: 0, transform: "translate(-50%, -160%) scale(1)" },
    ], { duration: 1300, easing: "ease-out" });
    const petted = look("anim-petted");
    if (petted && !still) show(petted, 1300, "is-petted");
    hop();
    pets = pets.filter((t) => Date.now() - t < 3600e3);
    if (pets.length < 3) { pets.push(Date.now()); fill("play", 0.1); save(); showNeeds(); }
    speak(["Baaa!", "Again!", "That's nice.", "Baaa, thank you!"][Math.floor(Math.random() * 4)], 1600);
  });

  // Asking before a goat is let go or swapped, on the page itself.
  let onYes = null;
  const ask = (text, yes) => {
    confirmRow.querySelector("span").textContent = text;
    confirmRow.hidden = false;
    onYes = yes;
    confirmRow.querySelector('[data-act="yes"]').focus();
  };
  const done = () => { confirmRow.hidden = true; onYes = null; };
  // "The goat" reads as "the goat" inside a sentence; a speaker's goat keeps their name.
  const called = (name) => name.replace(/^The /, "the ");
  const adopt = (b) => {
    if (!store || !canKeep()) {
      empty.querySelector("p").textContent = "This browser does not let pages keep anything, so your goat could not stay. Try another browser, or a window that is not private.";
      picks.forEach((p) => { p.disabled = true; });
      return;
    }
    // A goat swapped for another stops its reminders; the new goat starts with them off.
    if (goatState && goatState.remind) remindOff();
    const now = Date.now();
    goatState = { pose: b.dataset.pose, name: b.dataset.name, src: b.dataset.src, speaker: b.dataset.speaker || "", since: now,
      needs: Object.fromEntries(NEEDS.map((n) => [n, [1, now]])), cheered: [], cards: [],
      challenge: !!document.querySelector(".goatchi__challenge:checked") };
    save();
    render();
    startApp();
    showApp();
    speak(`Baaa! Hello!`, 2400);
    root.scrollIntoView({ behavior: still ? "auto" : "smooth", block: "start" });
  };

  root.addEventListener("click", (e) => {
    const act = e.target.closest("[data-act]");
    const cheer = e.target.closest("[data-cheer]");
    if (cheer && goatState && !goatState.cheered.includes(cheer.dataset.cheer)) {
      // The first time only: every need gets a lift, saved before the link is followed.
      goatState.cheered.push(cheer.dataset.cheer);
      NEEDS.forEach((n) => fill(n, 0.3));
      save();
      showNeeds();
      cheer.classList.add("is-done");
      return;
    }
    if (!act || !goatState || leftAt()) return;
    const name = act.dataset.act;
    if (name === "yes") { const f = onYes; done(); if (f) f(); return; }
    if (name === "no") { done(); return; }
    if (name === "let-go") { ask(`Let ${called(goatState.name)} go?`, () => { if (goatState.remind) remindOff(); goatState = null; save(); render(); showApp(); }); return; }
    if (acts[name]) { done(); acts[name](); save(); showNeeds(); }
  });
  picks.forEach((b) => b.addEventListener("click", () => {
    if (!goatState || leftAt()) { adopt(b); return; }
    if (goatState.pose === b.dataset.pose) { root.scrollIntoView({ behavior: still ? "auto" : "smooth", block: "start" }); return; }
    root.scrollIntoView({ behavior: still ? "auto" : "smooth", block: "start" });
    ask(`Swap ${called(goatState.name)} for ${called(b.dataset.name)}? The new goat starts fresh.`, () => adopt(b));
  }));
  // Installable, for this page only, once a goat is kept: the service worker keeps Goatchi for playing offline and,
  // only if the player turns them on, makes the reminders on this device (goatchi-sw.js). Nothing is registered
  // before a goat is picked.
  const TAG = "goatchi-check";
  const install = $(".goatchi__install"), remind = $(".goatchi__remind");
  const remindBox = remind.querySelector("input"), remindNote = $(".goatchi__remind-note");
  let reg = null, installPrompt = null;
  const canRemind = async () => {
    if (!reg || !("periodicSync" in reg) || !("Notification" in window) || !navigator.permissions) return false;
    try { return (await navigator.permissions.query({ name: "periodic-background-sync" })).state === "granted"; } catch (e) { return false; }
  };
  const showApp = async () => {
    install.hidden = !installPrompt || !goatState;
    remind.hidden = !goatState || !(await canRemind());
    remindBox.checked = !!(goatState && goatState.remind) && Notification.permission === "granted";
  };
  const startApp = () => {
    if (reg || !("serviceWorker" in navigator)) return;
    navigator.serviceWorker.register("goatchi-sw.js", { scope: "./goatchi" })
      .then(() => navigator.serviceWorker.ready).then((r) => { reg = r; showApp(); }).catch(() => {});
  };
  const remindOff = async () => {
    if (goatState) goatState.remind = false;
    try { if (reg && reg.periodicSync) await reg.periodicSync.unregister(TAG); } catch (e) { /* nothing was registered */ }
    await mirror(null);
  };
  addEventListener("beforeinstallprompt", (e) => { e.preventDefault(); installPrompt = e; showApp(); });
  addEventListener("appinstalled", () => { installPrompt = null; showApp(); });
  install.querySelector("button").addEventListener("click", async () => {
    if (!installPrompt) return;
    installPrompt.prompt();
    await installPrompt.userChoice;
    installPrompt = null;
    showApp();
  });
  remindBox.addEventListener("change", async () => {
    remindNote.textContent = "";
    if (!goatState) return;
    if (!remindBox.checked) { await remindOff(); save(); return; }
    if (await Notification.requestPermission() !== "granted") {
      remindBox.checked = false;
      remindNote.textContent = "This browser is set not to show Goatchi's notifications; you can allow them in its settings for this site.";
      return;
    }
    try { await reg.periodicSync.register(TAG, { minInterval: 12 * 3600e3 }); } catch (e) {
      remindBox.checked = false;
      remindNote.textContent = "This browser would not let Goatchi check on your goat.";
      return;
    }
    goatState.remind = true;
    save();
    remindNote.textContent = "Your goat will tell you on this device when it sulks, at most once a day.";
  });

  // While the page stays open, the needs keep drifting.
  setInterval(() => { if (goatState && !holding) render(); }, 60e3);
  // A goat at rest with painted frames fidgets now and then: flicks its ears, wags its tail, scratches, sneezes or
  // stretches. Not while it eats, plays or sleeps, nor with reduced motion.
  const FIDGETS = { ears: 500, tail: 700, scratch: 1400, sneeze: 600, stretch: 1700 };
  const fidget = () => {
    setTimeout(fidget, 7000 + Math.random() * 6000);
    if (still || !goatState || leftAt() || !["rest", "happy"].includes(mood()) || document.hidden) return;
    if (["is-eating", "is-playing", "is-sleeping", "is-petted", "is-fidget"].some((c) => stage.classList.contains(c))) return;
    const can = Object.keys(FIDGETS).filter((f) => look(`anim-${f}`));
    if (!can.length) return;
    const f = can[Math.floor(Math.random() * can.length)];
    show(look(`anim-${f}`), FIDGETS[f], "is-fidget");
  };
  setTimeout(fidget, 5000);
  render();
  if (goatState) startApp();
})();
