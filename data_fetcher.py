import os, requests
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("FOOTBALL_API_KEY", "")
BASE_URL = "https://api.football-data.org/v4"
WC_CODE  = "WC"
HEADERS  = {"X-Auth-Token": API_KEY}

GROUPS_DATA = {
    "A": ["México","Sudáfrica","Corea del Sur","Chequia"],
    "B": ["Canadá","Qatar","Suiza","Bosnia y Herz."],
    "C": ["Brasil","Marruecos","Haití","Escocia"],
    "D": ["EE.UU.","Paraguay","Australia","Turquía"],
    "E": ["Alemania","Ecuador","Costa de Marfil","Curazao"],
    "F": ["Países Bajos","Arabia Saudita","Uzbekistán","Noruega"],
    "G": ["Bélgica","Senegal","Egipto","Irán"],
    "H": ["España","Japón","Túnez","Irak"],
    "I": ["Francia","Colombia","Jordania","Uruguay"],
    "J": ["Argentina","Argelia","Austria","RD Congo"],
    "K": ["Portugal","Croacia","Ghana","Panamá"],
    "L": ["Inglaterra","Suecia","Cabo Verde","Australia"],
}

TEAM_FLAGS = {
    "México":"🇲🇽","Sudáfrica":"🇿🇦","Corea del Sur":"🇰🇷","Chequia":"🇨🇿",
    "Canadá":"🇨🇦","Qatar":"🇶🇦","Suiza":"🇨🇭","Bosnia y Herz.":"🇧🇦",
    "Brasil":"🇧🇷","Marruecos":"🇲🇦","Haití":"🇭🇹","Escocia":"🏴󠁧󠁢󠁳󠁣󠁴󠁿",
    "EE.UU.":"🇺🇸","Paraguay":"🇵🇾","Australia":"🇦🇺","Turquía":"🇹🇷",
    "Alemania":"🇩🇪","Ecuador":"🇪🇨","Costa de Marfil":"🇨🇮","Curazao":"🇨🇼",
    "Países Bajos":"🇳🇱","Arabia Saudita":"🇸🇦","Uzbekistán":"🇺🇿","Noruega":"🇳🇴",
    "Bélgica":"🇧🇪","Senegal":"🇸🇳","Egipto":"🇪🇬","Irán":"🇮🇷",
    "España":"🇪🇸","Japón":"🇯🇵","Túnez":"🇹🇳","Irak":"🇮🇶",
    "Francia":"🇫🇷","Colombia":"🇨🇴","Jordania":"🇯🇴","Uruguay":"🇺🇾",
    "Argentina":"🇦🇷","Argelia":"🇩🇿","Austria":"🇦🇹","RD Congo":"🇨🇩",
    "Portugal":"🇵🇹","Croacia":"🇭🇷","Ghana":"🇬🇭","Panamá":"🇵🇦",
    "Inglaterra":"🏴󠁧󠁢󠁥󠁮󠁧󠁿","Suecia":"🇸🇪","Cabo Verde":"🇨🇻",
}

FIFA_RATINGS = {
    "Argentina":1838,"Francia":1835,"España":1832,"Inglaterra":1814,
    "Brasil":1810,"Portugal":1805,"Países Bajos":1798,"Bélgica":1795,
    "Alemania":1790,"Uruguay":1785,"Marruecos":1775,"Japón":1770,
    "EE.UU.":1765,"México":1762,"Colombia":1758,"Croacia":1755,
    "Senegal":1748,"Corea del Sur":1745,"Ecuador":1740,"Suiza":1738,
    "Austria":1735,"Noruega":1730,"Turquía":1728,"Australia":1720,
    "Irán":1715,"Egipto":1710,"Canadá":1708,"Paraguay":1705,
    "Ghana":1700,"Chequia":1698,"Arabia Saudita":1695,"Escocia":1692,
    "Sudáfrica":1688,"Bosnia y Herz.":1685,"Uzbekistán":1680,"Túnez":1678,
    "Argelia":1675,"RD Congo":1670,"Costa de Marfil":1668,"Panamá":1662,
    "Qatar":1655,"Irak":1650,"Jordania":1645,"Haití":1640,
    "Suecia":1638,"Cabo Verde":1620,"Curazao":1610,
}

# Partidos reales del Mundial 2026 - Fase de grupos
LIVE_MATCHES_FALLBACK = [
    {"id":1,"homeTeam":{"name":"México"},"awayTeam":{"name":"Sudáfrica"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED","elapsed":None},"utcDate":"2026-06-11T18:00:00Z","group":"Grupo A"},
    {"id":2,"homeTeam":{"name":"EE.UU."},"awayTeam":{"name":"Paraguay"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED","elapsed":None},"utcDate":"2026-06-12T21:00:00Z","group":"Grupo D"},
    {"id":3,"homeTeam":{"name":"Canadá"},"awayTeam":{"name":"Qatar"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED","elapsed":None},"utcDate":"2026-06-12T18:00:00Z","group":"Grupo B"},
    {"id":4,"homeTeam":{"name":"Argentina"},"awayTeam":{"name":"Argelia"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED","elapsed":None},"utcDate":"2026-06-13T18:00:00Z","group":"Grupo J"},
    {"id":5,"homeTeam":{"name":"España"},"awayTeam":{"name":"Japón"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED","elapsed":None},"utcDate":"2026-06-13T21:00:00Z","group":"Grupo H"},
    {"id":6,"homeTeam":{"name":"Brasil"},"awayTeam":{"name":"Marruecos"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED","elapsed":None},"utcDate":"2026-06-14T18:00:00Z","group":"Grupo C"},
    {"id":7,"homeTeam":{"name":"Francia"},"awayTeam":{"name":"Colombia"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED","elapsed":None},"utcDate":"2026-06-14T21:00:00Z","group":"Grupo I"},
    {"id":8,"homeTeam":{"name":"Portugal"},"awayTeam":{"name":"Croacia"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED","elapsed":None},"utcDate":"2026-06-15T18:00:00Z","group":"Grupo K"},
    {"id":9,"homeTeam":{"name":"Alemania"},"awayTeam":{"name":"Ecuador"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED","elapsed":None},"utcDate":"2026-06-15T21:00:00Z","group":"Grupo E"},
    {"id":10,"homeTeam":{"name":"Inglaterra"},"awayTeam":{"name":"Suecia"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED","elapsed":None},"utcDate":"2026-06-16T18:00:00Z","group":"Grupo L"},
    {"id":11,"homeTeam":{"name":"Países Bajos"},"awayTeam":{"name":"Arabia Saudita"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED","elapsed":None},"utcDate":"2026-06-16T21:00:00Z","group":"Grupo F"},
    {"id":12,"homeTeam":{"name":"Bélgica"},"awayTeam":{"name":"Senegal"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED","elapsed":None},"utcDate":"2026-06-17T18:00:00Z","group":"Grupo G"},
]

def get_competition_info():
    if not API_KEY:
        return {"name": "Mundial 2026", "currentSeason": {}}
    try:
        r = requests.get(f"{BASE_URL}/competitions/{WC_CODE}", headers=HEADERS, timeout=10)
        if r.status_code == 200:
            return r.json()
    except Exception as e:
        print(f"API error: {e}")
    return {"name": "Mundial 2026", "currentSeason": {}}

def get_wc_matches():
    if not API_KEY:
        return LIVE_MATCHES_FALLBACK
    try:
        r = requests.get(f"{BASE_URL}/competitions/{WC_CODE}/matches", headers=HEADERS, timeout=15)
        if r.status_code == 200:
            matches = r.json().get("matches", [])
            if matches:
                return matches
        print(f"API matches error {r.status_code}")
    except Exception as e:
        print(f"API error: {e}")
    return LIVE_MATCHES_FALLBACK

def get_all_groups():
    teams = []
    for group, names in GROUPS_DATA.items():
        for name in names:
            teams.append({"group": group, "name": name,
                          "flag": TEAM_FLAGS.get(name, "🏳️"),
                          "fifa_rating": FIFA_RATINGS.get(name, 1600)})
    return teams
