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
