# Mundial 2026 Analyzer

Simulador y analizador de probabilidades para los 48 equipos del Mundial 2026.

## Stack
- **Backend**: Python + Flask (Railway)
- **Frontend**: HTML/CSS/JS vanilla (Vercel)
- **Datos**: football-data.org API v4

## Setup local
```bash
pip install -r requirements.txt
cp .env.example .env   # agrega tu API key
python app.py
```

## Variables de entorno (Railway)
- `FOOTBALL_API_KEY` — tu key de football-data.org

## Endpoints
- `GET /api/teams` — los 48 equipos con forma y stats
- `GET /api/match/analyze?home=Argentina&away=Francia` — análisis completo
- `POST /api/parlay` — construir parlay con picks
- `GET /api/status` — estado de la API
