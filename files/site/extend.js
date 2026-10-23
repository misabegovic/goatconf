// Make it yours: narrow the places in Tuzla by what a host wants to run. Without the script every place shows.
(() => {
  const form = document.querySelector("[data-finder]");
  if (!form) return;
  const cards = [...document.querySelectorAll("[data-venue]")];
  const count = form.querySelector("[data-count]");
  const none = document.querySelector("[data-none]");
  const sizes = { small: ["small"], medium: ["medium"], large: ["large"] };
  form.hidden = false;

  const apply = () => {
    const text = form.text.value.trim().toLowerCase();
    const kind = form.kind.value;
    const size = form.size.value;
    const far = form.far.value;
    const setting = form.setting.value;
    const first = form.first.checked;
    let shown = 0;
    cards.forEach((card) => {
      const d = card.dataset;
      const ok = (!text || d.text.includes(text))
        && (!kind || d.kinds.split(" ").includes(kind))
        && (!size || (sizes[size] || []).includes(d.size))
        && (!far || (far === "near" ? d.near === "1" : d.walk === "1"))
        && (!setting || d.setting === setting || d.setting === "both")
        && (!first || d.first !== "1");
      card.hidden = !ok;
      if (ok) shown += 1;
    });
    count.textContent = shown === cards.length ? `Showing all ${cards.length} places.` : `Showing ${shown} of ${cards.length} places.`;
    if (none) none.hidden = shown > 0;
  };

  form.addEventListener("input", apply);
  form.addEventListener("submit", (e) => e.preventDefault());
  document.querySelectorAll("[data-pick-kind]").forEach((a) => a.addEventListener("click", () => {
    form.kind.value = a.dataset.pickKind;
    apply();
  }));
  const wanted = new URLSearchParams(location.search).get("kind");
  if (wanted && [...form.kind.options].some((o) => o.value === wanted)) form.kind.value = wanted;
  apply();
})();
