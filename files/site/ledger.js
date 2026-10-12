(() => {
  const target = document.getElementById("ledger");
  if (!target || !window.fetch) return;

  const LABELS = {
    date: "Date", item: "Item", kind: "Base or menu", covered_by: "Covered by",
    supplier: "Supplier", amount_eur: "Amount (EUR)", in_kind: "In kind",
    receipt_in_hand: "Receipt", note: "Note",
  };

  function parse(text) {
    const rows = [];
    let row = [], cell = "", quoted = false;
    for (let i = 0; i < text.length; i++) {
      const c = text[i];
      if (quoted) {
        if (c === '"' && text[i + 1] === '"') { cell += '"'; i++; }
        else if (c === '"') quoted = false;
        else cell += c;
      } else if (c === '"') quoted = true;
      else if (c === ",") { row.push(cell); cell = ""; }
      else if (c === "\n" || c === "\r") {
        if (c === "\r" && text[i + 1] === "\n") i++;
        row.push(cell); cell = "";
        if (row.some((v) => v !== "")) rows.push(row);
        row = [];
      } else cell += c;
    }
    if (cell !== "" || row.length) { row.push(cell); if (row.some((v) => v !== "")) rows.push(row); }
    return rows;
  }

  function money(value) {
    const n = Number(value);
    return Number.isFinite(n) && value !== "" ? n.toLocaleString("en", { minimumFractionDigits: 2, maximumFractionDigits: 2 }) : value;
  }

  fetch("ledger.csv", { cache: "no-store" })
    .then((response) => (response.ok ? response.text() : Promise.reject(response.status)))
    .then((text) => {
      const [head, ...lines] = parse(text);
      if (!head) return;
      if (!lines.length) {
        target.innerHTML = '<p class="ledger-empty"><strong>Nothing spent and nothing received yet.</strong> The first line appears here the day something is paid for or given. The raw file is <a href="ledger.csv">ledger.csv</a>.</p>';
        return;
      }
      const table = document.createElement("table");
      table.className = "ledger";
      const caption = table.createCaption();
      caption.textContent = `${lines.length} ${lines.length === 1 ? "line" : "lines"} so far`;
      const tr = table.createTHead().insertRow();
      head.forEach((key) => {
        const th = document.createElement("th");
        th.scope = "col";
        th.textContent = LABELS[key] || key;
        if (key === "amount_eur") th.className = "num";
        tr.append(th);
      });
      const body = table.createTBody();
      let total = 0;
      lines.forEach((line) => {
        const r = body.insertRow();
        head.forEach((key, i) => {
          const td = r.insertCell();
          const value = line[i] || "";
          if (key === "amount_eur") { td.className = "num"; td.textContent = money(value); total += Number(value) || 0; }
          else td.textContent = value;
        });
      });
      const foot = table.createTFoot().insertRow();
      head.forEach((key, i) => {
        const td = foot.insertCell();
        if (i === 0) td.textContent = "Total";
        if (key === "amount_eur") { td.className = "num"; td.textContent = money(String(total)); }
      });
      target.replaceChildren(table);
      const raw = document.createElement("p");
      raw.innerHTML = 'The raw file is <a href="ledger.csv">ledger.csv</a>.';
      target.append(raw);
    })
    .catch(() => {});
})();
