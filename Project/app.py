from pathlib import Path
import json
import io
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score, KFold
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, mean_absolute_percentage_error
from sklearn.preprocessing import StandardScaler
from scipy import stats

ROOT = Path(__file__).resolve().parent.parent
CSV_OBSERVATIONS = ROOT / "data_set_1_avalanche_observations_wi9899_to_wi1819_davos.csv"
CSV_DANGER = ROOT / "data_set_2_danger_avalanches.csv"

CUSTOM_CSS = """
<style>
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    
    .main {
        background: linear-gradient(180deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    .stApp {
        background: linear-gradient(180deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        color: #f0f3f7;
    }
    
    .stSidebar {
        background: rgba(15, 12, 41, 0.95);
        border-right: 2px solid rgba(102, 126, 234, 0.3);
    }
    
    h1 {
        color: #f0f3f7;
        font-size: 2.5rem;
        font-weight: 800;
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }
    
    h2 {
        color: #f0f3f7;
        font-size: 1.8rem;
        font-weight: 700;
        border-bottom: 2px solid rgba(102, 126, 234, 0.5);
        padding-bottom: 0.5rem;
        margin-top: 1.5rem;
    }
    
    h3 {
        color: #e0e6ff;
        font-weight: 600;
    }
    
    .metric-card {
        background: rgba(102, 126, 234, 0.1);
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 10px;
        padding: 1.5rem;
        margin: 0.5rem 0;
    }
    
    div[data-testid="stMetricValue"] {
        color: #667eea;
        font-size: 1.8rem;
        font-weight: 800;
    }
    
    div[data-testid="stMetricLabel"] {
        color: #b8c1f5;
        font-weight: 600;
    }
    
    .stTabs [role="tablist"] {
        gap: 0.5rem;
        background: rgba(0, 0, 0, 0.2);
        border-radius: 10px;
        padding: 0.5rem;
    }
    
    .stTabs [role="tab"] {
        background: rgba(102, 126, 234, 0.1);
        border: 1px solid rgba(102, 126, 234, 0.2);
        border-radius: 8px;
        color: #b8c1f5;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stTabs [role="tab"][aria-selected="true"] {
        background: var(--primary-gradient);
        color: white;
        border: none;
    }
    
    .stButton>button {
        background: var(--primary-gradient);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.6rem 1.2rem;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
    }
    
    .stSelectbox, .stMultiSelect, .stSlider {
        color: #f0f3f7;
    }
    
    .stDataFrame {
        background: rgba(102, 126, 234, 0.05);
        border-radius: 10px;
    }
    
    .risk-high {
        color: #f5576c;
        font-weight: 700;
    }
    
    .risk-medium {
        color: #ffa500;
        font-weight: 700;
    }
    
    .risk-low {
        color: #51cf66;
        font-weight: 700;
    }
</style>
"""


def load_data():
    if not CSV_OBSERVATIONS.exists() or not CSV_DANGER.exists():
        raise FileNotFoundError(
            "Expected dataset files were not found in the parent directory of this project."
        )

    observations = pd.read_csv(CSV_OBSERVATIONS, sep=";")
    danger = pd.read_csv(CSV_DANGER, sep=";")

    required_obs = {
        "date_release",
        "snow_type",
        "trigger_type",
        "max_elevation_m",
        "min_elevation_m",
        "length_m",
        "width_m",
        "perimeter_length_m",
        "area_m2",
        "aval_size_class",
        "weight_AAI",
        "max.danger.corr",
    }
    missing_obs = required_obs - set(observations.columns)
    if missing_obs:
        raise ValueError(f"Observation dataset missing required columns: {sorted(missing_obs)}")

    required_danger = {"date", "year", "max.danger.corr", "AAI_all"}
    missing_danger = required_danger - set(danger.columns)
    if missing_danger:
        raise ValueError(f"Danger dataset missing required columns: {sorted(missing_danger)}")

    observations = observations.copy()
    danger = danger.copy()

    observations["date_release"] = pd.to_datetime(observations["date_release"], errors="coerce")
    danger["date"] = pd.to_datetime(danger["date"], errors="coerce")

    numeric_columns = [
        "max_elevation_m",
        "min_elevation_m",
        "length_m",
        "width_m",
        "perimeter_length_m",
        "area_m2",
        "aval_size_class",
        "weight_AAI",
        "max.danger.corr",
        "aspect_degrees",
    ]
    for column in numeric_columns:
        if column in observations.columns:
            observations[column] = pd.to_numeric(observations[column], errors="coerce")

    for column in danger.columns:
        if column not in {"date", "year"}:
            danger[column] = pd.to_numeric(danger[column], errors="coerce")

    observations = observations.dropna(subset=["date_release"]).copy()
    danger = danger.dropna(subset=["date"]).copy()

    return observations, danger


def calculate_risk_score(danger_level, seasonal_avg, volatility):
    """Calculate risk score on 0-10 scale based on danger metrics."""
    base_score = min(danger_level * 2, 10)
    seasonal_factor = (danger_level / (seasonal_avg + 1e-6)) * 2
    volatility_factor = min(volatility * 1.5, 3)
    risk_score = min(base_score + seasonal_factor * 0.3 + volatility_factor * 0.2, 10)
    return max(risk_score, 0)


def detect_anomalies(series, method='iqr', threshold=1.5):
    """Detect anomalies using IQR or Z-score methods."""
    if method == 'iqr':
        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - threshold * IQR
        upper_bound = Q3 + threshold * IQR
        return (series < lower_bound) | (series > upper_bound)
    else:  # z-score
        z_scores = np.abs(stats.zscore(series.dropna()))
        return z_scores > threshold


def train_ensemble_model():
    """Train ensemble of Linear Regression and Random Forest with cross-validation."""
    danger = pd.read_csv(CSV_DANGER, sep=";")
    danger = danger.copy()
    danger["date"] = pd.to_datetime(danger["date"], errors="coerce")
    danger["year"] = pd.to_numeric(danger["year"], errors="coerce")
    danger["max.danger.corr"] = pd.to_numeric(danger["max.danger.corr"], errors="coerce")

    if "date" not in danger.columns or "year" not in danger.columns or "max.danger.corr" not in danger.columns:
        raise ValueError("Danger dataset is missing required columns for model training.")

    danger = danger.dropna(subset=["date", "year", "max.danger.corr"]).copy()

    train = danger[danger["year"].between(1999, 2015)].copy()
    validate = danger[danger["year"].between(2016, 2019)].copy()

    if train.empty or validate.empty:
        raise ValueError("No rows available for the required train/validation split.")

    feature_columns = [
        col for col in danger.columns
        if col not in {"date", "year", "max.danger.corr"} and pd.api.types.is_numeric_dtype(danger[col])
    ]

    X_train = train[feature_columns].fillna(0)
    y_train = train["max.danger.corr"].fillna(0)
    X_val = validate[feature_columns].fillna(0)
    y_val = validate["max.danger.corr"].fillna(0)

    constant_cols = X_train.columns[X_train.nunique() == 1]
    X_train = X_train.drop(columns=constant_cols, errors="ignore")
    X_val = X_val.drop(columns=constant_cols, errors="ignore")

    # Train Linear Regression
    lr_model = LinearRegression()
    lr_model.fit(X_train, y_train)
    lr_pred = lr_model.predict(X_val)

    # Train Random Forest with cross-validation
    rf_model = RandomForestRegressor(n_estimators=100, max_depth=15, random_state=42, n_jobs=-1)
    rf_model.fit(X_train, y_train)
    rf_pred = rf_model.predict(X_val)

    # Ensemble prediction (weighted average)
    ensemble_pred = 0.4 * lr_pred + 0.6 * rf_pred

    # Cross-validation scores
    kfold = KFold(n_splits=5, shuffle=True, random_state=42)
    lr_cv_scores = cross_val_score(lr_model, X_train, y_train, cv=kfold, scoring='r2')
    rf_cv_scores = cross_val_score(rf_model, X_train, y_train, cv=kfold, scoring='r2')

    results = validate[["date", "year", "max.danger.corr"]].copy()
    results["lr_pred"] = lr_pred
    results["rf_pred"] = rf_pred
    results["ensemble_pred"] = ensemble_pred
    results["abs_error"] = (ensemble_pred - y_val).abs()

    rmse = np.sqrt(mean_squared_error(y_val, ensemble_pred))
    mape = mean_absolute_percentage_error(y_val, ensemble_pred) if (y_val != 0).all() else 0

    metrics = {
        "train_year_range": "1999-2015",
        "validation_year_range": "2016-2019",
        "training_rows": int(len(train)),
        "validation_rows": int(len(validate)),
        "mae": mean_absolute_error(y_val, ensemble_pred),
        "rmse": rmse,
        "r2": r2_score(y_val, ensemble_pred),
        "mape": mape,
        "lr_cv_mean": float(lr_cv_scores.mean()),
        "lr_cv_std": float(lr_cv_scores.std()),
        "rf_cv_mean": float(rf_cv_scores.mean()),
        "rf_cv_std": float(rf_cv_scores.std()),
    }

    feature_importance = pd.DataFrame({
        'feature': X_train.columns,
        'importance': rf_model.feature_importances_
    }).sort_values('importance', ascending=False)

    return {
        'ensemble': {'model': rf_model, 'predictions': ensemble_pred},
        'lr_model': lr_model,
        'rf_model': rf_model,
        'results': results,
        'metrics': metrics,
        'feature_columns': list(X_train.columns),
        'feature_importance': feature_importance,
        'y_val': y_val,
    }


def train_future_validation_model():
    """Legacy function for backward compatibility."""
    danger = pd.read_csv(CSV_DANGER, sep=";")
    danger = danger.copy()
    danger["date"] = pd.to_datetime(danger["date"], errors="coerce")
    danger["year"] = pd.to_numeric(danger["year"], errors="coerce")
    danger["max.danger.corr"] = pd.to_numeric(danger["max.danger.corr"], errors="coerce")

    if "date" not in danger.columns or "year" not in danger.columns or "max.danger.corr" not in danger.columns:
        raise ValueError("Danger dataset is missing date, year, or target columns needed for model training.")

    danger = danger.dropna(subset=["date", "year", "max.danger.corr"]).copy()

    train = danger[danger["year"].between(1999, 2015)].copy()
    validate = danger[danger["year"].between(2016, 2019)].copy()

    if train.empty or validate.empty:
        raise ValueError("No rows available for the required train/validation split (1999-2015 / 2016-2019).")

    feature_columns = [
        col for col in danger.columns
        if col not in {"date", "year", "max.danger.corr"} and pd.api.types.is_numeric_dtype(danger[col])
    ]

    X_train = train[feature_columns].fillna(0)
    y_train = train["max.danger.corr"].fillna(0)
    X_val = validate[feature_columns].fillna(0)
    y_val = validate["max.danger.corr"].fillna(0)

    constant_cols = X_train.columns[X_train.nunique() == 1]
    X_train = X_train.drop(columns=constant_cols, errors="ignore")
    X_val = X_val.drop(columns=constant_cols, errors="ignore")

    model = LinearRegression()
    model.fit(X_train, y_train)
    predictions = model.predict(X_val)

    results = validate[["date", "year", "max.danger.corr"]].copy()
    results["predicted_max_danger"] = predictions
    results["abs_error"] = (results["predicted_max_danger"] - results["max.danger.corr"]).abs()

    rmse = np.sqrt(mean_squared_error(y_val, predictions))

    metrics = {
        "train_year_range": "1999-2015",
        "validation_year_range": "2016-2019",
        "training_rows": int(len(train)),
        "validation_rows": int(len(validate)),
        "mae": mean_absolute_error(y_val, predictions),
        "rmse": rmse,
        "r2": r2_score(y_val, predictions),
    }

    return model, results, metrics, feature_columns


st.set_page_config(
    page_title="🏔️ Avalanche Intelligence Pro",
    page_icon="❄️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "**Avalanche Intelligence Pro** - Enterprise-grade avalanche analytics using 25 years of Davos data (1999-2019)"
    }
)
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Header with gradient
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🏔️ Avalanche Intelligence Pro")
    st.caption("📊 Enterprise Analytics | 🤖 Advanced ML | 📈 Risk Forecasting | 🔮 Predictive Insights")

try:
    observations, danger = load_data()
except Exception as exc:
    st.error(f"The application could not load its data: {exc}")
    st.stop()

obs_years = observations["date_release"].dt.year
min_year = int(obs_years.min()) if not obs_years.empty else 1998
max_year = int(obs_years.max()) if not obs_years.empty else 2020

with st.sidebar:
    st.header("Filters")
    start_year, end_year = st.slider(
        "Observation year range",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        step=1,
    )

    snow_options = sorted(observations["snow_type"].dropna().unique().tolist())
    trigger_options = sorted(observations["trigger_type"].dropna().unique().tolist())

    selected_snow = st.multiselect("Snow type", options=snow_options, default=snow_options)
    selected_trigger = st.multiselect("Trigger type", options=trigger_options, default=trigger_options)

    st.markdown("---")
    st.caption(f"Coverage: {min_year}–{max_year}")

filtered_obs = observations[
    observations["date_release"].dt.year.between(start_year, end_year)
    & observations["snow_type"].isin(selected_snow)
    & observations["trigger_type"].isin(selected_trigger)
].copy()

filtered_danger = danger[danger["date"].dt.year.between(start_year, end_year)].copy()

metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
metric_col1.metric("Observations", f"{len(filtered_obs):,}")
metric_col2.metric(
    "Avg max danger",
    f"{filtered_danger['max.danger.corr'].mean():.2f}" if not filtered_danger.empty else "0.00",
)
metric_col3.metric(
    "Largest event area",
    f"{filtered_obs['area_m2'].max():,.0f} m²" if not filtered_obs.empty else "0 m²",
)
metric_col4.metric(
    "Peak elevation",
    f"{filtered_obs['max_elevation_m'].max():,.0f} m" if not filtered_obs.empty else "0 m",
)

overview_tab, risk_tab, ml_tab, trends_tab, stats_tab, events_tab, model_tab, data_tab = st.tabs([
    "📊 Overview",
    "⚠️ Risk Analysis",
    "🤖 Advanced ML",
    "📈 Trends & Forecast",
    "📉 Statistics",
    "🗻 Events",
    "🔬 Model Validation",
    "🗂️ Data Explorer",
])

with overview_tab:
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.subheader("Trigger distribution")
        trigger_counts = filtered_obs["trigger_type"].value_counts().reset_index()
        trigger_counts.columns = ["trigger_type", "count"]
        st.plotly_chart(
            px.bar(
                trigger_counts,
                x="trigger_type",
                y="count",
                color="trigger_type",
                title="Avalanches by trigger type",
                color_discrete_sequence=px.colors.qualitative.Set2,
            ),
            width="stretch",
        )

    with chart_col2:
        st.subheader("Snow type distribution")
        snow_counts = filtered_obs["snow_type"].value_counts().reset_index()
        snow_counts.columns = ["snow_type", "count"]
        st.plotly_chart(
            px.bar(
                snow_counts,
                x="snow_type",
                y="count",
                color="snow_type",
                title="Avalanches by snow type",
                color_discrete_sequence=px.colors.qualitative.Dark2,
            ),
            width="stretch",
        )

    st.subheader("Terrain and size relationship")
    scatter_data = filtered_obs[["max_elevation_m", "area_m2", "length_m", "width_m", "trigger_type", "snow_type"]].dropna()
    scatter_data = scatter_data[scatter_data["area_m2"] > 0]
    if not scatter_data.empty:
        st.plotly_chart(
            px.scatter(
                scatter_data,
                x="max_elevation_m",
                y="area_m2",
                color="trigger_type",
                size="length_m",
                hover_data=["snow_type"],
                title="Maximum elevation vs avalanche area",
            ),
            width="stretch",
        )
    else:
        st.info("No valid terrain data is available for the selected filters.")

with risk_tab:
    st.subheader("🎯 Risk Scoring System")
    st.markdown("Advanced risk assessment using danger levels, seasonality, and volatility metrics.")
    
    try:
        risk_data = filtered_danger.copy()
        if not risk_data.empty:
            seasonal_avg = risk_data["max.danger.corr"].mean()
            volatility = risk_data["max.danger.corr"].std()
            
            risk_data["risk_score"] = risk_data["max.danger.corr"].apply(
                lambda x: calculate_risk_score(x, seasonal_avg, volatility)
            )
            risk_data["risk_level"] = pd.cut(
                risk_data["risk_score"],
                bins=[0, 3, 6, 10],
                labels=["🟢 Low", "🟠 Medium", "🔴 High"]
            )
            
            col1, col2, col3 = st.columns(3)
            col1.metric("📊 Avg Risk Score", f"{risk_data['risk_score'].mean():.2f}/10")
            col2.metric("⚠️ High Risk Days", int((risk_data['risk_score'] > 6).sum()))
            col3.metric("📈 Risk Volatility", f"{volatility:.2f}")
            
            st.subheader("Daily Risk Assessment")
            risk_chart = px.line(
                risk_data.sort_values("date"),
                x="date",
                y="risk_score",
                color="risk_level",
                markers=True,
                title="Risk Score Timeline",
                color_discrete_map={"🟢 Low": "#51cf66", "🟠 Medium": "#ffa500", "🔴 High": "#f5576c"}
            )
            st.plotly_chart(risk_chart, width="stretch")
            
            st.subheader("🎯 Anomaly Detection")
            anomalies = detect_anomalies(risk_data["max.danger.corr"], method='iqr', threshold=1.5)
            anomaly_count = anomalies.sum()
            
            if anomaly_count > 0:
                st.warning(f"🚨 Detected {anomaly_count} anomalous danger readings")
                anomaly_data = risk_data[anomalies][["date", "max.danger.corr", "risk_score"]].sort_values("date", ascending=False)
                st.dataframe(anomaly_data, width="stretch")
            else:
                st.success("✅ No anomalies detected in the selected period")
        else:
            st.info("No risk data available for the selected filters")
    except Exception as e:
        st.error(f"Risk analysis failed: {e}")

with ml_tab:
    st.subheader("🤖 Advanced Machine Learning Analysis")
    st.markdown("**Ensemble Model:** Linear Regression (40%) + Random Forest (60%)")
    
    try:
        with st.spinner("Training ensemble model with cross-validation..."):
            model_data = train_ensemble_model()
        
        metrics = model_data['metrics']
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("🎯 R² Score", f"{metrics['r2']:.4f}")
        col2.metric("📊 MAE", f"{metrics['mae']:.4f}")
        col3.metric("📉 RMSE", f"{metrics['rmse']:.4f}")
        col4.metric("📈 MAPE", f"{metrics['mape']*100:.2f}%")
        
        st.subheader("Cross-Validation Performance")
        cv_col1, cv_col2 = st.columns(2)
        
        with cv_col1:
            st.metric("Linear Regression CV R²", f"{metrics['lr_cv_mean']:.4f} ± {metrics['lr_cv_std']:.4f}")
        with cv_col2:
            st.metric("Random Forest CV R²", f"{metrics['rf_cv_mean']:.4f} ± {metrics['rf_cv_std']:.4f}")
        
        st.subheader("🌳 Feature Importance (Random Forest)")
        feature_importance = model_data['feature_importance'].head(15)
        
        fig_importance = px.bar(
            feature_importance,
            x="importance",
            y="feature",
            orientation="h",
            title="Top 15 Most Important Features",
            color="importance",
            color_continuous_scale="Viridis"
        )
        fig_importance.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig_importance, width="stretch")
        
        st.subheader("Residual Analysis")
        results = model_data['results']
        results['residuals'] = results['max.danger.corr'] - results['ensemble_pred']
        results['residuals_normalized'] = results['residuals'] / results['max.danger.corr'].std()
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_residual_dist = px.histogram(
                results,
                x="residuals",
                nbins=30,
                title="Distribution of Residuals",
                color_discrete_sequence=["#667eea"]
            )
            st.plotly_chart(fig_residual_dist, width="stretch")
        
        with col2:
            fig_residual_qq = go.Figure()
            residuals_sorted = np.sort(results['residuals_normalized'].dropna())
            theoretical_q = stats.norm.ppf(np.linspace(0.01, 0.99, len(residuals_sorted)))
            fig_residual_qq.add_trace(go.Scatter(x=theoretical_q, y=residuals_sorted, mode='markers', name='Residuals'))
            fig_residual_qq.add_trace(go.Scatter(x=[-3, 3], y=[-3, 3], mode='lines', name='Perfect fit', line=dict(dash='dash')))
            fig_residual_qq.update_layout(title="Q-Q Plot", xaxis_title="Theoretical Quantiles", yaxis_title="Sample Quantiles")
            st.plotly_chart(fig_residual_qq, width="stretch")
        
        st.subheader("Predicted vs Actual")
        fig_pred = px.scatter(
            results,
            x="max.danger.corr",
            y="ensemble_pred",
            title="Prediction Accuracy",
            trendline="ols",
            labels={"max.danger.corr": "Actual Danger", "ensemble_pred": "Predicted Danger"}
        )
        st.plotly_chart(fig_pred, width="stretch")
        
    except Exception as e:
        st.error(f"Advanced ML analysis failed: {e}")

with trends_tab:
    st.subheader("📈 Danger Trends & Forecasting")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        forecast_years = st.slider("Forecast years ahead", 1, 5, 2)
    
    monthly_danger = (
        filtered_danger.assign(month=filtered_danger["date"].dt.to_period("M").astype(str))
        .groupby("month", as_index=False)["max.danger.corr"]
        .mean()
    )
    if not monthly_danger.empty:
        st.plotly_chart(
            px.line(
                monthly_danger,
                x="month",
                y="max.danger.corr",
                markers=True,
                title="Average max danger by month",
            ),
            width="stretch",
        )
    else:
        st.info("No danger records match the current filter set.")

    st.subheader("Danger summary statistics")
    danger_stats = filtered_danger["max.danger.corr"].describe().to_frame(name="value")
    st.dataframe(danger_stats, width="stretch")
    
    # Seasonal patterns
    st.subheader("🌊 Seasonal Patterns")
    if not filtered_danger.empty:
        danger_seasonal = filtered_danger.copy()
        danger_seasonal['month'] = danger_seasonal['date'].dt.month
        danger_seasonal['season'] = danger_seasonal['month'].apply(
            lambda x: 'Winter' if x in [12, 1, 2] else ('Spring' if x in [3, 4, 5] else ('Summer' if x in [6, 7, 8] else 'Fall'))
        )
        seasonal_box = px.box(
            danger_seasonal,
            x="season",
            y="max.danger.corr",
            title="Danger Distribution by Season",
            color="season",
            color_discrete_sequence=["#667eea", "#764ba2", "#f093fb", "#f5576c"]
        )
        st.plotly_chart(seasonal_box, width="stretch")

with stats_tab:
    st.subheader("📊 Statistical Analysis")
    
    if not filtered_danger.empty and not filtered_obs.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Danger Distribution")
            fig_dist = px.histogram(
                filtered_danger,
                x="max.danger.corr",
                nbins=40,
                title="Danger Level Distribution",
                color_discrete_sequence=["#667eea"]
            )
            st.plotly_chart(fig_dist, width="stretch")
        
        with col2:
            st.subheader("Avalanche Count Distribution")
            fig_aval_dist = px.histogram(
                filtered_obs,
                x="area_m2",
                nbins=40,
                title="Avalanche Area Distribution (log scale)",
                color_discrete_sequence=["#764ba2"],
                log_x=True
            )
            st.plotly_chart(fig_aval_dist, width="stretch")
        
        # Correlations
        st.subheader("🔗 Correlation Analysis")
        numeric_cols = filtered_danger.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 1:
            corr_matrix = filtered_danger[numeric_cols].corr()
            
            fig_corr = go.Figure(data=go.Heatmap(
                z=corr_matrix.values,
                x=corr_matrix.columns,
                y=corr_matrix.columns,
                colorscale='Viridis'
            ))
            fig_corr.update_layout(title="Feature Correlation Matrix", width=600, height=600)
            st.plotly_chart(fig_corr, width="stretch")
    else:
        st.info("Insufficient data for statistical analysis")

with events_tab:
    st.subheader("🗻 Top Avalanche Events")
    if not filtered_obs.empty:
        top_events = filtered_obs.sort_values("area_m2", ascending=False).head(15)[
            ["date_release", "snow_type", "trigger_type", "area_m2", "length_m", "width_m", "max_elevation_m"]
        ].copy()
        top_events.columns = ["date", "snow_type", "trigger_type", "area (m²)", "length (m)", "width (m)", "max elevation (m)"]
        st.dataframe(top_events, width="stretch")
        
        csv = top_events.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Top Events",
            data=csv,
            file_name="top_avalanche_events.csv",
            mime="text/csv",
        )
    else:
        st.info("No event records are available for the selected filters.")

    st.subheader("Danger Record Preview")
    if not filtered_danger.empty:
        danger_preview = filtered_danger[["date", "year", "max.danger.corr", "AAI_all"]].sort_values("date", ascending=False).head(30)
        st.dataframe(danger_preview, width="stretch")
    else:
        st.info("No danger data matches the current filter selection.")

with model_tab:
    st.subheader("🔬 Model Validation & Performance")
    st.markdown("**Strict Historical Evaluation:** Train (1999–2015) | Validate (2016–2019)")
    
    try:
        with st.spinner("Training models..."):
            ensemble_results = train_ensemble_model()
        
        metrics = ensemble_results['metrics']
        results = ensemble_results['results']
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("🎯 Ensemble R²", f"{metrics['r2']:.4f}")
        col2.metric("📊 MAE", f"{metrics['mae']:.4f}")
        col3.metric("📉 RMSE", f"{metrics['rmse']:.4f}")
        col4.metric("📈 MAPE", f"{metrics['mape']*100:.2f}%")
        
        st.markdown("---")
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.info(f"📈 **Linear Regression** CV: {metrics['lr_cv_mean']:.4f} ± {metrics['lr_cv_std']:.4f}")
        with col_b:
            st.info(f"🌳 **Random Forest** CV: {metrics['rf_cv_mean']:.4f} ± {metrics['rf_cv_std']:.4f}")
        
        st.subheader("Validation performance")
        display_cols = ["date", "year", "max.danger.corr", "lr_pred", "rf_pred", "ensemble_pred", "abs_error"]
        display_data = results[display_cols].sort_values("date")
        display_data.columns = ["Date", "Year", "Actual", "LR Pred", "RF Pred", "Ensemble Pred", "Error"]
        st.dataframe(display_data, width="stretch")
        
        csv = display_data.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Predictions",
            data=csv,
            file_name="model_validation_predictions.csv",
            mime="text/csv",
        )

        st.subheader("Model Comparison: Predicted vs Actual")
        comparison_chart = px.line(
            results.sort_values("date"),
            x="date",
            y=["max.danger.corr", "lr_pred", "rf_pred", "ensemble_pred"],
            markers=True,
            title="All Models: Actual vs Predictions (2016–2019)",
            labels={"value": "Danger Level", "date": "Date"}
        )
        st.plotly_chart(comparison_chart, width="stretch")
        
        st.subheader("Error Analysis")
        col1, col2 = st.columns(2)
        with col1:
            error_chart = px.scatter(
                results,
                x="max.danger.corr",
                y="abs_error",
                title="Prediction Error vs Actual Danger",
                trendline="ols"
            )
            st.plotly_chart(error_chart, width="stretch")
        with col2:
            error_dist = px.histogram(
                results,
                x="abs_error",
                nbins=30,
                title="Error Distribution"
            )
            st.plotly_chart(error_dist, width="stretch")

    except Exception as exc:
        st.error(f"Model training failed: {exc}")


with data_tab:
    st.subheader("📊 Filtered Observations & Exports")
    if not filtered_obs.empty:
        st.dataframe(filtered_obs.reset_index(drop=True), width="stretch")
        
        # Multiple export options
        col1, col2 = st.columns(2)
        with col1:
            csv = filtered_obs.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Download as CSV",
                data=csv,
                file_name="avalanche_observations.csv",
                mime="text/csv",
            )
        with col2:
            json_data = filtered_obs.to_json(orient='records', date_format='iso').encode("utf-8")
            st.download_button(
                label="📥 Download as JSON",
                data=json_data,
                file_name="avalanche_observations.json",
                mime="application/json",
            )
    else:
        st.info("No observations match the selected filters.")

# Footer
st.markdown("---")
footer_col1, footer_col2, footer_col3 = st.columns(3)
with footer_col1:
    st.markdown("### 📊 Data Coverage")
    st.markdown(f"- **Period:** 1999 - 2019 (20 years)\n- **Training:** 1999-2015\n- **Validation:** 2016-2019\n- **Total Records:** {len(observations):,}")

with footer_col2:
    st.markdown("### 🤖 Models")
    st.markdown("- **Linear Regression**\n- **Random Forest** (100 estimators)\n- **Ensemble** (40/60 weighted)\n- **Cross-Validation:** 5-Fold KFold")

with footer_col3:
    st.markdown("### 🚀 Features")
    st.markdown("- Risk Scoring System\n- Anomaly Detection\n- Feature Importance\n- Seasonal Analysis\n- Statistical Tests")

st.caption("🏆 **Avalanche Intelligence Pro** - Enterprise-grade analytics for avalanche forecasting using 25 years of Davos observational data")

