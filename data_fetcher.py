import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FOOTBALL_API_KEY")
BASE_URL = "https://api.football-data.org/v4"
WC_CODE  = "WC"

HEADERS = {
    "X-Auth-Token": API_KEY
}

GROUPS_DATA = {
    "A": ["México",         "Sudáfrica",    "Corea del Sur", "Chequia"],
    "B": ["Canadá",         "Qatar",        "Suiza",         "Bosnia y Herz."],
    "C": ["Brasil",         "Marruecos",    "Haití",         "Escocia"],
    "D": ["EE.UU.",         "Paraguay",     "Australia",     "Turquía"],
    "E": ["Alemania",       "Ecuador",      "Costa de Marfil","Curazao"],
    "F": ["Países Bajos",   "Arabia Saudita","Uzbekistán",   "Noruega"],
    "G": ["Bélgica",        "Senegal",      "Egipto",        "Irán"],
    "H": ["España",         "Japón",        "Túnez",         "Irak"],
    "I": ["Francia",        "Colombia",     "Jordania",      "Uruguay"],
    "J": ["Argentina",      "Argelia",      "Austria",       "RD Congo"],
    "K": ["Portugal",       "Croacia",      "Ghana",         "Panamá"],
    "L": ["Inglaterra",     "Suecia",       "Cabo Verde",    "Australia"],
}

TEAM_FLAGS = {
    "México": "🇲🇽", "Sudáfrica": "🇿🇦", "Corea del Sur": "🇰🇷", "Chequia": "🇨🇿",
    "Canadá": "🇨🇦", "Qatar": "🇶🇦", "Suiza": "🇨🇭", "Bosnia y Herz.": "🇧🇦",
    "Brasil": "🇧🇷", "Marruecos": "🇲🇦", "Haití": "🇭🇹", "Escocia": "🏴󠁧󠁢󠁳󠁣󠁴󠁿",
    "EE.UU.": "🇺🇸", "Paraguay": "🇵🇾", "Australia": "🇦🇺", "Turquía": "🇹🇷",
    "Alemania": "🇩🇪", "Ecuador": "🇪🇨", "Costa de Marfil": "🇨🇮", "Curazao": "🇨🇼",
    "Países Bajos": "🇳🇱", "Arabia Saudita": "🇸🇦", "Uzbekistán": "🇺🇿", "Noruega": "🇳🇴",
    "Bélgica": "🇧🇪", "Senegal": "🇸🇳", "Egipto": "🇪🇬", "Irán": "🇮🇷",
    "España": "🇪🇸", "Japón": "🇯🇵", "Túnez": "🇹🇳", "Irak": "🇮🇶",
    "Francia": "🇫🇷", "Colombia": "🇨🇴", "Jordania": "🇯🇴", "Uruguay": "🇺🇾",
    "Argentina": "🇦🇷", "Argelia": "🇩🇿", "Austria": "🇦🇹", "RD Congo": "🇨🇩",
    "Portugal": "🇵🇹", "Croacia": "🇭🇷", "Ghana": "🇬🇭", "Panamá": "🇵🇦",
    "Inglaterra": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "Suecia": "🇸🇪", "Cabo Verde": "🇨🇻",
}

FIFA_RATINGS = {
    "Argentina": 1838, "Francia": 1835, "España": 1832, "Inglaterra": 1814,
    "Brasil": 1810, "Portugal": 1805, "Países Bajos": 1798, "Bélgica": 1795,
    "Alemania": 1790, "Uruguay": 1785, "Marruecos": 1775, "Japón": 1770,
    "EE.UU.": 1765, "México": 1762, "Colombia": 1758, "Croacia": 1755,
    "Senegal": 1748, "Corea del Sur": 1745, "Ecuador": 1740, "Suiza": 1738,
    "Austria": 1735, "Noruega": 1730, "Turquía": 1728, "Australia": 1720,
    "Irán": 1715, "Egipto": 1710, "Canadá": 1708, "Paraguay": 1705,
    "Ghana": 1700, "Chequia": 1698, "Arabia Saudita": 1695, "Escocia": 1692,
    "Sudáfrica": 1688, "Bosnia y Herz.": 1685, "Uzbekistán": 1680, "Túnez": 1678,
    "Argelia": 1675, "RD Congo": 1670, "Costa de Marfil": 1668, "Panamá": 1662,
    "Qatar": 1655, "Irak": 1650, "Jordania": 1645, "Haití": 1640,
    "Suecia": 1638, "Cabo Verde": 1620, "Curazao": 1610,
}


def get_competition_info():
    url = f"{BASE_URL}/competitions/{WC_CODE}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        if r.status_code == 200:
            return r.json()
    except Exception as e:
        print(f"Error fetching competition: {e}")
    return None


def get_wc_matches():
    url = f"{BASE_URL}/competitions/{WC_CODE}/matches"
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        if r.status_code == 200:
            return r.json().get("matches", [])
        print(f"API error {r.status_code}: {r.text[:200]}")
    except Exception as e:
        print(f"Error fetching matches: {e}")
    return []


def get_wc_teams():
    url = f"{BASE_URL}/competitions/{WC_CODE}/teams"
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        if r.status_code == 200:
            return r.json().get("teams", [])
        print(f"API error {r.status_code}: {r.text[:200]}")
    except Exception as e:
        print(f"Error fetching teams: {e}")
    return []


def get_wc_standings():
    url = f"{BASE_URL}/competitions/{WC_CODE}/standings"
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        if r.status_code == 200:
            return r.json().get("standings", [])
        print(f"API error {r.status_code}: {r.text[:200]}")
    except Exception as e:
        print(f"Error fetching standings: {e}")
    return []


def get_all_groups():
    teams = []
    for group, names in GROUPS_DATA.items():
        for name in names:
            teams.append({
                "group": group,
                "name": name,
                "flag": TEAM_FLAGS.get(name, "🏳️"),
                "fifa_rating": FIFA_RATINGS.get(name, 1600),
            })
    return teams


def get_team_recent_matches(team_id: int, limit: int = 5):
    url = f"{BASE_URL}/teams/{team_id}/matches"
    params = {"limit": limit, "status": "FINISHED"}
    try:
        r = requests.get(url, headers=HEADERS, params=params, timeout=10)
        if r.status_code == 200:
            return r.json().get("matches", [])
    except Exception as e:
        print(f"Error fetching team matches: {e}")
    return []


if __name__ == "__main__":
    print("=== TEST DATA FETCHER ===")
    info = get_competition_info()
    if info:
        print(f"Competición: {info.get('name')} — temporada actual: {info.get('currentSeason', {}).get('startDate', 'N/A')}")
    else:
        print("No se pudo conectar a la API — verifica tu API key en .env")

    groups = get_all_groups()
    print(f"\nEquipos cargados: {len(groups)}")
    for g in groups[:4]:
        print(f"  Grupo {g['group']}: {g['flag']} {g['name']} (FIFA {g['fifa_rating']})")
    print("  ...")
