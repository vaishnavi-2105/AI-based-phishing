# 🎣 PhishGuard — Phishing URL Detection

An AI-based phishing URL detection system built as a mini project for the B.E. in Computer Science and Engineering at Neil Gogte Institute of Technology, Hyderabad (2022–2026). It uses supervised machine learning with an ensemble of 5 trained classifiers on 450K+ real-world URLs — achieving up to **99.41% accuracy**.

> **Project title:** Phishing URL Detection Using Ensemble Learning: Random Forest, XGBoost, and Stacking Classifiers
---

## 📋 Project Overview

Phishing attacks are responsible for approximately 36% of all data breaches globally (IBM Security, 2023). Traditional blacklist-based defenses are reactive and brittle — a newly registered phishing domain typically operates for fewer than 24 hours before takedown, completing its attack well within that window.

This project addresses those limitations by training multiple ML models on a labeled dataset of 450,176 phishing and legitimate URLs, extracting 27 hand-crafted lexical features per URL, and serving real-time predictions through a Flask web API backed by all 5 models simultaneously. Feature extraction is performed purely on URL structure — no DNS, WHOIS, or HTTP calls required.

---

## 🗂️ Project Structure

```
phishing-url-detection/
│
├── train.ipynb                  # Full training pipeline (Kaggle notebook)
├── app.py                       # Flask web application (PhishGuard)
├── utils.py                     # Feature extraction logic
│
├── preprocessed_output/
│   ├── scaler.pkl               # Fitted StandardScaler
│   ├── correlation_heatmap
│   ├── feature_names.pkl
│   ├── X_test.pkl
│   ├── X_train.pkl
│   ├── y_test.pkl
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
- **Stacking Classifier** deployed as primary verdict model for its balanced precision-recall profile

---

## 📊 Dataset

| Property | Details |
|---|---|
| **Dataset Name** | Phishing URLs Dataset (450K+ LINKS) |
| **Source** | [Kaggle — Hassaan Mustafavi](https://www.kaggle.com/datasets/hassaanmustafavi/phishing-urls-dataset) |
| **Total Records** | 450,176 URLs |
| **Raw Features** | 2 columns: `url` (string), `type` (legitimate / phishing) |
| **Phishing Class** | 104,438 records (23.2%) |
| **Legitimate Class** | 345,738 records (76.8%) |
| **Missing Values** | None |
| **File Format** | CSV (.csv) |
| **File Size** | ~30.8 MB (uncompressed) |

Class imbalance is addressed using **SMOTE** (Synthetic Minority Over-sampling Technique) during training. All models are evaluated on a held-out test set of **90,036 URLs** not seen during training or hyperparameter tuning.

---

## 🤖 Models & Performance

All five models are evaluated on the same held-out test set. F1-Score and ROC-AUC are the primary metrics given the class imbalance in the dataset.

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC | PR-AUC |
|---|---|---|---|---|---|---|
| Logistic Regression | 98.66% | 0.9808 | 0.9611 | 0.9708 | 0.9932 | 0.9895 |
| Random Forest | **99.41%** | 0.9934 | 0.9810 | **0.9871** | 0.9981 | 0.9967 |
| XGBoost | 99.38% | 0.9895 | 0.9837 | 0.9866 | 0.9980 | 0.9965 |
| Voting Classifier | 99.39% | **0.9937** | 0.9799 | 0.9868 | 0.9978 | 0.9963 |
| Stacking Classifier | 99.36% | 0.9874 | **0.9851** | 0.9863 | **0.9981** | **0.9967** |

**Random Forest** achieves the highest accuracy and F1-Score.
**Stacking Classifier** is deployed as the primary model due to its highest recall and tied-best ROC-AUC — it catches the most actual phishing URLs while maintaining strong overall balance.

### Comparison with Prior Work

| Study | Year | Method | Best Accuracy |
|---|---|---|---|
| Mohammad et al. | 2012 | Decision Trees, 30 features | 92.4% |
| Rout et al. | 2020 | Random Forest, URL features | 96.7% |
| Chiew et al. | 2019 | Hybrid Ensemble + Feature Selection | 97.5% |
| Sahingoz et al. | 2019 | Random Forest, NLP features | 97.98% |
| Nallamala et al. | 2022 | Ensemble (Stacking) | 98.3% |
| **This work** | **2026** | **RF + XGBoost + Stacking, 27 features** | **99.41%** |

---

## 🔧 Feature Engineering

Features are extracted by `utils.py` and mirror the exact preprocessing from training. All 27 features are purely lexical (no network calls required):

**Lengths (5):** `url_length`, `hostname_length`, `path_length`, `query_length`, `fragment_length`

**Structural (2):** `num_subdomains`, `path_depth`

**Character counts (12):** counts of `.` `-` `_` `/` `?` `=` `@` `&` `!` `#` `%` `+`

**Composition (3):** `digit_count`, `letter_count`, `digit_letter_ratio`

**Boolean signals (5):** `has_ip`, `has_sensitive_word`, `is_shortened`, `https_in_hostname`, `uses_https`

### Key Insights from SHAP Analysis

SHAP (SHapley Additive exPlanations) was applied to the XGBoost model to explain individual predictions. Key findings:

- `url_length` and `hostname_length` are the most discriminative features — long URLs with long hostnames push strongly toward phishing.
- `has_ip` shows the sharpest signal: IP-based URLs are almost always phishing.
- `uses_https` confirms that legitimate sites predominantly use HTTPS (negative SHAP for HTTPS URLs).
- `count_hyphen` validates the known phishing tactic of inserting hyphens to mimic brand names.

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

1. Ingest and load the 450K+ CSV dataset
2. Clean and normalise labels (`benign=0`, `phishing=1`)
3. Apply SMOTE to address class imbalance (23.2% phishing vs 76.8% legitimate)
4. Extract 27 lexical features (vectorised with pandas)
5. Scale features with `StandardScaler`
6. Train 5 models (with `GridSearchCV` / `RandomizedSearchCV` for tuning)
7. Evaluate on held-out test set of 90,036 URLs (F1, Precision, Recall, PR-AUC, ROC-AUC, Accuracy)
8. Generate SHAP beeswarm plot (XGBoost) and feature importance charts (RF vs XGBoost)
9. Export all model `.pkl` files and the scaler

### Model Configurations

| Algorithm | Type | Key Hyperparameters |
|---|---|---|
| Logistic Regression | Linear Classifier | `C=1.0`, `solver='lbfgs'`, `max_iter=1000` |
| Random Forest | Ensemble (Bagging) | `n_estimators=100`, `max_depth=None` |
| XGBoost | Tree-based Boosting | `n_estimators=100`, `learning_rate=0.1`, `max_depth=6` |
| Voting Classifier | Soft Voting | LR + RF + XGBoost, `voting='soft'` |
| Stacking Classifier | Stacking | Base: LR, RF, XGBoost; Meta-learner: LR |

---

## 📊 Training Outputs

The notebook saves the following to `preprocessed_output/` and `saved_models/`:

| File | Description |
|---|---|
| `scaler.pkl` | Fitted StandardScaler |
| `*.pkl` | All 5 trained model files |
| `best_model.pkl` | Alias for the highest F1 model |
| `deployment_bundle.pkl` | Model + feature names in one file |
| `feature_importance_rf_vs_xgb.png` | Side-by-side importance charts |
| `shap_beeswarm_xgboost.png` | SHAP summary plot |
| `model_metrics_comparison.png` | Bar chart comparing all models |

---

## ⚠️ Limitations

- **Lexical features only:** A well-crafted phishing URL hosted on a compromised legitimate domain may evade detection — all 27 features could return values indistinguishable from legitimate traffic.
- **Dataset recency:** The training data was collected prior to 2024. Trends such as widespread HTTPS adoption by phishing sites and the use of legitimate URL shorteners for benign purposes may degrade performance on very recent URLs.
- **Class imbalance:** The dataset is 76.8% legitimate, 23.2% phishing. SMOTE is applied during training, but the original distribution means accuracy alone can be misleading — F1-Score and ROC-AUC are the primary evaluation metrics.
- **Single dataset evaluation:** All models are trained and evaluated on one dataset; cross-dataset generalization has not been tested.
- **Static feature lists:** The `SENSITIVE_WORDS` and `SHORTENING_SERVICES` lists may need updates as new threats emerge.

---

## 🔭 Future Scope

- **Deep learning:** LSTM and CNN models operating directly on raw URL character sequences, bypassing manual feature engineering.
- **Dynamic features:** WHOIS domain age, DNS record type, SSL certificate issuer, and page content similarity for detecting sophisticated phishing with no lexical anomalies.
- **Browser extension:** The Flask API can serve as the backend for a real-time in-browser phishing warning before page load.
- **Continuous retraining:** Automated pipelines ingesting fresh phishing URLs from live threat feeds (PhishTank, OpenPhish) to maintain detection effectiveness.
- **Multi-modal detection:** Combining URL analysis with page screenshot similarity and email header analysis.
- **Cross-dataset evaluation:** Testing generalization on independent datasets (UCI Phishing, ISCX-URL-2016, PhishStorm).

---

## 📄 License

This project was developed for academic purposes as a mini project at Neil Gogte Institute of Technology, Hyderabad (Dept. of CSE, 2022–2026). Please review the dataset license on Kaggle before any commercial use.
