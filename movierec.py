"""
INTI Movie Recommendation System — Enhanced Edition
Features:
  * Mood-based genre detection (conversational)
  * Rich movie details (year, rating, description)
  * "Surprise Me!" random pick
  * Personal watchlist with session summary
  * Star ratings after watching
  * Fun chatbot personality & ASCII banner
  * Age-appropriate content with friendly explanations
"""

import random

# ---------------------------------------------------------------------------
# Movie catalogue  — each entry is a dict with full details
# ---------------------------------------------------------------------------
MOVIES = {
    "Sci-Fi": {
        "adult": [
            {
                "title": "A Space Odyssey",
                "year": 2001,
                "rating": 8.3,
                "desc": "A visually stunning journey through space and human evolution. Kubrick's masterpiece that redefined cinema.",
            },
            {
                "title": "Blade Runner 2049",
                "year": 2017,
                "rating": 8.0,
                "desc": "A breathtaking neo-noir thriller where a young blade runner uncovers a secret that could plunge society into chaos.",
            },
            {
                "title": "The Matrix",
                "year": 1999,
                "rating": 8.7,
                "desc": "What if reality isn't real? A hacker discovers the shocking truth behind the world he lives in.",
            },
            {
                "title": "Mad Max: Fury Road",
                "year": 2015,
                "rating": 8.1,
                "desc": "A pulse-pounding, two-hour car chase through a post-apocalyptic wasteland. Pure adrenaline.",
            },
            {
                "title": "Annihilation",
                "year": 2018,
                "rating": 7.4,
                "desc": "A biologist ventures into a mysterious quarantine zone where the laws of nature don't apply. Eerily beautiful.",
            },
        ],
        "child": [
            {
                "title": "Sonic The Hedgehog",
                "year": 2020,
                "rating": 6.5,
                "desc": "The world's fastest hedgehog teams up with a small-town cop for a wild adventure. Fast, fun and full of laughs!",
            },
            {
                "title": "Star Wars",
                "year": 1977,
                "rating": 8.6,
                "desc": "A farm boy, a princess, and a smuggler take on an evil empire. The classic that started it all!",
            },
            {
                "title": "Ant-Man",
                "year": 2015,
                "rating": 7.3,
                "desc": "A thief gains the power to shrink to ant size. Small hero, BIG adventure!",
            },
            {
                "title": "Zathura: A Space Adventure",
                "year": 2005,
                "rating": 6.3,
                "desc": "Two brothers get sucked into a board game that launches them into outer space. Jumanji... in SPACE!",
            },
            {
                "title": "Spy Kids",
                "year": 2001,
                "rating": 5.9,
                "desc": "Two kids discover their parents are spies and must rescue them using crazy gadgets. The coolest family ever.",
            },
        ],
    },
    "Comedy": {
        "adult": [
            {
                "title": "Ted",
                "year": 2012,
                "rating": 6.9,
                "desc": "A man's childhood wish brings his teddy bear to life — and now the bear won't grow up. Hilariously adult.",
            },
            {
                "title": "The Hangover",
                "year": 2009,
                "rating": 7.7,
                "desc": "Three friends wake up after a bachelor party in Vegas with no memory and a missing groom. Comedy gold.",
            },
            {
                "title": "Shaun of the Dead",
                "year": 2004,
                "rating": 7.9,
                "desc": "A slacker and his best friend try to survive a zombie apocalypse without missing pub time. Brilliantly British.",
            },
            {
                "title": "Angry Boys",
                "year": 2011,
                "rating": 7.5,
                "desc": "A mockumentary following bizarre characters across Australia and America. Outrageous and oddly heartfelt.",
            },
            {
                "title": "American Reunion",
                "year": 2012,
                "rating": 6.7,
                "desc": "The gang from East Great Falls reunites for their high school reunion. Nostalgia meets non-stop chaos.",
            },
        ],
        "child": [
            {
                "title": "Jackass Forever",
                "year": 2022,
                "rating": 7.5,
                "desc": "The crew is back with wild stunts and pranks that'll have you crying with laughter.",
            },
            {
                "title": "Marry Me",
                "year": 2022,
                "rating": 6.2,
                "desc": "A pop star randomly picks a stranger from the crowd to marry. Sweet, funny, and surprisingly charming.",
            },
            {
                "title": "I Want You Back",
                "year": 2022,
                "rating": 6.8,
                "desc": "Two dumped strangers team up to win back their exes. Messy plans, big laughs.",
            },
            {
                "title": "Dog",
                "year": 2022,
                "rating": 6.7,
                "desc": "An army ranger and a Belgian Malinois take an unlikely road trip. Funny, touching, and full of heart.",
            },
            {
                "title": "Turning Red",
                "year": 2022,
                "rating": 7.0,
                "desc": "A 13-year-old girl turns into a giant red panda whenever she gets too excited. Relatable chaos!",
            },
        ],
    },
    "Fantasy": {
        "adult": [
            {
                "title": "Avatar: The Way of Water",
                "year": 2022,
                "rating": 7.6,
                "desc": "The Sully family faces a new threat on Pandora. Visually the most stunning film ever made.",
            },
            {
                "title": "The School for Good and Evil",
                "year": 2022,
                "rating": 5.9,
                "desc": "Two best friends are whisked away to a school that trains fairy-tale heroes and villains.",
            },
            {
                "title": "Disenchanted",
                "year": 2022,
                "rating": 5.8,
                "desc": "Giselle accidentally turns the real world into a fairy tale — with dark consequences.",
            },
            {
                "title": "Eternals",
                "year": 2021,
                "rating": 6.3,
                "desc": "Immortal beings who have secretly shaped human history must unite to save the planet.",
            },
            {
                "title": "Hocus Pocus 2",
                "year": 2022,
                "rating": 5.8,
                "desc": "The Sanderson Sisters are back, and three high schoolers must stop them before sunrise.",
            },
        ],
        "child": [
            {
                "title": "Dora and the Lost City of Gold",
                "year": 2019,
                "rating": 6.1,
                "desc": "Dora the Explorer leads her friends through the jungle to find a legendary Inca city. Adventure for all!",
            },
            {
                "title": "Cinderella",
                "year": 2021,
                "rating": 5.3,
                "desc": "A modern musical reimagining of the classic tale with bold songs and a fearless heroine.",
            },
            {
                "title": "We Can Be Heroes",
                "year": 2020,
                "rating": 5.4,
                "desc": "Kids of superheroes must save their parents from alien captors. Girl power and kid power combined!",
            },
            {
                "title": "Pan",
                "year": 2015,
                "rating": 5.8,
                "desc": "The origin story of Peter Pan — an orphan whisked away to Neverland on a flying pirate ship.",
            },
            {
                "title": "The Christmas Chronicles",
                "year": 2018,
                "rating": 6.6,
                "desc": "Two kids accidentally crash Santa's sleigh on Christmas Eve and must help him save the holiday.",
            },
        ],
    },
    "Action": {
        "adult": [
            {
                "title": "Black Panther: Wakanda Forever",
                "year": 2022,
                "rating": 7.3,
                "desc": "Wakanda fights to protect itself from a new world power after the loss of King T'Challa. Emotional and epic.",
            },
            {
                "title": "Black Adam",
                "year": 2022,
                "rating": 6.3,
                "desc": "An ancient anti-hero is unleashed on the modern world. Dwayne Johnson at full power.",
            },
            {
                "title": "Top Gun: Maverick",
                "year": 2022,
                "rating": 8.3,
                "desc": "Maverick pushes the limits of modern aviation on the most dangerous mission of his career. Edge-of-your-seat.",
            },
            {
                "title": "Thor: Love and Thunder",
                "year": 2022,
                "rating": 6.3,
                "desc": "Thor embarks on a journey of self-discovery while facing the deadliest villain he's ever met.",
            },
            {
                "title": "Violent Night",
                "year": 2022,
                "rating": 7.3,
                "desc": "Santa Claus must save a family taken hostage on Christmas Eve. It's Die Hard... with Santa.",
            },
        ],
        "child": None,  # Age-restricted
    },
    "Animation": {
        "adult": [
            {
                "title": "Your Name",
                "year": 2016,
                "rating": 8.4,
                "desc": "Two teenagers mysteriously swap bodies and must find each other before it's too late. Heartbreakingly beautiful.",
            },
            {
                "title": "In This Corner of the World",
                "year": 2016,
                "rating": 8.0,
                "desc": "A young woman's ordinary life during wartime Japan. Quietly devastating and deeply human.",
            },
            {
                "title": "The Simpsons Movie",
                "year": 2007,
                "rating": 7.3,
                "desc": "Homer accidentally dooms Springfield and the family must save the town. D'oh!",
            },
            {
                "title": "Demon Slayer: Mugen Train",
                "year": 2020,
                "rating": 8.2,
                "desc": "Tanjiro and the Flame Hashira face a demon on a supernatural train. The most beautiful animated fight scenes ever.",
            },
            {
                "title": "Suicide Squad: Hell to Pay",
                "year": 2018,
                "rating": 7.0,
                "desc": "Task Force X races to steal a mystical object that grants a second chance at life. Wild and brutal.",
            },
        ],
        "child": [
            {
                "title": "Coco",
                "year": 2017,
                "rating": 8.4,
                "desc": "A boy accidentally enters the Land of the Dead and discovers his family's secret history. Bring tissues!",
            },
            {
                "title": "How to Train Your Dragon: The Hidden World",
                "year": 2019,
                "rating": 7.5,
                "desc": "Hiccup and Toothless discover a hidden dragon world. A gorgeous, emotional farewell to an epic trilogy.",
            },
            {
                "title": "Spider-Man: Into the Spider-Verse",
                "year": 2018,
                "rating": 8.4,
                "desc": "Miles Morales becomes Spider-Man in a multiverse adventure with mind-blowing animation. Absolutely incredible.",
            },
            {
                "title": "PAW Patrol: The Movie",
                "year": 2021,
                "rating": 5.4,
                "desc": "The pups take on their biggest mission yet — saving Adventure City from the mayor's schemes!",
            },
            {
                "title": "The SpongeBob Movie: Sponge on the Run",
                "year": 2020,
                "rating": 5.7,
                "desc": "SpongeBob and Patrick go on a wild rescue mission to save Gary. Absurdly fun for the whole family.",
            },
        ],
    },
    "Romance": {
        "adult": [
            {
                "title": "My Policeman",
                "year": 2022,
                "rating": 6.4,
                "desc": "A forbidden love triangle across decades in 1950s England. Harry Styles gives a quietly powerful performance.",
            },
            {
                "title": "Falling for Christmas",
                "year": 2022,
                "rating": 5.5,
                "desc": "A spoiled heiress loses her memory and falls in love with a kind lodge owner. Festive and feel-good.",
            },
            {
                "title": "Ticket to Paradise",
                "year": 2022,
                "rating": 6.8,
                "desc": "Divorced parents fly to Bali to stop their daughter's wedding — and maybe rekindle old feelings.",
            },
            {
                "title": "The Lost City",
                "year": 2022,
                "rating": 6.9,
                "desc": "A romance novelist and her cover model get caught up in a jungle adventure. Funny, fast, and charming.",
            },
            {
                "title": "Downton Abbey: A New Era",
                "year": 2022,
                "rating": 7.0,
                "desc": "The Crawley family discovers a mysterious villa left to the Dowager Countess. Elegant and heartwarming.",
            },
        ],
        "child": None,
    },
    "Horror": {
        "adult": [
            {
                "title": "X",
                "year": 2022,
                "rating": 6.6,
                "desc": "A film crew shooting on a remote farm in 1979 finds their hosts have sinister intentions. Retro and terrifying.",
            },
            {
                "title": "Pearl",
                "year": 2022,
                "rating": 7.0,
                "desc": "The origin story of X's killer — a young woman trapped on a farm who dreams of stardom. Brilliantly disturbing.",
            },
            {
                "title": "Alien: Covenant",
                "year": 2017,
                "rating": 6.4,
                "desc": "Colonists discover a dark paradise that harbours a deadly threat. Ridley Scott returns to space horror.",
            },
            {
                "title": "Hellraiser",
                "year": 2022,
                "rating": 6.0,
                "desc": "A reimagining of the classic — a puzzle box opens a gateway to a dimension of pain and pleasure.",
            },
            {
                "title": "Last Night in Soho",
                "year": 2021,
                "rating": 7.1,
                "desc": "A girl studying fashion in London can somehow enter the 1960s — but the past is not what it seems.",
            },
        ],
        "child": None,
    },
}

# ---------------------------------------------------------------------------
# Mood -> genre mapping  (conversational feel)
# ---------------------------------------------------------------------------
MOOD_MAP = {
    "Sci-Fi":    ["science", "space", "robot", "spacecraft", "tech", "future", "sci-fi", "scifi", "alien"],
    "Comedy":    ["laugh", "humor", "funny", "happy", "comedy", "cheer", "bored", "lighthearted", "chill", "relax"],
    "Fantasy":   ["magic", "fairy", "myth", "supernatural", "fantasy", "dragon", "wizard", "enchant"],
    "Action":    ["thrill", "explosion", "gun", "fight", "heist", "action", "adventure", "intense", "adrenaline"],
    "Animation": ["animated", "animation", "cartoon", "anime", "3d", "drawn"],
    "Romance":   ["romantic", "love", "dating", "marriage", "emotional", "heartfelt", "couple", "sweet"],
    "Horror":    ["ghost", "fear", "shock", "scary", "disgust", "horror", "creepy", "dark", "jump scare"],
}

MOOD_RESPONSES = {
    "Sci-Fi":    "Ooh, a fellow space explorer! 🚀 Let me find something mind-bending for you.",
    "Comedy":    "You're in the mood to laugh? Great choice — life's too short for sad movies! 😄",
    "Fantasy":   "Escaping to a magical world? I love it. ✨ Here's some enchanting stuff for you.",
    "Action":    "Time to sit on the edge of your seat! 💥 Here's some high-octane action.",
    "Animation": "Animation is for everyone — don't let anyone tell you otherwise! 🎨",
    "Romance":   "Feeling the love tonight? 💕 Here are some heart-warming picks.",
    "Horror":    "Brave soul! 👻 Try not to scream too loud — your neighbours might hear you.",
}

FUN_FACTS = {
    "Sci-Fi":    "🤓 Fun fact: The word 'robot' was first used in a 1920 Czech play called R.U.R.",
    "Comedy":    "😂 Fun fact: Laughing for 10–15 minutes a day burns up to 40 calories. Movie therapy!",
    "Fantasy":   "🧙 Fun fact: Tolkien invented over 20 languages for his fantasy world.",
    "Action":    "💥 Fun fact: Tom Cruise performed his own stunts in Top Gun: Maverick, including actual jet flights.",
    "Animation": "🎥 Fun fact: Pixar's 'Coco' took 6 years to make and used over 1,000 visual effects shots.",
    "Romance":   "💌 Fun fact: The first on-screen kiss in cinema history was in 1896 — just 18 seconds long.",
    "Horror":    "👁️ Fun fact: Alfred Hitchcock bought the rights to 'Psycho' anonymously so no one knew he was making it.",
}

STARS = ["☆☆☆☆☆", "★☆☆☆☆", "★★☆☆☆", "★★★☆☆", "★★★★☆", "★★★★★"]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def stars(rating: float) -> str:
    """Convert a 10-point rating to a 5-star display."""
    filled = round(rating / 2)
    return "★" * filled + "☆" * (5 - filled)


def get_int_input(prompt: str) -> int | None:
    raw = input(prompt).strip()
    try:
        return int(raw)
    except ValueError:
        return None


def detect_genre(user_text: str) -> str | None:
    text = user_text.lower()
    for genre, keywords in MOOD_MAP.items():
        if any(kw in text for kw in keywords):
            return genre
    # Direct genre name match (e.g. user clicks a genre button)
    for genre in MOOD_MAP:
        if genre.lower() in text:
            return genre
    return None


def get_all_genres() -> list[str]:
    return list(MOVIES.keys())


def get_age_group(age: int) -> str:
    return "adult" if age >= 18 else "child"


def is_genre_available(genre: str, age_group: str) -> bool:
    return MOVIES.get(genre, {}).get(age_group) is not None


def get_movies_for_genre(genre: str, age_group: str) -> list[dict] | None:
    if genre not in MOVIES:
        return None
    return MOVIES[genre][age_group]


def get_all_movies(age_group: str) -> list[dict]:
    """Return every movie available for the given age group."""
    from movie_media import enrich_movie

    results = []
    for genre, age_dict in MOVIES.items():
        titles = age_dict[age_group]
        if not titles:
            continue
        for movie in titles:
            entry = enrich_movie(dict(movie))
            entry["genre"] = genre
            results.append(entry)
    return results


def search_movies(query: str, age_group: str) -> list[dict]:
    """Search movies by title, description, or genre keywords."""
    from movie_media import enrich_movie

    query = query.lower().strip()
    if not query:
        return get_all_movies(age_group)

    results = []
    detected = detect_genre(query)

    for genre, age_dict in MOVIES.items():
        if detected and genre != detected:
            continue
        titles = age_dict[age_group]
        if not titles:
            continue
        for movie in titles:
            haystack = f"{movie['title']} {movie['desc']} {genre}".lower()
            if query in haystack or (detected and genre == detected):
                entry = enrich_movie(dict(movie))
                entry["genre"] = genre
                results.append(entry)
    return results


def enrich_movie_for_web(movie: dict, genre: str) -> dict:
    from movie_media import enrich_movie

    entry = enrich_movie(dict(movie))
    entry["genre"] = genre
    entry["stars"] = stars(movie["rating"])
    return entry


def is_surprise_request(user_text: str) -> bool:
    text = user_text.lower()
    return any(w in text for w in ["surprise", "random", "anything", "don't know", "idk", "no idea"])


def display_movie_card(movie: dict, index: int) -> None:
    """Print a nicely formatted movie card."""
    rating_stars = stars(movie["rating"])
    print(f"  {index}. {movie['title']} ({movie['year']})")
    print(f"     {rating_stars}  IMDb {movie['rating']}/10")
    print(f"     {movie['desc']}")
    print()


def display_genre_list(genre: str, age_group: str) -> None:
    movies = MOVIES[genre][age_group]
    print(f"\n{'─'*54}")
    print(f"  🎬  {genre.upper()} PICKS FOR YOU")
    print(f"{'─'*54}\n")
    for i, movie in enumerate(movies, 1):
        display_movie_card(movie, i)
    print(f"  💡 {FUN_FACTS[genre]}\n")


def ask_rating() -> int | None:
    """Ask the user to rate the movie they just watched."""
    print("\nHow would you rate that movie?")
    print("  1 = 😴  2 = 😐  3 = 🙂  4 = 😄  5 = 🤩  (or 0 to skip)")
    while True:
        r = get_int_input("> ")
        if r is None:
            print("Please enter a number from 1 to 5.")
            continue
        if 0 <= r <= 5:
            if r > 0:
                print(f"  You gave it: {STARS[r]}  Thanks for rating!")
            return r
        print("Please enter a number from 0 to 5.")


def surprise_me(age_group: str) -> tuple[str, dict] | None:
    """Pick a random available movie across all genres."""
    pool = []
    for genre, age_dict in MOVIES.items():
        titles = age_dict[age_group]
        if titles:
            for movie in titles:
                pool.append((genre, movie))
    if not pool:
        return None
    return random.choice(pool)


def pick_movie(genre: str, age_group: str, watchlist: list, name: str) -> None:
    """Show movie list, let user pick, optionally add to watchlist."""
    movies = MOVIES[genre][age_group]
    display_genre_list(genre, age_group)

    while True:
        print("  Enter a number to watch a movie.")
        print("  S = Surprise me! 🎲   W = View my watchlist 📋   0 = Go back\n")
        raw = input("> ").strip().lower()

        if raw == "0":
            return

        if raw == "w":
            show_watchlist(watchlist)
            continue

        if raw == "s":
            result = surprise_me(age_group)
            if result:
                s_genre, s_movie = result
                print(f"\n🎲 Random pick: {s_movie['title']} ({s_movie['year']}) — {s_genre}")
                print(f"   {s_movie['desc']}")
                confirm = input("\nWatch this one? (y/n): ").strip().lower()
                if confirm == "y":
                    print(f"\n🎬  Now playing... {s_movie['title']}  🍿")
                    user_rating = ask_rating()
                    watchlist.append({
                        "title": s_movie["title"],
                        "genre": s_genre,
                        "your_rating": user_rating,
                    })
                    print(f"\n✅ Added to your watchlist, {name}!")
            continue

        choice = None
        try:
            choice = int(raw)
        except ValueError:
            print(f"  Hmm, I didn't get that. Enter a number 1–{len(movies)}, S, W, or 0.")
            continue

        if 1 <= choice <= len(movies):
            movie = movies[choice - 1]
            print(f"\n🎬  Now playing... {movie['title']} ({movie['year']})  🍿")
            print(f"   {MOOD_RESPONSES.get(genre, 'Enjoy!')}")
            user_rating = ask_rating()
            watchlist.append({
                "title": movie["title"],
                "genre": genre,
                "your_rating": user_rating,
            })
            print(f"\n✅ '{movie['title']}' added to your watchlist!")

            again = input(f"\nBrowse more {genre} movies? (y/n): ").strip().lower()
            if again != "y":
                return
            display_genre_list(genre, age_group)
        else:
            print(f"  Please enter a number between 1 and {len(movies)}.")


def show_watchlist(watchlist: list) -> None:
    if not watchlist:
        print("\n  📋 Your watchlist is empty so far.")
        return
    print(f"\n{'─'*54}")
    print("  📋  YOUR WATCHLIST THIS SESSION")
    print(f"{'─'*54}")
    for i, item in enumerate(watchlist, 1):
        rating_str = STARS[item["your_rating"]] if item["your_rating"] else "  (not rated)"
        print(f"  {i}. {item['title']}  [{item['genre']}]  {rating_str}")
    print()


def genre_session(age_group: str, watchlist: list, name: str) -> bool:
    """One round of mood detection → movie picking. Returns False to exit."""
    print(f"\n{'─'*54}")
    print("  What are you in the mood for today?")
    print("  (Describe how you feel, name a genre, or try 'surprise me!')")
    print("  Type 0 to exit | W to see your watchlist")
    print(f"{'─'*54}\n")
    user_text = input(f"  {name}: ").strip()

    if not user_text:
        return True

    if user_text == "0":
        return False

    if user_text.lower() == "w":
        show_watchlist(watchlist)
        return True

    if any(w in user_text.lower() for w in ["surprise", "random", "anything", "don't know", "idk", "no idea"]):
        result = surprise_me(age_group)
        if result:
            s_genre, s_movie = result
            print(f"\n🎲 How about... {s_movie['title']} ({s_movie['year']}) — {s_genre}?")
            print(f"   {s_movie['desc']}")
            print(f"   {stars(s_movie['rating'])}  IMDb {s_movie['rating']}/10")
            confirm = input("\n  Sound good? (y to watch / n to explore genres): ").strip().lower()
            if confirm == "y":
                print(f"\n🎬  Now playing... {s_movie['title']}  🍿")
                user_rating = ask_rating()
                watchlist.append({"title": s_movie["title"], "genre": s_genre, "your_rating": user_rating})
                print(f"\n✅ Added to your watchlist, {name}!")
                return True

    genre = detect_genre(user_text)

    if genre is None:
        print("\n  🤔 Hmm, I'm not sure what you're looking for.")
        print("  Try words like: funny, scary, romantic, action, sci-fi, fantasy, anime, space...")
        return True

    if MOVIES[genre][age_group] is None:
        print(f"\n  ⚠️  {genre} movies contain mature content (violence, adult themes, etc.)")
        print("  They're reserved for viewers 18 and above — to keep the fun safe for everyone!")
        print("  How about Comedy, Animation, Fantasy, or Sci-Fi instead?")
        return True

    print(f"\n  🎯 {MOOD_RESPONSES[genre]}")
    pick_movie(genre, age_group, watchlist, name)
    return True


def print_banner() -> None:
    print("""
╔══════════════════════════════════════════════════════╗
║                                                      ║
║        🎬  INTI MOVIE RECOMMENDATION SYSTEM  🎬      ║
║                                                      ║
║        Your personal cinema guide — let's find       ║
║        the perfect movie for your mood tonight!      ║
║                                                      ║
╚══════════════════════════════════════════════════════╝
""")


def farewell_summary(name: str, watchlist: list) -> None:
    print(f"\n{'═'*54}")
    print(f"  Thanks for visiting, {name}! 🎉")
    if watchlist:
        print(f"\n  🍿 Your session watchlist:")
        show_watchlist(watchlist)
        rated = [w for w in watchlist if w["your_rating"]]
        if rated:
            avg = sum(w["your_rating"] for w in rated) / len(rated)
            print(f"  Your average rating this session: {avg:.1f}/5  {STARS[round(avg)]}")
    else:
        print("  No movies watched this session — come back soon!")
    print(f"\n  Enjoy the show! 🎬✨")
    print(f"{'═'*54}\n")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    print_banner()

    name = input("  First, what's your name? ").strip() or "Guest"
    print(f"\n  Hey {name}! Great to have you here. 🙌")

    # Get valid age
    age = None
    while age is None:
        age = get_int_input(f"  And how old are you, {name}? ")
        if age is None or not (1 <= age <= 100):
            print("  Hmm, that doesn't look right. Please enter your age (1–100).")
            age = None

    age_group = "adult" if age >= 18 else "child"

    if age_group == "child":
        print(f"\n  Awesome! You're {age} — we've got some fantastic picks lined up for you! 🌟")
    else:
        print(f"\n  Perfect! At {age}, you've got access to our full catalogue. 🎞️")

    watchlist: list = []

    while True:
        keep_going = genre_session(age_group, watchlist, name)
        if not keep_going:
            break

    farewell_summary(name, watchlist)


if __name__ == "__main__":
    main()
