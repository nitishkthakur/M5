# M5 Forecasting Competition

A time series forecasting project using Darts, statsmodels, and other forecasting libraries for the M5 competition.

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd M5
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Data

The project contains the following data files:
- `data/calendar.csv` - Calendar information
- `data/sales_train_evaluation.csv` - Training data for evaluation
- `data/sales_train_validation.csv` - Training data for validation
- `data/sample_submission.csv` - Sample submission format
- `data/sell_prices.csv` - Price information

## Project Structure

```
M5/
├── data/                 # Data files
├── notebooks/           # Jupyter notebooks for exploration
├── src/                 # Source code
│   ├── data/           # Data processing modules
│   ├── models/         # Model implementations
│   ├── features/       # Feature engineering
│   └── utils/          # Utility functions
├── config/             # Configuration files
├── results/            # Model outputs and results
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Usage

To be updated as the project develops...

## Libraries Used

- **Darts**: Modern time series forecasting library
- **Statsmodels**: Statistical modeling and econometrics
- **PMDArima**: Auto-ARIMA implementation
- **Prophet**: Facebook's forecasting tool
- **SKTime**: Scikit-learn compatible time series library
- **XGBoost/LightGBM/CatBoost**: Gradient boosting frameworks
- **Scikit-learn**: Machine learning utilities
- **Pandas/NumPy**: Data manipulation
- **Matplotlib/Seaborn/Plotly**: Visualization

## Contributing

1. Create a feature branch
2. Make your changes
3. Add tests if applicable
4. Submit a pull request

## License

See LICENSE file for details.
