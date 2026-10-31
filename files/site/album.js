// The phone menu opens without a script; this closes it on Escape, on a tap outside it, or when a link in it is followed.
(() => {
  const menu = document.querySelector(".topbar__menu");
  if (!menu) return;
  const close = () => { menu.open = false; };
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && menu.open) { close(); menu.querySelector("summary").focus(); }
  });
  document.addEventListener("click", (e) => { if (menu.open && !menu.contains(e.target)) close(); });
  menu.querySelectorAll("a").forEach((a) => a.addEventListener("click", close));
})();

// One goat on screen at a time (ADR goat-mascot): it peeks over the open slot or the speaker's card nearest
// the middle of the screen, in that slot's role or as that speaker's own goat, or sits on a Tuzla or food
// photo as that photo's painted scene, and hops there as you scroll or
// point. While it waits it bobs, wiggles, stretches, turns its head to look around or plays peek-a-boo, and it
// looks towards the pointer when it comes close. Tapped or clicked, it plays the next of its tricks. A turn swaps in the goat's painted head turned left or
// right, from a second sheet loaded after the page; its body stays the painted goat's own. It moves by transform only, and appears once its sprite sheet
// has loaded, so nothing waits on the network mid-move. On Save-Data or a 2G connection there is no goat;
// without the script every slot keeps its own goat; with reduced motion the goat simply appears where it is.
(() => {
  const peeks = [...document.querySelectorAll(".peek--art, .peek--face, .goat-scene")];
  if (!peeks.length) return;
  const root = document.documentElement;
  const net = navigator.connection;
  if (net && (net.saveData || /2g$/.test(net.effectiveType || ""))) { root.classList.add("goat-none"); return; }
  root.classList.add("goat-one");
  const still = matchMedia("(prefers-reduced-motion: reduce)").matches;
  // One stop per element; a stop with several goats (the lakes photo, the goodbye) shows a different one each visit.
  const slots = [];
  peeks.forEach((p) => {
    const at = slots.find((s) => s.slot === p.parentElement);
    if (at) at.alts.push(p);
    else slots.push({ slot: p.parentElement, peek: p, alts: [p], turn: 0, scene: p.classList.contains("goat-scene") });
  });
  const next = (s) => { s.peek = s.alts[s.turn++ % s.alts.length]; };
  const stage = document.createElement("div");
  stage.className = "goat-one__stage";
  stage.setAttribute("aria-hidden", "true");
  stage.style.visibility = "hidden";
  let goat = null, current = null, wanted = null, busy = false, idling = false, down = true, facing = "front";
  const turnSheets = new Set(), gazeSheets = new Set();

  // Every transform names the same functions in the same order, so a turn passes through a thin goat
  // instead of spinning, and nothing is decomposed into a matrix.
  const T = (y = "0%", sx = 1, sy = 1, r = 0) => `translateY(${y}) rotate(${r}deg) scale(${sx}, ${sy})`;
  const REST = T(), HIDDEN = T("108%");
  // The goat takes the slot's goat's look: its body from the sheet, its eyes, and its head band for turning.
  // The element stays the same, so a change mid-move does not interrupt the move.
  const dress = (s) => {
    if (!goat) {
      goat = document.createElement("span");
      goat.style.transform = HIDDEN;
      stage.append(goat);
    }
    const pose = goat.style.transform;
    const own = s.peek.style;
    goat.className = "goat";
    goat.setAttribute("style", `--beat:${own.getPropertyValue("--beat")};--edge:${own.getPropertyValue("--edge")};aspect-ratio:${own.aspectRatio}`);
    goat.style.transform = pose;
    goat.innerHTML = `<i class="goat-body"></i>${s.peek.innerHTML}<i class="goat-head"></i>`;
    goat.rest = { backgroundImage: own.backgroundImage, backgroundSize: own.backgroundSize, backgroundPosition: own.backgroundPosition };
    Object.assign(goat.querySelector(".goat-body").style, goat.rest);
    goat.dataset.gaze = s.peek.dataset.gaze || "";
    gazing = "11";
    const blink = goat.querySelector(".goat-blink");
    if (blink) blink.style.backgroundImage = own.backgroundImage;
    goat.dataset.turn = s.peek.dataset.turn || "";
    if (goat.dataset.turn) {
      const [src, x, y, w, h, size, row, , cut] = goat.dataset.turn.split("|");
      Object.assign(goat.querySelector(".goat-head").style, { left: x, top: y, width: w, height: h, backgroundImage: `url(${src})`, backgroundSize: `${size} auto` });
      goat.style.setProperty("--cut", cut);
      goat.dataset.row = row;
    }
    stage.style.setProperty("--edge", own.getPropertyValue("--edge"));
    stage.style.setProperty("--size", own.getPropertyValue("--size") || "1");
    face(facing);
  };
  // Which way the goat looks: its own painted head turned left or right, or straight at you. A goat whose
  // turned heads are not painted or not loaded yet keeps looking at you.
  const canTurn = () => !!goat && ((!!goat.dataset.turn && turnSheets.has(goat.dataset.turn.split("|")[0])) || canGaze());
  const face = (dir) => {
    facing = dir;
    if (!goat) return;
    // A goat painted looking in nine directions turns with those frames: left, right, or back at you.
    if (canGaze()) { gazeTo(1, dir === "left" ? 0 : dir === "right" ? 2 : 1); return; }
    if (dir === "front" || !canTurn()) { goat.classList.remove("is-turned"); return; }
    const parts = goat.dataset.turn.split("|");
    goat.querySelector(".goat-head").style.backgroundPosition = `${dir === "left" ? "0%" : parts[7]} ${goat.dataset.row}`;
    goat.classList.add("is-turned");
  };
  // A goat painted looking in nine directions (a speaker's goat, ADR goatchi-full-game) looks where the mouse is,
  // anywhere on the page: its whole picture is swapped for the one looking that way, from a sheet of nine laid out
  // like its own cell, so only the head moves. Looking ahead it is its own picture again, and blinks.
  let gazing = "11", followed = 0, lookBack = 0, wish = "11", wishSince = 0, lookedAt = 0;
  const canGaze = () => !!goat && !!goat.dataset.gaze && gazeSheets.has(goat.dataset.gaze);
  const gazeTo = (r, c) => {
    const key = `${r}${c}`;
    if (!goat || key === gazing) return;
    gazing = key;
    const body = goat.querySelector(".goat-body");
    if (key === "11" || !canGaze()) { Object.assign(body.style, goat.rest); goat.classList.remove("is-gazing"); return; }
    Object.assign(body.style, { backgroundImage: `url(${goat.dataset.gaze})`, backgroundSize: "300% auto", backgroundPosition: `${c * 50}% ${r * 50}%` });
    goat.classList.add("is-gazing");
  };
  // A look: the head turns at the top of a small lift and squash, as a turn does, then the goat settles.
  const glance = (key) => {
    lookedAt = Date.now();
    setTimeout(() => gazeTo(+key[0], +key[1]), 110);
    play(goat, [
      { transform: REST, easing: "ease-out" }, { transform: T("-2.5%", 0.985, 1.015), offset: 0.45, easing: "ease-in-out" },
      { transform: T("0.8%", 1.01, 0.99), offset: 0.8 }, { transform: REST },
    ], { duration: 300 }).catch(() => {});
  };
  // The direction from its eyes to a point, in eight sectors; close to its face, at you; far away, it has not noticed.
  const SECTORS = [[1, 2], [2, 2], [2, 1], [2, 0], [1, 0], [0, 0], [0, 1], [0, 2]];
  const dirOf = (x, y) => {
    const r = goat.getBoundingClientRect();
    const dx = x - (r.left + r.width / 2), dy = y - (r.top + r.height * 0.35), d = Math.hypot(dx, dy);
    if (d > 700) return null;
    if (d < r.width * 0.6) return "11";
    return SECTORS[(Math.round(Math.atan2(dy, dx) / (Math.PI / 4)) + 8) % 8].join("");
  };
  // It notices you calmly: the pointer has to rest in one direction for a moment before it looks, it holds each
  // look for a while, and three seconds after the pointer stops it looks back at you and its own moves go on.
  const follow = (x, y) => {
    const d = dirOf(x, y);
    if (d === null) return;
    followed = Date.now();
    if (d !== wish) { wish = d; wishSince = followed; }
    clearTimeout(lookBack);
    lookBack = setTimeout(() => { wish = "11"; if (gazing !== "11") glance("11"); }, 3000);
  };
  const following = () => Date.now() - followed < 3000;
  setInterval(() => {
    if (!canGaze() || down || (busy && !idling) || wish === gazing) return;
    const now = Date.now();
    if (now - wishSince >= 350 && now - lookedAt >= 1000) glance(wish);
  }, 120);
  // A turn: the head swings at the top of a small lift and squash, then the goat settles.
  const turnTo = (dir) => {
    if (dir === facing) return Promise.resolve();
    setTimeout(() => face(dir), 120);
    return play(goat, [
      { transform: REST, easing: "ease-out" }, { transform: T("-3%", 0.98, 1.02), offset: 0.45, easing: "ease-in-out" },
      { transform: T("1%", 1.015, 0.985), offset: 0.8 }, { transform: REST },
    ], { duration: 300 });
  };
  // A pause that ends early once `stop` says so.
  const wait = (ms, stop = () => false) => new Promise((r) => {
    const end = Date.now() + ms;
    const tick = () => (Date.now() >= end || stop() ? r() : setTimeout(tick, 50));
    tick();
  });
  // Whether the goat is wanted at another slot than the one it is on, or for a trick.
  const called = () => !!wanted && wanted !== current;
  let asked = false;
  const interrupted = () => called() || asked;
  // The goat lives inside the slot it stands on, placed as the slot's own goat would be, so it moves with
  // the slot whatever the page does: fonts and images arriving, filters, a resize, a tilted card.
  const settle = (s) => {
    // On a photo it sits in the photo's corner (CSS); over a slot it stands where the slot's own goat would.
    stage.classList.toggle("is-scene", s.scene);
    const own = getComputedStyle(s.peek);
    // A goat sized by its height (a whole goat on a band) has no width while hidden, so it is measured shown.
    let width = own.width;
    if (width === "auto") {
      s.peek.style.display = "block";
      width = `${s.peek.getBoundingClientRect().width}px`;
      s.peek.style.display = "";
    }
    stage.style.width = s.scene ? "" : width;
    stage.style.right = s.scene ? "" : own.right;
    stage.style.bottom = s.scene ? "" : own.bottom;
    // On a photo it stands on the photo's own bottom edge, above the caption and the text under it.
    // A food card keeps its photo clear: the goat sits in the white corner beside the price instead (CSS).
    const food = !!s.scene && !!s.slot.querySelector(".price");
    stage.classList.toggle("is-food", food);
    const img = s.scene && !food && s.slot.querySelector("img");
    if (img) stage.style.bottom = `${s.slot.clientHeight - (img.offsetTop + img.offsetHeight) - 4}px`;
    const was = stage.parentElement;
    if (was && was !== s.slot) was.classList.remove("has-goat");
    s.slot.classList.add("has-goat");
    s.slot.append(stage);
  };
  const play = (el, frames, opts) => {
    const a = el.animate(frames, { fill: "forwards", ...opts });
    return a.finished.then(() => { el.style.transform = frames[frames.length - 1].transform; a.cancel(); });
  };

  // Ducking: a small lift first, as if pushing off, then down behind the edge, hooves last.
  const onPhoto = () => stage.classList.contains("is-scene");
  const TINY = T("0%", 0.02, 0.02);
  const duck = () => {
    stage.classList.add("is-tucked");
    down = true;
    if (onPhoto()) return play(goat, [
      { transform: REST, easing: "cubic-bezier(.3,0,.6,1)" },
      { transform: T("-4%", 1.06, 1.06, -4), offset: 0.3, easing: "cubic-bezier(.55,0,.85,.3)" },
      { transform: TINY },
    ], { duration: 380 });
    return play(goat, [
      { transform: REST, easing: "cubic-bezier(.3,0,.6,1)" },
      { transform: T("-5%", 0.97, 1.04), offset: 0.28, easing: "cubic-bezier(.55,0,.85,.3)" },
      { transform: HIDDEN },
    ], { duration: 420 });
  };
  // Popping up: a stretch on the way, an overshoot, a squash as it lands on its hooves, and a settle.
  const pop = () => {
    stage.classList.add("is-tucked");
    down = false;
    // On a photo: out of the corner, a little too big and tilted, back, and settled.
    if (onPhoto()) return play(goat, [
      { transform: TINY, easing: "cubic-bezier(.2,.75,.35,1)" },
      { transform: T("-6%", 1.1, 1.1, -5), offset: 0.55, easing: "cubic-bezier(.5,0,.6,1)" },
      { transform: T("1%", 0.96, 0.96, 2), offset: 0.78, easing: "ease-out" },
      { transform: REST },
    ], { duration: 620 }).then(() => stage.classList.remove("is-tucked"));
    return play(goat, [
      { transform: HIDDEN, easing: "cubic-bezier(.2,.75,.35,1)" },
      { transform: T("-10%", 0.94, 1.08), offset: 0.5, easing: "cubic-bezier(.5,0,.6,1)" },
      { transform: T("2%", 1.06, 0.94), offset: 0.74, easing: "ease-out" },
      { transform: T("-1%", 0.99, 1.01), offset: 0.88 },
      { transform: REST },
    ], { duration: 640 }).then(() => stage.classList.remove("is-tucked"));
  };
  // Hopping to another slot: it crouches and turns towards where it is going, takes off stretched, arcs
  // over, changes into the new slot's goat at the top, lands with a squash and turns back to face you. It
  // moves into the new slot first and flies the difference away, so it lands exactly where the slot is.
  const hop = (s) => {
    const a = stage.getBoundingClientRect();
    settle(s);
    const b = stage.getBoundingClientRect();
    const dx = a.left - b.left, dy = a.top - b.top, far = Math.hypot(dx, dy);
    const turn = dx > 8 ? -1 : 1;
    const arc = Math.min(150, 50 + far * 0.3);
    const time = Math.min(900, 620 + far * 0.4);
    // It looks where it is going, then back at you as it lands.
    if (canTurn() && Math.abs(dx) > 8) face(turn < 0 ? "left" : "right");
    setTimeout(() => face("front"), time * 0.86);
    setTimeout(() => { if (current === s) dress(s); }, time * 0.5);
    const body = play(goat, [
      { transform: REST, easing: "cubic-bezier(.4,0,.6,1)" },
      { transform: T("6%", 1.08, 0.86), offset: 0.16, easing: "cubic-bezier(.2,.6,.4,1)" },
      { transform: T(`${-arc * 0.55}px`, 0.92, 1.12, -4 * turn), offset: 0.32, easing: "cubic-bezier(.3,.6,.5,1)" },
      { transform: T(`${-arc}px`, 1, 1, -6 * turn), offset: 0.52, easing: "cubic-bezier(.5,0,.8,.4)" },
      { transform: T("5%", 1.12, 0.84), offset: 0.8, easing: "cubic-bezier(.3,.6,.5,1)" },
      { transform: T("-2%", 0.97, 1.04), offset: 0.9, easing: "ease-out" },
      { transform: REST },
    ], { duration: time });
    const away = `translate(${dx}px, ${dy}px)`, home = "translate(0px, 0px)";
    const trip = stage.animate([
      { transform: away }, { transform: away, offset: 0.18, easing: "cubic-bezier(.35,0,.65,1)" },
      { transform: home, offset: 0.8 }, { transform: home },
    ], { duration: time });
    return Promise.all([body, trip.finished]);
  };

  const pick = () => {
    const mid = innerHeight * 0.45;
    let best = null, gap = Infinity;
    for (const s of slots) {
      const r = s.slot.getBoundingClientRect();
      if (r.top < 70 || r.top > innerHeight - 12) continue;
      const d = Math.abs(r.top - mid);
      if (d < gap) { gap = d; best = s; }
    }
    return best;
  };
  const go = async (s) => {
    if (!s) return;
    wanted = s;
    // A move while it waits gives way at once; the goat goes on when it ends.
    if (busy) { if (idling) { goat.getAnimations().forEach((a) => a.finish()); face("front"); } return; }
    if (s === current) return;
    busy = true;
    const from = current;
    current = s;
    next(s);
    const arrive = () => { settle(s); dress(s); };
    // Whatever happens in a move, the goat is never left stuck: it ends up resting in the slot it went to.
    try {
      if (still) { arrive(); down = false; goat.style.transform = REST; return; }
      if (!from || down) {
        arrive();
        await pop();
      } else {
        // Far away, it ducks here and pops up there; near enough, it hops.
        const a = from.slot.getBoundingClientRect(), b = s.slot.getBoundingClientRect();
        if (from.scene || s.scene || Math.hypot(b.right - a.right, b.top - a.top) > innerHeight * 0.8) {
          await duck();
          arrive();
          await pop();
        } else {
          await hop(s);
          goat.style.transform = REST;
        }
      }
    } catch (e) {
      arrive(); face("front"); down = false; goat.style.transform = REST; stage.classList.remove("is-tucked");
    } finally {
      busy = false;
    }
    catchUp();
  };
  // A trick asked for while it was busy comes first, then where it was last asked to go, by a scroll or a pointer.
  const catchUp = () => {
    if (asked && !down) perform();
    else if (wanted && wanted !== current) go(wanted);
  };
  let tick = 0;
  const schedule = () => { cancelAnimationFrame(tick); tick = requestAnimationFrame(() => go(pick())); };

  // Moves while it waits, each one transform keyframes on the goat.
  const moves = {
    bob: () => play(goat, [REST, T("-6%"), REST, T("-6%"), REST].map((transform) => ({ transform, easing: "ease-in-out" })), { duration: 1700 }),
    wiggle: () => play(goat, [REST, T("0%", 1, 1, -7), T("0%", 1, 1, 6), T("0%", 1, 1, -3), REST].map((transform) => ({ transform, easing: "ease-in-out" })), { duration: 760 }),
    stretch: () => play(goat, [
      { transform: REST, easing: "ease-out" }, { transform: T("-3%", 0.95, 1.1), offset: 0.4, easing: "ease-in-out" },
      { transform: T("1%", 1.05, 0.95), offset: 0.7, easing: "ease-out" }, { transform: REST },
    ], { duration: 1300 }),
    // Looking around: its head turns one way, back to you, the other way, and back.
    // It stops looking as soon as it is wanted at another slot.
    look: async () => {
      if (canGaze()) {
        // A gazing goat glances about: a few directions, then back at you.
        for (let i = 0; i < 3 && !interrupted(); i++) {
          glance(SECTORS[Math.floor(Math.random() * SECTORS.length)].join(""));
          await wait(900 + Math.random() * 700, interrupted);
        }
        glance("11");
        await wait(300);
        return;
      }
      if (!canTurn()) return moves.bob();
      const [one, two] = Math.random() < 0.5 ? ["left", "right"] : ["right", "left"];
      for (const [dir, pause] of [[one, 900 + Math.random() * 500], ["front", 260], [two, 900 + Math.random() * 500]]) {
        if (interrupted()) break;
        await turnTo(dir);
        await wait(pause, interrupted);
      }
      await turnTo("front");
    },
    peekaboo: () => duck().then(() => wait(700, interrupted)).then(pop),
  };
  const idle = async () => {
    if (!busy && !down && goat && !(canGaze() && following())) {
      busy = idling = true;
      const names = Object.keys(moves);
      try { await moves[names[Math.floor(Math.random() * names.length)]](); } catch (e) { face("front"); goat.style.transform = REST; }
      busy = idling = false;
      catchUp();
    }
    setTimeout(idle, 3000 + Math.random() * 3000);
  };

  // Its tricks, one per tap or click, in turn, with something said between each: a jump for joy, a somersault and
  // a shake of its head. What it says is picked at random from what every goat says (written into the page by
  // tools/frame.py) and, for a speaker's goat, its own lines, never the same twice running.
  // A goat peeking over a slot is painted only down to the slot's edge, unless it is whole, so it never rises far enough to show
  // where the painting ends: it bounces instead of jumping, and ducks and pops up instead of a somersault.
  // With reduced motion it only speaks.
  const say = document.createElement("b");
  say.className = "goat-say";
  stage.append(say);
  const every = (() => { try { return JSON.parse(document.getElementById("goat-says").textContent); } catch (e) { return ["Baaa!"]; } })();
  let said = "";
  const meee = () => {
    const own = current && current.peek.dataset.says ? current.peek.dataset.says.split("|") : [];
    const lines = every.concat(own).filter((l) => l !== said);
    said = lines[Math.floor(Math.random() * lines.length)] || "Baaa!";
    say.textContent = said;
    // A wrapped line leaves the bubble at its widest; it is fitted to its longest line instead.
    say.style.width = "";
    say.style.transform = "none";
    const range = document.createRange();
    range.selectNodeContents(say);
    const rows = [...range.getClientRects()];
    if (rows.length > 1) {
      const cs = getComputedStyle(say);
      say.style.width = `${Math.ceil(Math.max(...rows.map((r) => r.width)) + parseFloat(cs.paddingLeft) + parseFloat(cs.paddingRight))}px`;
    }
    // Longer lines stay up longer, so they can be read.
    const duration = 1300 + said.length * 45;
    return play(say, still ? [{ opacity: 0 }, { opacity: 1, offset: 0.1 }, { opacity: 1, offset: 0.88 }, { opacity: 0 }] : [
      { opacity: 0, transform: "scale(0.4)", easing: "cubic-bezier(.2,.8,.3,1.3)" },
      { opacity: 1, transform: "scale(1)", offset: 0.12 }, { opacity: 1, transform: "scale(1)", offset: 0.88 },
      { opacity: 0, transform: "scale(0.9)" },
    ], { duration });
  };
  const jump = (up) => play(goat, [
    { transform: REST, easing: "cubic-bezier(.4,0,.6,1)" },
    { transform: T("6%", 1.1, 0.86), offset: 0.18, easing: "cubic-bezier(.2,.6,.4,1)" },
    { transform: T(up, 0.92, 1.1, -5), offset: 0.48, easing: "cubic-bezier(.5,0,.8,.4)" },
    { transform: T("4%", 1.1, 0.86), offset: 0.78, easing: "ease-out" },
    { transform: T("-2%", 0.97, 1.03), offset: 0.9 },
    { transform: REST },
  ], { duration: 760 });
  // It crouches, springs up, flips once round its middle in the air and lands with a squash. The picture
  // turns over but is never mirrored.
  const somersault = () => {
    goat.style.transformOrigin = "50% 50%";
    return play(goat, [
      { transform: REST, easing: "cubic-bezier(.4,0,.6,1)" },
      { transform: T("6%", 1.08, 0.88), offset: 0.15, easing: "cubic-bezier(.2,.6,.4,1)" },
      { transform: T("-42%", 1, 1, -180), offset: 0.5, easing: "cubic-bezier(.4,0,.8,.6)" },
      { transform: T("-6%", 1, 1, -350), offset: 0.76, easing: "ease-out" },
      { transform: T("3%", 1.08, 0.9, -360), offset: 0.88, easing: "ease-out" },
      { transform: T("0%", 1, 1, -360) },
    ], { duration: 1000 }).finally(() => { goat.style.transformOrigin = ""; goat.style.transform = REST; });
  };
  const whole = () => onPhoto() || current.peek.classList.contains("peek--whole");
  const speak = () => Promise.all([moves.stretch(), meee()]);
  const tricks = [
    () => (whole() ? jump("-45%") : jump("-9%")),
    speak,
    () => (whole() ? somersault() : duck().then(() => wait(250)).then(pop)),
    speak,
    // A goat without its turned heads wiggles instead.
    async () => {
      if (!canTurn()) return moves.wiggle();
      for (const dir of ["left", "right", "left"]) { await turnTo(dir); await wait(280); }
      await turnTo("front");
    },
    speak,
  ];
  let trick = 0;
  const perform = async () => {
    asked = false;
    busy = true;
    try { await (still ? meee() : tricks[trick++ % tricks.length]()); } catch (e) { face("front"); goat.style.transform = REST; }
    busy = false;
    catchUp();
  };
  // A tap on the goat is for the goat: on a speaker's card it plays a trick instead of opening the page.
  const tapped = (e) => {
    if (!goat || !goat.contains(e.target)) return;
    e.preventDefault();
    e.stopPropagation();
    // Taps in quick succession count as a double or triple click, which would select the text around it.
    if (e.detail > 1) getSelection().removeAllRanges();
    if (down) return;
    asked = true;
    if (!busy) return perform();
    // A move while it waits gives way, and the trick follows; a hop or a pop lands first.
    if (idling) { goat.getAnimations().forEach((a) => a.finish()); face("front"); }
  };

  const start = () => {
    stage.style.visibility = "";
    addEventListener("scroll", schedule, { passive: true });
    slots.forEach((s) => s.slot.addEventListener("pointerenter", () => go(s)));
    stage.addEventListener("click", tapped);
    stage.addEventListener("mousedown", (e) => { if (goat && goat.contains(e.target)) e.preventDefault(); });
    go(pick());
    if (still) return;
    setTimeout(idle, 3000);
    // A gazing goat notices the mouse when it comes near, and on a phone looks where you tap for a moment.
    addEventListener("pointermove", (e) => {
      if (e.pointerType !== "mouse" || down || !canGaze() || (busy && !idling)) return;
      follow(e.clientX, e.clientY);
    }, { passive: true });
    document.documentElement.addEventListener("pointerleave", () => { wish = "11"; });
    addEventListener("pointerdown", (e) => {
      if (e.pointerType === "mouse" || down || !canGaze() || goat.contains(e.target)) return;
      follow(e.clientX, e.clientY);
    }, { passive: true });
    // It looks towards a mouse pointer that comes close, and back at you when the pointer is over it or gone.
    addEventListener("pointermove", (e) => {
      if (e.pointerType !== "mouse" || busy || down || !canTurn() || canGaze()) return;
      const r = goat.getBoundingClientRect();
      const x = e.clientX - (r.left + r.width / 2), y = e.clientY - (r.top + r.height * 0.4);
      const dir = Math.hypot(x, y) > 260 || Math.abs(x) < r.width * 0.35 ? "front" : x < 0 ? "left" : "right";
      if (dir === facing) return;
      busy = true;
      turnTo(dir).then(() => { busy = false; catchUp(); }, () => { busy = false; });
    }, { passive: true });
  };
  // The sheets this page's goats are drawn from, decoded before the goat appears; if one fails, every slot
  // gets its own goat back.
  const sheets = [...new Set(peeks.map((p) => p.style.backgroundImage.slice(4, -1).replace(/"/g, "")))];
  const decode = (src) => { const i = new Image(); i.src = src; return i.decode(); };
  // The turned heads load once the goat is out; until then it simply looks at you.
  const turns = () => {
    [...new Set(peeks.map((p) => (p.dataset.turn || "").split("|")[0]).filter(Boolean))]
      .forEach((src) => decode(src).then(() => turnSheets.add(src), () => {}));
    [...new Set(peeks.map((p) => p.dataset.gaze).filter(Boolean))]
      .forEach((src) => decode(src).then(() => gazeSheets.add(src), () => {}));
  };
  const load = () => Promise.all(sheets.map(decode))
    .then(() => { start(); if (!still) later(turns); }, () => root.classList.remove("goat-one"));
  const later = window.requestIdleCallback || ((f) => setTimeout(f, 200));
  document.readyState === "complete" ? later(load) : addEventListener("load", () => later(load), { once: true });
})();
