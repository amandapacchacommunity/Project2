function renderRiskMatrix(data) {

  const matrix = {};

  for (let p = 1; p <= 5; p++) {
    for (let i = 1; i <= 5; i++) {
      matrix[`${p}-${i}`] = [];
    }
  }

  data.forEach(risk => {
    matrix[`${risk.probability_level}-${risk.impact_level}`].push(
      `${risk.risk_id} (${risk.risk_category})`
    );
  });

  const z = [];
  const text = [];
  const hover = [];

  for (let p = 5; p >= 1; p--) {

    const row = [];
    const rowText = [];
    const rowHover = [];

    for (let i = 1; i <= 5; i++) {

      const risks = matrix[`${p}-${i}`];
      const score = p * i;

      let zone = 0;
      if (score >= 15) zone = 2;
      else if (score >= 8) zone = 1;

      row.push(zone);
      rowText.push(risks.length);

      if (risks.length === 0) {
        rowHover.push(`Impact ${i}<br>Probability ${p}<br>No risks`);
      } else {
        rowHover.push(
          `Impact ${i}<br>Probability ${p}<br><br>${risks.join("<br>")}`
        );
      }

    }

    z.push(row);
    text.push(rowText);
    hover.push(rowHover);
  }

  Plotly.newPlot("riskMatrix", [{
    z: z,
    x: [1,2,3,4,5],
    y: [5,4,3,2,1],
    type: "heatmap",
    text: text,
    texttemplate: "%{text}",
    textfont: {size:18},
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
  }],
  {
    xaxis: {title: "Impact"},
    yaxis: {title: "Probability"},
    margin: {t:10}
  },
  {responsive:true});
}
