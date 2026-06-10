async function analyzeMatch() {
  const home = document.getElementById('pick-home').value;
  const away = document.getElementById('pick-away').value;
  if (!home || !away || home === away) { alert('Elige dos equipos distintos'); return; }
  const btn = document.querySelector('.analyze-btn');
  btn.textContent = 'Analizando...'; btn.disabled = true;
  try {
    const r = await fetch(`${API}/api/match/analyze?home=${encodeURIComponent(home)}&away=${encodeURIComponent(away)}`);
    const d = await r.json();
    renderMatchResult(d);
  } finally { btn.textContent = 'Analizar ↗'; btn.disabled = false; }
}

function renderMatchResult(d) {
  const el = document.getElementById('match-result');
  el.classList.remove('hidden');

  const topScores = Object.entries(d.score_matrix)
    .sort((a,b) => b[1]-a[1]).slice(0,6);

  el.innerHTML = `
    <div style="text-align:center;margin-bottom:1.5rem">
      <div style="font-size:22px;font-weight:700">${d.home_flag} ${d.home} <span style="color:#555">vs</span> ${d.away_flag} ${d.away}</div>
      <div style="font-size:13px;color:#888;margin-top:4px">Resultado más probable: <strong style="color:#facc15">${d.most_likely_score}</strong></div>
    </div>

    <div class="prob-row">
      <div class="prob-card win"><div class="prob-label">${d.home_flag} ${d.home} gana</div><div class="prob-value">${d.home_win_prob}%</div></div>
      <div class="prob-card draw"><div class="prob-label">Empate</div><div class="prob-value">${d.draw_prob}%</div></div>
      <div class="prob-card lose"><div class="prob-label">${d.away_flag} ${d.away} gana</div><div class="prob-value">${d.away_win_prob}%</div></div>
    </div>

    <div class="stats-two-col">
      <div>
        <div class="stat-section"><h4>Goles esperados (xG)</h4>
          <div class="xg-row"><span>${d.home_flag} ${d.home}</span><span class="xg-badge">${d.home_xg}</span></div>
          <div class="xg-row"><span>${d.away_flag} ${d.away}</span><span class="xg-badge" style="color:#7c3aed">${d.away_xg}</span></div>
        </div>
        <div class="stat-section" style="margin-top:1rem"><h4>Mercados de goles</h4>
          ${[['Más de 1.5',d.over_15],['Más de 2.5',d.over_25],['Más de 3.5',d.over_35],['Ambos anotan',d.btts]].map(([l,v])=>`
          <div class="pick-item"><span class="pick-label">${l}</span><span class="pick-prob">${v}%</span></div>`).join('')}
        </div>
      </div>
      <div>
        <div class="stat-section"><h4>Corners y tarjetas</h4>
          <div class="pick-item"><span class="pick-label">Más de 9 corners</span><span class="pick-prob">${d.over_9_corners}%</span></div>
          <div class="pick-item" style="margin-top:6px"><span class="pick-label">Más de 3 amarillas</span><span class="pick-prob">${d.over_3_yellow}%</span></div>
          <div style="font-size:12px;color:#666;margin-top:8px">Corners esperados: ~${d.corners_expected} | Amarillas: ~${d.yellows_expected}</div>
        </div>
        <div class="stat-section" style="margin-top:1rem"><h4>Mejores picks</h4>
          ${d.best_picks.map(p=>`
          <div class="pick-item"><span class="pick-label">${p.label}</span><div><span class="pick-prob">${p.probability}%</span><span class="pick-odds" style="margin-left:6px">${p.decimal_odds}x</span></div></div>`).join('')}
        </div>
      </div>
    </div>

    <div class="score-matrix">
      <h4>Marcadores más probables</h4>
      <div style="display:flex;flex-wrap:wrap;gap:6px;margin-top:8px">
        ${topScores.map(([s,p])=>`<div class="matrix-cell ${p>5?'high':p>2?'med':''}" style="min-width:70px">${s}<br><small>${p}%</small></div>`).join('')}
      </div>
    </div>

    <div style="text-align:center;margin-top:1rem">
      <button onclick="addToParlay('${d.home}','${d.away}')" style="background:#1e3a1e;color:#4ade80;border:1px solid #4ade80;padding:8px 18px;border-radius:8px;font-size:13px;cursor:pointer">
        + Agregar al parlay
      </button>
    </div>
  `;
}

function addToParlay(home, away) {
  showTab('parlay');
  document.querySelector('.nav-btn:nth-child(3)').classList.add('active');
  document.querySelector('.nav-btn.active:not(:nth-child(3))').classList.remove('active');
  document.getElementById('parlay-home').value = home;
  document.getElementById('parlay-away').value = away;
}
