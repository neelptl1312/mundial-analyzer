import os, sys, math, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, jsonify, render_template, request, make_response
from flask_cors import CORS

app = Flask(__name__, template_folder="frontend/templates", static_folder="frontend/static")
CORS(app)

# ── DATOS ──────────────────────────────────────────────────────────────────────
GROUPS_DATA = {
    "A":["México","Sudáfrica","Corea del Sur","Chequia"],
    "B":["Canadá","Qatar","Suiza","Bosnia y Herz."],
    "C":["Brasil","Marruecos","Haití","Escocia"],
    "D":["EE.UU.","Paraguay","Australia","Turquía"],
    "E":["Alemania","Curazao","Costa de Marfil","Ecuador"],
    "F":["Países Bajos","Japón","Túnez","Suecia"],
    "G":["Bélgica","Egipto","Irán","Nueva Zelanda"],
    "H":["España","Cabo Verde","Arabia Saudita","Uruguay"],
    "I":["Francia","Senegal","Noruega","Irak"],
    "J":["Argentina","Argelia","Austria","Jordania"],
    "K":["Portugal","Colombia","Uzbekistán","RD Congo"],
    "L":["Inglaterra","Croacia","Ghana","Panamá"],
}

FLAGS = {
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

FIFA = {
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

STATS = {
    "Argentina":  {"atk":92,"def":84,"mid":88,"gf":2.4,"gc":0.8,"form":["W","W","W","D","W"],"cs":3,"cor":6.2,"yel":1.8},
    "Francia":    {"atk":91,"def":86,"mid":87,"gf":2.2,"gc":0.9,"form":["W","W","D","W","W"],"cs":3,"cor":6.8,"yel":2.0},
    "España":     {"atk":87,"def":83,"mid":90,"gf":2.3,"gc":0.7,"form":["W","W","W","W","D"],"cs":4,"cor":7.1,"yel":1.6},
    "Inglaterra": {"atk":85,"def":82,"mid":83,"gf":2.0,"gc":1.0,"form":["W","D","W","W","W"],"cs":2,"cor":6.0,"yel":1.9},
    "Brasil":     {"atk":88,"def":80,"mid":86,"gf":2.1,"gc":1.1,"form":["W","W","L","W","W"],"cs":2,"cor":6.5,"yel":2.1},
    "Portugal":   {"atk":89,"def":78,"mid":82,"gf":2.5,"gc":1.2,"form":["W","W","W","D","W"],"cs":2,"cor":5.8,"yel":2.2},
    "Países Bajos":{"atk":84,"def":80,"mid":83,"gf":1.9,"gc":1.0,"form":["W","D","W","W","D"],"cs":2,"cor":5.9,"yel":1.7},
    "Bélgica":    {"atk":83,"def":78,"mid":82,"gf":1.8,"gc":1.1,"form":["D","W","W","L","W"],"cs":2,"cor":5.5,"yel":2.0},
    "Alemania":   {"atk":83,"def":81,"mid":84,"gf":2.0,"gc":1.0,"form":["W","W","D","W","W"],"cs":3,"cor":6.2,"yel":1.8},
    "Uruguay":    {"atk":82,"def":84,"mid":79,"gf":1.7,"gc":0.8,"form":["W","D","W","D","W"],"cs":3,"cor":4.8,"yel":2.3},
    "Marruecos":  {"atk":76,"def":82,"mid":76,"gf":1.5,"gc":0.7,"form":["W","W","D","W","D"],"cs":4,"cor":5.0,"yel":2.1},
    "Japón":      {"atk":76,"def":78,"mid":78,"gf":1.6,"gc":1.0,"form":["W","W","D","W","L"],"cs":2,"cor":5.2,"yel":1.5},
    "EE.UU.":     {"atk":74,"def":72,"mid":74,"gf":1.8,"gc":1.2,"form":["W","W","D","W","D"],"cs":2,"cor":5.8,"yel":1.9},
    "México":     {"atk":75,"def":73,"mid":75,"gf":1.6,"gc":1.1,"form":["D","W","W","D","W"],"cs":2,"cor":5.3,"yel":2.0},
    "Colombia":   {"atk":80,"def":76,"mid":79,"gf":1.9,"gc":1.0,"form":["W","W","W","D","W"],"cs":2,"cor":5.6,"yel":2.1},
    "Croacia":    {"atk":78,"def":79,"mid":80,"gf":1.6,"gc":0.9,"form":["D","W","D","W","W"],"cs":3,"cor":5.1,"yel":1.8},
    "Senegal":    {"atk":74,"def":74,"mid":72,"gf":1.5,"gc":1.0,"form":["W","D","W","W","D"],"cs":2,"cor":4.9,"yel":2.2},
    "Corea del Sur":{"atk":72,"def":70,"mid":74,"gf":1.4,"gc":1.2,"form":["W","L","W","D","W"],"cs":1,"cor":5.4,"yel":1.7},
    "Ecuador":    {"atk":72,"def":70,"mid":71,"gf":1.5,"gc":1.1,"form":["W","D","W","L","W"],"cs":2,"cor":4.7,"yel":2.0},
    "Suiza":      {"atk":74,"def":75,"mid":76,"gf":1.7,"gc":0.9,"form":["W","W","D","W","D"],"cs":3,"cor":5.3,"yel":1.6},
    "Austria":    {"atk":75,"def":73,"mid":74,"gf":1.8,"gc":1.1,"form":["W","W","D","W","L"],"cs":2,"cor":5.5,"yel":1.9},
    "Noruega":    {"atk":78,"def":72,"mid":74,"gf":2.0,"gc":1.3,"form":["W","W","W","D","W"],"cs":1,"cor":5.7,"yel":1.8},
    "Turquía":    {"atk":74,"def":71,"mid":72,"gf":1.6,"gc":1.2,"form":["W","D","W","W","L"],"cs":1,"cor":5.0,"yel":2.3},
    "Australia":  {"atk":68,"def":68,"mid":69,"gf":1.3,"gc":1.3,"form":["D","W","L","W","D"],"cs":1,"cor":4.5,"yel":1.7},
    "Irán":       {"atk":66,"def":70,"mid":67,"gf":1.2,"gc":1.0,"form":["D","D","W","D","W"],"cs":2,"cor":4.3,"yel":2.1},
    "Egipto":     {"atk":70,"def":68,"mid":68,"gf":1.4,"gc":1.1,"form":["W","D","W","D","D"],"cs":2,"cor":4.8,"yel":1.9},
    "Canadá":     {"atk":72,"def":70,"mid":72,"gf":1.6,"gc":1.2,"form":["W","W","D","W","W"],"cs":2,"cor":5.2,"yel":1.8},
    "Paraguay":   {"atk":68,"def":70,"mid":67,"gf":1.3,"gc":1.0,"form":["D","W","D","D","W"],"cs":2,"cor":4.6,"yel":2.2},
    "Ghana":      {"atk":68,"def":65,"mid":66,"gf":1.4,"gc":1.4,"form":["W","L","W","D","W"],"cs":1,"cor":4.7,"yel":2.0},
    "Chequia":    {"atk":70,"def":68,"mid":69,"gf":1.5,"gc":1.2,"form":["W","D","W","D","L"],"cs":1,"cor":5.0,"yel":1.7},
    "Arabia Saudita":{"atk":65,"def":66,"mid":64,"gf":1.2,"gc":1.3,"form":["D","W","D","W","L"],"cs":1,"cor":4.1,"yel":2.0},
    "Escocia":    {"atk":66,"def":67,"mid":68,"gf":1.3,"gc":1.1,"form":["D","D","W","W","D"],"cs":2,"cor":4.8,"yel":1.6},
    "Bosnia y Herz.":{"atk":67,"def":65,"mid":66,"gf":1.4,"gc":1.3,"form":["W","L","W","D","W"],"cs":1,"cor":4.5,"yel":2.1},
    "Uzbekistán": {"atk":64,"def":63,"mid":64,"gf":1.2,"gc":1.2,"form":["D","W","D","W","D"],"cs":1,"cor":4.0,"yel":1.8},
    "Túnez":      {"atk":65,"def":66,"mid":64,"gf":1.1,"gc":1.0,"form":["D","W","D","D","W"],"cs":2,"cor":4.2,"yel":1.9},
    "Argelia":    {"atk":66,"def":65,"mid":65,"gf":1.3,"gc":1.2,"form":["W","D","D","W","D"],"cs":1,"cor":4.4,"yel":2.0},
    "RD Congo":   {"atk":64,"def":63,"mid":63,"gf":1.2,"gc":1.3,"form":["D","W","L","W","D"],"cs":1,"cor":4.1,"yel":2.2},
    "Costa de Marfil":{"atk":68,"def":64,"mid":66,"gf":1.4,"gc":1.2,"form":["W","D","W","L","W"],"cs":1,"cor":4.6,"yel":2.1},
    "Panamá":     {"atk":62,"def":65,"mid":62,"gf":1.1,"gc":1.1,"form":["D","D","W","D","D"],"cs":2,"cor":3.9,"yel":2.0},
    "Qatar":      {"atk":62,"def":60,"mid":61,"gf":1.0,"gc":1.4,"form":["L","D","W","L","D"],"cs":1,"cor":3.8,"yel":1.8},
    "Irak":       {"atk":61,"def":62,"mid":60,"gf":1.1,"gc":1.3,"form":["W","D","D","L","W"],"cs":1,"cor":3.7,"yel":2.2},
    "Jordania":   {"atk":60,"def":61,"mid":60,"gf":0.9,"gc":1.2,"form":["D","W","D","D","L"],"cs":1,"cor":3.6,"yel":1.9},
    "Haití":      {"atk":58,"def":59,"mid":58,"gf":0.8,"gc":1.5,"form":["L","D","D","W","L"],"cs":0,"cor":3.4,"yel":2.1},
    "Suecia":     {"atk":69,"def":68,"mid":70,"gf":1.5,"gc":1.1,"form":["W","D","W","W","D"],"cs":2,"cor":5.0,"yel":1.7},
    "Cabo Verde": {"atk":60,"def":60,"mid":59,"gf":1.0,"gc":1.3,"form":["D","W","L","D","W"],"cs":1,"cor":3.5,"yel":2.0},
    "Curazao":    {"atk":56,"def":55,"mid":55,"gf":0.8,"gc":1.6,"form":["L","D","L","W","D"],"cs":0,"cor":3.2,"yel":2.1},
    "Nueva Zelanda":{"atk":62,"def":62,"mid":61,"gf":1.1,"gc":1.2,"form":["W","D","W","L","D"],"cs":1,"cor":4.0,"yel":1.8},
    "Irak":        {"atk":61,"def":62,"mid":60,"gf":1.1,"gc":1.3,"form":["W","D","D","L","W"],"cs":1,"cor":3.7,"yel":2.2},
}

FALLBACK_MATCHES = [
    # GRUPO A - Jun 11-25
    {"id":1,"homeTeam":{"name":"México"},"awayTeam":{"name":"Corea del Sur"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-11T19:00:00Z","group":"Grupo A"},
    {"id":2,"homeTeam":{"name":"Sudáfrica"},"awayTeam":{"name":"Chequia"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-11T22:00:00Z","group":"Grupo A"},
    {"id":3,"homeTeam":{"name":"México"},"awayTeam":{"name":"Chequia"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-15T19:00:00Z","group":"Grupo A"},
    {"id":4,"homeTeam":{"name":"Corea del Sur"},"awayTeam":{"name":"Sudáfrica"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-15T22:00:00Z","group":"Grupo A"},
    {"id":5,"homeTeam":{"name":"Chequia"},"awayTeam":{"name":"Corea del Sur"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-25T19:00:00Z","group":"Grupo A"},
    {"id":6,"homeTeam":{"name":"Sudáfrica"},"awayTeam":{"name":"México"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-25T19:00:00Z","group":"Grupo A"},
    # GRUPO B - Jun 12-26
    {"id":7,"homeTeam":{"name":"Canadá"},"awayTeam":{"name":"Qatar"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-12T19:00:00Z","group":"Grupo B"},
    {"id":8,"homeTeam":{"name":"Suiza"},"awayTeam":{"name":"Bosnia y Herz."},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-12T22:00:00Z","group":"Grupo B"},
    {"id":9,"homeTeam":{"name":"Canadá"},"awayTeam":{"name":"Bosnia y Herz."},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-16T19:00:00Z","group":"Grupo B"},
    {"id":10,"homeTeam":{"name":"Qatar"},"awayTeam":{"name":"Suiza"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-16T22:00:00Z","group":"Grupo B"},
    # GRUPO C - Jun 12-26
    {"id":11,"homeTeam":{"name":"Brasil"},"awayTeam":{"name":"Marruecos"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-13T19:00:00Z","group":"Grupo C"},
    {"id":12,"homeTeam":{"name":"Haití"},"awayTeam":{"name":"Escocia"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-13T22:00:00Z","group":"Grupo C"},
    {"id":13,"homeTeam":{"name":"Brasil"},"awayTeam":{"name":"Escocia"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-17T19:00:00Z","group":"Grupo C"},
    {"id":14,"homeTeam":{"name":"Marruecos"},"awayTeam":{"name":"Haití"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-17T22:00:00Z","group":"Grupo C"},
    # GRUPO D - Jun 12-26
    {"id":15,"homeTeam":{"name":"EE.UU."},"awayTeam":{"name":"Paraguay"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-12T01:00:00Z","group":"Grupo D"},
    {"id":16,"homeTeam":{"name":"Australia"},"awayTeam":{"name":"Turquía"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-13T01:00:00Z","group":"Grupo D"},
    # GRUPO E - Jun 13-27
    {"id":17,"homeTeam":{"name":"Alemania"},"awayTeam":{"name":"Curazao"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-14T01:00:00Z","group":"Grupo E"},
    {"id":18,"homeTeam":{"name":"Costa de Marfil"},"awayTeam":{"name":"Ecuador"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-14T22:00:00Z","group":"Grupo E"},
    # GRUPO F - Jun 14-28
    {"id":19,"homeTeam":{"name":"Países Bajos"},"awayTeam":{"name":"Japón"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-15T01:00:00Z","group":"Grupo F"},
    {"id":20,"homeTeam":{"name":"Túnez"},"awayTeam":{"name":"Suecia"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-15T22:00:00Z","group":"Grupo F"},
    # GRUPO G - Jun 15-29
    {"id":21,"homeTeam":{"name":"Bélgica"},"awayTeam":{"name":"Egipto"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-16T01:00:00Z","group":"Grupo G"},
    {"id":22,"homeTeam":{"name":"Irán"},"awayTeam":{"name":"Nueva Zelanda"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-16T22:00:00Z","group":"Grupo G"},
    # GRUPO H - Jun 16-30
    {"id":23,"homeTeam":{"name":"España"},"awayTeam":{"name":"Cabo Verde"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-17T01:00:00Z","group":"Grupo H"},
    {"id":24,"homeTeam":{"name":"Arabia Saudita"},"awayTeam":{"name":"Uruguay"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-17T22:00:00Z","group":"Grupo H"},
    # GRUPO I - Jun 17-Jul 1
    {"id":25,"homeTeam":{"name":"Francia"},"awayTeam":{"name":"Senegal"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-18T01:00:00Z","group":"Grupo I"},
    {"id":26,"homeTeam":{"name":"Noruega"},"awayTeam":{"name":"Irak"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-18T22:00:00Z","group":"Grupo I"},
    # GRUPO J - Jun 18-Jul 2
    {"id":27,"homeTeam":{"name":"Argentina"},"awayTeam":{"name":"Argelia"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-19T01:00:00Z","group":"Grupo J"},
    {"id":28,"homeTeam":{"name":"Austria"},"awayTeam":{"name":"Jordania"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-19T22:00:00Z","group":"Grupo J"},
    # GRUPO K - Jun 19-Jul 3
    {"id":29,"homeTeam":{"name":"Portugal"},"awayTeam":{"name":"Colombia"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-20T01:00:00Z","group":"Grupo K"},
    {"id":30,"homeTeam":{"name":"Uzbekistán"},"awayTeam":{"name":"RD Congo"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-20T22:00:00Z","group":"Grupo K"},
    # GRUPO L - Jun 20-Jul 4
    {"id":31,"homeTeam":{"name":"Inglaterra"},"awayTeam":{"name":"Croacia"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-21T01:00:00Z","group":"Grupo L"},
    {"id":32,"homeTeam":{"name":"Ghana"},"awayTeam":{"name":"Panamá"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-21T22:00:00Z","group":"Grupo L"},
]



# ── HELPERS ────────────────────────────────────────────────────────────────────
def form_score(team):
    s = STATS.get(team, {})
    form = s.get("form", ["D","D","D","D","D"])
    pts = {"W":3,"D":1,"L":0}
    weights = [0.35,0.25,0.20,0.12,0.08]
    wp = sum(pts[r]*w for r,w in zip(form,weights))
    return round((wp / (3*sum(weights)))*100)

def get_team_data(name):
    s = STATS.get(name, {"atk":65,"def":65,"mid":65,"gf":1.2,"gc":1.2,"form":["D","D","D","D","D"],"cs":1,"cor":4.5,"yel":2.0})
    fs = form_score(name)
    wins = s["form"].count("W"); losses = s["form"].count("L")
    trend = "ascendente" if wins>=3 else "descendente" if losses>=2 else "estable"
    return {
        "team":name,"flag":FLAGS.get(name,"🏳️"),"group":"",
        "fifa_rating":FIFA.get(name,1600),
        "form":s["form"],"form_score":fs,"trend":trend,
        "attack":s["atk"],"defense":s["def"],"midfield":s["mid"],
        "avg_goals_scored":s["gf"],"avg_goals_conceded":s["gc"],
        "avg_corners":s["cor"],"avg_yellow":s["yel"],"clean_sheets":s["cs"],
    }

def poisson(lam, k):
    return (math.exp(-lam) * (lam**k)) / math.factorial(k)

def analyze(home, away):
    h = get_team_data(home); a = get_team_data(away)
    hxg = round(h["avg_goals_scored"]*0.5 + (1-a["defense"]/100)*h["attack"]/40 + h["form_score"]/200 + 0.15, 2)
    axg = round(a["avg_goals_scored"]*0.5 + (1-h["defense"]/100)*a["attack"]/40 + a["form_score"]/200, 2)
    hw=dw=aw=0.0; mat={}
    for i in range(6):
        for j in range(6):
            p = poisson(hxg,i)*poisson(axg,j)
            mat[f"{i}-{j}"] = round(p*100,2)
            if i>j: hw+=p
            elif i==j: dw+=p
            else: aw+=p
    tot=hw+dw+aw
    o15=sum(p/100 for s,p in mat.items() if sum(int(x) for x in s.split("-"))>1)
    o25=sum(p/100 for s,p in mat.items() if sum(int(x) for x in s.split("-"))>2)
    o35=sum(p/100 for s,p in mat.items() if sum(int(x) for x in s.split("-"))>3)
    bt=sum(p/100 for s,p in mat.items() if int(s.split("-")[0])>0 and int(s.split("-")[1])>0)
    ce=round((h["avg_corners"]+a["avg_corners"])/2,1)
    ye=round((h["avg_yellow"]+a["avg_yellow"])/2,1)
    top=max(mat,key=mat.get)
    res = {
        "home":home,"away":away,"home_flag":h["flag"],"away_flag":a["flag"],
        "home_xg":hxg,"away_xg":axg,
        "home_form":h["form"],"away_form":a["form"],
        "home_form_score":h["form_score"],"away_form_score":a["form_score"],
        "home_win_prob":round(hw/tot*100,1),"draw_prob":round(dw/tot*100,1),"away_win_prob":round(aw/tot*100,1),
        "over_15":round(o15*100,1),"over_25":round(o25*100,1),"over_35":round(o35*100,1),"btts":round(bt*100,1),
        "corners_expected":ce,"over_9_corners":round(min(0.95,ce/12)*100,1),"over_10_corners":round(min(0.88,ce/14)*100,1),
        "yellows_expected":ye,"over_3_yellow":round(min(0.90,ye/4)*100,1),
        "most_likely_score":top,"score_matrix":mat,
    }
    # best picks
    PICK_MAP = {
        "home_win":(res["home_win_prob"],f"{h['flag']} {home} gana"),
        "away_win":(res["away_win_prob"],f"{a['flag']} {away} gana"),
        "draw":(res["draw_prob"],"Empate"),
        "over_25":(res["over_25"],"Más de 2.5 goles"),
        "under_25":(100-res["over_25"],"Menos de 2.5 goles"),
        "btts_yes":(res["btts"],"Ambos anotan"),
        "over_35":(res["over_35"],"Más de 3.5 goles"),
        "over_9_corners":(res["over_9_corners"],"Más de 9 corners"),
        "over_3_yellow":(res["over_3_yellow"],"Más de 3 amarillas"),
    }
    picks=[]
    for k,(prob,lbl) in PICK_MAP.items():
        if prob>=55:
            picks.append({"pick_type":k,"label":lbl,"probability":prob,
                          "decimal_odds":round(100/prob,2) if prob>0 else 0,
                          "american_odds":f"-{round((prob/100/(1-prob/100))*100)}" if prob>=50 else f"+{round(((1-prob/100)/(prob/100))*100)}"})
    picks.sort(key=lambda x:-x["probability"])
    res["best_picks"]=picks[:4]
    return res

def build_parlay(picks_in):
    GETTERS = {
        "home_win":lambda r:r["home_win_prob"],"away_win":lambda r:r["away_win_prob"],
        "draw":lambda r:r["draw_prob"],"over_25":lambda r:r["over_25"],
        "under_25":lambda r:100-r["over_25"],"btts_yes":lambda r:r["btts"],
        "btts_no":lambda r:100-r["btts"],"over_35":lambda r:r["over_35"],
        "over_9_corners":lambda r:r["over_9_corners"],"over_3_yellow":lambda r:r["over_3_yellow"],
    }
    LABELS = {
        "home_win":lambda r:f"{r['home_flag']} {r['home']} gana",
        "away_win":lambda r:f"{r['away_flag']} {r['away']} gana",
        "draw":lambda r:"Empate","over_25":lambda r:"Más de 2.5 goles",
        "under_25":lambda r:"Menos de 2.5 goles","btts_yes":lambda r:"Ambos anotan",
        "btts_no":lambda r:"No ambos anotan","over_35":lambda r:"Más de 3.5 goles",
        "over_9_corners":lambda r:"Más de 9 corners","over_3_yellow":lambda r:"Más de 3 amarillas",
    }
    processed=[]; combined=1.0
    for p in picks_in:
        r=analyze(p["home"],p["away"])
        prob=GETTERS.get(p["pick_type"],lambda r:50)(r)
        combined*=(prob/100)
        processed.append({
            "match":f"{r['home_flag']}{p['home']} vs {r['away_flag']}{p['away']}",
            "pick":LABELS.get(p["pick_type"],lambda r:p["pick_type"])(r),
            "probability":prob,"decimal_odds":round(100/prob,2) if prob>0 else 0,
            "american_odds":f"-{round((prob/100/(1-prob/100))*100)}" if prob>=50 else f"+{round(((1-prob/100)/(prob/100))*100)}",
            "xg":f"{r['home_xg']} - {r['away_xg']}","form_home":r["home_form"],"form_away":r["away_form"],
        })
    cp=round(combined*100,2)
    return {
        "picks":processed,"combined_probability":cp,
        "parlay_decimal_odds":round(1/combined,2) if combined>0 else 0,
        "parlay_american_odds":f"+{round(((1-combined)/combined)*100)}" if combined<0.5 else f"-{round((combined/(1-combined))*100)}",
        "value_rating":"🔥 Alto valor" if cp>20 else "✅ Valor moderado" if cp>8 else "⚠️ Riesgo alto",
        "num_legs":len(processed),
    }

def get_wc_matches():
    api_key = os.environ.get("FOOTBALL_API_KEY","")
    if not api_key or len(api_key) < 10 or api_key.startswith("GET"):
        return FALLBACK_MATCHES
    try:
        import requests as req
        r = req.get("https://api.football-data.org/v4/competitions/WC/matches",
                    headers={"X-Auth-Token":api_key}, timeout=10)
        if r.status_code == 200:
            matches = r.json().get("matches",[])
            if matches: return matches
    except Exception as e:
        print(f"API error: {e}")
    return FALLBACK_MATCHES

# ── ROUTES ─────────────────────────────────────────────────────────────────────
@app.after_request
def add_headers(r):
    r.headers["Cache-Control"]="no-cache, no-store, must-revalidate"
    r.headers["Pragma"]="no-cache"
    return r

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/status")
def api_status():
    api_key = os.environ.get("FOOTBALL_API_KEY","")
    has_key = bool(api_key) and len(api_key)>10 and not api_key.startswith("GET")
    return jsonify({"status":"ok","competition":"Mundial 2026","teams_loaded":48,"has_api_key":has_key,"version":"4.0"})

@app.route("/api/teams")
def api_teams():
    try:
        out=[]
        for grp,names in GROUPS_DATA.items():
            for n in names:
                d=get_team_data(n); d["group"]=grp; out.append(d)
        return jsonify(out)
    except Exception as e:
        return jsonify({"error":str(e)}),500

@app.route("/api/teams/<group>")
def api_teams_group(group):
    names=GROUPS_DATA.get(group.upper(),[])
    out=[]
    for n in names:
        d=get_team_data(n); d["group"]=group.upper(); out.append(d)
    return jsonify(out)

@app.route("/api/match/analyze")
def api_match_analyze():
    home=request.args.get("home",""); away=request.args.get("away","")
    if not home or not away: return jsonify({"error":"Faltan parámetros"}),400
    return jsonify(analyze(home,away))

@app.route("/api/parlay", methods=["POST"])
def api_parlay():
    data=request.get_json() or {}
    picks=data.get("picks",[])
    if not picks: return jsonify({"error":"Sin picks"}),400
    return jsonify(build_parlay(picks))

@app.route("/api/matches/live")
def api_matches_live():
    return jsonify(get_wc_matches())

if __name__ == "__main__":
    port=int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0",port=port,debug=False)
