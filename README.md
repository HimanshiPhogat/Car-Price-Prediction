# 🚗 Car Price Prediction

An end-to-end machine learning project that predicts the **resale price of a used car** from its brand, age, mileage, fuel type, transmission, seller type and ownership history.

It covers the full ML workflow: data cleaning → feature engineering → model comparison with cross-validation → hyper-parameter tuning → evaluation → saved model → CLI prediction → **Streamlit web app**.

![Actual vs Predicted](reports/figures/actual_vs_predicted.png)

## ✨ Features

- Clean, modular code (`src/`) using scikit-learn `Pipeline` + `ColumnTransformer` (no data leakage)
- Log-transformed target (prices are right-skewed) via `TransformedTargetRegressor`
- Compares **Linear Regression, Ridge, Random Forest, Gradient Boosting** with 5-fold CV
- Optional `RandomizedSearchCV` tuning (`--tune`)
- Metrics: R², MAE, RMSE, MAPE + permutation feature importance
- Interactive **Streamlit** app and a command-line predictor
- Unit tests + GitHub Actions CI

## 📁 Project Structure

```
car-price-prediction/
├── app.py                         # Streamlit web app
├── requirements.txt
├── data/
│   ├── README.md                  # How to get the real dataset
│   └── sample_cars.csv            # Small synthetic dataset (runs out of the box)
├── src/
│   ├── config.py                  # Paths, features, constants
│   ├── data.py                    # Loading, cleaning, feature engineering
│   ├── model.py                   # Pipelines, estimators, param grids
│   ├── train.py                   # Train / compare / tune / save
│   ├── predict.py                 # Inference (CLI + importable function)
│   ├── eda.py                     # Exploratory plots
│   └── generate_synthetic_data.py # Synthetic data generator
├── tests/test_pipeline.py
├── models/                        # Saved model (generated)
├── reports/                       # metrics.json + figures (generated)
└── .github/workflows/ci.yml
```

## 🚀 Quick Start

```bash
git clone https://github.com/<your-username>/car-price-prediction.git
cd car-price-prediction

python -m venv venv
source venv/bin/activate            # Windows: venv\Scripts\activate
pip install -r requirements.txt

python -m src.eda                   # (optional) EDA figures
python -m src.train                 # train + compare models, save best
python -m src.train --tune          # (optional) with hyper-parameter tuning

streamlit run app.py                # launch the web app
```

Predict from the command line:

```bash
python -m src.predict --name "Hyundai Creta" --year 2019 --km 35000 \
    --fuel Diesel --seller Dealer --transmission Automatic --owner "First Owner"
```

Or from Python:

```python
from src.predict import predict_price
predict_price("Maruti Swift", 2018, 45000, "Petrol", "Individual", "Manual", "First Owner")
```

## 📊 Dataset

The repo ships with a **synthetic** sample (`data/sample_cars.csv`) so everything runs immediately.
For real-world results, download the
[CarDekho dataset from Kaggle](https://www.kaggle.com/datasets/nehalbirla/vehicle-dataset-from-cardekho),
save it as `data/car_data.csv`, and re-run `python -m src.train`. Details in [`data/README.md`](data/README.md).

## 🧠 Methodology

1. **Cleaning** – drop duplicates/invalid rows, clip price outliers (1st–99th percentile).
2. **Feature engineering** – `brand` from the car name, `car_age = current_year - year`.
3. **Preprocessing** – median-impute + scale numeric features; mode-impute + one-hot encode categoricals.
4. **Modelling** – compare 4 regressors on log-price with 5-fold CV; pick the best by CV R².
5. **Evaluation** – hold-out 20% test set; report R², MAE, RMSE, MAPE; permutation importance.

## 📈 Results (on the bundled synthetic sample)

| Model | CV R² | Test R² | Test MAE (₹) |
|---|---|---|---|
| Linear Regression | 0.951 | 0.965 | 47,395 |
| **Ridge** | **0.953** | **0.966** | **47,317** |
| Random Forest | 0.933 | 0.951 | 56,999 |
| Gradient Boosting | 0.932 | 0.954 | 53,685 |

> ⚠️ **Note:** the sample data is generated with a log-linear price formula, so linear models naturally win here.
> On the real CarDekho data, tree-based models (Random Forest / Gradient Boosting) usually perform best —
> run `python -m src.train --data data/car_data.csv --tune` and update this table with your own numbers.

Full metrics are saved to `reports/metrics.json`.

## 🧪 Tests

```bash
pytest -q
```

## 🔮 Future Improvements

- Add XGBoost / LightGBM / CatBoost and compare
- Extract more features from the full car name (variant, engine, power)
- Add SHAP explanations to the Streamlit app
- Dockerize and deploy (Streamlit Community Cloud / Hugging Face Spaces / Render)
- Add a FastAPI endpoint and MLflow experiment tracking

## 📄 License

MIT – see [LICENSE](LICENSE).
