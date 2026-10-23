// Stickers peel and settle once as they reach the viewport. The peeled start is set in the head, before first paint.
(() => {
  const root = document.documentElement;
  if (!root.classList.contains("js-peel")) return;
  const stickers = document.querySelectorAll("[data-peel]");
  const io = new IntersectionObserver((entries) => {
    entries.filter((e) => e.isIntersecting).forEach((entry, i) => {
      const el = entry.target;
      setTimeout(() => el.classList.add("is-stuck"), 120 + 90 * i);
      io.unobserve(el);
    });
  }, { threshold: 0.35 });
  stickers.forEach((el) => io.observe(el));
})();

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
