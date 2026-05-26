# 🎣 Phishing URL Detection

A machine learning web application that detects phishing URLs in real time using an ensemble of 5 trained classifiers — achieving up to **99.4% accuracy**.

---

## 📋 Project Overview

This project trains multiple ML models on a labeled dataset of phishing and benign URLs, extracts 27 hand-crafted lexical features per URL, and serves predictions through a Flask web API backed by all 5 models simultaneously.

---

## 🗂️ Project Structure

```
phishing-url-detection/
│
├── train.ipynb                  # Full training pipeline (Kaggle notebook)
├── app.py                       # Flask web application
├── utils.py                     # Feature extraction logic
│
├── preprocessed_output/
│   └── scaler.pkl             # Fitted StandardScaler
│   └── correlation_heatmap
│   └── feature_names.pkl
│   └── X_test.pkl
│   └── X_train.pkl
│   └── y_test.pkl
│   └── y_train.pkl
│
├── saved_models/
│   ├── logistic_regression.pkl
│   ├── random_forest.pkl
│   ├── xgboost.pkl
│   ├── voting_classifier.pkl
│   ├── stacking_classifier.pkl
│   └── best_model.pkl           # Alias for the best-performing model
│
└── templates/
    └── index.html               # Frontend UI
```

---

## ✨ Features

- **27 lexical URL features** extracted without external DNS or WHOIS lookups — fully offline
- **5 trained models**: Logistic Regression, Random Forest, XGBoost, Voting Classifier, Stacking Classifier
- **Consensus prediction** across all models (majority vote)
- **Per-model probability scores** returned on every request
- **SHAP explainability** (XGBoost) and feature importance plots generated during training

---

## 🤖 Models & Performance

| Model               | Accuracy | F1-Score | ROC-AUC |
|---------------------|----------|----------|---------|
| Logistic Regression | 98.66%   | 0.9708   | 0.9932  |
| Random Forest       | 99.41%   | 0.9871   | 0.9981  |
| XGBoost             | 99.38%   | 0.9866   | 0.9980  |
| Voting Classifier   | 99.39%   | 0.9868   | 0.9978  |
| Stacking Classifier | 99.36%   | 0.9863   | 0.9981  |

---

## 🔧 Feature Engineering

Features are extracted by `utils.py` and mirror the exact preprocessing from training. All 27 features are purely lexical (no network calls required):

**Lengths (5):** `url_length`, `hostname_length`, `path_length`, `query_length`, `fragment_length`

**Structural (2):** `num_subdomains`, `path_depth`

**Character counts (12):** counts of `.` `-` `_` `/` `?` `=` `@` `&` `!` `#` `%` `+`

**Composition (3):** `digit_count`, `letter_count`, `digit_letter_ratio`

**Boolean signals (5):** `has_ip`, `has_sensitive_word`, `is_shortened`, `https_in_hostname`, `uses_https`

---

## 🚀 Getting Started

### Prerequisites

```bash
pip install flask scikit-learn xgboost joblib numpy
```

### Running the App

```bash
python app.py
```

The server starts on `http://0.0.0.0:5000`. Open your browser and navigate to `http://localhost:5000`.

### Making a Prediction (API)

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"url": "http://paypal-login-verify.suspicious.com/signin"}'
```

**Example response:**

```json
{
  "url": "http://paypal-login-verify.suspicious.com/signin",
  "consensus": "Phishing",
  "phishing_votes": 5,
  "total_models": 5,
  "stacking_verdict": {
    "model": "Stacking Classifier",
    "label": "Phishing",
    "phishing_probability": 99.21,
    "safe_probability": 0.79,
    "confidence": 99.21
  },
  "results": [ ... ]
}
```

---

## 🏋️ Training the Models

Training is done in `train.ipynb`, designed to run on Kaggle with the [Phishing URLs Dataset](https://www.kaggle.com/datasets/hassaanmustafavi/phishing-urls-dataset).

**Pipeline steps:**

1. Discover and load CSV dataset
2. Clean and normalise labels (`benign=0`, `phishing=1`)
3. Extract 27 lexical features (vectorised with pandas)
4. Scale features with `StandardScaler`
5. Train 5 models (with `GridSearchCV` / `RandomizedSearchCV` for tuning)
6. Evaluate on held-out test set (F1, Precision, Recall, PR-AUC, ROC-AUC, Accuracy)
7. Generate SHAP beeswarm plot and feature importance charts
8. Export all model `.pkl` files and the scaler

---

## 📊 Training Outputs

The notebook saves the following to `preprocessed_output/` and `saved_models/`:

| File | Description |
|------|-------------|
| `scaler.pkl` | Fitted StandardScaler |
| `*.pkl` | All 5 trained model files |
| `best_model.pkl` | Alias for the highest F1 model |
| `deployment_bundle.pkl` | Model + feature names in one file |
| `feature_importance_rf_vs_xgb.png` | Side-by-side importance charts |
| `shap_beeswarm_xgboost.png` | SHAP summary plot |
| `model_metrics_comparison.png` | Bar chart comparing all models |

---

## ⚠️ Limitations

- Features are **lexical only** — a well-crafted phishing URL with no suspicious keywords or structure may evade detection.
- The `SENSITIVE_WORDS` and `SHORTENING_SERVICES` lists are static; they may need updates as new threats emerge.
- Models were trained on a specific Kaggle dataset; performance on out-of-distribution URLs may differ.

---

## 📄 License

This project is for educational purposes. Please review the dataset license on Kaggle before any commercial use.
