# Enterprise Risk Register Demo (Synthetic Data)

A public, GitHub-friendly recreation of an enterprise risk register and actions tracker using **synthetic data only**.

This repo mirrors the overall structure of the uploaded risk register concept—risk scoring, mitigation plans, action tracking, aggregation, and lightweight reporting—without exposing any real institutional data. It was inspired by the source document you shared. fileciteturn0file0

## What is included

- `data/synthetic_risk_register.csv` — synthetic risk register
- `data/synthetic_actions.csv` — synthetic mitigation action log
- `data/synthetic_aggregations.csv` — prebuilt rollups by risk and mitigation plan
- `src/generate_data.py` — reproducible synthetic data generator
- `src/build_reports.py` — aggregation and reporting utilities
- `app.py` — Streamlit dashboard
- `tests/test_data_integrity.py` — basic integrity checks
- `docs/data_dictionary.md` — field definitions
- `docs/repo_mapping.md` — how this repo maps to the original workbook/PDF concept

## Conceptual model

### Risk Register
Each risk has:
- `impact_level` from 1–5
- `probability_level` from 1–5
- `priority_level = impact_level * probability_level`
- one or more mitigation plans
- an owner and status summary

### Actions Tracker
Each mitigation plan contains individual actions with:
- owner
- deadline
- status
- mitigation impact contribution

### Residual / adjusted risk example
The source document described an adjusted score using squared values, averaging, subtracting mitigation effect, then rounding. This repo implements that idea as:

```python
adjusted_score = round(((impact_level**2 + probability_level**2) / 2) - mitigation_effect)
```

That makes higher impact/probability weigh more heavily, while completed mitigation lowers the score.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # macOS / Linux
# .venv\Scripts\activate  # Windows

pip install -r requirements.txt
python src/generate_data.py
python src/build_reports.py
streamlit run app.py
```

## Example visuals included in the app

- risk heatmap
- priority by category
- action status summary
- mitigation impact by plan
- overdue actions table

## Repo structure

```text
erm_synthetic_github_repo/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── data/
│   ├── synthetic_risk_register.csv
│   ├── synthetic_actions.csv
│   └── synthetic_aggregations.csv
├── docs/
│   ├── data_dictionary.md
│   └── repo_mapping.md
├── src/
│   ├── generate_data.py
│   └── build_reports.py
└── tests/
    └── test_data_integrity.py
```

## Notes

- All data is synthetic and generated for demonstration purposes.
- The schema is designed for easy export to Excel, Power BI, Tableau, or a relational database.
- You can safely publish this repo as a starter template.

## Suggested GitHub repo name

`synthetic-enterprise-risk-register`

## License

MIT