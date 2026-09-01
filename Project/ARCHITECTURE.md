# 🏗️ Architecture & Design

**Avalanche Intelligence Pro - System Architecture Documentation**

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERFACE LAYER                       │
│                  (Streamlit Dashboard)                        │
│  ┌──────────┬──────────┬──────────┬──────────┬──────────┐   │
│  │ Overview │   Risk   │ Advanced │  Trends  │Statistics│   │
│  │Dashboard │ Analysis │   ML     │& Forecast│  & Corr  │   │
│  └──────────┴──────────┴──────────┴──────────┴──────────┘   │
└─────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────┐
│                APPLICATION LOGIC LAYER                        │
│  ┌────────────────┬──────────────────┬─────────────────┐   │
│  │   Data Loader  │  Model Training  │ Risk Calculator │   │
│  │ (Data Prep)    │ (Ensemble Model) │ (Anomaly Detect)│   │
│  └────────────────┴──────────────────┴─────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────┐
│              MACHINE LEARNING LAYER                           │
│  ┌─────────────────┬─────────────────┬──────────────────┐  │
│  │ Linear Regression│  Random Forest  │ Ensemble Predictor│ │
│  │  (40% weight)   │  (60% weight)   │   (Blended)      │  │
│  │  Single Pass    │ 100 Estimators  │  Cross-Validation│  │
│  └─────────────────┴─────────────────┴──────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────┐
│                    DATA LAYER                                 │
│  ┌──────────────────┬────────────────────────────────────┐  │
│  │ CSV Data Sources │ Feature Engineering Pipeline      │  │
│  │ (Historical Data)│ (Preprocessing & Validation)      │  │
│  └──────────────────┴────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## Component Architecture

### 1. Frontend Layer (Streamlit)

**Responsibility**: User interaction, visualization, real-time updates

```python
# app.py - Main application
├── Configuration & Styling (CSS)
├── Page Setup (st.set_page_config)
├── Data Loading & Caching
├── Multi-Tab Interface
│   ├── Overview Tab (KPIs, distribution charts)
│   ├── Risk Analysis Tab (scoring, anomaly detection)
│   ├── Advanced ML Tab (feature importance, residuals)
│   ├── Trends Tab (seasonal patterns, forecasting)
│   ├── Statistics Tab (distributions, correlations)
│   ├── Events Tab (top events, preview data)
│   ├── Model Validation Tab (performance metrics)
│   └── Data Explorer Tab (full dataset, exports)
├── Sidebar Filters (year range, snow type, trigger)
└── Footer (metadata, summary)
```

**Key Features**:
- Responsive grid layouts
- Interactive Plotly visualizations
- Real-time filtering
- Export functionality
- Professional styling with gradients

### 2. Business Logic Layer

**Responsibility**: Data processing, calculations, model orchestration

#### Data Loading (`load_data()`)
```
CSV Files → Pandas DataFrame
         ↓
   Date Parsing
   Type Conversion
   Missing Value Handling
   Feature Validation
         ↓
   Filtered DataFrames (cached)
```

#### Risk Scoring (`calculate_risk_score()`)
```
Danger Level + Seasonal Context + Volatility
         ↓
Risk Formula Applied
         ↓
0-10 Risk Score Generated
         ↓
Risk Level Assigned (Low/Med/High)
```

#### Anomaly Detection (`detect_anomalies()`)
```
Time Series Data
         ↓
IQR or Z-Score Method
         ↓
Outlier Threshold Applied
         ↓
Boolean Mask Returned
```

### 3. Machine Learning Pipeline

#### Data Preparation
```python
Load Data (20 years)
    ↓
Remove Constant Columns
    ↓
Handle Missing Values (fillna)
    ↓
Temporal Split:
  - Train: 1999-2015 (17 years)
  - Validate: 2016-2019 (4 years)
    ↓
Feature Matrix (X) & Target Vector (y)
```

#### Model Training

**Linear Regression**
```
Features (119) → StandardScaler → LinearRegression
                                        ↓
                              Coefficients Learned
                                        ↓
                          Predictions Generated
                                        ↓
                   Performance: MAE ~0.49, R² ~0.18
```

**Random Forest**
```
Features (119) → RandomForestRegressor
                (100 estimators, depth=15)
                        ↓
                Decision Trees Trained
                        ↓
                Feature Importance Calculated
                        ↓
                Predictions Generated
                        ↓
         Performance: MAE ~0.38, R² ~0.30
         (Stronger than Linear Regression)
```

**Ensemble**
```
   LR Predictions (40%)  +  RF Predictions (60%)
              ↓                        ↓
         Weighted Average
              ↓
      Final Predictions
              ↓
Cross-Validation (5-Fold)
              ↓
Final Metrics: MAE ~0.49, RMSE ~0.63, R² ~0.245
```

#### Cross-Validation Strategy
```
Data Split (1999-2015)
    ↓
5-Fold Split:
  ├─ Fold 1: Train on 4, Test on 1
  ├─ Fold 2: Train on 4, Test on 1
  ├─ Fold 3: Train on 4, Test on 1
  ├─ Fold 4: Train on 4, Test on 1
  └─ Fold 5: Train on 4, Test on 1
    ↓
Average R² Score: ±std
```

### 4. Data Layer

#### Input Data Schema

**Observations Dataset**
```
119 features including:
├─ Temporal: date_release, year (implicit)
├─ Avalanche Metrics: area_m2, length_m, width_m
├─ Classification: snow_type, trigger_type, aval_size_class
├─ Geographic: max_elevation_m, min_elevation_m
└─ Index: weight_AAI, aspect_degrees, etc.

Format: CSV (20 years × ~20,000 records)
Size: ~10 MB
```

**Danger Dataset**
```
7 features:
├─ date: datetime
├─ year: int (1999-2019)
├─ max.danger.corr: float (target variable)
├─ AAI_all: float (activity index)
└─ Other indices

Format: CSV (20 years × ~7,300 records)
Size: ~0.5 MB
```

#### Feature Engineering Pipeline

```python
Raw Data
    ↓
├─ Date Parsing (pd.to_datetime)
├─ Type Conversion (pd.to_numeric)
├─ Missing Value Handling (fillna(0))
├─ Outlier Detection (IQR method)
├─ Feature Scaling (StandardScaler - optional for tree models)
└─ Feature Selection (drop constants)
    ↓
Clean Feature Matrix
```

---

## Data Flow Diagrams

### Training Pipeline

```
┌─────────────────┐
│  CSV Data Files │
└────────┬────────┘
         │
         ▼
    ┌─────────────┐
    │ Data Loader │
    └────┬────────┘
         │
    ┌────▼────────────────────────────────────┐
    │  Preprocessing                           │
    │  ├─ Parse Dates                          │
    │  ├─ Convert Types                        │
    │  ├─ Handle Missing                       │
    │  └─ Validate Features                    │
    └────┬────────────────────────────────────┘
         │
    ┌────▼─────────────────────────┐
    │  Temporal Train/Val Split    │
    │  Train: 1999-2015            │
    │  Validate: 2016-2019         │
    └────┬──────────────────────────┘
         │
    ┌────▼──────────┐
    │ Model Training│
    │ ├─ LR Model   │
    │ ├─ RF Model   │
    │ └─ Ensemble   │
    └────┬──────────┘
         │
    ┌────▼──────────────────────────┐
    │  Cross-Validation (5-Fold)    │
    │  Compute CV Scores            │
    └────┬──────────────────────────┘
         │
    ┌────▼──────────────────────────┐
    │  Validation & Metrics         │
    │  ├─ R², MAE, RMSE, MAPE       │
    │  ├─ Feature Importance        │
    │  └─ Residual Analysis         │
    └────▼──────────────────────────┘
         │
         ▼
    ┌──────────────┐
    │  Dashboard   │
    │  Display     │
    └──────────────┘
```

### Inference Pipeline

```
User Interaction (Filters Selected)
         │
         ▼
    Load Filtered Data
         │
         ▼
    Calculate Risk Score
         │
         ▼
    Detect Anomalies
         │
         ▼
    Generate Visualizations
         │
         ▼
    Render in Streamlit UI
```

---

## Caching Strategy

### Data Caching
```python
@st.cache_data  # Decorator on load_data()
def load_data():
    # Loads CSV files
    # Preprocesses data
    # Cached for session (cleared on file change)
    return observations, danger
```

**Cache Benefits**:
- ✅ Avoids re-loading CSV files
- ✅ Reduces computational overhead
- ✅ Faster tab switching
- ✅ Better user experience

### Model Caching (Implicit)
```python
def train_ensemble_model():
    # No @st.cache_data decorator
    # Reason: Streamlit's spinner context required
    # Trade-off: Retrains on each run (acceptable for demo)
```

---

## Performance Characteristics

### Computation Complexity

| Operation | Time Complexity | Space Complexity |
|-----------|-----------------|------------------|
| Load CSV | O(n) | O(n) |
| Preprocess | O(n × m) | O(n × m) |
| LR Train | O(m²) + O(n × m) | O(m²) |
| RF Train | O(n × log n × m) | O(n × m) |
| Predict | O(m) | O(1) |
| Cross-Val | O(5 × training) | O(n × m) |

Where `n` = records, `m` = features

### Empirical Performance
- Data loading: ~2-3 seconds
- ML training: ~5-8 seconds
- Inference: <1 second
- Total UI load: ~10-15 seconds

### Memory Usage
- Observations DF: ~50-100 MB
- Danger DF: ~2-5 MB
- Models: ~5-10 MB
- **Total Peak**: ~150-200 MB

---

## Error Handling Architecture

### Data Validation Layer

```python
try:
    observations, danger = load_data()
except FileNotFoundError:
    st.error("Dataset files not found...")
except ValueError:
    st.error("Missing required columns...")
```

### Model Execution Layer

```python
try:
    ensemble_results = train_ensemble_model()
except ValueError as e:
    st.error(f"Model training failed: {e}")
except Exception as e:
    st.error(f"Unexpected error: {e}")
    logger.exception("Training error")
```

### Risk Calculation Layer

```python
try:
    risk_scores = risk_data["max.danger.corr"].apply(
        lambda x: calculate_risk_score(x, seasonal_avg, volatility)
    )
except ZeroDivisionError:
    risk_scores = 0
```

---

## Scalability Considerations

### Current Limitations
- ❌ Single-threaded execution (Streamlit limitation)
- ❌ In-memory data loading (max ~500MB)
- ❌ No database integration
- ❌ No distributed computing

### Scaling Recommendations

**Vertical Scaling** (More resources)
- Increase container memory → 2-4GB
- Use faster CPU → 2-4 cores
- Enable model optimizations

**Horizontal Scaling** (Multiple instances)
- Deploy multiple app containers
- Use load balancer (AWS ALB, etc.)
- Share cache via Redis
- Use session management

**Data Scalability**
- Implement database (PostgreSQL, BigQuery)
- Use data warehousing (Snowflake, DuckDB)
- Implement feature stores
- Add data streaming (Kafka)

### Performance Optimization Roadmap
1. Add Redis caching for model predictions
2. Implement incremental model retraining
3. Use Dask for parallel processing
4. Add async data loading
5. Implement WebSocket for live updates

---

## Security Architecture

### Data Security
- ✅ Input validation (dropna, type checking)
- ✅ No SQL injection (pandas only)
- ⚠️ No authentication/authorization (add if needed)
- ⚠️ No encryption (add for production)

### Application Security
- ✅ No code injection (Streamlit sandboxed)
- ✅ No dangerous libraries
- ⚠️ Add CORS headers
- ⚠️ Add rate limiting
- ⚠️ Add request validation

### Deployment Security
- ✅ Dockerfile hardened (python:3.12-slim)
- ✅ No exposed credentials (use secrets)
- ✅ Health checks enabled
- ⚠️ Add log monitoring
- ⚠️ Add intrusion detection

---

## Testing Strategy

### Unit Tests
```python
# test_config.py
def test_risk_score_range():
    score = calculate_risk_score(5.0, 3.0, 1.0)
    assert 0 <= score <= 10

def test_anomaly_detection():
    series = pd.Series([1, 2, 3, 100, 4, 5])
    anomalies = detect_anomalies(series)
    assert anomalies.sum() >= 1
```

### Integration Tests
```python
# test_app.py
def test_app_loads():
    # Verify all data loads without error
    obs, danger = load_data()
    assert len(obs) > 0
    assert len(danger) > 0

def test_model_training():
    # Verify models train successfully
    results = train_ensemble_model()
    assert results['metrics']['r2'] >= 0
```

### End-to-End Tests
```
# e2e_test.py
1. Launch Streamlit app
2. Load all tabs
3. Apply filters
4. Export data
5. Verify output formats
```

---

## Monitoring & Observability

### Metrics to Track
```
Application Metrics:
├─ Request count
├─ Response time
├─ Error rate
└─ Cache hit rate

Business Metrics:
├─ Model R² score
├─ Prediction errors
├─ Risk score distribution
└─ Feature importance changes

Infrastructure Metrics:
├─ CPU usage
├─ Memory usage
├─ Disk I/O
└─ Network latency
```

### Logging Strategy
```python
import logging

logger = logging.getLogger(__name__)

logger.info("App started")
logger.debug(f"Model trained: R²={r2_score:.3f}")
logger.warning("High memory usage detected")
logger.error("Model training failed")
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2026-09-01 | ✨ Advanced ML, Risk Scoring, Multi-Tab UI |
| 1.5.0 | 2026-08-15 | 📈 Added statistical analysis, seasonal patterns |
| 1.0.0 | 2026-07-01 | 🚀 Initial release with basic dashboard |

---

## References

- [Streamlit Architecture](https://docs.streamlit.io/library/architecture)
- [Scikit-Learn ML Pipelines](https://scikit-learn.org/stable/modules/compose.html)
- [Ensemble Methods](https://en.wikipedia.org/wiki/Ensemble_learning)
- [Cross-Validation](https://scikit-learn.org/stable/modules/cross_validation.html)

---

**Last Updated**: 2026-09-01  
**Maintainer**: Avalanche Intelligence Team  
**License**: MIT
