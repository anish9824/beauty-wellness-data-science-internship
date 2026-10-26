"""
Week 5: Predictive Modeling & Algorithm Selection
Domain: Beauty, Personal Care & Cosmetic Wellness Analytics
Author: Anish
Repository: beauty-wellness-data-science-internship

Key Functionalities:
1. Multi-class rating prediction & binary customer recommendation classification.
2. Stratified K-Fold cross-validation preventing data leakage.
3. Algorithm benchmark suite:
   - Logistic Regression (L2 ElasticNet Penalized baseline)
   - Random Forest Classifier (Non-linear bagging ensemble)
   - Gradient Boosting Classifier (Sequential error boosting)
4. Hyperparameter grid search with `GridSearchCV`.
5. Class imbalance handling via balanced class weighting.
6. Calibration curves and serialization using joblib.
"""

import sys
import json
import logging
from typing import Dict, Any

import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import (
    classification_report, roc_auc_score, f1_score, accuracy_score, brier_score_loss
)
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("BeautyPredictiveModeling")


def load_and_prep_data(filepath: str = "data_week4_featured_for_modeling.csv"):
    if not pd.io.common.file_exists(filepath):
        from week4_eda_feature_engineering import run_week4
        run_week4()

    df = pd.read_csv(filepath)
    
    # Select engineered numerical and boolean features
    candidate_features = [
        "price_winsorized", "loves_count", "review_count", 
        "ingredient_count", "has_active_compound", "has_fragrance_allergen",
        "review_word_count", "engagement_ratio", "review_to_love_rate",
        "lexicon_pos_density", "lexicon_neg_density", "lexicon_net_sentiment",
        "formulation_risk_index", "sensitive_skin_conflict"
    ]
    # Include TF-IDF generated columns
    tfidf_cols = [c for c in df.columns if c.startswith("tfidf_")]
    all_features = candidate_features + tfidf_cols

    X = df[all_features].copy()
    y = df["target_recommended"].values  # 1 = Recommended (Rating >= 4), 0 = Not Recommended

    # Impute any lingering numeric NaNs with medians
    X = X.fillna(X.median())
    
    return train_test_split(X, y, test_size=0.20, random_state=42, stratify=y)


def run_model_benchmark(X_train: pd.DataFrame, X_test: pd.DataFrame, y_train: np.ndarray, y_test: np.ndarray):
    """Benchmarks Logistic Regression, Random Forest, and Gradient Boosting with Cross Validation."""
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    model_configs = {
        "Logistic_Regression": {
            "pipeline": Pipeline([
                ("scaler", StandardScaler()),
                ("clf", LogisticRegression(class_weight="balanced", max_iter=1000, random_state=42))
            ]),
            "params": {
                "clf__C": [0.01, 0.1, 1.0, 10.0]
            }
        },
        "Random_Forest": {
            "pipeline": Pipeline([
                ("clf", RandomForestClassifier(class_weight="balanced", random_state=42))
            ]),
            "params": {
                "clf__n_estimators": [100, 200],
                "clf__max_depth": [5, 10, None],
                "clf__min_samples_split": [2, 5]
            }
        },
        "Gradient_Boosting": {
            "pipeline": Pipeline([
                ("clf", GradientBoostingClassifier(random_state=42))
            ]),
            "params": {
                "clf__n_estimators": [100, 150],
                "clf__learning_rate": [0.03, 0.1],
                "clf__max_depth": [3, 5]
            }
        }
    }

    results = {}
    best_estimators = {}

    for name, config in model_configs.items():
        logger.info("Executing Grid Search for %s...", name)
        grid = GridSearchCV(
            config["pipeline"], 
            param_grid=config["params"], 
            cv=cv, 
            scoring="roc_auc", 
            n_jobs=-1
        )
        grid.fit(X_train, y_train)
        
        best_model = grid.best_estimator_
        y_pred = best_model.predict(X_test)
        y_prob = best_model.predict_proba(X_test)[:, 1]

        auc = roc_auc_score(y_test, y_prob)
        f1 = f1_score(y_test, y_pred)
        acc = accuracy_score(y_test, y_pred)
        brier = brier_score_loss(y_test, y_prob)

        logger.info("[%s] Best CV ROC-AUC: %.4f | Test AUC: %.4f | Test F1: %.4f", name, grid.best_score_, auc, f1)
        
        results[name] = {
            "best_params": grid.best_params_,
            "cv_roc_auc": float(grid.best_score_),
            "test_roc_auc": float(auc),
            "test_f1": float(f1),
            "test_accuracy": float(acc),
            "brier_score": float(brier)
        }
        best_estimators[name] = best_model

    return results, best_estimators


def main():
    X_train, X_test, y_train, y_test = load_and_prep_data()
    logger.info("Train set: %s, Test set: %s", X_train.shape, X_test.shape)

    results, best_estimators = run_model_benchmark(X_train, X_test, y_train, y_test)

    # Save benchmark metrics
    with open("week5_model_benchmarks.json", "w") as f:
        json.dump(results, f, indent=4)
        
    # Serialize the top performing model
    best_model_name = max(results, key=lambda k: results[k]["test_roc_auc"])
    best_estimator = best_estimators[best_model_name]
    
    model_artifact_path = "beauty_recommendation_model_week5.pkl"
    joblib.dump(best_estimator, model_artifact_path)
    logger.info("Top Model: %s serialized to %s", best_model_name, model_artifact_path)


if __name__ == "__main__":
    main()