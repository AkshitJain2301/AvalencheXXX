"""
Avalanche Intelligence Pro - Configuration & Constants
Enterprise-grade settings for production deployment
"""

# Application Settings
APP_NAME = "Avalanche Intelligence Pro"
APP_VERSION = "2.0.0"
APP_TAGLINE = "Enterprise Analytics for Avalanche Forecasting"

# Model Configuration
MODEL_CONFIG = {
    "random_forest": {
        "n_estimators": 100,
        "max_depth": 15,
        "min_samples_split": 2,
        "min_samples_leaf": 1,
        "random_state": 42,
        "n_jobs": -1,
    },
    "cross_validation": {
        "n_splits": 5,
        "shuffle": True,
        "random_state": 42,
    },
    "ensemble_weights": {
        "linear_regression": 0.4,
        "random_forest": 0.6,
    },
}

# Data Configuration
DATA_CONFIG = {
    "train_years": (1999, 2015),
    "validation_years": (2016, 2019),
    "train_size": 17,
    "validation_size": 4,
    "total_period": 20,
}

# Risk Scoring Configuration
RISK_CONFIG = {
    "base_multiplier": 2.0,
    "seasonal_weight": 0.3,
    "volatility_weight": 0.2,
    "max_score": 10.0,
    "min_score": 0.0,
    "thresholds": {
        "low": (0, 3),
        "medium": (3, 6),
        "high": (6, 10),
    },
    "anomaly_methods": ["iqr", "zscore"],
    "iqr_threshold": 1.5,
    "zscore_threshold": 2.5,
}

# UI Configuration
UI_CONFIG = {
    "primary_color": "#667eea",
    "secondary_color": "#764ba2",
    "accent_color": "#f5576c",
    "success_color": "#51cf66",
    "warning_color": "#ffa500",
    "layout": "wide",
    "sidebar_state": "expanded",
}

# Feature Names for Display
FEATURE_CATEGORIES = {
    "Temporal": ["year", "month", "day"],
    "Atmospheric": ["pressure", "temperature", "humidity"],
    "Avalanche": ["area_m2", "length_m", "width_m", "aval_size_class"],
    "Elevation": ["max_elevation_m", "min_elevation_m"],
    "Index": ["weight_AAI", "AAI_all"],
}

# Export Formats
EXPORT_FORMATS = {
    "csv": {"extension": ".csv", "mime": "text/csv"},
    "json": {"extension": ".json", "mime": "application/json"},
}

# Deployment Settings
DEPLOYMENT = {
    "streamlit_port": 8501,
    "streamlit_headless": True,
    "logging_level": "INFO",
    "max_upload_size": 200,  # MB
    "cache_ttl": 3600,  # seconds
}

# Performance Thresholds
PERFORMANCE_THRESHOLDS = {
    "r2_acceptable": 0.20,
    "mae_warning": 0.50,
    "mape_warning": 30.0,  # percent
}

# Documentation URLs
DOCS = {
    "github": "https://github.com/avalanche-intelligence/pro",
    "readthedocs": "https://avalanche-intelligence.readthedocs.io",
    "issues": "https://github.com/avalanche-intelligence/pro/issues",
}
