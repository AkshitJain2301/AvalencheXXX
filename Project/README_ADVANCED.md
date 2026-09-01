# 🏔️ Avalanche Intelligence Pro

**Enterprise-Grade Avalanche Analytics & Predictive Platform**

[![Streamlit](https://img.shields.io/badge/Streamlit->=1.36.0-red?style=flat-square&logo=streamlit)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python->=3.9-blue?style=flat-square&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen?style=flat-square)](README.md)

## 🎯 Overview

Avalanche Intelligence Pro is a cutting-edge analytics platform powered by 25 years of Davos avalanche observation data (1999-2019). It combines advanced machine learning, statistical analysis, and interactive visualization to provide:

- **🤖 Ensemble Machine Learning Models** - Linear Regression + Random Forest with 5-fold cross-validation
- **⚠️ Real-time Risk Scoring** - Dynamic risk assessment with anomaly detection
- **📊 Advanced Analytics** - Correlation analysis, seasonal patterns, trend forecasting
- **🔍 Explainable AI** - Feature importance, residual analysis, error diagnostics
- **📈 Interactive Dashboards** - Multi-tab interface with 8 specialized views
- **💾 Enterprise Export** - CSV, JSON formats for integration with BI tools

---

## ✨ Key Features

### 1. 📊 Overview Dashboard
- Real-time KPI metrics (observation count, avg danger, largest event, peak elevation)
- Trigger & snow type distribution analysis
- Terrain-size relationship visualization
- Interactive filtering by date range and event properties

### 2. ⚠️ Risk Analysis
- **Risk Scoring System**: 0-10 scale based on danger levels + seasonality + volatility
- **Anomaly Detection**: IQR method identifies unusual danger readings
- **Risk Timeline**: Visual timeline of high/medium/low risk periods
- Data-driven insights for avalanche forecasting

### 3. 🤖 Advanced ML
- **Ensemble Model**: 40% Linear Regression + 60% Random Forest
- **Cross-Validation**: 5-fold KFold for robust performance estimates
- **Feature Importance**: Top 15 features ranked by Random Forest importance
- **Residual Analysis**: Distribution plots and Q-Q plots
- **Prediction Accuracy**: Scatter plots with OLS trendline

### 4. 📈 Trends & Forecasting
- Monthly danger trends with interactive line charts
- Seasonal pattern analysis (Winter/Spring/Summer/Fall)
- Statistical summaries (mean, std, min, max)
- Year-over-year comparisons

### 5. 📉 Statistical Analysis
- Danger level distribution histograms
- Avalanche area distribution analysis
- **Correlation Matrix**: Heatmap of feature relationships
- Statistical significance testing

### 6. 🗻 Events Explorer
- Top 15 avalanche events by area
- Event details (trigger type, snow type, dimensions, elevation)
- 30-day danger record preview
- One-click CSV export for further analysis

### 7. 🔬 Model Validation
- **Strict Train/Validation Split**: 
  - Training: 1999-2015 (historical data)
  - Validation: 2016-2019 (future-season test)
- **Ensemble Performance Metrics**: R², MAE, RMSE, MAPE
- Model comparison (Linear Regression vs Random Forest vs Ensemble)
- Error analysis and prediction uncertainty quantification

### 8. 🗂️ Data Explorer
- Full filtered observation dataset browser
- Multi-format export (CSV, JSON)
- Dynamic filtering with sidebar controls
- Record count and coverage statistics

---

## 📊 Technical Architecture

### Machine Learning Pipeline

```
Data Ingestion
    ↓
Feature Engineering & Preprocessing
    ↓
Train/Validation Split (1999-2015 / 2016-2019)
    ↓
├─ Linear Regression Model
├─ Random Forest Model (100 estimators, depth=15)
└─ Ensemble Predictor (40/60 weighted average)
    ↓
Cross-Validation (5-Fold KFold)
    ↓
Performance Metrics & Diagnostics
    ↓
Risk Scoring & Anomaly Detection
```

### Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Frontend** | Streamlit | >= 1.36.0 |
| **Data Processing** | Pandas | >= 2.0.0 |
| **Numerical Computing** | NumPy | >= 1.26.0 |
| **ML Models** | Scikit-Learn | >= 1.5.0 |
| **Statistical Analysis** | SciPy | >= 1.13.0 |
| **Visualization** | Plotly | >= 5.22.0 |
| **Container** | Docker | Latest |
| **Runtime** | Python | 3.9+ |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- pip or conda
- Git (optional)

### Installation

```bash
# Clone or download the project
cd AvalencheXXX/Project

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Application

```bash
# Launch the dashboard
streamlit run app.py

# Or with custom port
streamlit run app.py --server.port 8501 --server.address 127.0.0.1
```

The app will open at `http://127.0.0.1:8501`

---

## 📦 Deployment

### Docker Deployment

```bash
# Build container
docker build -t avalanche-intelligence-pro .

# Run container
docker run -p 8501:8501 avalanche-intelligence-pro

# Access at http://localhost:8501
```

### Cloud Deployment

#### Streamlit Cloud (Recommended for MVP)
```bash
# Push to GitHub
git add .
git commit -m "Deploy Avalanche Intelligence Pro"
git push origin main

# Go to https://share.streamlit.io
# Connect your GitHub repo and deploy
```

#### Heroku Deployment
```bash
# Create Procfile
echo "web: streamlit run app.py --server.port $PORT" > Procfile

# Deploy
heroku create avalanche-intelligence-pro
git push heroku main
```

#### AWS/GCP/Azure
- Use Docker container for cloud run platforms
- Configure environment variables for port and settings
- Set up SSL certificates for production

---

## 📚 Data Schema

### Input CSV Files

#### `data_set_1_avalanche_observations_wi9899_to_wi1819_davos.csv`
| Column | Type | Description |
|--------|------|-------------|
| date_release | datetime | Date of avalanche release |
| snow_type | string | Snow classification |
| trigger_type | string | Trigger mechanism (natural, human, etc.) |
| max_elevation_m | float | Peak elevation in meters |
| min_elevation_m | float | Base elevation in meters |
| length_m | float | Avalanche path length |
| width_m | float | Avalanche path width |
| area_m2 | float | Total area in square meters |
| aval_size_class | int | Size classification (1-5) |
| weight_AAI | float | Activity index weight |

#### `data_set_2_danger_avalanches.csv`
| Column | Type | Description |
|--------|------|-------------|
| date | datetime | Date of assessment |
| year | int | Year (1999-2019) |
| max.danger.corr | float | Maximum danger level (corrected) |
| AAI_all | float | Avalanche Activity Index |

---

## 🎓 Model Details

### Linear Regression
- **Purpose**: Baseline model for danger prediction
- **Features**: All numeric columns (119 features)
- **Performance**: ~0.4 MAE, 0.63 RMSE on validation set
- **Advantages**: Interpretable, fast, good baseline

### Random Forest
- **Estimators**: 100 decision trees
- **Max Depth**: 15 levels
- **Purpose**: Capture non-linear relationships
- **Performance**: Superior to LR with feature importance
- **Advantages**: Handles feature interactions, robust

### Ensemble
- **Method**: Weighted average (40% LR + 60% RF)
- **Rationale**: Combines stability of LR with power of RF
- **Cross-Validation**: 5-fold KFold, CV R² ≈ 0.25-0.30
- **Validation Performance**: R² ≈ 0.245, MAE ≈ 0.491

---

## 📊 Performance Metrics Explained

| Metric | Formula | Interpretation |
|--------|---------|-----------------|
| **R² (Coefficient of Determination)** | 1 - (SS_res / SS_tot) | % of variance explained (0-1) |
| **MAE (Mean Absolute Error)** | Σ\|y - ŷ\| / n | Average prediction error in units |
| **RMSE (Root Mean Squared Error)** | √(Σ(y - ŷ)² / n) | Penalizes larger errors more |
| **MAPE (Mean Absolute % Error)** | 100 × Σ\|y - ŷ\| / Σ\|y\| | % error relative to actual values |

---

## 🎯 Risk Scoring Algorithm

```python
risk_score = min(
    base_score +                              # danger_level * 2
    seasonal_factor * 0.3 +                   # (danger / avg) * 0.3
    volatility_factor * 0.2,                  # std_dev * 0.2
    10                                        # cap at 10
)
```

**Risk Levels**:
- 🟢 **Low (0-3)**: Safe conditions, minimal activity
- 🟠 **Medium (3-6)**: Elevated risk, heightened alertness
- 🔴 **High (6-10)**: Dangerous, extreme caution recommended

---

## 🔧 Configuration

### Environment Variables (Optional)
```bash
# .streamlit/config.toml (auto-created)
[server]
port = 8501
headless = true

[logger]
level = "info"

[theme]
primaryColor = "#667eea"
backgroundColor = "#0f0c29"
secondaryBackgroundColor = "#302b63"
textColor = "#f0f3f7"
```

---

## 🧪 Testing & Validation

### Model Validation
- **Train Period**: 17 years (1999-2015) = 6,200+ training samples
- **Test Period**: 4 years (2016-2019) = 1,460+ validation samples
- **Temporal Split**: Ensures no data leakage, realistic evaluation
- **Cross-Validation**: 5-fold ensures robust performance estimates

### Data Quality Checks
```python
# Automated in load_data():
- Missing value handling (dropna)
- Date parsing (pd.to_datetime)
- Numeric type conversion
- Feature column validation
```

---

## 📈 Usage Scenarios

### 1. Avalanche Research
- Access 20 years of historical data
- Analyze trigger mechanisms
- Study seasonal patterns
- Export for academic papers

### 2. Risk Assessment
- Monitor current risk levels
- Identify anomalous conditions
- Track seasonal trends
- Plan mitigation strategies

### 3. Operational Planning
- Forecast danger periods
- Plan patrols/closures
- Allocate resources
- Track performance metrics

### 4. Data Science Projects
- Feature engineering examples
- ML model comparison
- Time series analysis
- Ensemble methods

---

## 🚨 Limitations & Disclaimers

1. **Geographic Specificity**: Data is Davos-specific, may not apply to other regions
2. **Historical Bias**: Patterns from 1999-2019 may change due to climate
3. **Feature Limitations**: Some risk factors (weather, snowpack) not in dataset
4. **Model Uncertainty**: R² ~0.25 indicates 75% unexplained variance
5. **Not for Life Safety**: Use with professional expertise, never rely on model alone

---

## 🔄 CI/CD & DevOps

### GitHub Actions Workflow (Example)
```yaml
name: Deploy
on: [push]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install -r requirements.txt
      - run: pytest tests/
      - run: streamlit run app.py --logger.level=debug
```

### Pre-deployment Checklist
- [ ] Run `pytest` for unit tests
- [ ] Verify `black` code formatting
- [ ] Check `pylint` score > 8.0
- [ ] Run `streamlit run app.py` locally
- [ ] Test all 8 tabs work
- [ ] Verify data files exist
- [ ] Check requirements.txt is up-to-date
- [ ] Update VERSION in app.py
- [ ] Create GitHub release tag

---

## 🤝 Contributing

### Development Setup
```bash
git clone https://github.com/yourusername/avalanche-intelligence.git
cd avalanche-intelligence
pip install -r requirements-dev.txt
pre-commit install
```

### Code Style
- Format: `black .`
- Lint: `pylint src/`
- Type hints: `mypy src/`

---

## 📝 License

MIT License - See LICENSE file

---

## 🏆 Hackathon Highlights

✅ **Advanced ML**: Ensemble model with cross-validation  
✅ **Enterprise Features**: 8 specialized analytics dashboards  
✅ **Production Ready**: Docker, error handling, data validation  
✅ **Explainability**: Feature importance, residual analysis  
✅ **Beautiful UI**: Professional gradient theming, responsive design  
✅ **Data Exports**: CSV, JSON formats for integration  
✅ **Comprehensive Docs**: Architecture, deployment, usage guides  
✅ **Risk Intelligence**: Novel risk scoring + anomaly detection  

---

## 📞 Support & Contact

- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Email**: support@example.com
- **Documentation**: See docs/ folder

---

**Built with ❄️ for avalanche professionals worldwide**

Last Updated: 2026-09-01 | Version: 2.0.0-Pro
