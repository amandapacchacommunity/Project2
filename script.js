const risks = [
  { risk_id: "R001", risk_category: "Technology", owner: "IT", impact_level: 5, probability_level: 4 },
  { risk_id: "R002", risk_category: "Financial", owner: "Finance", impact_level: 5, probability_level: 3 },
  { risk_id: "R003", risk_category: "Service Disruption", owner: "Operations", impact_level: 4, probability_level: 3 },
  { risk_id: "R004", risk_category: "Market Demand", owner: "Strategy", impact_level: 4, probability_level: 3 },
  { risk_id: "R005", risk_category: "Facilities", owner: "Facilities", impact_level: 4, probability_level: 2 },
  { risk_id: "R006", risk_category: "Staffing", owner: "HR", impact_level: 4, probability_level: 3 },
  { risk_id: "R007", risk_category: "Health & Safety", owner: "Safety", impact_level: 5, probability_level: 2 },
  { risk_id: "R008", risk_category: "Compliance", owner: "Compliance", impact_level: 5, probability_level: 2 },
  { risk_id: "R009", risk_category: "Cybersecurity", owner: "Security", impact_level: 5, probability_level: 4 },
  { risk_id: "R010", risk_category: "Reputation", owner: "Communications", impact_level: 4, probability_level: 3 }
];

function riskScore(risk) {
  return risk.impact_level * risk.probability_level;
}

function riskLevel(score) {
  if (score >= 15) return "High";
  if (score >= 8) return "Medium";
  return "Low";
}

const enrichedRisks = risks.map((risk) => {
  const score = riskScore(risk);
  return {
    ...risk,
    risk_score: score,
    risk_level: riskLevel(score)
  };
});

function updateCards(data) {
  const total = data.length;
  const high = data.filter((d) => d.risk_level === "High").length;
  const avgImpact = data.reduce((sum, d) => sum + d.impact_level, 0) / total;
  const avgProbability = data.reduce((sum, d) => sum + d.probability_level, 0) / total;

  document.getElementById("totalRisks").textContent = total;
  document.getElementById("highRisks").textContent = high;
  document.getElementById("avgImpact").textContent = avgImpact.toFixed(1);
  document.getElementById("avgProbability").textContent = avgProbability.toFixed(1);
}

function renderCategoryChart(data) {
  const counts = {};
  data.forEach((d) => {
    counts[d.risk_category] = (counts[d.risk_category] || 0) + 1;
  });

  const categories = Object.keys(counts);
  const values = Object.values(counts);

  Plotly.newPlot(
    "categoryChart",
    [{
      x: categories,
      y: values,
      type: "bar",
      marker: {
        color: "#5b8cff",
        line: { color: "#88adff", width: 1.2 }
      },
      text: values,
      textposition: "outside",
      hovertemplate: "%{x}<br>Risks: %{y}<extra></extra>"
    }],
    {
      paper_bgcolor: "rgba(0,0,0,0)",
      plot_bgcolor: "rgba(0,0,0,0)",
      font: { color: "#dbe5f5" },
      margin: { t: 10, l: 45, r: 10, b: 90 },
      xaxis: { tickangle: -25, gridcolor: "rgba(255,255,255,0.06)" },
      yaxis: { title: "Count", gridcolor: "rgba(255,255,255,0.06)", zerolinecolor: "rgba(255,255,255,0.06)" }
    },
    { responsive: true, displayModeBar: false }
  );
}

function renderRiskLevelChart(data) {
  const levelCounts = { High: 0, Medium: 0, Low: 0 };
  data.forEach((d) => {
    levelCounts[d.risk_level] += 1;
  });

  Plotly.newPlot(
    "riskLevelChart",
    [{
      labels: Object.keys(levelCounts),
      values: Object.values(levelCounts),
      type: "pie",
      hole: 0.6,
      textinfo: "label+value",
      marker: {
        colors: ["#ef4444", "#facc15", "#22c55e"]
      },
      hovertemplate: "%{label}: %{value}<extra></extra>"
    }],
    {
      paper_bgcolor: "rgba(0,0,0,0)",
      font: { color: "#dbe5f5" },
      margin: { t: 10, l: 10, r: 10, b: 10 },
      showlegend: false
    },
    { responsive: true, displayModeBar: false }
  );
}

function renderRiskMatrix(data) {
  const counts = {};
  for (let p = 1; p <= 5; p++) {
    for (let i = 1; i <= 5; i++) {
      counts[`${p}-${i}`] = 0;
    }
  }

  data.forEach((d) => {
    counts[`${d.probability_level}-${d.impact_level}`] += 1;
  });

  const z = [];
  const text = [];

  for (let p = 5; p >= 1; p--) {
    const zoneRow = [];
    const textRow = [];

    for (let i = 1; i <= 5; i++) {
      const score = p * i;
      let zoneCode = 0;
      if (score >= 15) zoneCode = 2;
      else if (score >= 8) zoneCode = 1;

      zoneRow.push(zoneCode);
      textRow.push(String(counts[`${p}-${i}`]));
    }

    z.push(zoneRow);
    text.push(textRow);
  }

  Plotly.newPlot(
    "riskMatrix",
    [{
      z: z,
      x: [1, 2, 3, 4, 5],
      y: [5, 4, 3, 2, 1],
      type: "heatmap",
      text: text,
      texttemplate: "%{text}",
      textfont: { size: 18, color: "#0b1220" },
      colorscale: [
        [0.0, "#22c55e"],
        [0.33, "#22c55e"],
        [0.34, "#facc15"],
        [0.66, "#facc15"],
        [0.67, "#ef4444"],
        [1.0, "#ef4444"]
      ],
      zmin: 0,
      zmax: 2,
      showscale: false,
      hovertemplate: "Impact: %{x}<br>Probability: %{y}<br>Risks: %{text}<extra></extra>"
    }],
    {
      paper_bgcolor: "rgba(0,0,0,0)",
      plot_bgcolor: "rgba(0,0,0,0)",
      font: { color: "#dbe5f5" },
      margin: { t: 10, l: 50, r: 10, b: 50 },
      xaxis: { title: "Impact", dtick: 1 },
      yaxis: { title: "Probability", dtick: 1 }
    },
    { responsive: true, displayModeBar: false }
  );
}

function renderTopRisks(data) {
  const container = document.getElementById("topRisks");
  container.innerHTML = "";

  const top = [...data].sort((a, b) => b.risk_score - a.risk_score).slice(0, 5);

  top.forEach((risk) => {
    const item = document.createElement("div");
    item.className = "top-risk-item";
    item.innerHTML = `
      <div class="top-risk-top">
        <div>
          <div class="top-risk-id">${risk.risk_id} · ${risk.risk_category}</div>
          <div class="top-risk-meta">${risk.owner}</div>
        </div>
        <span class="badge ${risk.risk_level.toLowerCase()}">${risk.risk_level}</span>
      </div>
      <div class="top-risk-meta">Impact ${risk.impact_level} × Probability ${risk.probability_level} = Score ${risk.risk_score}</div>
    `;
    container.appendChild(item);
  });
}

function renderOwnerChart(data) {
  const ownerMap = {};
  data.forEach((risk) => {
    if (!ownerMap[risk.owner]) ownerMap[risk.owner] = [];
    ownerMap[risk.owner].push(risk.risk_score);
  });

  const owners = Object.keys(ownerMap);
  const scores = owners.map((owner) => {
    const arr = ownerMap[owner];
    return arr.reduce((a, b) => a + b, 0) / arr.length;
  });

  Plotly.newPlot(
    "ownerChart",
    [{
      x: owners,
      y: scores,
      type: "bar",
      marker: { color: "#7dd3fc" },
      text: scores.map((s) => s.toFixed(1)),
      textposition: "outside",
      hovertemplate: "%{x}<br>Average Score: %{y:.1f}<extra></extra>"
    }],
    {
      paper_bgcolor: "rgba(0,0,0,0)",
      plot_bgcolor: "rgba(0,0,0,0)",
      font: { color: "#dbe5f5" },
      margin: { t: 10, l: 45, r: 10, b: 90 },
      xaxis: { tickangle: -25, gridcolor: "rgba(255,255,255,0.06)" },
      yaxis: { title: "Average Risk Score", gridcolor: "rgba(255,255,255,0.06)" }
    },
    { responsive: true, displayModeBar: false }
  );
}

function renderTable(data) {
  const tbody = document.querySelector("#riskTable tbody");
  tbody.innerHTML = "";

  const sorted = [...data].sort((a, b) => b.risk_score - a.risk_score);

  sorted.forEach((risk) => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${risk.risk_id}</td>
      <td>${risk.risk_category}</td>
      <td>${risk.owner}</td>
      <td>${risk.impact_level}</td>
      <td>${risk.probability_level}</td>
      <td>${risk.risk_score}</td>
      <td><span class="level-pill ${risk.risk_level.toLowerCase()}">${risk.risk_level}</span></td>
    `;
    tbody.appendChild(row);
  });
}

updateCards(enrichedRisks);
renderCategoryChart(enrichedRisks);
renderRiskLevelChart(enrichedRisks);
renderRiskMatrix(enrichedRisks);
renderTopRisks(enrichedRisks);
renderOwnerChart(enrichedRisks);
renderTable(enrichedRisks);
