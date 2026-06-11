/* INTI Movie Recommendation — Web GUI (IMDb-powered) */

const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => document.querySelectorAll(sel);

let sessionData = null;
let currentMovies = [];
let selectedMovie = null;
let trailerPollTimer = null;
let pendingTrailerRating = null;

const FALLBACK_POSTER = (title) =>
  `https://placehold.co/300x450/1a1a2e/e94560?text=${encodeURIComponent(title)}`;

function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text ?? "";
  return div.innerHTML;
}

// --- Welcome / session ---

$("#welcome-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const name = $("#user-name").value.trim();
  const age = $("#user-age").value;
  const omdbApiKey = $("#omdb-api-key").value.trim();
  const errEl = $("#welcome-error");

  try {
    const res = await fetch("/api/session", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, age, omdbApiKey }),
    });
    const data = await res.json();
    if (!res.ok) {
      errEl.textContent = data.error;
      errEl.classList.remove("hidden");
      return;
    }
    sessionData = data;
    $("#omdb-api-key").value = "";
    errEl.classList.add("hidden");
    showApp();
  } catch {
    errEl.textContent = "Could not connect to the server. Is Flask running?";
    errEl.classList.remove("hidden");
  }
});

function showApp() {
  $("#welcome-screen").classList.remove("active");
  $("#app-screen").classList.add("active");
  $("#user-greeting").textContent = sessionData.name;
  renderGenres(sessionData.genres);
  addBotMessage(
    `${sessionData.greeting}\n\nMovies and posters are loaded live from IMDb. ` +
      `Describe your mood, search, or pick a genre. You can also say "surprise me!" 🎲`
  );
}

function renderGenres(genres) {
  const list = $("#genre-list");
  list.innerHTML = "";
  genres.forEach((g) => {
    const li = document.createElement("li");
    const btn = document.createElement("button");
    const label = document.createElement("span");
    label.textContent = g.name;
    btn.appendChild(label);
    btn.dataset.genre = g.name;
    if (!g.available) {
      btn.classList.add("disabled");
      btn.title = "18+ only";
    } else {
      btn.addEventListener("click", () => loadGenre(g.name));
    }
    const count = document.createElement("span");
    count.className = "genre-count";
    count.textContent = g.available ? "IMDb" : "18+";
    btn.appendChild(count);
    li.appendChild(btn);
    list.appendChild(li);
  });
}

// --- Chat ---

function addBotMessage(text, extras = {}) {
  const div = document.createElement("div");
  div.className = "msg bot";
  div.innerHTML = `<p>${escapeHtml(text).replace(/\n/g, "<br>")}</p>`;
  if (extras.funFact) {
    div.innerHTML += `<div class="fun-fact">${escapeHtml(extras.funFact)}</div>`;
  }
  if (extras.movies && extras.movies.length) {
    div.appendChild(buildMovieGrid(extras.movies));
  }
  if (extras.ratingPrompt && selectedMovie) {
    div.appendChild(buildInlineRating(selectedMovie));
  }
  $("#chat-messages").appendChild(div);
  scrollChat();
}

function addUserMessage(text) {
  const div = document.createElement("div");
  div.className = "msg user";
  div.textContent = text;
  $("#chat-messages").appendChild(div);
  scrollChat();
}

function scrollChat() {
  const el = $("#chat-messages");
  el.scrollTop = el.scrollHeight;
}

function buildMovieGrid(movies) {
  currentMovies = movies;
  const grid = document.createElement("div");
  grid.className = "movie-grid";
  movies.forEach((m) => {
    const card = document.createElement("div");
    card.className = "movie-card";
    const ratingLabel = m.rating ? `${m.rating}/10` : "N/A";
    card.innerHTML = `
      <img src="${escapeHtml(m.poster)}" alt="${escapeHtml(m.title)}" loading="lazy"
           onerror="this.src='${FALLBACK_POSTER(m.title)}'">
      <div class="movie-card-info">
        <h4>${escapeHtml(m.title)}</h4>
        <div class="meta">${escapeHtml(String(m.year))} · ${escapeHtml(m.genre)}</div>
        <div class="rating">${escapeHtml(m.stars || "")} IMDb ${escapeHtml(ratingLabel)}</div>
      </div>`;
    card.addEventListener("click", () => showMovieDetail(m));
    grid.appendChild(card);
  });
  return grid;
}

$("#chat-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const input = $("#chat-input");
  const msg = input.value.trim();
  if (!msg) return;
  input.value = "";
  addUserMessage(msg);
  await sendChat(msg);
});

async function sendChat(message) {
  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });
    const data = await res.json();
    if (!res.ok) {
      addBotMessage(data.error || "Something went wrong.");
      return;
    }
    addBotMessage(data.reply, {
      funFact: data.fun_fact,
      movies: data.movies,
    });
    if (data.type === "surprise" && data.movie) {
      showMovieDetail(data.movie);
    }
  } catch {
    addBotMessage("Connection error. Please try again.");
  }
}

// --- Genre / search / browse ---

async function loadGenre(genre) {
  $$(".genre-list button").forEach((b) => {
    b.classList.toggle("active", b.dataset.genre === genre);
  });
  addUserMessage(`Show me ${genre} movies`);
  try {
    const res = await fetch(`/api/movies?genre=${encodeURIComponent(genre)}`);
    const data = await res.json();
    if (data.blocked) {
      addBotMessage(data.message);
      return;
    }
    if (!data.movies?.length) {
      addBotMessage(data.error || `No ${genre} movies found on IMDb right now.`);
      return;
    }
    addBotMessage(data.mood_response || `Here are ${genre} picks from IMDb:`, {
      funFact: data.fun_fact,
      movies: data.movies,
    });
  } catch {
    addBotMessage("Could not load movies from IMDb.");
  }
}

$("#search-input").addEventListener("keydown", async (e) => {
  if (e.key !== "Enter") return;
  const q = e.target.value.trim();
  if (!q) return;
  addUserMessage(`Search: ${q}`);
  try {
    const res = await fetch(`/api/movies?q=${encodeURIComponent(q)}`);
    const data = await res.json();
    addBotMessage(
      data.count
        ? `Found ${data.count} movie(s) on IMDb matching "${q}":`
        : `No movies found for "${q}". Try another mood or genre!`,
      { movies: data.movies }
    );
  } catch {
    addBotMessage("Search failed.");
  }
});

$("#btn-show-all").addEventListener("click", async () => {
  addUserMessage("Browse popular movies");
  try {
    const res = await fetch("/api/movies");
    const data = await res.json();
    addBotMessage(`Popular picks from IMDb — ${data.count} movies for you:`, {
      movies: data.movies,
    });
  } catch {
    addBotMessage("Could not load catalogue.");
  }
});

$("#btn-surprise").addEventListener("click", async () => {
  addUserMessage("Surprise me!");
  await sendChat("surprise me");
});

// --- Movie detail + YouTube trailer in new tab ---

function showMovieDetail(movie) {
  selectedMovie = { ...movie, userRating: 0 };
  const panel = $("#detail-panel");
  panel.classList.remove("hidden");

  const ratingLabel = movie.rating ? `${movie.rating}/10` : "N/A";

  $("#detail-content").innerHTML = `
    <span class="imdb-badge">Powered by IMDb</span>
    <img class="detail-poster" src="${escapeHtml(movie.poster)}" alt="${escapeHtml(movie.title)}"
         onerror="this.src='${FALLBACK_POSTER(movie.title)}'">
    <h2>${escapeHtml(movie.title)}</h2>
    <div class="detail-meta">
      <span>${escapeHtml(String(movie.year))}</span> · <span>${escapeHtml(movie.genre)}</span><br>
      <span class="stars">${escapeHtml(movie.stars || "")}</span> IMDb ${escapeHtml(ratingLabel)}
      ${movie.rated ? `<br>Rated: ${escapeHtml(movie.rated)}` : ""}
    </div>
    <p class="detail-desc">${escapeHtml(movie.desc)}</p>
    <button class="btn btn-watch" id="watch-trailer-btn">▶ Watch Trailer on YouTube</button>
    <p style="color:var(--muted);font-size:0.8rem;margin-bottom:16px;">
      Opens in a new tab. I'll ask for your rating when you close it.
    </p>
    <div class="rating-section hidden" id="detail-rating-section">
      <p id="rating-label">Rate this movie after watching:</p>
      <div class="star-btns" id="star-btns"></div>
    </div>
    <button class="btn btn-primary hidden" id="add-watchlist-btn" style="width:100%;margin-top:8px;">
      ✅ Add to Watchlist
    </button>`;

  $("#watch-trailer-btn").addEventListener("click", () => watchTrailerInNewTab(selectedMovie));
}

async function watchTrailerInNewTab(movie) {
  const fallbackUrl = `https://www.youtube.com/results?search_query=${encodeURIComponent(
    `${movie.title} ${movie.year} official trailer`
  )}`;
  let trailerUrl = movie.trailer_url || fallbackUrl;
  const win = window.open(trailerUrl, "_blank");

  pendingTrailerRating = {
    movie,
    prompted: false,
    readyAt: Date.now() + 2500,
  };

  if (!movie.trailer_url && movie.imdb_id) {
    try {
      const res = await fetch(`/api/movie/${movie.imdb_id}?genre=${encodeURIComponent(movie.genre || "")}`);
      const data = await res.json();
      if (data.movie?.trailer_url) {
        trailerUrl = data.movie.trailer_url;
        selectedMovie.trailer_url = trailerUrl;
        if (win && !win.closed) {
          win.location.href = trailerUrl;
        }
      }
    } catch {
      /* use fallback below */
    }
  }

  addBotMessage(
    `Now playing the trailer for "${movie.title}" on YouTube! 🍿\n` +
      `Come back here after you close the tab — I'll ask for your rating.`
  );

  if (trailerPollTimer) clearInterval(trailerPollTimer);
  trailerPollTimer = setInterval(() => {
    if (win && win.closed) {
      clearInterval(trailerPollTimer);
      trailerPollTimer = null;
      promptPendingTrailerRating();
    }
  }, 500);
}

function promptPendingTrailerRating() {
  if (!pendingTrailerRating || pendingTrailerRating.prompted) return;
  if (Date.now() < pendingTrailerRating.readyAt) return;
  pendingTrailerRating.prompted = true;
  promptRatingAfterWatch(pendingTrailerRating.movie);
  pendingTrailerRating = null;
}

window.addEventListener("focus", promptPendingTrailerRating);
document.addEventListener("visibilitychange", () => {
  if (!document.hidden) promptPendingTrailerRating();
});

function promptRatingAfterWatch(movie) {
  addBotMessage(
    `Welcome back! How would you rate "${movie.title}"? Pick a star rating below or in the detail panel.`,
    { ratingPrompt: true }
  );

  const section = $("#detail-rating-section");
  if (section) {
    section.classList.remove("hidden");
    section.classList.add("highlight");
    $("#rating-label").textContent = `How would you rate "${movie.title}"?`;
    renderStarButtons("#star-btns", movie, () => {
      $("#add-watchlist-btn")?.classList.remove("hidden");
    });
    $("#add-watchlist-btn")?.classList.remove("hidden");
  }
}

function renderStarButtons(containerSel, movie, onSelect) {
  const container = $(containerSel);
  if (!container) return;
  container.innerHTML = [
    ...[1, 2, 3, 4, 5].map(
      (n) =>
        `<button type="button" data-rating="${n}">${"★".repeat(n)}${"☆".repeat(5 - n)}</button>`
    ),
    `<button type="button" data-rating="0">Skip</button>`,
  ].join("");

  container.querySelectorAll("button").forEach((btn) => {
    btn.addEventListener("click", async () => {
      container.querySelectorAll("button").forEach((b) => b.classList.remove("selected"));
      btn.classList.add("selected");
      movie.userRating = parseInt(btn.dataset.rating, 10);
      onSelect?.(movie.userRating);

      if (movie.userRating > 0) {
        addBotMessage(
          `Thanks! You rated "${movie.title}" ${"★".repeat(movie.userRating)}${"☆".repeat(5 - movie.userRating)}`
        );
      }

      if (!movie._watchlistAdded) {
        movie._watchlistAdded = true;
        await addToWatchlist(movie, true);
      }
    });
  });
}

function buildInlineRating(movie) {
  const wrap = document.createElement("div");
  wrap.className = "rating-section highlight";
  wrap.style.marginTop = "12px";
  wrap.innerHTML = `<p>Rate <strong>${escapeHtml(movie.title)}</strong>:</p><div class="star-btns" id="inline-star-btns"></div>`;
  setTimeout(() => {
    renderStarButtons("#inline-star-btns", movie);
  }, 0);
  return wrap;
}

$("#close-detail").addEventListener("click", () => {
  $("#detail-panel").classList.add("hidden");
});

async function addToWatchlist(movie, silent = false) {
  try {
    const res = await fetch("/api/watchlist", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        title: movie.title,
        genre: movie.genre,
        imdb_id: movie.imdb_id || "",
        your_rating: movie.userRating || 0,
      }),
    });
    const data = await res.json();
    if (res.ok) {
      updateWatchlistCount(data.watchlist.length);
      if (!silent) addBotMessage(data.message);
    }
  } catch {
    if (!silent) addBotMessage("Could not add to watchlist.");
  }
}

// --- Watchlist modal ---

async function refreshWatchlist() {
  try {
    const res = await fetch("/api/watchlist");
    const data = await res.json();
    updateWatchlistCount(data.watchlist.length);
    renderWatchlist(data.watchlist);
  } catch {
    $("#watchlist-body").innerHTML = '<p class="watchlist-empty">Could not load watchlist.</p>';
  }
}

function updateWatchlistCount(n) {
  $("#watchlist-count").textContent = n;
}

function renderWatchlist(items) {
  const body = $("#watchlist-body");
  if (!items.length) {
    body.innerHTML = '<p class="watchlist-empty">Your watchlist is empty. Pick a movie to get started!</p>';
    return;
  }
  body.innerHTML = items
    .map(
      (item, i) => `
    <div class="watchlist-item">
      <span>${i + 1}. ${escapeHtml(item.title)} <small style="color:var(--muted)">[${escapeHtml(item.genre)}]</small></span>
      <span style="color:var(--gold)">${escapeHtml(item.stars || "—")}</span>
    </div>`
    )
    .join("");
}

$("#btn-watchlist").addEventListener("click", () => {
  refreshWatchlist();
  $("#watchlist-modal").classList.remove("hidden");
});

$("#close-watchlist").addEventListener("click", () => {
  $("#watchlist-modal").classList.add("hidden");
});

$("#watchlist-modal").addEventListener("click", (e) => {
  if (e.target === $("#watchlist-modal")) {
    $("#watchlist-modal").classList.add("hidden");
  }
});
