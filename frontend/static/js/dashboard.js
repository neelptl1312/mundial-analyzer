const API = window.location.origin;
let allTeams = [];

async function init() {
  await checkStatus();
  await loadTeams();
  populateSelects();
}

async function checkStatus() {
  try {
    const r = await fetch(`${API}/api/status`);
    const d = await r.json();
    const el = document.getElementById('api-status');
    el.textContent = `${d.competition} · ${d.teams_loaded} equipos`;
    el.className = 'status-badge';
  } catch {
    document.getElementById('api-status').textContent = 'Sin conexión';
    document.getElementById('api-status').className = 'status-badge error';
  }
}

async function loadTeams() {
  const r = await fetch(`${API}/api/teams`);
  allTeams = await r.json();
  renderTeams(allTeams);
}

function renderTeams(teams) {
  const grid = document.getElementById('teams-grid');
  grid.innerHTML = teams.map(t => `
    <div class="team-card" onclick="showMatch('${t.team}')">
      <div class="team-card-top">
        <span class="team-flag">${t.flag}</span>
        <div>
          <div class="team-name">${t.team}</div>
          <div class="team-group">Grupo ${t.group}</div>
        </div>
      </div>
      <div class="form-badges">
        ${t.form.map(r => `<div class="form-badge ${r}">${r}</div>`).join('')}
      </div>
      <div class="stat-bar-row"><span>Ataque</span><div class="stat-bar"><div class="stat-bar-fill" style="width:${t.attack}%"></div></div><span>${t.attack}</span></div>
      <div class="stat-bar-row"><span>Defensa</span><div class="stat-bar"><div class="stat-bar-fill defense" style="width:${t.defense}%"></div></div><span>${t.defense}</span></div>
      <div class="stat-bar-row"><span>Forma</span><div class="stat-bar"><div class="stat-bar-fill form" style="width:${t.form_score}%"></div></div><span>${t.form_score}</span></div>
      <div class="fifa-rating">FIFA: ${t.fifa_rating} · xG prom: ${t.avg_goals_scored}</div>
    </div>
  `).join('');
}

function filterTeams() {
  const group = document.getElementById('filter-group').value;
  const sort  = document.getElementById('sort-teams').value;
  let filtered = group ? allTeams.filter(t => t.group === group) : [...allTeams];
  filtered.sort((a, b) => (b[sort] || 0) - (a[sort] || 0));
  renderTeams(filtered);
}

function populateSelects() {
  const names = allTeams.map(t => `<option value="${t.team}">${t.flag} ${t.team}</option>`).join('');
  ['pick-home','pick-away','parlay-home','parlay-away'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.innerHTML = (id.includes('parlay') ? '<option value="">Local...</option>' : '') + names;
  });
  document.getElementById('pick-away').selectedIndex = 1;
}

function showTab(name) {
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
  document.getElementById(`tab-${name}`).classList.add('active');
  event.target.classList.add('active');
}

function showMatch(teamName) {
  showTab('match');
  document.querySelector('.nav-btn:nth-child(2)').classList.add('active');
  document.querySelector('.nav-btn:nth-child(1)').classList.remove('active');
  const sel = document.getElementById('pick-home');
  for (let o of sel.options) if (o.value === teamName) { sel.value = teamName; break; }
}

window.addEventListener('DOMContentLoaded', init);
