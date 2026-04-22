# 🛡️ AI-Based Phishing Detection System

> **Mini Project | Dept. of CSE | Neil Gogte Institute of Technology | 2025–26**  
> Supervised machine learning system to classify URLs as **Phishing** or **Legitimate**

---

## 📌 Overview

Phishing attacks exploit fraudulent URLs to steal sensitive user information. Traditional blacklist-based approaches fail to catch new and evolving threats. This system uses supervised ML to classify URLs in real time through a structured pipeline:

```
Raw URL → Preprocessing → Feature Extraction (15 features) → ML Model → Phishing / Legitimate + Confidence %
```

**Dataset:** 549,346 labeled URLs (Kaggle — Phishing Site URLs)  
**Problem Type:** Binary Classification (Phishing = 1, Legitimate = 0)  
**Interface:** Flask-based web application (localhost)

---

## 🧠 ML Models Used

| Model | Type | Key Parameters |
|---|---|---|
| Logistic Regression | Linear Classifier | C=1.0, solver='lbfgs' |
| Random Forest | Ensemble (Bagging) | n_estimators=100 |
| Support Vector Machine | Kernel-based | kernel='rbf', C=1.0 |
| Voting Classifier | Ensemble (Soft Voting) | LR + RF + SVM |
| Stacking Classifier | Ensemble (Stacking) | Base: LR, RF, SVM — Meta: LR |

---

## ⚙️ Features Extracted (15 URL Features)

| # | Feature | Type |
|---|---|---|
| 1 | url_length | Numeric |
| 2 | num_dots | Numeric |
| 3 | num_hyphens | Numeric |
| 4 | num_slashes | Numeric |
| 5 | num_at | Binary |
| 6 | has_ip | Binary |
| 7 | has_https | Binary |
| 8 | domain_length | Numeric |
| 9 | num_subdomains | Numeric |
| 10 | digit_ratio | Float |
| 11 | special_char_count | Numeric |
| 12 | tld_length | Numeric |
| 13 | path_length | Numeric |
| 14 | num_params | Numeric |
| 15 | has_suspicious_words | Binary |

---

## 🗂️ Project Structure

```
phishing-detection/
│
├── dataset/
│   └── phishing_site_urls.csv          # Raw dataset (download from Kaggle)
│
├── src/
│   ├── preprocessing.py                # URL cleaning, label encoding
│   ├── feature_engineering.py          # 15-feature extraction logic
│   ├── models.py                       # LR, RF, SVM training
│   ├── ensemble.py                     # Voting + Stacking classifiers
│   └── evaluate.py                     # Metrics, confusion matrix, comparison
│
├── models/
│   ├── lr_model.pkl
│   ├── rf_model.pkl
│   ├── svm_model.pkl
│   ├── voting_model.pkl
│   └── stacking_model.pkl
│
├── templates/
│   ├── index.html                      # URL input form
│   ├── result.html                     # Prediction result page
│   ├── compare.html                    # Model comparison page
│   └── admin.html                      # Admin dashboard
│
├── static/                             # CSS, JS assets
├── app.py                              # Flask application entry point
├── requirements.txt
└── README.md
```

---

## 🚀 Setup and Run

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/phishing-detection.git
cd phishing-detection
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Download the Dataset
Download from [Kaggle](https://www.kaggle.com/datasets/taruntiwarihp/phishing-site-urls) and place `phishing_site_urls.csv` inside the `dataset/` folder.

### 4. Train the Models
```bash
python src/models.py
python src/ensemble.py
```
Trained `.pkl` files will be saved to the `models/` folder.

### 5. Run the Flask App
```bash
python app.py
```
Open your browser and go to: `http://127.0.0.1:5000`

---

## 📊 Evaluation Metrics

| Metric | Description |
|---|---|
| Accuracy | Overall correct predictions |
| Precision | Low false positive rate |
| Recall | Low false negative rate |
| F1-Score | Balanced precision and recall |
| ROC-AUC | Overall discriminative ability |
| Confusion Matrix | Visual TP/TN/FP/FN breakdown |

---

## 🖥️ System Requirements

| Component | Specification |
|---|---|
| OS | Windows 10/11 or Ubuntu 20.04+ |
| Python | 3.9+ |
| RAM | 4 GB minimum (8 GB recommended) |
| Storage | 2 GB free disk space |
| GPU | Not required |

---

## 📦 requirements.txt (Key Libraries)

```
flask
scikit-learn
pandas
numpy
matplotlib
seaborn
imbalanced-learn
joblib
```

---

## 🔮 Future Enhancements

- LSTM/CNN-based sequence analysis of URLs
- WHOIS domain age and DNS lookup features
- Browser extension for real-time detection
- Periodic retraining with PhishTank live feed

---

## 📄 References

1. [Kaggle – Phishing Site URLs Dataset](https://www.kaggle.com/datasets/taruntiwarihp/phishing-site-urls)
2. [Scikit-learn Documentation](https://scikit-learn.org/stable/)
3. [Flask Documentation](https://flask.palletsprojects.com/)
4. [UCI Phishing Websites Dataset](https://archive.ics.uci.edu/dataset/327/phishing+websites)

---

> **Disclaimer:** This system is an academic prototype. It is not intended for production deployment and has not been hardened for internet-facing use.
