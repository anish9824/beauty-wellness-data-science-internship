"""
Week 3: Production Data Cleaning & Preprocessing Pipeline
Domain: Beauty, Personal Care & Cosmetic Wellness Analytics
Author: Anish
Repository: beauty-wellness-data-science-internship

Key Functionalities:
1. Multi-source cosmetic data ingestion and validation.
2. Advanced missing value imputation (stratified domain medians & indicator flags).
3. Cosmetic ingredient (INCI) standardization, allergen flag tagging, and normalization.
4. Text sanitization for noisy customer reviews (emojis, casing, punctuation).
5. Statistical outlier identification & capping using IQR Winsorization.
6. Target-leakage-free scikit-learn transformers for scaling and encoding.
"""

import os
import re
import sys
import json
import logging
from typing import List, Tuple, Dict, Any

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, RobustScaler

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("pipeline_cleaning_week3.log", mode="w")
    ]
)
logger = logging.getLogger("BeautyPreprocessingPipeline")


# ==========================================
# 1. SYNTHETIC RAW DATASET GENERATOR
# ==========================================
def generate_raw_beauty_dataset(n_samples: int = 1500, random_seed: int = 42) -> pd.DataFrame:
    """Generates realistic e-commerce beauty data with noise, missingness, and messy strings."""
    np.random.seed(random_seed)
    
    brands = [
        "The Ordinary", "CeraVe", "La Roche-Posay", "Drunk Elephant", 
        "Glow Recipe", "Fenty Skin", "Paula's Choice", "Kiehl's", "Estee Lauder"
    ]
    categories = ["Cleanser", "Moisturizer", "Serum", "Sunscreen", "Toner", "Eye Cream"]
    skin_types = ["Oily", "Dry", "Combination", "Sensitive", "Normal", None]
    
    sample_ingredients = [
        "Aqua/Water/Eau, Niacinamide (5%), Glycerin, Zinc PCA, Phenoxyethanol, Ethylhexylglycerin.",
        "Dimethicone, Salicylic Acid (BHA), Parfum / Fragrance, Alcohol Denat., CI 19140.",
        "Water, Hyaluronic Acid, Sodium Hyaluronate, Panthenol, Disodium EDTA.",
        "Centella Asiatica Extract, Madecassoside, Butylene Glycol, 1,2-Hexanediol, Limonene.",
        "Retinol, Squalane, Caprylic/Capric Triglyceride, BHT, Simmondsia Chinensis Seed Oil."
    ]
    
    sample_reviews = [
        "Absolutely in love! Cleared my hormonal acne within 2 weeks. Must buy! ❤️✨",
        "HORRIBLE reaction. Woke up with severe redness, burning sensations and hives.",
        "Decent daily moisturizer. Feels a bit greasy under makeup, but hydrating enough.",
        "Overpriced for what it is. Does not absorb well and pilled immediately.",
        "Great staple for sensitive dry skin. No fragrance, highly recommended!",
        np.nan
    ]

    records = []
    for i in range(n_samples):
        cat = np.random.choice(categories)
        brand = np.random.choice(brands)
        base_price = 12.0 if brand in ["The Ordinary", "CeraVe"] else 55.0
        price = np.random.exponential(scale=base_price) + 4.0
        
        # Inject luxury anomalies and extreme review counts
        if np.random.rand() < 0.03:
            price = np.random.uniform(250.0, 600.0)
            
        loves = int(np.random.exponential(scale=2500) + 10)
        reviews_count = int(loves * np.random.uniform(0.05, 0.4))
        
        records.append({
            "product_id": f"SKU_{2026000 + i}",
            "brand": brand,
            "product_name": f"{brand} {cat} Solution {i+1}",
            "primary_category": cat,
            "price_usd": price,
            "loves_count": loves,
            "review_count": reviews_count,
            "user_skin_type": np.random.choice(skin_types, p=[0.25, 0.20, 0.25, 0.15, 0.10, 0.05]),
            "ingredients_raw": np.random.choice(sample_ingredients),
            "review_text": np.random.choice(sample_reviews),
            "rating": np.random.choice([1, 2, 3, 4, 5], p=[0.10, 0.08, 0.17, 0.35, 0.30])
        })
        
    df = pd.DataFrame(records)
    
    # Introduce real-world data corruption
    mask_price = np.random.rand(len(df)) < 0.06
    df.loc[mask_price, "price_usd"] = np.nan
    
    mask_reviews = np.random.rand(len(df)) < 0.04
    df.loc[mask_reviews, "review_count"] = -1  # Invalid corrupt counts
    
    logger.info("Generated synthetic raw beauty dataset: %d rows, %d columns", df.shape[0], df.shape[1])
    return df


# ==========================================
# 2. INGREDIENT & TEXT PARSING MODULES
# ==========================================
class CosmeticIngredientParser:
    """Parses raw cosmetic ingredient statements (INCI), flags sensitizers & active ingredients."""
    
    ACTIVE_ACTIVES = {
        "niacinamide", "salicylic acid", "retinol", "hyaluronic acid", 
        "glycolic acid", "lactic acid", "vitamin c", "madecassoside", "zinc pca"
    }
    
    KNOWN_ALLERGENS_FRAGRANCE = {
        "parfum", "fragrance", "limonene", "linalool", "alcohol denat", "citronellol"
    }

    @classmethod
    def clean_and_extract(cls, ingredient_str: str) -> Dict[str, Any]:
        if not isinstance(ingredient_str, str) or not ingredient_str.strip():
            return {
                "ingredient_count": 0,
                "has_active_compound": 0,
                "has_fragrance_allergen": 0,
                "clean_ingredient_tokens": []
            }
            
        # Strip parenthetical concentrations e.g., (BHA), (5%), [Water/Eau]
        cleaned = re.sub(r"\(.*?\)|\[.*?\]", "", ingredient_str.lower())
        # Split across commas, semicolons, or slashes
        tokens = [re.sub(r"[^a-z0-9\s-]", "", item).strip() for item in re.split(r"[,;/.]", cleaned)]
        tokens = [t for t in tokens if len(t) > 2]

        token_set = set(tokens)
        has_active = int(any(act in token_set or any(act in t for t in tokens) for act in cls.ACTIVE_ACTIVES))
        has_allergen = int(any(alg in token_set or any(alg in t for t in tokens) for alg in cls.KNOWN_ALLERGENS_FRAGRANCE))

        return {
            "ingredient_count": len(tokens),
            "has_active_compound": has_active,
            "has_fragrance_allergen": has_allergen,
            "clean_ingredient_tokens": tokens
        }


class BeautyTextSanitizer:
    """Normalizes and extracts signals from noisy customer reviews."""
    
    @staticmethod
    def clean_review_text(text: Any) -> str:
        if not isinstance(text, str):
            return ""
        # Remove HTML tags, emojis, and non-alphanumeric punctuation
        text = re.sub(r"<.*?>", " ", text)
        text = re.sub(r"[^\w\s]", " ", text)
        text = re.sub(r"\s+", " ", text).strip().lower()
        return text


# ==========================================
# 3. SCIKIT-LEARN COMPLIANT TRANSFORMER
# ==========================================
class RawBeautyDataPreprocessor(BaseEstimator, TransformerMixin):
    """Production-grade transformer that handles missing values, bounds outliers, and builds features."""

    def __init__(self, iqr_multiplier: float = 1.5):
        self.iqr_multiplier = iqr_multiplier
        self.category_price_medians_: Dict[str, float] = {}
        self.price_bounds_: Dict[str, float] = {}
        self.global_median_price_: float = 0.0

    def fit(self, X: pd.DataFrame, y=None):
        logger.info("Fitting RawBeautyDataPreprocessor...")
        df = X.copy()
        
        # 1. Learn category-level price medians
        valid_prices = df[df["price_usd"] > 0]
        self.global_median_price_ = float(valid_prices["price_usd"].median())
        self.category_price_medians_ = valid_prices.groupby("primary_category")["price_usd"].median().to_dict()

        # 2. Learn IQR bounds for outlier capping on prices
        q1 = valid_prices["price_usd"].quantile(0.25)
        q3 = valid_prices["price_usd"].quantile(0.75)
        iqr = q3 - q1
        self.price_bounds_ = {
            "lower": max(2.0, q1 - self.iqr_multiplier * iqr),
            "upper": q3 + self.iqr_multiplier * iqr
        }
        logger.info("Learned Price Bounds: Lower=%.2f, Upper=%.2f", self.price_bounds_["lower"], self.price_bounds_["upper"])
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        logger.info("Transforming dataset (Shape: %s)...", X.shape)
        df = X.copy()

        # --- A. Clean Inconsistent Numeric Records ---
        df.loc[df["review_count"] < 0, "review_count"] = 0
        df.loc[df["loves_count"] < 0, "loves_count"] = 0

        # --- B. Missing Value Imputation ---
        def impute_price(row):
            if pd.isna(row["price_usd"]) or row["price_usd"] <= 0:
                return self.category_price_medians_.get(row["primary_category"], self.global_median_price_)
            return row["price_usd"]

        df["price_imputed"] = df.apply(impute_price, axis=1)
        df["user_skin_type"] = df["user_skin_type"].fillna("Unknown")

        # --- C. Outlier Winsorization ---
        df["price_winsorized"] = np.clip(
            df["price_imputed"], 
            self.price_bounds_["lower"], 
            self.price_bounds_["upper"]
        )

        # --- D. Ingredient Parsing & Extraction ---
        parsed_ingredients = df["ingredients_raw"].apply(CosmeticIngredientParser.clean_and_extract)
        df["ingredient_count"] = [p["ingredient_count"] for p in parsed_ingredients]
        df["has_active_compound"] = [p["has_active_compound"] for p in parsed_ingredients]
        df["has_fragrance_allergen"] = [p["has_fragrance_allergen"] for p in parsed_ingredients]

        # --- E. Text Cleaning ---
        df["cleaned_review"] = df["review_text"].apply(BeautyTextSanitizer.clean_review_text)
        df["review_char_length"] = df["cleaned_review"].apply(len)
        df["review_word_count"] = df["cleaned_review"].apply(lambda t: len(t.split()))

        # --- F. Domain Ratio Interactions ---
        df["engagement_ratio"] = df["loves_count"] / (df["price_winsorized"] + 1.0)
        df["review_to_love_rate"] = df["review_count"] / (df["loves_count"] + 1.0)

        logger.info("Transform complete. New transformed shape: %s", df.shape)
        return df


# ==========================================
# 4. EXECUTION PIPELINE
# ==========================================
def run_pipeline():
    # 1. Ingestion
    raw_df = generate_raw_beauty_dataset(n_samples=2000, random_seed=42)
    raw_output_path = "data_week3_raw_simulated.csv"
    raw_df.to_csv(raw_output_path, index=False)
    logger.info("Saved raw simulated data to %s", raw_output_path)

    # 2. Pipeline Fit-Transform
    preprocessor = RawBeautyDataPreprocessor(iqr_multiplier=1.5)
    preprocessor.fit(raw_df)
    cleaned_df = preprocessor.transform(raw_df)

    # 3. Multi-Column Encoders & Scalers
    numeric_features = [
        "price_winsorized", "loves_count", "review_count", 
        "ingredient_count", "review_word_count", "engagement_ratio"
    ]
    categorical_features = ["primary_category", "user_skin_type"]

    col_transformer = ColumnTransformer(
        transformers=[
            ("num", RobustScaler(), numeric_features),
            ("cat", OneHotEncoder(drop="first", sparse_output=False, handle_unknown="ignore"), categorical_features)
        ],
        remainder="drop"
    )

    full_matrix = col_transformer.fit_transform(cleaned_df)
    feature_names = numeric_features + list(col_transformer.named_transformers_["cat"].get_feature_names_out(categorical_features))
    
    preprocessed_matrix_df = pd.DataFrame(full_matrix, columns=feature_names)
    preprocessed_matrix_df["target_rating"] = cleaned_df["rating"].values

    # 4. Save Processed Artifacts
    processed_output_path = "data_week3_cleaned_preprocessed.csv"
    preprocessed_matrix_df.to_csv(processed_output_path, index=False)
    logger.info("Saved fully cleaned & scaled feature matrix to %s (Shape: %s)", processed_output_path, preprocessed_matrix_df.shape)

    # Summary Report
    summary = {
        "raw_rows": int(len(raw_df)),
        "processed_rows": int(len(preprocessed_matrix_df)),
        "engineered_features_count": len(feature_names),
        "engineered_feature_columns": feature_names,
        "missing_values_after_cleaning": int(cleaned_df["price_winsorized"].isna().sum())
    }
    with open("week3_preprocessing_metadata.json", "w") as f:
        json.dump(summary, f, indent=4)
    logger.info("Metadata report successfully exported to week3_preprocessing_metadata.json")


if __name__ == "__main__":
    run_pipeline()