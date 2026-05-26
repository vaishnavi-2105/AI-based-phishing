"""
app.py — Flask web application for Phishing URL Detection
Loads all 5 trained models at startup and serves real-time predictions.
"""

import os
import warnings
import numpy as np
import joblib
from flask import Flask, request, jsonify, render_template

from utils import extract_features

# Silence sklearn version mismatch warnings (models still work fine)
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "saved_models")
PREPROC_DIR = os.path.join(BASE_DIR, "preprocessed_output")

# ── Load artefacts at startup ─────────────────────────────────────────────────
print("Loading scaler and models …", flush=True)

SCALER = joblib.load(os.path.join(PREPROC_DIR, "scaler.pkl"))

MODELS = {
    "Logistic Regression": joblib.load(
        os.path.join(MODELS_DIR, "logistic_regression.pkl")
    ),
    "Random Forest": joblib.load(
        os.path.join(MODELS_DIR, "random_forest.pkl")
    ),
    "XGBoost": joblib.load(
        os.path.join(MODELS_DIR, "xgboost.pkl")
    ),
    "Voting Classifier": joblib.load(
        os.path.join(MODELS_DIR, "voting_classifier.pkl")
    ),
    "Stacking Classifier": joblib.load(
        os.path.join(MODELS_DIR, "stacking_classifier.pkl")
    ),
}

print("All models loaded successfully.", flush=True)

# ── Static metrics from training (used for the dashboard display) ─────────────
MODEL_METRICS = {
    "Logistic Regression": {
        "f1": 0.9708, "precision": 0.9808, "recall": 0.9611,
        "pr_auc": 0.9895, "roc_auc": 0.9932, "accuracy": 0.9866,
    },
    "Random Forest": {
        "f1": 0.9871, "precision": 0.9934, "recall": 0.9810,
        "pr_auc": 0.9967, "roc_auc": 0.9981, "accuracy": 0.9941,
    },
    "XGBoost": {
        "f1": 0.9866, "precision": 0.9895, "recall": 0.9837,
        "pr_auc": 0.9965, "roc_auc": 0.9980, "accuracy": 0.9938,
    },
    "Voting Classifier": {
        "f1": 0.9868, "precision": 0.9937, "recall": 0.9799,
        "pr_auc": 0.9963, "roc_auc": 0.9978, "accuracy": 0.9939,
    },
    "Stacking Classifier": {
        "f1": 0.9863, "precision": 0.9874, "recall": 0.9851,
        "pr_auc": 0.9967, "roc_auc": 0.9981, "accuracy": 0.9936,
    },
}

# ── Flask app ─────────────────────────────────────────────────────────────────
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", metrics=MODEL_METRICS)


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True) or {}
    url = (data.get("url") or "").strip()

    if not url:
        return jsonify({"error": "No URL provided."}), 400

    # ── Feature extraction ────────────────────────────────────────────────────
    try:
        raw_features = extract_features(url)
        feature_array = np.array(raw_features).reshape(1, -1)
        scaled_features = SCALER.transform(feature_array)
    except Exception as exc:
        return jsonify({"error": f"Feature extraction failed: {exc}"}), 500

    # ── Predictions from all 5 models ─────────────────────────────────────────
    results = []
    stacking_verdict = None

    for model_name, model in MODELS.items():
        try:
            prediction = int(model.predict(scaled_features)[0])
            proba = model.predict_proba(scaled_features)[0]
            phishing_prob = float(proba[1])
            safe_prob = float(proba[0])

            result = {
                "model": model_name,
                "prediction": prediction,          # 0 = safe, 1 = phishing
                "label": "Phishing" if prediction == 1 else "Safe",
                "phishing_probability": round(phishing_prob * 100, 2),
                "safe_probability": round(safe_prob * 100, 2),
                "confidence": round(max(phishing_prob, safe_prob) * 100, 2),
            }
            results.append(result)

            if model_name == "Stacking Classifier":
                stacking_verdict = result

        except Exception as exc:
            results.append({
                "model": model_name,
                "error": str(exc),
            })

    # ── Consensus across all models ───────────────────────────────────────────
    valid = [r for r in results if "error" not in r]
    phishing_votes = sum(1 for r in valid if r["prediction"] == 1)
    consensus = "Phishing" if phishing_votes > len(valid) / 2 else "Safe"

    return jsonify({
        "url": url,
        "stacking_verdict": stacking_verdict,
        "consensus": consensus,
        "phishing_votes": phishing_votes,
        "total_models": len(valid),
        "results": results,
    })


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
