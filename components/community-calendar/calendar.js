/* Progressive enhancement only: all event details are present in static HTML. */
(() => {
  "use strict";
  const form = document.querySelector("#event-filters");
  const cards = Array.from(document.querySelectorAll(".event-card"));
  if (!form) return;

  const area = form.querySelector("#filter-area");
  const category = form.querySelector("#filter-category");
  const range = form.querySelector("#filter-range");
  const free = form.querySelector("#filter-free");
  const status = document.querySelector("#results-count");
  const noResults = document.querySelector("#no-results");
  const featured = document.querySelector("#featured-section");
  const featuredItems = Array.from(document.querySelectorAll("[data-feature-ref]"));

  function chicagoDate(today) {
    const parts = new Intl.DateTimeFormat("en-US", {
      timeZone: "America/Chicago", year: "numeric", month: "2-digit", day: "2-digit"
    }).formatToParts(today);
    const dateParts = Object.fromEntries(parts.map((part) => [part.type, part.value]));
    return `${dateParts.year}-${dateParts.month}-${dateParts.day}`;
  }
  function datePlusDays(day, number) {
    const dt = new Date(`${day}T12:00:00Z`);
    dt.setUTCDate(dt.getUTCDate() + number);
    return dt.toISOString().slice(0, 10);
  }
  function applyFilters() {
    const now = new Date();
    const today = chicagoDate(now);
    const through = datePlusDays(today, 13);
    let count = 0;
    for (const card of cards) {
      const old = card.dataset.day < today;
      const finished = card.dataset.end ? new Date(card.dataset.end) < now : false;
      const outOfWindow = range.value === "14" && card.dataset.day > through;
      const notArea = area.value && card.dataset.area !== area.value;
      const notCategory = category.value && card.dataset.category !== category.value;
      const notFree = free.checked && card.dataset.cost !== "free";
      card.hidden = Boolean(old || finished || outOfWindow || notArea || notCategory || notFree);
      if (!card.hidden) count += 1;
    }
    for (const item of featuredItems) {
      const matchingCard = document.getElementById(item.dataset.featureRef);
      item.hidden = !matchingCard || matchingCard.hidden;
    }
    if (featured) featured.hidden = featuredItems.every((item) => item.hidden);
    if (status) {
      const template = count === 1 ? status.dataset.single : status.dataset.plural;
      status.textContent = template.replace("{count}", String(count));
    }
    if (noResults) noResults.hidden = count !== 0;
  }
  form.hidden = false;
  if (status) status.hidden = false;
  form.addEventListener("change", applyFilters);
  form.addEventListener("reset", () => requestAnimationFrame(applyFilters));
  applyFilters();
})();
