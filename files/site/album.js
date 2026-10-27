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
