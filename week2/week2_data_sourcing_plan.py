"""
Week 2: Data Identification, Sourcing Strategy & Ingestion Pipeline
Domain: Beauty, Personal Care & Cosmetic Wellness Analytics
Author: Anish
Repository: beauty-wellness-data-science-internship

Key Functionalities:
1. Multi-source data contract definition (E-Commerce, INCI Chemical Registries, Social Sentiment).
2. Data quality scoring engine (Completeness, Uniqueness, Validity, Timeliness).
3. Realistic, stratified raw beauty dataset generator for prototype development.
4. Schema validation and missing-data diagnostic matrix generation.
5. Ingestion metadata export for downstream Week 3 cleaning pipelines.
"""

import os
import sys
import json
import logging
from typing import Dict, List, Any
from dataclasses import dataclass, asdict

import numpy as np
import pandas as pd

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("pipeline_sourcing_week2.log", mode="w")
    ]
)
logger = logging.getLogger("BeautyDataSourcing")


# =====================================================================
# 1. DATA SOURCE TAXONOMY & AUDIT CONTRACTS
# =====================================================================
@dataclass
class DataSourceEvaluation:
    source_name: str
    source_type: str
    access_protocol: str
    update_frequency: str
    reliability_tier: str
    licensing: str
    primary_entities: List[str]
    potential_limitations: List[str]

def get_data_sources_catalog() -> List[DataSourceEvaluation]:
    """Catalog of public beauty and wellness data repositories."""
    return [
        DataSourceEvaluation(
            source_name="Sephora / Ulta Public E-Commerce Dataset (Kaggle/GitHub Archive)",
            source_type="E-Commerce Catalog & Consumer Reviews",
            access_protocol="Batch CSV / REST Dump",
            update_frequency="Static Historical Snapshot (Quarterly Refresh)",
            reliability_tier="Tier 1 - Commercial Empirical",
            licensing="CC BY-NC-SA 4.0",
            primary_entities=["product_id", "brand", "price_usd", "rating", "loves_count", "ingredients", "skin_type"],
            potential_limitations=["Sparse user metadata", "Bimodal rating polarization", "Unverified purchases"]
        ),
        DataSourceEvaluation(
            source_name="CosIng (European Commission Cosmetic Ingredient Database)",
            source_type="Regulatory & Chemical Ingredient Registry",
            access_protocol="Web Scraping / XML Export",
            update_frequency="Monthly Regulatory Amendments",
            reliability_tier="Tier 1 - Governmental Standard",
            licensing="Public Sector Information (EU Open Data)",
            primary_entities=["inci_name", "cas_number", "chemical_function", "restriction_status", "allergen_flag"],
            potential_limitations=["Lacks consumer efficacy data", "Complex chemical nomenclature synonyms"]
        ),
        DataSourceEvaluation(
            source_name="Reddit Community Corpus (r/SkincareAddiction, r/AsianBeauty via Pushshift)",
            source_type="Unfiltered Social Sentiment & Efficacy Discussions",
            access_protocol="Pushshift / PRAW API",
            update_frequency="Real-time Stream",
            reliability_tier="Tier 2 - Qualitative Sentiment",
            licensing="Reddit Developer Terms",
            primary_entities=["post_id", "thread_title", "body_text", "upvote_ratio", "timestamp"],
            potential_limitations=["Noisy slang", "Self-selection bias", "Lacks demographic verification"]
        )
    ]


# =====================================================================
# 2. RAW SIMULATED DATASET GENERATOR (REALISTIC SOURCE INGESTION)
# =====================================================================
class BeautyDatasetGenerator:
    """Generates synthetic multi-source data with controlled real-world data flaws."""

    def __init__(self, random_seed: int = 42):
        self.rng = np.random.default_rng(random_seed)

    def generate_sourcing_corpus(self, n_records: int = 1800) -> pd.DataFrame:
        logger.info("Generating synthetic raw sourcing corpus (%d records)...", n_records)

        brands_and_tiers = {
            "The Ordinary": "Mass_Budget",
            "CeraVe": "Mass_Budget",
            "Inkey List": "Mass_Budget",
            "La Roche-Posay": "Masstige",
            "Paula's Choice": "Masstige",
            "Glow Recipe": "Masstige",
            "Drunk Elephant": "Prestige_Luxury",
            "Sunday Riley": "Prestige_Luxury",
            "SkinCeuticals": "Prestige_Luxury"
        }
        brand_keys = list(brands_and_tiers.keys())

        categories = ["Cleanser", "Serum", "Moisturizer", "Sunscreen", "Exfoliant", "Eye Care"]
        skin_types = ["Oily", "Dry", "Combination", "Sensitive", "Normal", None]
        skin_tones = ["Fair", "Light", "Medium", "Tan", "Deep", None]

        inci_samples = [
            "Aqua, Glycerin, Niacinamide (10%), Zinc PCA (1%), Phenoxyethanol, Chlorphenesin.",
            "Water, Ethylhexyl Methoxycinnamate, Butyl Methoxydibenzoylmethane, Parfum, CI 77891.",
            "Dimethicone, Salicylic Acid (2%), Alcohol Denat., Fragrance, Limonene, Linalool.",
            "Centella Asiatica Extract, Madecassoside, Butylene Glycol, Panthenol, Disodium EDTA.",
            "Squalane, Retinol (0.5%), Caprylic/Capric Triglyceride, BHT, Rosa Canina Seed Oil.",
            "Aqua, Ascorbic Acid (15%), Tocopherol, Ferulic Acid, Ethoxydiglycol, Triethanolamine."
        ]

        review_corpus = [
            ("Transformed my texture! My dark spots faded in 3 weeks. Repurchasing forever.", 5),
            ("Gave me severe cystic acne and allergic hives. Redness wouldn't subside for days.", 1),
            ("Average serum. Does provide hydration, but leaves a tacky residue under sunscreen.", 3),
            ("Decent product for the price. Not holy grail status, but safe for sensitive skin.", 4),
            ("Pills terribly when layered with makeup. Smells strongly like perfume.", 2),
            ("Zero noticeable results after finishing the whole bottle. Waste of money.", 1),
            ("Leaves my skin glowing, plump, and deeply hydrated. Zero breakouts!", 5)
        ]

        records = []
        for i in range(n_records):
            brand = self.rng.choice(brand_keys)
            tier = brands_and_tiers[brand]
            cat = self.rng.choice(categories)

            # Pricing distribution conditioned on brand tier
            if tier == "Mass_Budget":
                price = float(np.round(self.rng.uniform(6.0, 18.0), 2))
            elif tier == "Masstige":
                price = float(np.round(self.rng.uniform(22.0, 48.0), 2))
            else:
                price = float(np.round(self.rng.exponential(scale=45.0) + 60.0, 2))

            # Engagement counts (Negative Binomial distribution)
            loves = int(self.rng.negative_binomial(4, 0.002))
            review_count = int(max(1, loves * self.rng.uniform(0.02, 0.25)))

            # Sample review & target rating
            rev_text, base_rating = review_corpus[self.rng.integers(0, len(review_corpus))]
            rating_jitter = self.rng.choice([-1, 0, 1], p=[0.15, 0.70, 0.15])
            rating = int(np.clip(base_rating + rating_jitter, 1, 5))

            records.append({
                "product_id": f"SKU_{300000 + i}",
                "brand_name": brand,
                "brand_tier": tier,
                "product_title": f"{brand} {cat} Formula #{i+1}",
                "category": cat,
                "price_usd": price,
                "loves_count": loves,
                "review_count": review_count,
                "raw_ingredients": self.rng.choice(inci_samples),
                "user_skin_type": self.rng.choice(skin_types, p=[0.24, 0.20, 0.26, 0.16, 0.09, 0.05]),
                "user_skin_tone": self.rng.choice(skin_tones, p=[0.22, 0.25, 0.23, 0.15, 0.08, 0.07]),
                "review_content": rev_text if self.rng.random() > 0.03 else None,
                "rating": rating
            })

        df = pd.DataFrame(records)

        # Inject real-world anomalies: Missing prices & negative counts
        missing_idx = self.rng.choice(df.index, size=int(0.04 * len(df)), replace=False)
        df.loc[missing_idx, "price_usd"] = np.nan

        corrupt_reviews = self.rng.choice(df.index, size=int(0.02 * len(df)), replace=False)
        df.loc[corrupt_reviews, "review_count"] = -1

        return df


# =====================================================================
# 3. DATA QUALITY AUDIT & RELEVANCE ASSESSMENT
# =====================================================================
class DataQualityAssessor:
    """Computes multidimensional data hygiene metrics on raw sourced data."""

    @staticmethod
    def audit_dataframe(df: pd.DataFrame) -> Dict[str, Any]:
        total_rows = len(df)
        audit_results = {
            "total_records": total_rows,
            "column_metrics": {},
            "duplicate_records": int(df.duplicated(subset=["product_id"]).sum()),
            "overall_completeness_pct": float(np.round((1 - df.isna().sum().sum() / (total_rows * df.shape[1])) * 100, 2))
        }

        for col in df.columns:
            missing_count = int(df[col].isna().sum())
            unique_count = int(df[col].nunique(dropna=True))
            data_type = str(df[col].dtype)

            col_report = {
                "dtype": data_type,
                "missing_values": missing_count,
                "missing_pct": float(np.round((missing_count / total_rows) * 100, 2)),
                "cardinality": unique_count
            }

            if np.issubdtype(df[col].dtype, np.number):
                valid_num = df[col].dropna()
                col_report["min"] = float(np.round(valid_num.min(), 2)) if len(valid_num) > 0 else None
                col_report["median"] = float(np.round(valid_num.median(), 2)) if len(valid_num) > 0 else None
                col_report["max"] = float(np.round(valid_num.max(), 2)) if len(valid_num) > 0 else None

            audit_results["column_metrics"][col] = col_report

        return audit_results


# =====================================================================
# 4. INITIAL EXPLORATORY ANALYSIS BLUEPRINT
# =====================================================================
class InitialAnalysisPlanner:
    """Executes preliminary descriptive summaries aligned with Week 1 hypotheses."""

    @staticmethod
    def summarize_hypotheses_feasibility(df: pd.DataFrame):
        logger.info("Executing Hypothesis 1 & 2 Preliminary Variable Audits...")

        # Hypothesis 1: Rating by Skin Type
        skin_summary = (
            df.groupby("user_skin_type", observed=False)["rating"]
            .agg(count="count", mean_rating="mean", median_rating="median", std_dev="std")
            .reset_index()
        )
        logger.info("\n--- Preliminary Rating Distribution by Skin Type ---\n%s", skin_summary.to_string(index=False))

        # Hypothesis 2: Engagement & Price by Brand Tier
        tier_summary = (
            df.groupby("brand_tier", observed=False)
            .agg(
                product_count=("product_id", "count"),
                median_price=("price_usd", "median"),
                avg_loves=("loves_count", "mean"),
                avg_rating=("rating", "mean")
            )
            .reset_index()
        )
        logger.info("\n--- Preliminary Metrics by Brand Tier ---\n%s", tier_summary.to_string(index=False))

        return {"skin_type_audit": skin_summary.to_dict(orient="records"), "brand_tier_audit": tier_summary.to_dict(orient="records")}


# =====================================================================
# 5. MAIN EXECUTION PIPELINE
# =====================================================================
def run_week2_pipeline():
    logger.info("Starting Week 2 Data Sourcing & Audit Workflow...")

    # Step 1: Export Source Catalog
    catalog = [asdict(src) for src in get_data_sources_catalog()]
    catalog_path = "week2_data_sources_catalog.json"
    with open(catalog_path, "w") as f:
        json.dump(catalog, f, indent=4)
    logger.info("Data source catalog written to %s", catalog_path)

    # Step 2: Generate Raw Sourced Data
    generator = BeautyDatasetGenerator(random_seed=101)
    raw_df = generator.generate_sourcing_corpus(n_records=2000)
    data_path = "week2_raw_sourced_beauty_data.csv"
    raw_df.to_csv(data_path, index=False)
    logger.info("Raw sourced dataset written to %s (Shape: %s)", data_path, raw_df.shape)

    # Step 3: Run Quality Audit
    audit_results = DataQualityAssessor.audit_dataframe(raw_df)
    audit_path = "week2_data_quality_audit.json"
    with open(audit_path, "w") as f:
        json.dump(audit_results, f, indent=4)
    logger.info("Quality assessment exported to %s", audit_path)

    # Step 4: Plan Exploratory Analysis
    planner = InitialAnalysisPlanner()
    analysis_insights = planner.summarize_hypotheses_feasibility(raw_df)

    logger.info("Week 2 Execution complete. Completeness score: %.2f%%", audit_results["overall_completeness_pct"])


if __name__ == "__main__":
    run_week2_pipeline()