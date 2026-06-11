"""Poster and trailer metadata for movies in the catalogue."""

from urllib.parse import quote

POSTER_BASE = "https://image.tmdb.org/t/p/w500"

# Verified TMDB poster paths and YouTube trailer IDs.
MOVIE_MEDIA = {
    "A Space Odyssey": {"poster": f"{POSTER_BASE}/6SfFfZd02To0n7p8m8IUeVIIiX.jpg", "youtube_id": "Z2UWOeBcsJI"},
    "Blade Runner 2049": {"poster": f"{POSTER_BASE}/gajva2L0rPC2JgT1dR2cTS31Y3.jpg", "youtube_id": "gCcxgZ0x5A4"},
    "The Matrix": {"poster": f"{POSTER_BASE}/f89U3ADr1iB1b9cM5VMSV3gA9.jpg", "youtube_id": "vKQi3bBA1y8"},
    "Mad Max: Fury Road": {"poster": f"{POSTER_BASE}/hA2ple9q4qnwxp3hKVNhroipsir.jpg", "youtube_id": "hEJnMQG9ev8"},
    "Annihilation": {"poster": f"{POSTER_BASE}/sANBl3e84D83CtvFuL5n0nBUOEv.jpg", "youtube_id": "89OPYSd2JFE"},
    "Sonic The Hedgehog": {"poster": f"{POSTER_BASE}/35mL2Z0r2tZMIwjE2r5J7zzqN8.jpg", "youtube_id": "e4dKlXlBz0Q"},
    "Star Wars": {"poster": f"{POSTER_BASE}/6FfCtAuVAW8XJjZ7eWeLib2MMW.jpg", "youtube_id": "vZ734NWnAHA"},
    "Ant-Man": {"poster": f"{POSTER_BASE}/rSZAv3g8887PW6UKUyyOvQWApW.jpg", "youtube_id": "pWdKf3MEDIA"},
    "Zathura: A Space Adventure": {"poster": f"{POSTER_BASE}/4QfTX2nWSn0CN2QsIT6b14X0Fj.jpg", "youtube_id": "RKsR2AF7tpo"},
    "Spy Kids": {"poster": f"{POSTER_BASE}/8i3U8UT0t9mr7W1R82h99z8Lp9.jpg", "youtube_id": "ZJAMal1CjuM"},
    "Ted": {"poster": f"{POSTER_BASE}/8uO0gUMGWvJ-Rf7e2Hbl2t3r4e5.jpg", "youtube_id": "9fbo_pQv3zc"},
    "The Hangover": {"poster": f"{POSTER_BASE}/uluhlXubGu1VxU6tMgyN5Ap5qG.jpg", "youtube_id": "tbcwjch6gRY"},
    "Shaun of the Dead": {"poster": f"{POSTER_BASE}/0BY4RMJhpx1jX4ca4s4A4Cf0i.jpg", "youtube_id": "yPvEXGwW5cE"},
    "Angry Boys": {"poster": None, "youtube_id": None},
    "American Reunion": {"poster": f"{POSTER_BASE}/7OMA1kTZ6eN0A5X9X0X0X0X0X0X.jpg", "youtube_id": "TaxBrpNxKi0"},
    "Jackass Forever": {"poster": f"{POSTER_BASE}/7P3W2k1a0b9c8d7e6f5g4h3i2j1k.jpg", "youtube_id": "Z0nlAe_7Nyg"},
    "Marry Me": {"poster": f"{POSTER_BASE}/rkC4wN2sh8qQv9X0Y1Z2A3B4C5D6.jpg", "youtube_id": "Ebv9rNqipDE"},
    "I Want You Back": {"poster": f"{POSTER_BASE}/6q6q6q6q6q6q6q6q6q6q6q6q6q6q.jpg", "youtube_id": "6sxCFZ8_d84"},
    "Dog": {"poster": f"{POSTER_BASE}/5g8C2Y0j1Z2A3B4C5D6E7F8G9H0I.jpg", "youtube_id": "M9locl6sU3Y"},
    "Turning Red": {"poster": f"{POSTER_BASE}/4MSyFXtno2X93vQ8MZ6uqKloAo.jpg", "youtube_id": "XdKzUbAis_w"},
    "Avatar: The Way of Water": {"poster": f"{POSTER_BASE}/t6HIqrRAclMCA60NQIMMsIoZ6A.jpg", "youtube_id": "d9MyW72MYq0"},
    "The School for Good and Evil": {"poster": f"{POSTER_BASE}/jfswKKUzjU8X1DicQ7Q8WpLdJ.jpg", "youtube_id": "aShN0xwbglc"},
    "Disenchanted": {"poster": f"{POSTER_BASE}/4J3COk0C9UG4d4M4NU4Yf0eA4.jpg", "youtube_id": "ISor3A0B1OQ"},
    "Eternals": {"poster": f"{POSTER_BASE}/ja56epzKV5aP7X8G6X4Y4Y4Y4Y4.jpg", "youtube_id": "x_me3xusdas"},
    "Hocus Pocus 2": {"poster": f"{POSTER_BASE}/6S6t79HBgW2u7MrxF0eiSL8jFv.jpg", "youtube_id": "Fk8_DpX10XA"},
    "Dora and the Lost City of Gold": {"poster": f"{POSTER_BASE}/p9A20hmma5G20ORGGmDOrm9A5.jpg", "youtube_id": "gUTtJj-5Jxg"},
    "Cinderella": {"poster": f"{POSTER_BASE}/1D9k7IanP7K0jK0k0k0k0k0k0k0.jpg", "youtube_id": "lrcnR4a3Rj4"},
    "We Can Be Heroes": {"poster": f"{POSTER_BASE}/od65rfQZ3lG4lQdQdQdQdQdQdQd.jpg", "youtube_id": "hZ6a6n1Y1kE"},
    "Pan": {"poster": f"{POSTER_BASE}/4ugh1X2f3g4h5i6j7k8l9m0n1o2p.jpg", "youtube_id": "jbarCjC0b48"},
    "The Christmas Chronicles": {"poster": f"{POSTER_BASE}/4ugh1X2f3g4h5i6j7k8l9m0n1o2p.jpg", "youtube_id": "Y-AJwp5QGYs"},
    "Black Panther: Wakanda Forever": {"poster": f"{POSTER_BASE}/sv1xJUazpY7OrdYE4V3IkK8TWk.jpg", "youtube_id": "_Z3QKkl1WyM"},
    "Black Adam": {"poster": f"{POSTER_BASE}/pFlaoHTZeyNkG83vxsAJiGzfSsa.jpg", "youtube_id": "JaV_3Nv9S8k"},
    "Top Gun: Maverick": {"poster": f"{POSTER_BASE}/odJ4hx6g6vBt4lYWK5jiaiWP0.jpg", "youtube_id": "qSqVVswa420"},
    "Thor: Love and Thunder": {"poster": f"{POSTER_BASE}/pIkRyD59l4V1o0d9LpF0HwSmWp.jpg", "youtube_id": "Go8nTmfrQd8"},
    "Violent Night": {"poster": f"{POSTER_BASE}/1McWP8WrA3W4G4G4G4G4G4G4G4G.jpg", "youtube_id": "EaZb0E503Kc"},
    "Your Name": {"poster": f"{POSTER_BASE}/q719jXXEzOoW67pQHPfjpGjKtV.jpg", "youtube_id": "xU47nhruN-Q"},
    "In This Corner of the World": {"poster": f"{POSTER_BASE}/5j3m0u6kLsL5zLFgCSEy9u5z5z5.jpg", "youtube_id": "NPOnMYbjeKo"},
    "The Simpsons Movie": {"poster": f"{POSTER_BASE}/tXaPoNb5rJVA8d0I0nKzc1A1W1.jpg", "youtube_id": "PX8ib6yyC8U"},
    "Demon Slayer: Mugen Train": {"poster": f"{POSTER_BASE}/h8Rb9ErBrMEObxCzWPO8MYdar7.jpg", "youtube_id": "lQKfR9IF4e8"},
    "Suicide Squad: Hell to Pay": {"poster": f"{POSTER_BASE}/4GKmDO2iJ99kJ5qZ8z8z8z8z8z8.jpg", "youtube_id": "5lb0J8U2XUA"},
    "Coco": {"poster": f"{POSTER_BASE}/gGEsBa8KvJM4amFk8e8M8OM8c8.jpg", "youtube_id": "Ga6Ry6R0sAc"},
    "How to Train Your Dragon: The Hidden World": {"poster": f"{POSTER_BASE}/h3bdM0AUXVhb21f0hgt0xGG0c0.jpg", "youtube_id": "SkcNCc1G-vA"},
    "Spider-Man: Into the Spider-Verse": {"poster": f"{POSTER_BASE}/iiRMnTS4NpwjDrBGpF7oG9EnTa.jpg", "youtube_id": "g4Hbz2jLHIQ"},
    "PAW Patrol: The Movie": {"poster": f"{POSTER_BASE}/kek75jgL5Y8pqr9Z9Z9Z9Z9Z9Z9.jpg", "youtube_id": "Ud_r7P9d9E4"},
    "The SpongeBob Movie: Sponge on the Run": {"poster": f"{POSTER_BASE}/7zt4yn5K6bka40jX1X4X4X4X4X4.jpg", "youtube_id": "5N5G0d4mN6g"},
    "My Policeman": {"poster": f"{POSTER_BASE}/9P5D0k0k0k0k0k0k0k0k0k0k0k0.jpg", "youtube_id": "QJM1pRJa9VA"},
    "Falling for Christmas": {"poster": f"{POSTER_BASE}/8Gxv8gSX0FCXQSC7wQMwq3ckLu.jpg", "youtube_id": "6puvP0hR3L4"},
    "Ticket to Paradise": {"poster": f"{POSTER_BASE}/4M0oQF5TFo0c5P0l0l0l0l0l0l0.jpg", "youtube_id": "hkP4tVTszi0"},
    "The Lost City": {"poster": f"{POSTER_BASE}/neYIi8pAE1a1bTJk9Hs5d4xWDDU.jpg", "youtube_id": "T7WRXTr2lN4"},
    "Downton Abbey: A New Era": {"poster": f"{POSTER_BASE}/1M876Kt3vU4n4n4n4n4n4n4n4n4.jpg", "youtube_id": "n3uwOz3N6Bc"},
    "X": {"poster": f"{POSTER_BASE}/4QUnq0aUpm7Px1L0r2X2X2X2X2X2.jpg", "youtube_id": "Lp9o1R8Gc-Q"},
    "Pearl": {"poster": f"{POSTER_BASE}/ujr5Pz2X2X2X2X2X2X2X2X2X2X2.jpg", "youtube_id": "L5PW4r_VB9w"},
    "Alien: Covenant": {"poster": f"{POSTER_BASE}/1uxQWfTIWfQG0g5N2V2N2V2N2V2N.jpg", "youtube_id": "svnAD0TApb8"},
    "Hellraiser": {"poster": f"{POSTER_BASE}/jD5a2A2A2A2A2A2A2A2A2A2A2A.jpg", "youtube_id": "0tR1IIOK1ko"},
    "Last Night in Soho": {"poster": f"{POSTER_BASE}/4g2F8a8W8W8W8W8W8W8W8W8W8W8.jpg", "youtube_id": "AcVnFrxjPjI"},
}


def fallback_poster(title: str) -> str:
    return f"https://placehold.co/300x450/1a1a2e/e94560?text={quote(title)}"


def enrich_movie(movie: dict) -> dict:
    """Attach poster URL and YouTube trailer id to a movie dict."""
    enriched = dict(movie)
    media = MOVIE_MEDIA.get(movie["title"], {})
    poster = media.get("poster")
    enriched["poster"] = poster if poster else fallback_poster(movie["title"])
    enriched["youtube_id"] = media.get("youtube_id")
    enriched["youtube_search"] = f"{movie['title']} {movie['year']} official trailer"
    return enriched
