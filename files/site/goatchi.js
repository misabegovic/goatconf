// Goatchi: keep a GoatConf goat (ADR goat-tamagotchi-on-the-site). The goat lives in this browser's storage only:
// which goat, and for each need its value and when it was last set. A need's value now is worked out from the time
// passed, so nothing runs while you are away. Each need empties over a day and a half; below a quarter the goat
// sulks and says so; it never dies. Picking, swapping and letting go all happen on this page, and nothing is sent
// anywhere.
(() => {
  const root = document.getElementById("goatchi");
  if (!root) return;
  const KEY = "goatconf-goatchi";
  const EMPTY_AFTER = 36 * 3600e3;
  const SULK = 0.25;
  const NEEDS = ["food", "play", "sleep"];
  const still = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const $ = (s) => root.querySelector(s);
  const playing = $(".goatchi__play"), empty = $(".goatchi__empty"), goat = $(".goatchi__goat"), say = $(".goatchi__say");
  const confirmRow = $(".goatchi__confirm");
  const picks = [...document.querySelectorAll(".goatchi__pick-goat")];
  const food = root.dataset.food.split("|"), sleepSrc = root.dataset.sleep;
  const dayOne = new Date(`${root.dataset.day}T09:00:00+02:00`);

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
      return s && s.pose && s.src && s.needs && NEEDS.every((n) => Array.isArray(s.needs[n])) ? s : null;
    } catch (e) { return null; }
  };
  let goatState = store ? load() : null;
  const save = () => { if (goatState) store.setItem(KEY, JSON.stringify(goatState)); else store.removeItem(KEY); };
  const level = (n) => Math.max(0, Math.min(1, goatState.needs[n][0] - (Date.now() - goatState.needs[n][1]) / EMPTY_AFTER));
  const fill = (n, by) => { goatState.needs[n] = [Math.min(1, (by === 1 ? 0 : level(n)) + by), Date.now()]; };
  const sulking = () => NEEDS.some((n) => level(n) < SULK);
  // Each need as a bar, full to empty, and the goat sulking when any runs low.
  const showNeeds = () => {
    root.querySelectorAll("[data-need]").forEach((bar) => {
      const v = level(bar.dataset.need);
      bar.setAttribute("aria-valuenow", String(Math.round(v * 100)));
      bar.style.setProperty("--level", v.toFixed(3));
      bar.classList.toggle("is-low", v < SULK);
    });
    root.classList.toggle("is-sulking", sulking());
  };

  // What the goat says when nothing has just happened: sulking, or the days to Tuzla.
  const trip = () => {
    const days = Math.ceil((dayOne - Date.now()) / 864e5);
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
  const render = () => {
    const kept = !!goatState;
    playing.hidden = !kept;
    empty.hidden = kept;
    picks.forEach((b) => b.setAttribute("aria-pressed", String(kept && b.dataset.pose === goatState.pose)));
    if (!kept) return;
    goat.src = goatState.src;
    goat.alt = goatState.name;
    $(".goatchi__name").textContent = goatState.name;
    showNeeds();
    const speaker = $('[data-cheer="speaker"]');
    if (goatState.speaker) { speaker.href = goatState.speaker; speaker.textContent = `Read about ${goatState.name.replace(/'s goat$/, "")}`; }
    root.querySelectorAll("[data-cheer]").forEach((a) => a.classList.toggle("is-done", goatState.cheered.includes(a.dataset.cheer)));
    $(".goatchi__trip").textContent = trip().replace("!", ".");
    speak(sulking() ? "Baaa…" : trip());
  };

  // A small move for the goat, by transform only; with reduced motion it stays where it is.
  const hop = () => still ? null : goat.animate([
    { transform: "none", easing: "cubic-bezier(.4,0,.6,1)" },
    { transform: "translateY(4%) scale(1.06, 0.9)", offset: 0.18, easing: "cubic-bezier(.2,.6,.4,1)" },
    { transform: "translateY(-22%) scale(0.95, 1.06) rotate(-4deg)", offset: 0.5, easing: "cubic-bezier(.5,0,.8,.4)" },
    { transform: "translateY(3%) scale(1.06, 0.92)", offset: 0.8, easing: "ease-out" },
    { transform: "none" },
  ], { duration: 760 });
  // For a moment the goat is shown eating or asleep, then it is itself again.
  const show = (src, ms) => { goat.src = src; setTimeout(() => { if (goatState) goat.src = goatState.src; }, ms); };
  const acts = {
    feed: () => { fill("food", 1); show(food[Math.floor(Math.random() * food.length)], 2600); speak("Yum! Baaa!", 2600); },
    play: () => { fill("play", 1); hop(); speak("Baaa! Again!", 1800); },
    sleep: () => { fill("sleep", 1); show(sleepSrc, 3200); speak("Zzz…", 3200); },
  };

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
    const now = Date.now();
    goatState = { pose: b.dataset.pose, name: b.dataset.name, src: b.dataset.src, speaker: b.dataset.speaker || "", since: now,
      needs: Object.fromEntries(NEEDS.map((n) => [n, [1, now]])), cheered: [] };
    save();
    render();
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
    if (!act || !goatState) return;
    const name = act.dataset.act;
    if (name === "yes") { const f = onYes; done(); if (f) f(); return; }
    if (name === "no") { done(); return; }
    if (name === "let-go") { ask(`Let ${called(goatState.name)} go?`, () => { goatState = null; save(); render(); }); return; }
    if (acts[name]) { done(); acts[name](); save(); showNeeds(); }
  });
  picks.forEach((b) => b.addEventListener("click", () => {
    if (!goatState) { adopt(b); return; }
    if (goatState.pose === b.dataset.pose) { root.scrollIntoView({ behavior: still ? "auto" : "smooth", block: "start" }); return; }
    root.scrollIntoView({ behavior: still ? "auto" : "smooth", block: "start" });
    ask(`Swap ${called(goatState.name)} for ${called(b.dataset.name)}? The new goat starts fresh.`, () => adopt(b));
  }));
  // While the page stays open, the needs keep drifting.
  setInterval(() => { if (goatState && !holding) render(); }, 60e3);
  render();
})();
