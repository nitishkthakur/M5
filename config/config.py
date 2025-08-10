# Configuration settings for the M5 forecasting project

# Data paths
DATA_DIR = "data"
RESULTS_DIR = "results"
MODELS_DIR = "models"

# Data files
CALENDAR_FILE = "calendar.csv"
SALES_TRAIN_EVAL_FILE = "sales_train_evaluation.csv"
SALES_TRAIN_VAL_FILE = "sales_train_validation.csv"
SAMPLE_SUBMISSION_FILE = "sample_submission.csv"
SELL_PRICES_FILE = "sell_prices.csv"

# Model parameters
RANDOM_STATE = 42
TEST_SIZE = 0.2
VALIDATION_DAYS = 28  # M5 competition validation period

# Forecasting horizon
FORECAST_HORIZON = 28  # Days to forecast

# Cross-validation settings
N_SPLITS = 5
GAP = 0  # Gap between train and validation

# Optimization
N_TRIALS = 100  # For hyperparameter optimization
TIMEOUT = 3600  # Timeout in seconds for optimization

# Feature engineering
LAG_FEATURES = [1, 2, 3, 7, 14, 21, 28]
ROLLING_WINDOW_SIZES = [7, 14, 28]
ROLLING_FEATURES = ["mean", "std", "min", "max"]

# Model configurations
MODELS_CONFIG = {
    "arima": {
        "max_p": 5,
        "max_d": 2,
        "max_q": 5,
        "seasonal": True,
        "m": 7  # Weekly seasonality
    },
    "prophet": {
        "yearly_seasonality": True,
        "weekly_seasonality": True,
        "daily_seasonality": False,
        "seasonality_mode": "multiplicative"
    },
    "lightgbm": {
        "objective": "regression",
        "metric": "rmse",
        "boosting_type": "gbdt",
        "num_leaves": 31,
        "learning_rate": 0.05,
        "feature_fraction": 0.9
    }
}

# Evaluation metrics
METRICS = ["mae", "mse", "rmse", "mape", "smape"]

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
