const risks = [
  {
    risk_id: "R001",
    risk_category: "Technology",
    owner: "IT",
    impact_level: 5,
    probability_level: 4
  },
  {
    risk_id: "R002",
    risk_category: "Financial",
    owner: "Finance",
    impact_level: 5,
    probability_level: 3
  },
  {
    risk_id: "R003",
    risk_category: "Service Disruption",
    owner: "Operations",
    impact_level: 4,
    probability_level: 3
  },
  {
    risk_id: "R004",
    risk_category: "Market Demand",
    owner: "Strategy",
    impact_level: 4,
    probability_level: 3
  },
  {
    risk_id: "R005",
    risk_category: "Facilities",
    owner: "Facilities",
    impact_level: 4,
    probability_level: 2
  },
  {
    risk_id: "R006",
    risk_category: "Staffing",
    owner: "HR",
    impact_level: 4,
    probability_level: 3
  },
  {
    risk_id: "R007",
    risk_category: "Health & Safety",
    owner: "Safety",
    impact_level: 5,
    probability_level: 2
  },
  {
    risk_id: "R008",
    risk_category: "Compliance",
    owner: "Compliance",
    impact_level: 5,
    probability_level: 2
  },
  {
    risk_id: "R009",
    risk_category: "Cybersecurity",
    owner: "Security",
    impact_level: 5,
    probability_level: 4
  },
  {
    risk_id: "R010",
    risk_category: "Reputation",
    owner: "Communications",
    impact_level: 4,
    probability_level: 3
  }
];

function getRiskScore(risk) {
  return risk.impact_level * risk.probability_level;
}

function getRiskLevel(score) {
  if (score >= 15) return "High";
  if (score >= 8) return "Medium";
  return "Low";
}

const enrichedRisks = risks.map((risk) => {
  const risk_score = getRiskScore(risk);
  return {
    ...risk,
    risk_score,
    risk_level: getRiskLevel(risk_score)
  };
});

function updateCards(data) {
  const totalRisks = data.length;
  const highRisks = data.filter((d) => d.risk_level === "High").length;
  const avgImpact =
    data.reduce((sum, d) => sum + d.impact_level, 0) / data.length;
  const avgProbability =
    data.reduce((sum, d) => sum + d.probability_level, 0) / data.length;

  document.getElementById("totalRisks").textContent = totalRisks;
  document.getElementById("highRisks").textContent = highRisks;
  document.getElementById("avgImpact").textContent = avgImpact.toFixed(1);
  document.getElementById("avgProbability").textContent =
    avgProbability.toFixed(1);
}

function renderCategoryChart(data) {
  const categoryMap = {};
  data.forEach((d) => {
    categoryMap[d.risk_category] = (categoryMap[d.risk_category] || 0) + 1;
  });

  const categories = Object.keys(categoryMap);
  const counts = Object.values(categoryMap);

  Plotly.newPlot(
    "categoryChart",
    [
      {
        x: categories,
        y: counts,
        type: "bar"
      }
    ],
    {
      margin: { t: 10 },
      paper_bgcolor: "white",
      plot_bgcolor: "white",
      yaxis: { title: "Count" }
    },
    { responsive: true }
  );
}

function renderRiskLevelChart(data) {
  const levelMap = { High: 0, Medium: 0, Low: 0 };
  data.forEach((d) => {
    levelMap[d.risk_level] += 1;
  });

  Plotly.newPlot(
    "riskLevelChart",
    [
      {
        labels: Object.keys(levelMap),
        values: Object.values(levelMap),
        type: "pie",
        hole: 0.55,
        marker: {
          colors: ["#dc2626", "#f59e0b", "#16a34a"]
        }
      }
    ],
    {
      margin: { t: 10 },
      paper_bgcolor: "white"
    },
    { responsive: true }
  );
}

function renderRiskMatrix(data) {
  const matrixCounts = {};
  for (let p = 1; p <= 5; p++) {
    for (let i = 1; i <= 5; i++) {
      matrixCounts[`${p}-${i}`] = 0;
    }
  }

  data.forEach((d) => {
    matrixCounts[`${d.probability_level}-${d.impact_level}`] += 1;
  });

  const z = [];
  const text = [];

  for (let p = 5; p >= 1; p--) {
    const zRow = [];
    const textRow = [];

    for (let i = 1; i <= 5; i++) {
      const score = p * i;
      let zone = 0;
      if (score >= 15) zone = 2;
      else if (score >= 8) zone = 1;

      zRow.push(zone);
      textRow.push(String(matrixCounts[`${p}-${i}`]));
    }

    z.push(zRow);
    text.push(textRow);
  }

  Plotly.newPlot(
    "riskMatrix",
    [
      {
        z,
        x: [1, 2, 3, 4, 5],
        y: [5, 4, 3, 2, 1],
        type: "heatmap",
        text,
        texttemplate: "%{text}",
        textfont: { size: 18, color: "black" },
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
      }
    ],
    {
      margin: { t: 10 },
      xaxis: { title: "Impact" },
      yaxis: { title: "Probability" },
      paper_bgcolor: "white",
      plot_bgcolor: "white"
    },
    { responsive: true }
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
      <td><span class="level ${risk.risk_level.toLowerCase()}">${risk.risk_level}</span></td>
    `;
    tbody.appendChild(row);
  });
}

updateCards(enrichedRisks);
renderCategoryChart(enrichedRisks);
renderRiskLevelChart(enrichedRisks);
renderRiskMatrix(enrichedRisks);
renderTable(enrichedRisks);
