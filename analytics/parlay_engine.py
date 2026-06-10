from analytics.xg_model import match_probabilities


PICK_TYPES = {
    "home_win":       lambda r: r["home_win_prob"],
    "draw":           lambda r: r["draw_prob"],
    "away_win":       lambda r: r["away_win_prob"],
    "over_25":        lambda r: r["over_25"],
    "under_25":       lambda r: 100 - r["over_25"],
    "btts_yes":       lambda r: r["btts"],
    "btts_no":        lambda r: 100 - r["btts"],
    "over_35":        lambda r: r["over_35"],
    "over_9_corners": lambda r: r["over_9_corners"],
    "over_3_yellow":  lambda r: r["over_3_yellow"],
}

PICK_LABELS = {
    "home_win":       lambda r: f"{r['home_flag']} {r['home']} gana",
    "draw":           lambda r: "Empate",
    "away_win":       lambda r: f"{r['away_flag']} {r['away']} gana",
    "over_25":        lambda r: "Más de 2.5 goles",
    "under_25":       lambda r: "Menos de 2.5 goles",
    "btts_yes":       lambda r: "Ambos anotan",
    "btts_no":        lambda r: "No ambos anotan",
    "over_35":        lambda r: "Más de 3.5 goles",
    "over_9_corners": lambda r: "Más de 9 corners",
    "over_3_yellow":  lambda r: "Más de 3 tarjetas amarillas",
}


def prob_to_american_odds(prob: float) -> str:
    if prob <= 0 or prob >= 100:
        return "N/A"
    p = prob / 100
    if p >= 0.5:
        return f"-{round((p / (1 - p)) * 100)}"
    else:
        return f"+{round(((1 - p) / p) * 100)}"


def prob_to_decimal_odds(prob: float) -> float:
    if prob <= 0:
        return 0.0
    return round(100 / prob, 2)


def build_parlay(picks: list) -> dict:
    """
    picks: lista de dicts con keys: home, away, pick_type
    Ej: [{"home": "Argentina", "away": "Francia", "pick_type": "home_win"}, ...]
    """
    processed = []
    combined_prob = 1.0

    for pick in picks:
        result = match_probabilities(pick["home"], pick["away"])
        getter = PICK_TYPES.get(pick["pick_type"])
        labeler = PICK_LABELS.get(pick["pick_type"])
        if not getter:
            continue
        prob = getter(result)
        combined_prob *= (prob / 100)
        processed.append({
            "match": f"{result['home_flag']} {pick['home']} vs {result['away_flag']} {pick['away']}",
            "pick": labeler(result) if labeler else pick["pick_type"],
            "probability": prob,
            "decimal_odds": prob_to_decimal_odds(prob),
            "american_odds": prob_to_american_odds(prob),
            "xg": f"{result['home_xg']} - {result['away_xg']}",
            "form_home": result["home_form"],
            "form_away": result["away_form"],
        })

    combined_prob_pct = round(combined_prob * 100, 2)
    parlay_decimal    = round(1 / combined_prob, 2) if combined_prob > 0 else 0
    value_rating = "🔥 Alto valor" if combined_prob_pct > 20 else \
                   "✅ Valor moderado" if combined_prob_pct > 8 else \
                   "⚠️ Riesgo alto"

    return {
        "picks": processed,
        "combined_probability": combined_prob_pct,
        "parlay_decimal_odds": parlay_decimal,
        "parlay_american_odds": prob_to_american_odds(combined_prob_pct),
        "value_rating": value_rating,
        "num_legs": len(processed),
    }


def suggest_best_picks(home: str, away: str, top_n: int = 3) -> list:
    result = match_probabilities(home, away)
    candidates = []
    for key, getter in PICK_TYPES.items():
        prob = getter(result)
        if prob >= 55:
            labeler = PICK_LABELS[key]
            candidates.append({
                "pick_type": key,
                "label": labeler(result),
                "probability": prob,
                "decimal_odds": prob_to_decimal_odds(prob),
                "american_odds": prob_to_american_odds(prob),
            })
    candidates.sort(key=lambda x: x["probability"], reverse=True)
    return candidates[:top_n]
