let parlayLegs = [];

function addParlay() {
  const home = document.getElementById('parlay-home').value;
  const away = document.getElementById('parlay-away').value;
  const type = document.getElementById('parlay-type').value;
  if (!home || !away || home === away) { alert('Elige dos equipos distintos'); return; }
  const label = document.getElementById('parlay-type').selectedOptions[0].text;
  const homeFlag = allTeams.find(t=>t.team===home)?.flag||'';
  const awayFlag = allTeams.find(t=>t.team===away)?.flag||'';
  parlayLegs.push({ home, away, pick_type: type,
    display: `${homeFlag}${home} vs ${awayFlag}${away} — ${label}` });
  renderLegs();
}

function renderLegs() {
  const el = document.getElementById('parlay-legs');
  el.innerHTML = parlayLegs.map((l,i)=>`
    <div class="leg-item">
      <span>${l.display}</span>
      <button class="leg-remove" onclick="removeLeg(${i})">✕</button>
    </div>`).join('');
  document.getElementById('calc-parlay-btn').disabled = parlayLegs.length === 0;
}

function removeLeg(i) { parlayLegs.splice(i,1); renderLegs(); }

async function calculateParlay() {
  if (!parlayLegs.length) return;
  const btn = document.getElementById('calc-parlay-btn');
  btn.textContent = 'Calculando...'; btn.disabled = true;
  try {
    const r = await fetch(`${API}/api/parlay`, {
      method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({ picks: parlayLegs })
    });
    const d = await r.json();
    renderParlayResult(d);
  } finally { btn.textContent = 'Calcular parlay ↗'; btn.disabled = false; }
}

function renderParlayResult(d) {
  const el = document.getElementById('parlay-result');
  const colorClass = d.combined_probability > 20 ? '#4ade80' : d.combined_probability > 8 ? '#facc15' : '#f87171';
  el.innerHTML = `
    <div class="parlay-summary">
      <div class="parlay-odds">${d.parlay_decimal_odds}x</div>
      <div class="parlay-prob">Probabilidad combinada: <strong style="color:${colorClass}">${d.combined_probability}%</strong></div>
      <div class="parlay-prob" style="margin-top:4px">Cuota americana: ${d.parlay_american_odds}</div>
      <div class="parlay-rating" style="margin-top:8px;font-size:16px">${d.value_rating}</div>
    </div>
    <div class="parlay-legs-detail">
      ${d.picks.map(p=>`
      <div class="parlay-leg-card">
        <div class="parlay-leg-match">${p.match}</div>
        <div class="parlay-leg-pick">${p.pick}</div>
        <div class="parlay-leg-stats">
          Prob: ${p.probability}% · Cuota: ${p.decimal_odds}x (${p.american_odds}) · xG: ${p.xg}
        </div>
        <div class="parlay-leg-stats" style="margin-top:2px">
          Forma local: ${p.form_home.join(' ')} | Visitante: ${p.form_away.join(' ')}
        </div>
      </div>`).join('')}
    </div>
    <div style="text-align:center;margin-top:1rem">
      <button onclick="parlayLegs=[];renderLegs();document.getElementById('parlay-result').innerHTML=''"
        style="background:#3a1e1e;color:#f87171;border:1px solid #f87171;padding:6px 16px;border-radius:6px;font-size:13px;cursor:pointer">
        Limpiar parlay
      </button>
    </div>
  `;
}
