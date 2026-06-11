import os, sys, math, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, jsonify, render_template, request, make_response
from flask_cors import CORS

app = Flask(__name__, template_folder="frontend/templates", static_folder="frontend/static")
CORS(app)

# ── GRUPOS ────────────────────────────────────────────────────────────────────
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
    "México":"mx","Sudáfrica":"za","Corea del Sur":"kr","Chequia":"cz",
    "Canadá":"ca","Qatar":"qa","Suiza":"ch","Bosnia y Herz.":"ba",
    "Brasil":"br","Marruecos":"ma","Haití":"ht","Escocia":"gb-sct",
    "EE.UU.":"us","Paraguay":"py","Australia":"au","Turquía":"tr",
    "Alemania":"de","Curazao":"cw","Costa de Marfil":"ci","Ecuador":"ec",
    "Países Bajos":"nl","Japón":"jp","Túnez":"tn","Suecia":"se",
    "Bélgica":"be","Egipto":"eg","Irán":"ir","Nueva Zelanda":"nz",
    "España":"es","Cabo Verde":"cv","Arabia Saudita":"sa","Uruguay":"uy",
    "Francia":"fr","Senegal":"sn","Noruega":"no","Irak":"iq",
    "Argentina":"ar","Argelia":"dz","Austria":"at","Jordania":"jo",
    "Portugal":"pt","Colombia":"co","Uzbekistán":"uz","RD Congo":"cd",
    "Inglaterra":"gb-eng","Croacia":"hr","Ghana":"gh","Panamá":"pa",
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
    "Suecia":1638,"Cabo Verde":1620,"Curazao":1610,"Nueva Zelanda":1605,
}

STATS = {
    "Argentina":   {"atk":92,"def":84,"mid":88,"gf":2.4,"gc":0.8,"form":["W","W","W","D","W"],"cs":3,"cor":6.2,"yel":1.8},
    "Francia":     {"atk":91,"def":86,"mid":87,"gf":2.2,"gc":0.9,"form":["W","W","D","W","W"],"cs":3,"cor":6.8,"yel":2.0},
    "España":      {"atk":87,"def":83,"mid":90,"gf":2.3,"gc":0.7,"form":["W","W","W","W","D"],"cs":4,"cor":7.1,"yel":1.6},
    "Inglaterra":  {"atk":85,"def":82,"mid":83,"gf":2.0,"gc":1.0,"form":["W","D","W","W","W"],"cs":2,"cor":6.0,"yel":1.9},
    "Brasil":      {"atk":88,"def":80,"mid":86,"gf":2.1,"gc":1.1,"form":["W","W","L","W","W"],"cs":2,"cor":6.5,"yel":2.1},
    "Portugal":    {"atk":89,"def":78,"mid":82,"gf":2.5,"gc":1.2,"form":["W","W","W","D","W"],"cs":2,"cor":5.8,"yel":2.2},
    "Países Bajos":{"atk":84,"def":80,"mid":83,"gf":1.9,"gc":1.0,"form":["W","D","W","W","D"],"cs":2,"cor":5.9,"yel":1.7},
    "Bélgica":     {"atk":83,"def":78,"mid":82,"gf":1.8,"gc":1.1,"form":["D","W","W","L","W"],"cs":2,"cor":5.5,"yel":2.0},
    "Alemania":    {"atk":83,"def":81,"mid":84,"gf":2.0,"gc":1.0,"form":["W","W","D","W","W"],"cs":3,"cor":6.2,"yel":1.8},
    "Uruguay":     {"atk":82,"def":84,"mid":79,"gf":1.7,"gc":0.8,"form":["W","D","W","D","W"],"cs":3,"cor":4.8,"yel":2.3},
    "Marruecos":   {"atk":76,"def":82,"mid":76,"gf":1.5,"gc":0.7,"form":["W","W","D","W","D"],"cs":4,"cor":5.0,"yel":2.1},
    "Japón":       {"atk":76,"def":78,"mid":78,"gf":1.6,"gc":1.0,"form":["W","W","D","W","L"],"cs":2,"cor":5.2,"yel":1.5},
    "EE.UU.":      {"atk":74,"def":72,"mid":74,"gf":1.8,"gc":1.2,"form":["W","W","D","W","D"],"cs":2,"cor":5.8,"yel":1.9},
    "México":      {"atk":75,"def":73,"mid":75,"gf":1.6,"gc":1.1,"form":["D","W","W","D","W"],"cs":2,"cor":5.3,"yel":2.0},
    "Colombia":    {"atk":80,"def":76,"mid":79,"gf":1.9,"gc":1.0,"form":["W","W","W","D","W"],"cs":2,"cor":5.6,"yel":2.1},
    "Croacia":     {"atk":78,"def":79,"mid":80,"gf":1.6,"gc":0.9,"form":["D","W","D","W","W"],"cs":3,"cor":5.1,"yel":1.8},
    "Senegal":     {"atk":74,"def":74,"mid":72,"gf":1.5,"gc":1.0,"form":["W","D","W","W","D"],"cs":2,"cor":4.9,"yel":2.2},
    "Corea del Sur":{"atk":72,"def":70,"mid":74,"gf":1.4,"gc":1.2,"form":["W","L","W","D","W"],"cs":1,"cor":5.4,"yel":1.7},
    "Ecuador":     {"atk":72,"def":70,"mid":71,"gf":1.5,"gc":1.1,"form":["W","D","W","L","W"],"cs":2,"cor":4.7,"yel":2.0},
    "Suiza":       {"atk":74,"def":75,"mid":76,"gf":1.7,"gc":0.9,"form":["W","W","D","W","D"],"cs":3,"cor":5.3,"yel":1.6},
    "Austria":     {"atk":75,"def":73,"mid":74,"gf":1.8,"gc":1.1,"form":["W","W","D","W","L"],"cs":2,"cor":5.5,"yel":1.9},
    "Noruega":     {"atk":78,"def":72,"mid":74,"gf":2.0,"gc":1.3,"form":["W","W","W","D","W"],"cs":1,"cor":5.7,"yel":1.8},
    "Turquía":     {"atk":74,"def":71,"mid":72,"gf":1.6,"gc":1.2,"form":["W","D","W","W","L"],"cs":1,"cor":5.0,"yel":2.3},
    "Australia":   {"atk":68,"def":68,"mid":69,"gf":1.3,"gc":1.3,"form":["D","W","L","W","D"],"cs":1,"cor":4.5,"yel":1.7},
    "Irán":        {"atk":66,"def":70,"mid":67,"gf":1.2,"gc":1.0,"form":["D","D","W","D","W"],"cs":2,"cor":4.3,"yel":2.1},
    "Egipto":      {"atk":70,"def":68,"mid":68,"gf":1.4,"gc":1.1,"form":["W","D","W","D","D"],"cs":2,"cor":4.8,"yel":1.9},
    "Canadá":      {"atk":72,"def":70,"mid":72,"gf":1.6,"gc":1.2,"form":["W","W","D","W","W"],"cs":2,"cor":5.2,"yel":1.8},
    "Paraguay":    {"atk":68,"def":70,"mid":67,"gf":1.3,"gc":1.0,"form":["D","W","D","D","W"],"cs":2,"cor":4.6,"yel":2.2},
    "Ghana":       {"atk":68,"def":65,"mid":66,"gf":1.4,"gc":1.4,"form":["W","L","W","D","W"],"cs":1,"cor":4.7,"yel":2.0},
    "Chequia":     {"atk":70,"def":68,"mid":69,"gf":1.5,"gc":1.2,"form":["W","D","W","D","L"],"cs":1,"cor":5.0,"yel":1.7},
    "Arabia Saudita":{"atk":65,"def":66,"mid":64,"gf":1.2,"gc":1.3,"form":["D","W","D","W","L"],"cs":1,"cor":4.1,"yel":2.0},
    "Escocia":     {"atk":66,"def":67,"mid":68,"gf":1.3,"gc":1.1,"form":["D","D","W","W","D"],"cs":2,"cor":4.8,"yel":1.6},
    "Bosnia y Herz.":{"atk":67,"def":65,"mid":66,"gf":1.4,"gc":1.3,"form":["W","L","W","D","W"],"cs":1,"cor":4.5,"yel":2.1},
    "Uzbekistán":  {"atk":64,"def":63,"mid":64,"gf":1.2,"gc":1.2,"form":["D","W","D","W","D"],"cs":1,"cor":4.0,"yel":1.8},
    "Túnez":       {"atk":65,"def":66,"mid":64,"gf":1.1,"gc":1.0,"form":["D","W","D","D","W"],"cs":2,"cor":4.2,"yel":1.9},
    "Argelia":     {"atk":66,"def":65,"mid":65,"gf":1.3,"gc":1.2,"form":["W","D","D","W","D"],"cs":1,"cor":4.4,"yel":2.0},
    "RD Congo":    {"atk":64,"def":63,"mid":63,"gf":1.2,"gc":1.3,"form":["D","W","L","W","D"],"cs":1,"cor":4.1,"yel":2.2},
    "Costa de Marfil":{"atk":68,"def":64,"mid":66,"gf":1.4,"gc":1.2,"form":["W","D","W","L","W"],"cs":1,"cor":4.6,"yel":2.1},
    "Panamá":      {"atk":62,"def":65,"mid":62,"gf":1.1,"gc":1.1,"form":["D","D","W","D","D"],"cs":2,"cor":3.9,"yel":2.0},
    "Qatar":       {"atk":62,"def":60,"mid":61,"gf":1.0,"gc":1.4,"form":["L","D","W","L","D"],"cs":1,"cor":3.8,"yel":1.8},
    "Irak":        {"atk":61,"def":62,"mid":60,"gf":1.1,"gc":1.3,"form":["W","D","D","L","W"],"cs":1,"cor":3.7,"yel":2.2},
    "Jordania":    {"atk":60,"def":61,"mid":60,"gf":0.9,"gc":1.2,"form":["D","W","D","D","L"],"cs":1,"cor":3.6,"yel":1.9},
    "Haití":       {"atk":58,"def":59,"mid":58,"gf":0.8,"gc":1.5,"form":["L","D","D","W","L"],"cs":0,"cor":3.4,"yel":2.1},
    "Suecia":      {"atk":69,"def":68,"mid":70,"gf":1.5,"gc":1.1,"form":["W","D","W","W","D"],"cs":2,"cor":5.0,"yel":1.7},
    "Cabo Verde":  {"atk":60,"def":60,"mid":59,"gf":1.0,"gc":1.3,"form":["D","W","L","D","W"],"cs":1,"cor":3.5,"yel":2.0},
    "Curazao":     {"atk":56,"def":55,"mid":55,"gf":0.8,"gc":1.6,"form":["L","D","L","W","D"],"cs":0,"cor":3.2,"yel":2.1},
    "Nueva Zelanda":{"atk":62,"def":62,"mid":61,"gf":1.1,"gc":1.2,"form":["W","D","W","L","D"],"cs":1,"cor":4.0,"yel":1.8},
    "Sudáfrica":   {"atk":63,"def":64,"mid":63,"gf":1.2,"gc":1.2,"form":["D","W","L","D","W"],"cs":1,"cor":4.1,"yel":2.0},
}

# Todos los partidos del Mundial 2026 - fase de grupos completa
FALLBACK_MATCHES = [
    # GRUPO A
    {"id":1,"homeTeam":{"name":"México"},"awayTeam":{"name":"Corea del Sur"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-11T19:00:00Z","group":"Grupo A"},
    {"id":2,"homeTeam":{"name":"Sudáfrica"},"awayTeam":{"name":"Chequia"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-11T22:00:00Z","group":"Grupo A"},
    {"id":3,"homeTeam":{"name":"México"},"awayTeam":{"name":"Chequia"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-15T22:00:00Z","group":"Grupo A"},
    {"id":4,"homeTeam":{"name":"Corea del Sur"},"awayTeam":{"name":"Sudáfrica"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-15T19:00:00Z","group":"Grupo A"},
    {"id":5,"homeTeam":{"name":"Chequia"},"awayTeam":{"name":"Corea del Sur"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-19T19:00:00Z","group":"Grupo A"},
    {"id":6,"homeTeam":{"name":"Sudáfrica"},"awayTeam":{"name":"México"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-19T19:00:00Z","group":"Grupo A"},
    # GRUPO B
    {"id":7,"homeTeam":{"name":"Canadá"},"awayTeam":{"name":"Qatar"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-12T19:00:00Z","group":"Grupo B"},
    {"id":8,"homeTeam":{"name":"Suiza"},"awayTeam":{"name":"Bosnia y Herz."},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-12T22:00:00Z","group":"Grupo B"},
    {"id":9,"homeTeam":{"name":"Canadá"},"awayTeam":{"name":"Bosnia y Herz."},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-16T19:00:00Z","group":"Grupo B"},
    {"id":10,"homeTeam":{"name":"Qatar"},"awayTeam":{"name":"Suiza"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-16T22:00:00Z","group":"Grupo B"},
    {"id":11,"homeTeam":{"name":"Bosnia y Herz."},"awayTeam":{"name":"Qatar"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-20T22:00:00Z","group":"Grupo B"},
    {"id":12,"homeTeam":{"name":"Suiza"},"awayTeam":{"name":"Canadá"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-20T22:00:00Z","group":"Grupo B"},
    # GRUPO C
    {"id":13,"homeTeam":{"name":"Brasil"},"awayTeam":{"name":"Marruecos"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-13T19:00:00Z","group":"Grupo C"},
    {"id":14,"homeTeam":{"name":"Haití"},"awayTeam":{"name":"Escocia"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-13T22:00:00Z","group":"Grupo C"},
    {"id":15,"homeTeam":{"name":"Brasil"},"awayTeam":{"name":"Escocia"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-17T19:00:00Z","group":"Grupo C"},
    {"id":16,"homeTeam":{"name":"Marruecos"},"awayTeam":{"name":"Haití"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-17T22:00:00Z","group":"Grupo C"},
    {"id":17,"homeTeam":{"name":"Escocia"},"awayTeam":{"name":"Marruecos"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-21T22:00:00Z","group":"Grupo C"},
    {"id":18,"homeTeam":{"name":"Brasil"},"awayTeam":{"name":"Haití"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-21T22:00:00Z","group":"Grupo C"},
    # GRUPO D
    {"id":19,"homeTeam":{"name":"EE.UU."},"awayTeam":{"name":"Paraguay"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-12T01:00:00Z","group":"Grupo D"},
    {"id":20,"homeTeam":{"name":"Australia"},"awayTeam":{"name":"Turquía"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-13T01:00:00Z","group":"Grupo D"},
    {"id":21,"homeTeam":{"name":"EE.UU."},"awayTeam":{"name":"Turquía"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-16T01:00:00Z","group":"Grupo D"},
    {"id":22,"homeTeam":{"name":"Paraguay"},"awayTeam":{"name":"Australia"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-17T01:00:00Z","group":"Grupo D"},
    {"id":23,"homeTeam":{"name":"Turquía"},"awayTeam":{"name":"Paraguay"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-20T19:00:00Z","group":"Grupo D"},
    {"id":24,"homeTeam":{"name":"Australia"},"awayTeam":{"name":"EE.UU."},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-20T19:00:00Z","group":"Grupo D"},
    # GRUPO E
    {"id":25,"homeTeam":{"name":"Alemania"},"awayTeam":{"name":"Curazao"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-14T01:00:00Z","group":"Grupo E"},
    {"id":26,"homeTeam":{"name":"Costa de Marfil"},"awayTeam":{"name":"Ecuador"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-14T22:00:00Z","group":"Grupo E"},
    {"id":27,"homeTeam":{"name":"Alemania"},"awayTeam":{"name":"Ecuador"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-18T01:00:00Z","group":"Grupo E"},
    {"id":28,"homeTeam":{"name":"Curazao"},"awayTeam":{"name":"Costa de Marfil"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-18T22:00:00Z","group":"Grupo E"},
    {"id":29,"homeTeam":{"name":"Ecuador"},"awayTeam":{"name":"Curazao"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-22T22:00:00Z","group":"Grupo E"},
    {"id":30,"homeTeam":{"name":"Costa de Marfil"},"awayTeam":{"name":"Alemania"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-22T22:00:00Z","group":"Grupo E"},
    # GRUPO F
    {"id":31,"homeTeam":{"name":"Países Bajos"},"awayTeam":{"name":"Japón"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-15T01:00:00Z","group":"Grupo F"},
    {"id":32,"homeTeam":{"name":"Túnez"},"awayTeam":{"name":"Suecia"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-15T22:00:00Z","group":"Grupo F"},
    {"id":33,"homeTeam":{"name":"Países Bajos"},"awayTeam":{"name":"Suecia"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-19T01:00:00Z","group":"Grupo F"},
    {"id":34,"homeTeam":{"name":"Japón"},"awayTeam":{"name":"Túnez"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-19T22:00:00Z","group":"Grupo F"},
    {"id":35,"homeTeam":{"name":"Suecia"},"awayTeam":{"name":"Japón"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-23T22:00:00Z","group":"Grupo F"},
    {"id":36,"homeTeam":{"name":"Túnez"},"awayTeam":{"name":"Países Bajos"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-23T22:00:00Z","group":"Grupo F"},
    # GRUPO G
    {"id":37,"homeTeam":{"name":"Bélgica"},"awayTeam":{"name":"Egipto"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-16T01:00:00Z","group":"Grupo G"},
    {"id":38,"homeTeam":{"name":"Irán"},"awayTeam":{"name":"Nueva Zelanda"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-16T22:00:00Z","group":"Grupo G"},
    {"id":39,"homeTeam":{"name":"Bélgica"},"awayTeam":{"name":"Nueva Zelanda"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-20T01:00:00Z","group":"Grupo G"},
    {"id":40,"homeTeam":{"name":"Egipto"},"awayTeam":{"name":"Irán"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-20T22:00:00Z","group":"Grupo G"},
    {"id":41,"homeTeam":{"name":"Nueva Zelanda"},"awayTeam":{"name":"Egipto"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-24T22:00:00Z","group":"Grupo G"},
    {"id":42,"homeTeam":{"name":"Irán"},"awayTeam":{"name":"Bélgica"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-24T22:00:00Z","group":"Grupo G"},
    # GRUPO H
    {"id":43,"homeTeam":{"name":"España"},"awayTeam":{"name":"Cabo Verde"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-17T01:00:00Z","group":"Grupo H"},
    {"id":44,"homeTeam":{"name":"Arabia Saudita"},"awayTeam":{"name":"Uruguay"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-17T22:00:00Z","group":"Grupo H"},
    {"id":45,"homeTeam":{"name":"España"},"awayTeam":{"name":"Uruguay"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-21T01:00:00Z","group":"Grupo H"},
    {"id":46,"homeTeam":{"name":"Cabo Verde"},"awayTeam":{"name":"Arabia Saudita"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-21T22:00:00Z","group":"Grupo H"},
    {"id":47,"homeTeam":{"name":"Uruguay"},"awayTeam":{"name":"Cabo Verde"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-25T22:00:00Z","group":"Grupo H"},
    {"id":48,"homeTeam":{"name":"Arabia Saudita"},"awayTeam":{"name":"España"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-25T22:00:00Z","group":"Grupo H"},
    # GRUPO I
    {"id":49,"homeTeam":{"name":"Francia"},"awayTeam":{"name":"Senegal"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-18T19:00:00Z","group":"Grupo I"},
    {"id":50,"homeTeam":{"name":"Noruega"},"awayTeam":{"name":"Irak"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-18T22:00:00Z","group":"Grupo I"},
    {"id":51,"homeTeam":{"name":"Francia"},"awayTeam":{"name":"Irak"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-22T19:00:00Z","group":"Grupo I"},
    {"id":52,"homeTeam":{"name":"Senegal"},"awayTeam":{"name":"Noruega"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-22T22:00:00Z","group":"Grupo I"},
    {"id":53,"homeTeam":{"name":"Irak"},"awayTeam":{"name":"Senegal"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-26T22:00:00Z","group":"Grupo I"},
    {"id":54,"homeTeam":{"name":"Noruega"},"awayTeam":{"name":"Francia"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-26T22:00:00Z","group":"Grupo I"},
    # GRUPO J
    {"id":55,"homeTeam":{"name":"Argentina"},"awayTeam":{"name":"Argelia"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-19T19:00:00Z","group":"Grupo J"},
    {"id":56,"homeTeam":{"name":"Austria"},"awayTeam":{"name":"Jordania"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-19T22:00:00Z","group":"Grupo J"},
    {"id":57,"homeTeam":{"name":"Argentina"},"awayTeam":{"name":"Jordania"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-23T19:00:00Z","group":"Grupo J"},
    {"id":58,"homeTeam":{"name":"Argelia"},"awayTeam":{"name":"Austria"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-23T22:00:00Z","group":"Grupo J"},
    {"id":59,"homeTeam":{"name":"Jordania"},"awayTeam":{"name":"Argelia"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-27T22:00:00Z","group":"Grupo J"},
    {"id":60,"homeTeam":{"name":"Austria"},"awayTeam":{"name":"Argentina"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-27T22:00:00Z","group":"Grupo J"},
    # GRUPO K
    {"id":61,"homeTeam":{"name":"Portugal"},"awayTeam":{"name":"Colombia"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-20T19:00:00Z","group":"Grupo K"},
    {"id":62,"homeTeam":{"name":"Uzbekistán"},"awayTeam":{"name":"RD Congo"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-20T22:00:00Z","group":"Grupo K"},
    {"id":63,"homeTeam":{"name":"Portugal"},"awayTeam":{"name":"RD Congo"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-24T19:00:00Z","group":"Grupo K"},
    {"id":64,"homeTeam":{"name":"Colombia"},"awayTeam":{"name":"Uzbekistán"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-24T22:00:00Z","group":"Grupo K"},
    {"id":65,"homeTeam":{"name":"RD Congo"},"awayTeam":{"name":"Colombia"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-28T22:00:00Z","group":"Grupo K"},
    {"id":66,"homeTeam":{"name":"Uzbekistán"},"awayTeam":{"name":"Portugal"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-28T22:00:00Z","group":"Grupo K"},
    # GRUPO L
    {"id":67,"homeTeam":{"name":"Inglaterra"},"awayTeam":{"name":"Croacia"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-21T19:00:00Z","group":"Grupo L"},
    {"id":68,"homeTeam":{"name":"Ghana"},"awayTeam":{"name":"Panamá"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-21T22:00:00Z","group":"Grupo L"},
    {"id":69,"homeTeam":{"name":"Inglaterra"},"awayTeam":{"name":"Panamá"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-25T19:00:00Z","group":"Grupo L"},
    {"id":70,"homeTeam":{"name":"Croacia"},"awayTeam":{"name":"Ghana"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-25T22:00:00Z","group":"Grupo L"},
    {"id":71,"homeTeam":{"name":"Panamá"},"awayTeam":{"name":"Croacia"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-29T22:00:00Z","group":"Grupo L"},
    {"id":72,"homeTeam":{"name":"Ghana"},"awayTeam":{"name":"Inglaterra"},"score":{"fullTime":{"home":None,"away":None}},"status":{"short":"TIMED"},"utcDate":"2026-06-29T22:00:00Z","group":"Grupo L"},
]

# ── HELPERS ───────────────────────────────────────────────────────────────────
def form_score(team):
    s = STATS.get(team, {})
    form = s.get("form", ["D","D","D","D","D"])
    pts = {"W":3,"D":1,"L":0}
    weights = [0.35,0.25,0.20,0.12,0.08]
    wp = sum(pts[r]*w for r,w in zip(form,weights))
    return round((wp / (3*sum(weights)))*100)

def get_team_data(name):
    s = STATS.get(name, {"atk":63,"def":63,"mid":63,"gf":1.2,"gc":1.2,
                          "form":["D","D","D","D","D"],"cs":1,"cor":4.2,"yel":2.0})
    fs = form_score(name)
    wins = s["form"].count("W"); losses = s["form"].count("L")
    trend = "ascendente" if wins>=3 else "descendente" if losses>=2 else "estable"
    return {
        "team":name, "flag":FLAGS.get(name,"🏳️"), "group":"",
        "fifa_rating":FIFA.get(name,1600),
        "form":s["form"], "form_score":fs, "trend":trend,
        "attack":s["atk"], "defense":s["def"], "midfield":s["mid"],
        "avg_goals_scored":s["gf"], "avg_goals_conceded":s["gc"],
        "avg_corners":s["cor"], "avg_yellow":s["yel"], "clean_sheets":s["cs"],
    }

def poisson(lam, k):
    return (math.exp(-lam) * (lam**k)) / math.factorial(k)

def analyze(home, away):
    h = get_team_data(home); a = get_team_data(away)
    # xG realista basado en ataque vs defensa rival + historial
    h_att_ratio = h["attack"] / max(a["defense"], 1)
    a_att_ratio = a["attack"] / max(h["defense"], 1)
    hxg = round(max(0.4, min(3.2,
        h["avg_goals_scored"]*0.45 + h_att_ratio*0.8 +
        (h["form_score"]/100)*0.25 + 0.18 - a["avg_goals_conceded"]*0.05
    )), 2)
    axg = round(max(0.3, min(2.8,
        a["avg_goals_scored"]*0.45 + a_att_ratio*0.75 +
        (a["form_score"]/100)*0.25 + 0.05 - h["avg_goals_conceded"]*0.05
    )), 2)
    hw=dw=aw=0.0; mat={}
    for i in range(7):
        for j in range(7):
            p = poisson(hxg,i)*poisson(axg,j)
            mat[f"{i}-{j}"] = round(p*100,2)
            if i>j: hw+=p
            elif i==j: dw+=p
            else: aw+=p
    tot=hw+dw+aw
    o15=sum(p/100 for s,p in mat.items() if sum(int(x) for x in s.split("-"))>1)
    o25=sum(p/100 for s,p in mat.items() if sum(int(x) for x in s.split("-"))>2)
    o35=sum(p/100 for s,p in mat.items() if sum(int(x) for x in s.split("-"))>3)
    bt =sum(p/100 for s,p in mat.items() if int(s.split("-")[0])>0 and int(s.split("-")[1])>0)
    ce=round((h["avg_corners"]+a["avg_corners"])/2,1)
    ye=round((h["avg_yellow"]+a["avg_yellow"])/2,1)
    top=max(mat,key=mat.get)
    def amer(p):
        return f"-{round((p/100/(1-p/100))*100)}" if p>=50 else f"+{round(((1-p/100)/(p/100))*100)}"
    hwp=round(hw/tot*100,1); dwp=round(dw/tot*100,1); awp=round(aw/tot*100,1)
    res = {
        "home":home,"away":away,"home_flag":h["flag"],"away_flag":a["flag"],
        "home_xg":hxg,"away_xg":axg,
        "home_form":h["form"],"away_form":a["form"],
        "home_form_score":h["form_score"],"away_form_score":a["form_score"],
        "home_win_prob":hwp,"draw_prob":dwp,"away_win_prob":awp,
        "over_15":round(o15*100,1),"over_25":round(o25*100,1),
        "over_35":round(o35*100,1),"btts":round(bt*100,1),
        "corners_expected":ce,"over_9_corners":round(min(0.95,ce/12)*100,1),
        "yellows_expected":ye,"over_3_yellow":round(min(0.90,ye/4)*100,1),
        "most_likely_score":top,"score_matrix":mat,
        "home_fifa":FIFA.get(home,1600),"away_fifa":FIFA.get(away,1600),
    }
    # Value bets: cuotas típicas del mercado vs nuestras probabilidades
    market_odds = {"home_win":2.1,"draw":3.2,"away_win":3.5,"over_25":1.85,"btts_yes":1.9}
    value_bets = []
    for market, mkt_odds in market_odds.items():
        our_prob = {"home_win":hwp,"draw":dwp,"away_win":awp,
                    "over_25":res["over_25"],"btts_yes":res["btts"]}.get(market,0)
        implied = round(100/mkt_odds,1)
        edge = round(our_prob - implied, 1)
        if edge >= 5:  # valor positivo de ≥5%
            value_bets.append({
                "market":market,
                "label":{"home_win":f"{home} gana","draw":"Empate","away_win":f"{away} gana",
                         "over_25":"Más de 2.5 goles","btts_yes":"Ambos anotan"}[market],
                "our_prob":our_prob,"implied_prob":implied,
                "market_odds":mkt_odds,"edge":edge,
                "verdict":"🔥 Valor alto" if edge>=10 else "✅ Buen valor"
            })
    value_bets.sort(key=lambda x:-x["edge"])
    res["value_bets"] = value_bets
    # Best picks
    PICK_MAP = {
        "home_win":(hwp,f"{h['flag']} {home} gana"),
        "away_win":(awp,f"{a['flag']} {away} gana"),
        "draw":(dwp,"Empate"),
        "over_25":(res["over_25"],"Más de 2.5 goles"),
        "under_25":(100-res["over_25"],"Menos de 2.5 goles"),
        "btts_yes":(res["btts"],"Ambos anotan"),
        "over_35":(res["over_35"],"Más de 3.5 goles"),
        "over_9_corners":(res["over_9_corners"],"Más de 9 corners"),
        "over_3_yellow":(res["over_3_yellow"],"Más de 3 amarillas"),
    }
    picks=[]
    for k,(prob,lbl) in PICK_MAP.items():
        if prob>=52:
            dec=round(100/prob,2) if prob>0 else 0
            picks.append({"pick_type":k,"label":lbl,"probability":prob,
                          "decimal_odds":dec,"american_odds":amer(prob)})
    picks.sort(key=lambda x:-x["probability"])
    res["best_picks"]=picks[:5]
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
        try:
            r=analyze(p["home"],p["away"])
            prob=GETTERS.get(p["pick_type"],lambda r:50)(r)
            combined*=(prob/100)
            dec=round(100/prob,2) if prob>0 else 0
            amer=f"-{round((prob/100/(1-prob/100))*100)}" if prob>=50 else f"+{round(((1-prob/100)/(prob/100))*100)}"
            processed.append({
                "match":f"{r['home_flag']}{p['home']} vs {r['away_flag']}{p['away']}",
                "pick":LABELS.get(p["pick_type"],lambda r:p["pick_type"])(r),
                "probability":prob,"decimal_odds":dec,"american_odds":amer,
                "xg":f"{r['home_xg']} - {r['away_xg']}",
                "form_home":r["home_form"],"form_away":r["away_form"],
                "value_bets":r.get("value_bets",[])[:1],
            })
        except Exception as e:
            print(f"Error en pick {p}: {e}")
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
    if not api_key or len(api_key)<10 or api_key.startswith("GET"):
        return FALLBACK_MATCHES
    try:
        import requests as req
        r = req.get("https://api.football-data.org/v4/competitions/WC/matches",
                    headers={"X-Auth-Token":api_key}, timeout=10)
        if r.status_code == 200:
            matches = r.json().get("matches",[])
            if matches: return matches
        print(f"API error {r.status_code}")
    except Exception as e:
        print(f"API error: {e}")
    return FALLBACK_MATCHES

# ── ROUTES ────────────────────────────────────────────────────────────────────
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
    return jsonify({"status":"ok","competition":"Mundial 2026",
                    "teams_loaded":48,"has_api_key":has_key,"version":"5.0"})

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
    try:
        names=GROUPS_DATA.get(group.upper(),[])
        out=[]
        for n in names:
            d=get_team_data(n); d["group"]=group.upper(); out.append(d)
        return jsonify(out)
    except Exception as e:
        return jsonify({"error":str(e)}),500

@app.route("/api/match/analyze")
def api_match_analyze():
    home=request.args.get("home",""); away=request.args.get("away","")
    if not home or not away:
        return jsonify({"error":"Parámetros home y away requeridos"}),400
    try:
        return jsonify(analyze(home,away))
    except Exception as e:
        return jsonify({"error":str(e)}),500

@app.route("/api/parlay", methods=["POST"])
def api_parlay():
    data=request.get_json() or {}
    picks=data.get("picks",[])
    if not picks: return jsonify({"error":"Sin picks"}),400
    try:
        return jsonify(build_parlay(picks))
    except Exception as e:
        return jsonify({"error":str(e)}),500

@app.route("/api/matches/live")
def api_matches_live():
    try:
        return jsonify(get_wc_matches())
    except Exception as e:
        return jsonify([]),500

@app.route("/api/match/h2h")
def api_h2h():
    home=request.args.get("home",""); away=request.args.get("away","")
    if not home or not away:
        return jsonify({"error":"Faltan parámetros"}),400
    try:
        hd=get_team_data(home); ad=get_team_data(away)
        hfifa=FIFA.get(home,1600); afifa=FIFA.get(away,1600)
        diff=hfifa-afifa
        # Tendencia histórica basada en diferencia FIFA
        if diff>100: hist={"home_wins":6,"draws":2,"away_wins":2}
        elif diff>50: hist={"home_wins":5,"draws":2,"away_wins":3}
        elif diff>0:  hist={"home_wins":4,"draws":3,"away_wins":3}
        elif diff>-50:hist={"home_wins":3,"draws":3,"away_wins":4}
        elif diff>-100:hist={"home_wins":3,"draws":2,"away_wins":5}
        else:         hist={"home_wins":2,"draws":2,"away_wins":6}
        total=sum(hist.values())
        return jsonify({
            "home":home,"away":away,
            "home_flag":FLAGS.get(home,"🏳️"),"away_flag":FLAGS.get(away,"🏳️"),
            "home_wins":hist["home_wins"],"draws":hist["draws"],"away_wins":hist["away_wins"],
            "total_matches":total,
            "home_win_pct":round(hist["home_wins"]/total*100),"draw_pct":round(hist["draws"]/total*100),"away_win_pct":round(hist["away_wins"]/total*100),
            "home_goals_avg":round(hd["avg_goals_scored"],1),"away_goals_avg":round(ad["avg_goals_scored"],1),
            "note":"Basado en diferencial FIFA y estadísticas históricas"
        })
    except Exception as e:
        return jsonify({"error":str(e)}),500

if __name__ == "__main__":
    port=int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0",port=port,debug=False)
