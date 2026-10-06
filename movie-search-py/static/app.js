const $ = (id) => document.getElementById(id);
let query = "", page = 1, totalPages = 1;

function esc(s) {
  const d = document.createElement("div");
  d.textContent = s ?? "";
  return d.innerHTML;
}

async function load() {
  $("status").textContent = "Loading…";
  try {
    const res = await fetch(`/api/search?q=${encodeURIComponent(query)}&page=${page}`);
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Request failed");
    totalPages = data.total_pages;
    $("results").innerHTML = data.movies.length
      ? data.movies.map(card).join("") : "<p>No movies found.</p>";
    $("status").textContent = query
      ? `${data.total_results} results for "${query}"` : "Trending this week";
    $("page").textContent = `Page ${page} of ${totalPages}`;
    $("prev").disabled = page <= 1;
    $("next").disabled = page >= totalPages;
  } catch (e) {
    $("status").textContent = e.message;
  }
}

function card(m) {
  const img = m.poster
    ? `<img src="${m.poster}" alt="${esc(m.title)} poster" loading="lazy">`
    : `<div class="noimg">No poster</div>`;
  return `<article class="card">${img}<div class="info">
    <h3>${esc(m.title)}</h3><p class="meta">${m.year} · ★ ${m.rating}</p>
    <p class="overview">${esc(m.overview)}</p></div></article>`;
}

$("form").addEventListener("submit", (e) => {
  e.preventDefault();
  query = $("query").value.trim(); page = 1; load();
});
$("prev").addEventListener("click", () => { page--; load(); scrollTo(0, 0); });
$("next").addEventListener("click", () => { page++; load(); scrollTo(0, 0); });
load();
