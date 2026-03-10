function renderRiskMatrix(data) {
  const matrix = {};

  for (let p = 1; p <= 5; p++) {
    for (let i = 1; i <= 5; i++) {
      matrix[`${p}-${i}`] = [];
    }
  }

  data.forEach((risk) => {
    matrix[`${risk.probability_level}-${risk.impact_level}`].push(risk);
  });

  const z = [];
  const text = [];
  const hover = [];

  for (let p = 5; p >= 1; p--) {
    const row = [];
    const rowText = [];
    const rowHover = [];

    for (let i = 1; i <= 5; i++) {
      const risksInCell = matrix[`${p}-${i}`];
      const score = p * i;

      let zone = 0;
      if (score >= 15) zone = 2;
      else if (score >= 8) zone = 1;

      row.push(zone);
      rowText.push(risksInCell.length);

      if (risksInCell.length === 0) {
        rowHover.push(`Impact ${i}<br>Probability ${p}<br><br>No risks`);
      } else {
        const riskList = risksInCell
          .map(
            (r) =>
              `${r.risk_id} · ${r.risk_category} · ${r.owner} · Score ${r.risk_score}`
          )
          .join("<br>");

        rowHover.push(
          `Impact ${i}<br>Probability ${p}<br><br>${riskList}<br><br><b>Click to filter table</b>`
        );
      }
    }

    z.push(row);
    text.push(rowText);
    hover.push(rowHover);
  }

  const matrixDiv = document.getElementById("riskMatrix");

  Plotly.newPlot(
    matrixDiv,
    [
      {
        z: z,
        x: [1, 2, 3, 4, 5],
        y: [5, 4, 3, 2, 1],
        type: "heatmap",
        text: text,
        texttemplate: "%{text}",
        textfont: { size: 18, color: "#0b1220" },
        hovertext: hover,
        hoverinfo: "text",
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
        showscale: false
      }
    ],
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

  matrixDiv.on("plotly_click", function (eventData) {
    const clickedImpact = eventData.points[0].x;
    const clickedProbability = eventData.points[0].y;

    const filtered = data.filter(
      (risk) =>
        risk.impact_level === clickedImpact &&
        risk.probability_level === clickedProbability
    );

    renderTable(filtered);
    renderSelectedCellInfo(clickedImpact, clickedProbability, filtered);
  });
}
function renderSelectedCellInfo(impact, probability, filteredRisks) {
  let infoBox = document.getElementById("selectedCellInfo");

  if (!infoBox) {
    infoBox = document.createElement("div");
    infoBox.id = "selectedCellInfo";
    infoBox.style.marginBottom = "16px";
    infoBox.style.padding = "14px 16px";
    infoBox.style.borderRadius = "14px";
    infoBox.style.background = "rgba(255,255,255,0.04)";
    infoBox.style.border = "1px solid rgba(255,255,255,0.08)";
    infoBox.style.color = "#dbe5f5";

    const registerSection = document.getElementById("register");
    registerSection.insertBefore(infoBox, registerSection.querySelector(".table-wrap"));
  }

  infoBox.innerHTML = `
    <strong>Filtered View:</strong> Impact ${impact} × Probability ${probability}
    <br>
    <span style="color:#9aa8bf;">Showing ${filteredRisks.length} risk(s) from the selected matrix cell.</span>
    <br><br>
    <button onclick="resetTable()" style="
      background:#5b8cff;
      color:white;
      border:none;
      padding:8px 12px;
      border-radius:10px;
      cursor:pointer;
      font-weight:600;
    ">
      Reset Table
    </button>
  `;
}
function resetTable() {
  renderTable(enrichedRisks);

  const infoBox = document.getElementById("selectedCellInfo");
  if (infoBox) {
    infoBox.remove();
  }
}
