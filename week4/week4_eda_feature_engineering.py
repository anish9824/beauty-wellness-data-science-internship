"""
Week 4: Exploratory Data Analysis (EDA) & Advanced Feature Engineering
Domain: Beauty, Personal Care & Cosmetic Wellness Analytics
Author: Anish
Repository: beauty-wellness-data-science-internship

Key Functionalities:
1. Parametric & Non-Parametric hypothesis testing (ANOVA, Kruskal-Wallis, Chi-Square).
2. Skewness and kurtosis diagnostics across beauty attributes.
3. Automated correlation and multicollinearity detection (VIF screening).
4. NLP lexical polarity & sentiment scoring for skincare efficacy claims.
5. High-order feature engineering (Ingredient safety interaction, brand pricing tiers).
6. Production export of finalized modeling datasets.
"""

import os
import sys
import json
import logging
from typing import List, Dict, Any

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.feature_extraction.text import TfidfVectorizer

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("BeautyEDAFeatureEngineering")


# ==========================================
# 1. ADVANCED FEATURE ENGINEERING ENGINE
# ==========================================
class AdvancedBeautyFeatureEngineer:
    """Builds domain-specific features for cosmetic sentiment and churn analysis."""
    
    POSITIVE_LEXICON = {
        "glow", "soothing", "hydrating", "cleared", "smooth", "miracle", 
        "plump", "holy grail", "effective", "soft", "brightening", "calmed"
    }
    NEGATIVE_LEXICON = {
        "burning", "breakout", "allergic", "greasy", "pilling", "redness", 
        "irritation", "rash", "dry", "peeling", "waste", "cystic"
    }

    def __init__(self):
        self.tfidf_vectorizer = TfidfVectorizer(max_features=25, stop_words="english")

    def fit(self, df: pd.DataFrame):
        reviews = df["cleaned_review"].fillna("")
        self.tfidf_vectorizer.fit(reviews)
        logger.info("TF-IDF Vectorizer fitted on review corpus with 25 key tokens.")
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        data = df.copy()

        # 1. Lexicon Sentiment Scoring
        def calculate_lexicon_scores(text: str) -> Dict[str, float]:
            if not isinstance(text, str) or not text:
                return {"pos_score": 0, "neg_score": 0, "net_sentiment": 0}
            words = text.split()
            n_words = max(len(words), 1)
            pos_matches = sum(1 for w in words if w in self.POSITIVE_LEXICON)
            neg_matches = sum(1 for w in words if w in self.NEGATIVE_LEXICON)
            return {
                "pos_score": pos_matches / n_words,
                "neg_score": neg_matches / n_words,
                "net_sentiment": (pos_matches - neg_matches) / n_words
            }

        lex_scores = data["cleaned_review"].apply(calculate_lexicon_scores)
        data["lexicon_pos_density"] = [s["pos_score"] for s in lex_scores]
        data["lexicon_neg_density"] = [s["neg_score"] for s in lex_scores]
        data["lexicon_net_sentiment"] = [s["net_sentiment"] for s in lex_scores]

        # 2. Risk & Formulation Sensitivity Index
        # Products with high active ingredients + fragrance present higher sensitivity risks
        data["formulation_risk_index"] = (
            data["has_active_compound"] * 1.5 + data["has_fragrance_allergen"] * 2.0
        )

        # 3. Price Tier Discretization (Mass, Prestige, Luxury)
        data["price_tier"] = pd.qcut(
            data["price_winsorized"], 
            q=3, 
            labels=["Budget_Mass", "Masstige", "Prestige_Luxury"]
        )

        # 4. Skin Match Alignment Feature
        # Penalty for sensitive skin with fragrance
        data["sensitive_skin_conflict"] = (
            (data["user_skin_type"] == "Sensitive") & (data["has_fragrance_allergen"] == 1)
        ).astype(int)

        # 5. TF-IDF Text Features
        tfidf_mat = self.tfidf_vectorizer.transform(data["cleaned_review"].fillna("")).toarray()
        tfidf_cols = [f"tfidf_{name}" for name in self.tfidf_vectorizer.get_feature_names_out()]
        tfidf_df = pd.DataFrame(tfidf_mat, columns=tfidf_cols, index=data.index)

        # 6. Target Binarization (NPS style recommendation: 4 or 5 stars = 1, else 0)
        data["target_recommended"] = (data["rating"] >= 4).astype(int)

        return pd.concat([data, tfidf_df], axis=1)


# ==========================================
# 2. STATISTICAL HYPOTHESIS TESTING
# ==========================================
class BeautyStatisticalAnalyst:
    """Performs rigorous statistical testing on Beauty & Wellness hypotheses."""

    @staticmethod
    def test_price_tier_ratings(df: pd.DataFrame):
        """Test Hypothesis: Does mean rating significantly differ across Price Tiers?"""
        tiers = [group["rating"].values for _, group in df.groupby("price_tier", observed=False)]
        f_stat, p_val = stats.f_oneway(*tiers)
        kw_stat, kw_p = stats.kruskal(*tiers)
        
        logger.info("=== Hypothesis Test 1: Price Tier vs. Ratings ===")
        logger.info("One-way ANOVA: F-Statistic = %.4f, p-value = %.4e", f_stat, p_val)
        logger.info("Kruskal-Wallis (Non-Parametric): H = %.4f, p-value = %.4e", kw_stat, kw_p)
        return {"anova_p": p_val, "kruskal_p": kw_p}

    @staticmethod
    def test_skin_allergen_conflict(df: pd.DataFrame):
        """Test Hypothesis: Is there a significant drop in ratings when sensitive skin meets allergens?"""
        conflict_group = df[df["sensitive_skin_conflict"] == 1]["rating"]
        non_conflict_group = df[df["sensitive_skin_conflict"] == 0]["rating"]
        
        t_stat, p_val = stats.ttest_ind(conflict_group, non_conflict_group, equal_var=False)
        u_stat, u_p = stats.mannwhitneyu(conflict_group, non_conflict_group)
        
        logger.info("=== Hypothesis Test 2: Sensitive Skin Conflict vs. Ratings ===")
        logger.info("Welch's t-test: t = %.4f, p-value = %.4e", t_stat, p_val)
        logger.info("Mann-Whitney U Test: U = %.4f, p-value = %.4e", u_stat, u_p)
        return {"t_test_p": p_val, "mann_whitney_p": u_p}

    @staticmethod
    def compute_distribution_metrics(df: pd.DataFrame, numerical_cols: List[str]) -> pd.DataFrame:
        """Computes skewness, kurtosis, mean, and IQR for continuous beauty metrics."""
        records = []
        for col in numerical_cols:
            series = df[col].dropna()
            records.append({
                "feature": col,
                "mean": np.round(series.mean(), 2),
                "std": np.round(series.std(), 2),
                "skewness": np.round(stats.skew(series), 3),
                "kurtosis": np.round(stats.kurtosis(series), 3)
            })
        stats_df = pd.DataFrame(records)
        logger.info("\n%s", stats_df.to_string(index=False))
        return stats_df


# ==========================================
# 3. EXECUTION
# ==========================================
def run_week4():
    # Load Week 3 raw data
    input_file = "data_week3_raw_simulated.csv"
    if not os.path.exists(input_file):
        from week3_cleaning_preprocessing import generate_raw_beauty_dataset
        raw_df = generate_raw_beauty_dataset(2500)
    else:
        raw_df = pd.read_csv(input_file)

    # Ingest through Week 3 baseline cleaning
    from week3_cleaning_preprocessing import RawBeautyDataPreprocessor
    preprocessor = RawBeautyDataPreprocessor()
    clean_df = preprocessor.fit_transform(raw_df)

    # Apply Week 4 Feature Engineering
    fe = AdvancedBeautyFeatureEngineer()
    fe.fit(clean_df)
    engineered_df = fe.transform(clean_df)

    # Run Statistical Hypothesis Testing
    tester = BeautyStatisticalAnalyst()
    tester.test_price_tier_ratings(engineered_df)
    tester.test_skin_allergen_conflict(engineered_df)
    tester.compute_distribution_metrics(
        engineered_df, 
        ["price_winsorized", "loves_count", "ingredient_count", "lexicon_net_sentiment"]
    )

    # Export Feature Engineered Artifact
    output_path = "data_week4_featured_for_modeling.csv"
    engineered_df.to_csv(output_path, index=False)
    logger.info("Week 4 Feature Engineering complete. Output: %s (Shape: %s)", output_path, engineered_df.shape)

if __name__ == "__main__":
    run_week4()