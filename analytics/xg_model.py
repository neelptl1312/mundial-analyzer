import math
from analytics.form_model import calculate_form_score


def poisson_prob(lam: float, k: int) -> float:
    return (math.exp(-lam) * (lam ** k)) / math.factorial(k)


def match_probabilities(home_name: str, away_name: str) -> dict:
    h = calculate_form_score(home_name)
    a = calculate_form_score(away_name)

    home_xg = round(
        (h["avg_goals_scored"] * 0.5 +
         (1 - a["defense"] / 100) * h["attack"] / 40 +
         h["form_score"] / 200 +
         0.15),  # ventaja local
        2
    )
    away_xg = round(
        (a["avg_goals_scored"] * 0.5 +
         (1 - h["defense"] / 100) * a["attack"] / 40 +
         a["form_score"] / 200),
        2
    )

    max_goals = 6
    home_win = draw = away_win = 0.0
    score_matrix = {}

    for i in range(max_goals):
        for j in range(max_goals):
            p = poisson_prob(home_xg, i) * poisson_prob(away_xg, j)
            score_matrix[f"{i}-{j}"] = round(p * 100, 2)
            if i > j:
                home_win += p
            elif i == j:
                draw += p
            else:
                away_win += p

    total = home_win + draw + away_win
    home_win /= total
    draw     /= total
    away_win /= total

    over_15 = sum(p/100 for s, p in score_matrix.items()
                  if sum(int(x) for x in s.split("-")) > 1)
    over_25 = sum(p/100 for s, p in score_matrix.items()
                  if sum(int(x) for x in s.split("-")) > 2)
    over_35 = sum(p/100 for s, p in score_matrix.items()
                  if sum(int(x) for x in s.split("-")) > 3)
    btts     = sum(p/100 for s, p in score_matrix.items()
                   if int(s.split("-")[0]) > 0 and int(s.split("-")[1]) > 0)

    corners_expected = round((h["avg_corners"] + a["avg_corners"]) / 2, 1)
    over_9_corners   = round(min(0.95, corners_expected / 12), 2)
    over_10_corners  = round(min(0.88, corners_expected / 14), 2)

    yellows_expected = round((h["avg_yellow"] + a["avg_yellow"]) / 2, 1)
    over_3_yellow    = round(min(0.90, yellows_expected / 4), 2)

    top_score = max(score_matrix, key=score_matrix.get)

    return {
        "home": home_name,
        "away": away_name,
        "home_flag": h["flag"],
        "away_flag": a["flag"],
        "home_xg": home_xg,
        "away_xg": away_xg,
        "home_form": h["form"],
        "away_form": a["form"],
        "home_form_score": h["form_score"],
        "away_form_score": a["form_score"],
        "home_win_prob":  round(home_win * 100, 1),
        "draw_prob":      round(draw     * 100, 1),
        "away_win_prob":  round(away_win * 100, 1),
        "over_15": round(over_15 * 100, 1),
        "over_25": round(over_25 * 100, 1),
        "over_35": round(over_35 * 100, 1),
        "btts":    round(btts    * 100, 1),
        "corners_expected": corners_expected,
        "over_9_corners":  round(over_9_corners  * 100, 1),
        "over_10_corners": round(over_10_corners * 100, 1),
        "yellows_expected": yellows_expected,
        "over_3_yellow":   round(over_3_yellow   * 100, 1),
        "most_likely_score": top_score,
        "score_matrix": score_matrix,
    }
