from data_fetcher import GROUPS_DATA, FIFA_RATINGS, TEAM_FLAGS


WC_STATS = {
    "Argentina":      {"attack": 92, "defense": 84, "midfield": 88, "avg_goals_scored": 2.4, "avg_goals_conceded": 0.8, "form": ["W","W","W","D","W"], "clean_sheets": 3, "avg_corners": 6.2, "avg_yellow": 1.8},
    "Francia":        {"attack": 91, "defense": 86, "midfield": 87, "avg_goals_scored": 2.2, "avg_goals_conceded": 0.9, "form": ["W","W","D","W","W"], "clean_sheets": 3, "avg_corners": 6.8, "avg_yellow": 2.0},
    "España":         {"attack": 87, "defense": 83, "midfield": 90, "avg_goals_scored": 2.3, "avg_goals_conceded": 0.7, "form": ["W","W","W","W","D"], "clean_sheets": 4, "avg_corners": 7.1, "avg_yellow": 1.6},
    "Inglaterra":     {"attack": 85, "defense": 82, "midfield": 83, "avg_goals_scored": 2.0, "avg_goals_conceded": 1.0, "form": ["W","D","W","W","W"], "clean_sheets": 2, "avg_corners": 6.0, "avg_yellow": 1.9},
    "Brasil":         {"attack": 88, "defense": 80, "midfield": 86, "avg_goals_scored": 2.1, "avg_goals_conceded": 1.1, "form": ["W","W","L","W","W"], "clean_sheets": 2, "avg_corners": 6.5, "avg_yellow": 2.1},
    "Portugal":       {"attack": 89, "defense": 78, "midfield": 82, "avg_goals_scored": 2.5, "avg_goals_conceded": 1.2, "form": ["W","W","W","D","W"], "clean_sheets": 2, "avg_corners": 5.8, "avg_yellow": 2.2},
    "Países Bajos":   {"attack": 84, "defense": 80, "midfield": 83, "avg_goals_scored": 1.9, "avg_goals_conceded": 1.0, "form": ["W","D","W","W","D"], "clean_sheets": 2, "avg_corners": 5.9, "avg_yellow": 1.7},
    "Bélgica":        {"attack": 83, "defense": 78, "midfield": 82, "avg_goals_scored": 1.8, "avg_goals_conceded": 1.1, "form": ["D","W","W","L","W"], "clean_sheets": 2, "avg_corners": 5.5, "avg_yellow": 2.0},
    "Alemania":       {"attack": 83, "defense": 81, "midfield": 84, "avg_goals_scored": 2.0, "avg_goals_conceded": 1.0, "form": ["W","W","D","W","W"], "clean_sheets": 3, "avg_corners": 6.2, "avg_yellow": 1.8},
    "Uruguay":        {"attack": 82, "defense": 84, "midfield": 79, "avg_goals_scored": 1.7, "avg_goals_conceded": 0.8, "form": ["W","D","W","D","W"], "clean_sheets": 3, "avg_corners": 4.8, "avg_yellow": 2.3},
    "Marruecos":      {"attack": 76, "defense": 82, "midfield": 76, "avg_goals_scored": 1.5, "avg_goals_conceded": 0.7, "form": ["W","W","D","W","D"], "clean_sheets": 4, "avg_corners": 5.0, "avg_yellow": 2.1},
    "Japón":          {"attack": 76, "defense": 78, "midfield": 78, "avg_goals_scored": 1.6, "avg_goals_conceded": 1.0, "form": ["W","W","D","W","L"], "clean_sheets": 2, "avg_corners": 5.2, "avg_yellow": 1.5},
    "EE.UU.":         {"attack": 74, "defense": 72, "midfield": 74, "avg_goals_scored": 1.8, "avg_goals_conceded": 1.2, "form": ["W","W","D","W","D"], "clean_sheets": 2, "avg_corners": 5.8, "avg_yellow": 1.9},
    "México":         {"attack": 75, "defense": 73, "midfield": 75, "avg_goals_scored": 1.6, "avg_goals_conceded": 1.1, "form": ["D","W","W","D","W"], "clean_sheets": 2, "avg_corners": 5.3, "avg_yellow": 2.0},
    "Colombia":       {"attack": 80, "defense": 76, "midfield": 79, "avg_goals_scored": 1.9, "avg_goals_conceded": 1.0, "form": ["W","W","W","D","W"], "clean_sheets": 2, "avg_corners": 5.6, "avg_yellow": 2.1},
    "Croacia":        {"attack": 78, "defense": 79, "midfield": 80, "avg_goals_scored": 1.6, "avg_goals_conceded": 0.9, "form": ["D","W","D","W","W"], "clean_sheets": 3, "avg_corners": 5.1, "avg_yellow": 1.8},
    "Senegal":        {"attack": 74, "defense": 74, "midfield": 72, "avg_goals_scored": 1.5, "avg_goals_conceded": 1.0, "form": ["W","D","W","W","D"], "clean_sheets": 2, "avg_corners": 4.9, "avg_yellow": 2.2},
    "Corea del Sur":  {"attack": 72, "defense": 70, "midfield": 74, "avg_goals_scored": 1.4, "avg_goals_conceded": 1.2, "form": ["W","L","W","D","W"], "clean_sheets": 1, "avg_corners": 5.4, "avg_yellow": 1.7},
    "Ecuador":        {"attack": 72, "defense": 70, "midfield": 71, "avg_goals_scored": 1.5, "avg_goals_conceded": 1.1, "form": ["W","D","W","L","W"], "clean_sheets": 2, "avg_corners": 4.7, "avg_yellow": 2.0},
    "Suiza":          {"attack": 74, "defense": 75, "midfield": 76, "avg_goals_scored": 1.7, "avg_goals_conceded": 0.9, "form": ["W","W","D","W","D"], "clean_sheets": 3, "avg_corners": 5.3, "avg_yellow": 1.6},
    "Austria":        {"attack": 75, "defense": 73, "midfield": 74, "avg_goals_scored": 1.8, "avg_goals_conceded": 1.1, "form": ["W","W","D","W","L"], "clean_sheets": 2, "avg_corners": 5.5, "avg_yellow": 1.9},
    "Noruega":        {"attack": 78, "defense": 72, "midfield": 74, "avg_goals_scored": 2.0, "avg_goals_conceded": 1.3, "form": ["W","W","W","D","W"], "clean_sheets": 1, "avg_corners": 5.7, "avg_yellow": 1.8},
    "Turquía":        {"attack": 74, "defense": 71, "midfield": 72, "avg_goals_scored": 1.6, "avg_goals_conceded": 1.2, "form": ["W","D","W","W","L"], "clean_sheets": 1, "avg_corners": 5.0, "avg_yellow": 2.3},
    "Australia":      {"attack": 68, "defense": 68, "midfield": 69, "avg_goals_scored": 1.3, "avg_goals_conceded": 1.3, "form": ["D","W","L","W","D"], "clean_sheets": 1, "avg_corners": 4.5, "avg_yellow": 1.7},
    "Irán":           {"attack": 66, "defense": 70, "midfield": 67, "avg_goals_scored": 1.2, "avg_goals_conceded": 1.0, "form": ["D","D","W","D","W"], "clean_sheets": 2, "avg_corners": 4.3, "avg_yellow": 2.1},
    "Egipto":         {"attack": 70, "defense": 68, "midfield": 68, "avg_goals_scored": 1.4, "avg_goals_conceded": 1.1, "form": ["W","D","W","D","D"], "clean_sheets": 2, "avg_corners": 4.8, "avg_yellow": 1.9},
    "Canadá":         {"attack": 72, "defense": 70, "midfield": 72, "avg_goals_scored": 1.6, "avg_goals_conceded": 1.2, "form": ["W","W","D","W","W"], "clean_sheets": 2, "avg_corners": 5.2, "avg_yellow": 1.8},
    "Paraguay":       {"attack": 68, "defense": 70, "midfield": 67, "avg_goals_scored": 1.3, "avg_goals_conceded": 1.0, "form": ["D","W","D","D","W"], "clean_sheets": 2, "avg_corners": 4.6, "avg_yellow": 2.2},
    "Ghana":          {"attack": 68, "defense": 65, "midfield": 66, "avg_goals_scored": 1.4, "avg_goals_conceded": 1.4, "form": ["W","L","W","D","W"], "clean_sheets": 1, "avg_corners": 4.7, "avg_yellow": 2.0},
    "Chequia":        {"attack": 70, "defense": 68, "midfield": 69, "avg_goals_scored": 1.5, "avg_goals_conceded": 1.2, "form": ["W","D","W","D","L"], "clean_sheets": 1, "avg_corners": 5.0, "avg_yellow": 1.7},
    "Arabia Saudita": {"attack": 65, "defense": 66, "midfield": 64, "avg_goals_scored": 1.2, "avg_goals_conceded": 1.3, "form": ["D","W","D","W","L"], "clean_sheets": 1, "avg_corners": 4.1, "avg_yellow": 2.0},
    "Escocia":        {"attack": 66, "defense": 67, "midfield": 68, "avg_goals_scored": 1.3, "avg_goals_conceded": 1.1, "form": ["D","D","W","W","D"], "clean_sheets": 2, "avg_corners": 4.8, "avg_yellow": 1.6},
    "Bosnia y Herz.": {"attack": 67, "defense": 65, "midfield": 66, "avg_goals_scored": 1.4, "avg_goals_conceded": 1.3, "form": ["W","L","W","D","W"], "clean_sheets": 1, "avg_corners": 4.5, "avg_yellow": 2.1},
    "Uzbekistán":     {"attack": 64, "defense": 63, "midfield": 64, "avg_goals_scored": 1.2, "avg_goals_conceded": 1.2, "form": ["D","W","D","W","D"], "clean_sheets": 1, "avg_corners": 4.0, "avg_yellow": 1.8},
    "Túnez":          {"attack": 65, "defense": 66, "midfield": 64, "avg_goals_scored": 1.1, "avg_goals_conceded": 1.0, "form": ["D","W","D","D","W"], "clean_sheets": 2, "avg_corners": 4.2, "avg_yellow": 1.9},
    "Argelia":        {"attack": 66, "defense": 65, "midfield": 65, "avg_goals_scored": 1.3, "avg_goals_conceded": 1.2, "form": ["W","D","D","W","D"], "clean_sheets": 1, "avg_corners": 4.4, "avg_yellow": 2.0},
    "RD Congo":       {"attack": 64, "defense": 63, "midfield": 63, "avg_goals_scored": 1.2, "avg_goals_conceded": 1.3, "form": ["D","W","L","W","D"], "clean_sheets": 1, "avg_corners": 4.1, "avg_yellow": 2.2},
    "Costa de Marfil":{"attack": 68, "defense": 64, "midfield": 66, "avg_goals_scored": 1.4, "avg_goals_conceded": 1.2, "form": ["W","D","W","L","W"], "clean_sheets": 1, "avg_corners": 4.6, "avg_yellow": 2.1},
    "Panamá":         {"attack": 62, "defense": 65, "midfield": 62, "avg_goals_scored": 1.1, "avg_goals_conceded": 1.1, "form": ["D","D","W","D","D"], "clean_sheets": 2, "avg_corners": 3.9, "avg_yellow": 2.0},
    "Qatar":          {"attack": 62, "defense": 60, "midfield": 61, "avg_goals_scored": 1.0, "avg_goals_conceded": 1.4, "form": ["L","D","W","L","D"], "clean_sheets": 1, "avg_corners": 3.8, "avg_yellow": 1.8},
    "Irak":           {"attack": 61, "defense": 62, "midfield": 60, "avg_goals_scored": 1.1, "avg_goals_conceded": 1.3, "form": ["W","D","D","L","W"], "clean_sheets": 1, "avg_corners": 3.7, "avg_yellow": 2.2},
    "Jordania":       {"attack": 60, "defense": 61, "midfield": 60, "avg_goals_scored": 0.9, "avg_goals_conceded": 1.2, "form": ["D","W","D","D","L"], "clean_sheets": 1, "avg_corners": 3.6, "avg_yellow": 1.9},
    "Haití":          {"attack": 58, "defense": 59, "midfield": 58, "avg_goals_scored": 0.8, "avg_goals_conceded": 1.5, "form": ["L","D","D","W","L"], "clean_sheets": 0, "avg_corners": 3.4, "avg_yellow": 2.1},
    "Suecia":         {"attack": 69, "defense": 68, "midfield": 70, "avg_goals_scored": 1.5, "avg_goals_conceded": 1.1, "form": ["W","D","W","W","D"], "clean_sheets": 2, "avg_corners": 5.0, "avg_yellow": 1.7},
    "Cabo Verde":     {"attack": 60, "defense": 60, "midfield": 59, "avg_goals_scored": 1.0, "avg_goals_conceded": 1.3, "form": ["D","W","L","D","W"], "clean_sheets": 1, "avg_corners": 3.5, "avg_yellow": 2.0},
    "Curazao":        {"attack": 56, "defense": 55, "midfield": 55, "avg_goals_scored": 0.8, "avg_goals_conceded": 1.6, "form": ["L","D","L","W","D"], "clean_sheets": 0, "avg_corners": 3.2, "avg_yellow": 2.1},
}


def calculate_form_score(team_name: str) -> dict:
    stats = WC_STATS.get(team_name)
    if not stats:
        return {"form_score": 50, "trend": "neutral"}

    form = stats["form"]
    points = {"W": 3, "D": 1, "L": 0}
    weights = [0.35, 0.25, 0.20, 0.12, 0.08]
    weighted_pts = sum(points[r] * w for r, w in zip(form, weights))
    max_pts = 3 * sum(weights)
    form_score = round((weighted_pts / max_pts) * 100)

    wins = form.count("W")
    losses = form.count("L")
    trend = "ascendente" if wins >= 3 else "descendente" if losses >= 2 else "estable"

    return {
        "team": team_name,
        "flag": TEAM_FLAGS.get(team_name, "🏳️"),
        "fifa_rating": FIFA_RATINGS.get(team_name, 1600),
        "form": form,
        "form_score": form_score,
        "trend": trend,
        "attack": stats["attack"],
        "defense": stats["defense"],
        "midfield": stats["midfield"],
        "avg_goals_scored": stats["avg_goals_scored"],
        "avg_goals_conceded": stats["avg_goals_conceded"],
        "avg_corners": stats["avg_corners"],
        "avg_yellow": stats["avg_yellow"],
        "clean_sheets": stats["clean_sheets"],
    }


def get_all_teams_form() -> list:
    result = []
    for group, names in GROUPS_DATA.items():
        for name in names:
            data = calculate_form_score(name)
            data["group"] = group
            result.append(data)
    return result


def get_group_teams(group: str) -> list:
    names = GROUPS_DATA.get(group.upper(), [])
    return [calculate_form_score(n) for n in names]
