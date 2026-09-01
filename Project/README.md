# Avalanche Intelligence Project

This project transforms the avalanche datasets in the parent folder into a polished, production-oriented dashboard for operational analysis and reporting.

## Included data

- `data_set_1_avalanche_observations_wi9899_to_wi1819_davos.csv`
- `data_set_2_danger_avalanches.csv`

The dashboard reads these files directly from the workspace parent folder, so no data copy is required.

## Run locally

1. Open a terminal in the [Project](Project) directory.
2. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```
3. Start the app:
   ```bash
   streamlit run app.py
   ```
4. Open the local URL shown in the terminal.

## Deployment-ready features

- Clean production-style dashboard layout
- Filter controls for year, snow type, and trigger type
- KPI summary cards for observations and danger conditions
- Trend visualizations and event analysis views
- Downloadable filtered datasets
- Docker support for deployment environments

## Deployment container

A Dockerfile is included for deployment to container platforms such as Azure Container Apps, Render, Railway, or a standard Docker host.

## Project structure

- `app.py` — main dashboard application
- `requirements.txt` — Python dependencies
- `Dockerfile` — container definition for deployment
- `.streamlit/config.toml` — Streamlit runtime config
- `README.md` — project instructions
