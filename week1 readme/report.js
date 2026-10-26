const {
  Document,
  Packer,
  Paragraph,
  TextRun,
  Table,
  TableRow,
  TableCell,
  Header,
  Footer,
  AlignmentType,
  HeadingLevel,
  BorderStyle,
  WidthType,
  ShadingType,
  PageNumber,
  LevelFormat
} = require('docx');
const fs = require('fs');

// Border style definitions
const noBorder = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
const thinBorder = { style: BorderStyle.SINGLE, size: 4, color: "CCCCCC" };
const headerBorder = { style: BorderStyle.SINGLE, size: 4, color: "1F4E79" };

const doc = new Document({
  styles: {
    default: {
      document: {
        run: { font: "Arial", size: 22 } // 11pt
      }
    },
    paragraphStyles: [
      {
        id: "Title",
        name: "Title",
        basedOn: "Normal",
        next: "Normal",
        quickStyle: true,
        run: { font: "Arial", size: 36, bold: true, color: "1F4E79" },
        paragraph: { spacing: { before: 0, after: 200 }, alignment: AlignmentType.CENTER }
      },
      {
        id: "Heading1",
        name: "Heading 1",
        basedOn: "Normal",
        next: "Normal",
        quickStyle: true,
        run: { font: "Arial", size: 28, bold: true, color: "1F4E79" },
        paragraph: { spacing: { before: 360, after: 160 }, outlineLevel: 0 }
      },
      {
        id: "Heading2",
        name: "Heading 2",
        basedOn: "Normal",
        next: "Normal",
        quickStyle: true,
        run: { font: "Arial", size: 24, bold: true, color: "2E75B6" },
        paragraph: { spacing: { before: 280, after: 120 }, outlineLevel: 1 }
      },
      {
        id: "Heading3",
        name: "Heading 3",
        basedOn: "Normal",
        next: "Normal",
        quickStyle: true,
        run: { font: "Arial", size: 22, bold: true, color: "5B9BD5" },
        paragraph: { spacing: { before: 200, after: 100 }, outlineLevel: 2 }
      }
    ]
  },
  numbering: {
    config: [
      {
        reference: "main-bullets",
        levels: [{
          level: 0,
          format: LevelFormat.BULLET,
          text: "•",
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } }
        }]
      },
      {
        reference: "numbered-steps",
        levels: [{
          level: 0,
          format: LevelFormat.DECIMAL,
          text: "%1.",
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } }
        }]
      },
      {
        reference: "sub-bullets",
        levels: [{
          level: 0,
          format: LevelFormat.BULLET,
          text: "○",
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 1080, hanging: 360 } } }
        }]
      },
      {
        reference: "hypotheses",
        levels: [{
          level: 0,
          format: LevelFormat.DECIMAL,
          text: "H%1:",
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } }
        }]
      },
      {
        reference: "rq",
        levels: [{
          level: 0,
          format: LevelFormat.DECIMAL,
          text: "RQ%1:",
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } }
        }]
      }
    ]
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 }, // US Letter
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
      }
    },
    headers: {
      default: new Header({
        children: [
          new Paragraph({
            children: [
              new TextRun({ text: "Data Science Internship | Beauty & Wellness", italics: true, size: 18, color: "666666" })
            ],
            alignment: AlignmentType.RIGHT,
            border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "1F4E79", space: 4 } }
          })
        ]
      })
    },
    footers: {
      default: new Footer({
        children: [
          new Paragraph({
            children: [
              new TextRun({ text: "Week 1 Report  |  Page ", size: 18, color: "666666" }),
              new TextRun({ children: [PageNumber.CURRENT], size: 18, color: "666666" }),
              new TextRun({ text: " of ", size: 18, color: "666666" }),
              new TextRun({ children: [PageNumber.TOTAL_PAGES], size: 18, color: "666666" })
            ],
            alignment: AlignmentType.CENTER,
            border: { top: { style: BorderStyle.SINGLE, size: 6, color: "1F4E79", space: 4 } }
          })
        ]
      })
    },
    children: [
      // Title Page
      new Paragraph({ spacing: { before: 1200 }, children: [] }),
      new Paragraph({
        style: "Title",
        children: [new TextRun({ text: "Data Science Orientation &", size: 40, bold: true, color: "1F4E79" })]
      }),
      new Paragraph({
        style: "Title",
        children: [new TextRun({ text: "Problem Definition in", size: 40, bold: true, color: "1F4E79" })]
      }),
      new Paragraph({
        style: "Title",
        children: [new TextRun({ text: "Beauty & Wellness", size: 40, bold: true, color: "1F4E79" })]
      }),
      new Paragraph({ spacing: { before: 400 }, children: [] }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: "Week 1 Task Report", size: 28, bold: true, color: "2E75B6" })]
      }),
      new Paragraph({ spacing: { before: 600 }, children: [] }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: "Predicting and Mitigating Customer Churn", size: 24, color: "333333" })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: "in the Beauty & Wellness Industry", size: 24, color: "333333" })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 200 },
        children: [new TextRun({ text: "Through Predictive Analytics and Personalized Engagement Strategies", size: 22, italics: true, color: "555555" })]
      }),
      new Paragraph({ spacing: { before: 800 }, children: [] }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: "Data Science Internship Program", size: 20, color: "666666" })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: "October 2025", size: 20, color: "666666" })]
      }),

      // Page break
      new Paragraph({ children: [], pageBreakBefore: true }),

      // 1. Executive Summary
      new Paragraph({
        style: "Heading1",
        children: [new TextRun("1. Executive Summary")]
      }),
      new Paragraph({
        spacing: { after: 200 },
        children: [new TextRun("The global beauty and wellness industry continues to expand rapidly, with core beauty categories projected to reach approximately $590–605 billion by 2030 and the broader wellness economy valued at $6.3 trillion (growing toward $9 trillion by 2028). Despite strong overall growth, many brands and service providers face a critical challenge: high customer churn. Industry analyses indicate average retention rates as low as 20–30% in some beauty segments, with nearly half of wellness businesses reporting the loss of long-time clients in a single year.")]
      }),
      new Paragraph({
        spacing: { after: 200 },
        children: [new TextRun("This report defines a focused data science problem: developing predictive models to identify customers at high risk of churn and designing personalized engagement interventions that improve retention and lifetime value. The problem sits at the intersection of marketing insight and analytic rigor. Success requires understanding behavioral signals (purchase frequency, engagement patterns, product preferences, service history), building reliable predictive models, and translating model outputs into actionable, customer-centric strategies.")]
      }),
      new Paragraph({
        spacing: { after: 200 },
        children: [new TextRun("The chosen problem is highly relevant given the industry’s shift toward hyper-personalization, AI-driven recommendations, longevity and holistic wellness, and the rising cost of customer acquisition. By applying supervised learning techniques (classification models), exploratory analysis, and feature engineering grounded in domain knowledge, organizations can move from reactive retention tactics to proactive, data-informed relationship management.")]
      }),

      // 2. Industry Context and Trends
      new Paragraph({
        style: "Heading1",
        children: [new TextRun("2. Industry Context and Key Trends")]
      }),
      new Paragraph({
        style: "Heading2",
        children: [new TextRun("2.1 Market Size and Growth")]
      }),
      new Paragraph({
        spacing: { after: 200 },
        children: [new TextRun("Recent industry reports from McKinsey, NielsenIQ, and others confirm that beauty remains one of the most resilient consumer categories. Core segments (skincare, color cosmetics, haircare, fragrance) are expected to form a market of roughly $590–605 billion by 2025–2030, growing at approximately 4–5% annually. When adjacent categories—aesthetic injectables, beauty supplements, spa and med-spa services, and wellness offerings—are included, the total addressable opportunity expands substantially.")]
      }),
      new Paragraph({
        spacing: { after: 200 },
        children: [new TextRun("NielsenIQ’s State of Beauty 2025 noted global beauty sales growth of around 10% year-over-year in the preceding period, with online channels growing significantly faster than in-store. Asia-Pacific continues to lead growth, while North America and other markets show solid but more moderate expansion. Concurrently, the Global Wellness Institute valued the wellness economy at $6.3 trillion, underscoring the deep convergence between beauty and broader well-being.")]
      }),
      new Paragraph({
        style: "Heading2",
        children: [new TextRun("2.2 Major Industry Shifts")]
      }),
      new Paragraph({
        spacing: { after: 120 },
        children: [new TextRun({ text: "Several structural shifts are reshaping competitive dynamics:", bold: false })]
      }),
      new Paragraph({
        numbering: { reference: "main-bullets", level: 0 },
        children: [new TextRun({ text: "Hyper-personalization and AI: ", bold: true }), new TextRun("Consumers increasingly expect tailored product recommendations, skin analysis, and routines. AI-powered diagnostics, virtual try-ons, and generative recommendation engines are moving from novelty to necessity. McKinsey and others highlight agentic commerce and generative engine optimization as emerging frontiers.")]
      }),
      new Paragraph({
        numbering: { reference: "main-bullets", level: 0 },
        children: [new TextRun({ text: "Beauty–wellness convergence: ", bold: true }), new TextRun("“Beauty from within,” nutricosmetics, sleep care, longevity ecosystems, and post-procedure recovery products blur traditional category boundaries. Consumers seek integrated solutions rather than isolated products.")]
      }),
      new Paragraph({
        numbering: { reference: "main-bullets", level: 0 },
        children: [new TextRun({ text: "Longevity and preventive care: ", bold: true }), new TextRun("Anti-aging is evolving into longevity science. Brands emphasize cellular health, microbiome support, and measurable biological outcomes.")]
      }),
      new Paragraph({
        numbering: { reference: "main-bullets", level: 0 },
        children: [new TextRun({ text: "Digital and social commerce acceleration: ", bold: true }), new TextRun("TikTok Shop and similar platforms have shown explosive growth. Discovery, education, and purchase increasingly happen in social and AI-mediated environments.")]
      }),
      new Paragraph({
        numbering: { reference: "main-bullets", level: 0 },
        spacing: { after: 200 },
        children: [new TextRun({ text: "Rising acquisition costs and loyalty pressure: ", bold: true }), new TextRun("High churn rates mean that acquiring new customers is expensive. Zenoti’s 2025 Wellness Loyalty Survey found that 48% of businesses lost long-time clients, with nearly 60% of those previously considered loyal. Price sensitivity, lack of personalization, and perceived value gaps are primary drivers.")]
      }),
      new Paragraph({
        style: "Heading2",
        children: [new TextRun("2.3 The Retention Imperative")]
      }),
      new Paragraph({
        spacing: { after: 200 },
        children: [new TextRun("Research consistently shows that improving retention by even a few percentage points can substantially lift profitability. In beauty and wellness, churn often occurs at predictable windows (early after first purchase, around the natural product-replenishment cycle, or after service intervals). Behavioral signals—declining engagement, lengthening inter-purchase times, reduced open rates, support tickets, or subscription modifications—provide early warning indicators. Predictive analytics can surface these signals before the customer has fully disengaged, enabling timely, personalized interventions.")]
      }),

      // 3. Business Problem Definition
      new Paragraph({
        style: "Heading1",
        children: [new TextRun("3. Business Problem Definition")]
      }),
      new Paragraph({
        style: "Heading2",
        children: [new TextRun("3.1 Problem Statement")]
      }),
      new Paragraph({
        spacing: { after: 200 },
        children: [new TextRun({ text: "Primary Problem: ", bold: true }), new TextRun("Beauty and wellness brands and service providers experience elevated customer churn, resulting in lost lifetime value, inefficient marketing spend, and weakened competitive position. Existing retention efforts are frequently reactive, generic, or based on simple rules rather than robust predictive models that incorporate rich behavioral, transactional, and engagement data.")]
      }),
      new Paragraph({
        spacing: { after: 200 },
        children: [new TextRun("The data science opportunity is to build and validate models that accurately predict the probability of a customer churning within a defined future window (e.g., next 30, 60, or 90 days) and to link these predictions to personalized retention actions—targeted offers, routine reminders, educational content, loyalty incentives, or service recommendations—that demonstrably reduce churn and increase engagement.")]
      }),
      new Paragraph({
        style: "Heading2",
        children: [new TextRun("3.2 Business Objectives")]
      }),
      new Paragraph({
        numbering: { reference: "main-bullets", level: 0 },
        children: [new TextRun("Identify customers at elevated risk of churn with high precision and reasonable recall so that limited intervention budgets can be focused effectively.")]
      }),
      new Paragraph({
        numbering: { reference: "main-bullets", level: 0 },
        children: [new TextRun("Understand the key drivers of churn (behavioral, demographic, product/service, and engagement-related) to inform both model features and marketing strategy.")]
      }),
      new Paragraph({
        numbering: { reference: "main-bullets", level: 0 },
        children: [new TextRun("Design and prioritize personalized retention interventions that improve retention rates and customer lifetime value (CLV).")]
      }),
      new Paragraph({
        numbering: { reference: "main-bullets", level: 0 },
        children: [new TextRun("Establish a repeatable analytic pipeline that can be monitored, retrained, and refined as new data arrives and market conditions change.")]
      }),
      new Paragraph({
        numbering: { reference: "main-bullets", level: 0 },
        spacing: { after: 200 },
        children: [new TextRun("Provide clear, interpretable insights that marketing, CRM, and product teams can act upon.")]
      }),
      new Paragraph({
        style: "Heading2",
        children: [new TextRun("3.3 Scope and Boundaries")]
      }),
      new Paragraph({
        spacing: { after: 200 },
        children: [new TextRun("The problem is framed for brands or multi-location service businesses (salons, spas, med-spas, DTC beauty/wellness brands) that possess first-party transactional and engagement data. Publicly available industry data and open datasets will be used as references and proxies during the conceptual and planning phases. The eventual modeling work will focus on supervised classification of churn risk, with supporting exploratory analysis and feature engineering. Causal evaluation of interventions (e.g., A/B testing of retention campaigns) is acknowledged as a later-stage activity.")]
      }),

      // 4. Research Questions and Hypotheses
      new Paragraph({
        style: "Heading1",
        children: [new TextRun("4. Research Questions and Hypotheses")]
      }),
      new Paragraph({
        style: "Heading2",
        children: [new TextRun("4.1 Research Questions")]
      }),
      new Paragraph({
        numbering: { reference: "rq", level: 0 },
        children: [new TextRun("Which behavioral, transactional, and engagement features most strongly predict customer churn in beauty and wellness contexts within a 30–90 day horizon?")]
      }),
      new Paragraph({
        numbering: { reference: "rq", level: 0 },
        children: [new TextRun("How accurately can supervised machine learning models (logistic regression, tree-based ensembles, gradient boosting) classify customers into high-, medium-, and low-churn-risk segments using available first-party data?")]
      }),
      new Paragraph({
        numbering: { reference: "rq", level: 0 },
        children: [new TextRun("Do personalized interventions informed by model scores (e.g., product replenishment reminders, tailored loyalty offers, educational content) produce measurable improvements in retention and repurchase rates compared with generic or no intervention?")]
      }),
      new Paragraph({
        numbering: { reference: "rq", level: 0 },
        children: [new TextRun("How do churn drivers and model performance differ across customer segments (e.g., by age cohort, product category preference, service vs. product-only purchasers, acquisition channel)?")]
      }),
      new Paragraph({
        numbering: { reference: "rq", level: 0 },
        spacing: { after: 200 },
        children: [new TextRun("What is the relative contribution of early post-purchase behavior versus longer-term engagement patterns in predicting eventual churn?")]
      }),
      new Paragraph({
        style: "Heading2",
        children: [new TextRun("4.2 Hypotheses")]
      }),
      new Paragraph({
        numbering: { reference: "hypotheses", level: 0 },
        children: [new TextRun("Customers exhibiting declining purchase frequency, lengthening inter-purchase intervals, or reduced digital engagement (email opens, app sessions) within a recent window will show significantly higher churn probability than customers with stable or increasing activity.")]
      }),
      new Paragraph({
        numbering: { reference: "hypotheses", level: 0 },
        children: [new TextRun("Tree-based and gradient-boosting models will outperform simple linear models in predictive accuracy because of non-linear interactions among behavioral features common in retail and service data.")]
      }),
      new Paragraph({
        numbering: { reference: "hypotheses", level: 0 },
        children: [new TextRun("Personalized retention actions triggered by high predicted churn risk will yield higher retention rates and higher average order value among treated customers relative to a control group receiving standard communications.")]
      }),
      new Paragraph({
        numbering: { reference: "hypotheses", level: 0 },
        children: [new TextRun("Churn predictors and optimal intervention timing will vary meaningfully across segments (for example, Gen Z vs. older cohorts, skincare-focused vs. multi-category buyers, or salon-service clients vs. pure e-commerce customers).")]
      }),
      new Paragraph({
        numbering: { reference: "hypotheses", level: 0 },
        spacing: { after: 200 },
        children: [new TextRun("Early signals observable in the first 14–30 days after acquisition or last purchase will contribute substantial predictive power, enabling cost-effective early intervention.")]
      }),

      // 5. Variables and Potential Data
      new Paragraph({
        style: "Heading1",
        children: [new TextRun("5. Key Variables and Potential Data Sources")]
      }),
      new Paragraph({
        style: "Heading2",
        children: [new TextRun("5.1 Target Variable")]
      }),
      new Paragraph({
        spacing: { after: 200 },
        children: [new TextRun({ text: "Churn indicator: ", bold: true }), new TextRun("A binary (or multi-class) label defined as whether a customer makes no qualifying purchase or service visit within a specified future window (e.g., 60 or 90 days) after a reference date. Alternative continuous formulations (days until next purchase, predicted future CLV) may also be explored.")]
      }),
      new Paragraph({
        style: "Heading2",
        children: [new TextRun("5.2 Candidate Predictor Variables")]
      }),
      new Paragraph({
        spacing: { after: 120 },
        children: [new TextRun({ text: "Transactional / Behavioral", bold: true })]
      }),
      new Paragraph({
        numbering: { reference: "main-bullets", level: 0 },
        children: [new TextRun("Recency, frequency, and monetary value (RFM) metrics and their trends over time")]
      }),
      new Paragraph({
        numbering: { reference: "main-bullets", level: 0 },
        children: [new TextRun("Average order value, category mix, and product/service diversity")]
      }),
      new Paragraph({
        numbering: { reference: "main-bullets", level: 0 },
        children: [new TextRun("Inter-purchase interval statistics and deviations from individual baseline")]
      }),
      new Paragraph({
        numbering: { reference: "main-bullets", level: 0 },
        children: [new TextRun("Subscription status and modification/cancellation history (where applicable)")]
      }),
      new Paragraph({
        numbering: { reference: "main-bullets", level: 0 },
        spacing: { after: 120 },
        children: [new TextRun("Returns, complaints, or support ticket volume and recency")]
      }),
      new Paragraph({
        spacing: { after: 120 },
        children: [new TextRun({ text: "Engagement", bold: true })]
      }),
      new Paragraph({
        numbering: { reference: "main-bullets", level: 0 },
        children: [new TextRun("Email open and click rates; app session frequency and duration")]
      }),
      new Paragraph({
        numbering: { reference: "main-bullets", level: 0 },
        children: [new TextRun("Loyalty program participation and point redemption behavior")]
      }),
      new Paragraph({
        numbering: { reference: "main-bullets", level: 0 },
        spacing: { after: 120 },
        children: [new TextRun("Content consumption (tutorials, routine guides, reviews)")]
      }),
      new Paragraph({
        spacing: { after: 120 },
        children: [new TextRun({ text: "Customer Profile & Context", bold: true })]
      }),
      new Paragraph({
        numbering: { reference: "main-bullets", level: 0 },
        children: [new TextRun("Demographics (age band, location, gender where available and ethically usable)")]
      }),
      new Paragraph({
        numbering: { reference: "main-bullets", level: 0 },
        children: [new TextRun("Acquisition channel and cohort")]
      }),
      new Paragraph({
        numbering: { reference: "main-bullets", level: 0 },
        children: [new TextRun("Preferred product categories or service types (skincare, hair, wellness treatments, etc.)")]
      }),
      new Paragraph({
        numbering: { reference: "main-bullets", level: 0 },
        spacing: { after: 200 },
        children: [new TextRun("Device or channel preference (mobile app, web, in-store)")]
      }),
      new Paragraph({
        style: "Heading2",
        children: [new TextRun("5.3 Data Sources (Conceptual / Public References)")]
      }),
      new Paragraph({
        spacing: { after: 200 },
        children: [new TextRun("For this internship, modeling will initially rely on publicly available datasets and industry benchmarks as proxies, supplemented by simulated or synthetic data that mirror realistic beauty/wellness transaction and engagement patterns. Candidate public resources include:")]
      }),
      new Paragraph({
        numbering: { reference: "main-bullets", level: 0 },
        children: [new TextRun("Kaggle and similar repositories hosting retail, e-commerce, or subscription churn datasets that can be adapted or used for methodological experimentation.")]
      }),
      new Paragraph({
        numbering: { reference: "main-bullets", level: 0 },
        children: [new TextRun("Industry reports and aggregated statistics from NielsenIQ, McKinsey, Zenoti, Global Wellness Institute, and trade publications for market context and validation of assumptions.")]
      }),
      new Paragraph({
        numbering: { reference: "main-bullets", level: 0 },
        children: [new TextRun("Public APIs or open data related to consumer behavior, product reviews (e.g., beauty product review corpora), or social listening where ethically and legally permissible.")]
      }),
      new Paragraph({
        numbering: { reference: "main-bullets", level: 0 },
        spacing: { after: 200 },
        children: [new TextRun("Company-internal CRM, POS, e-commerce, and marketing automation platforms (conceptual target environment for eventual real-world deployment).")]
      }),

      // 6. Anticipated Approach
      new Paragraph({
        style: "Heading1",
        children: [new TextRun("6. Anticipated Analytic Approach")]
      }),
      new Paragraph({
        spacing: { after: 200 },
        children: [new TextRun("The planned approach follows a structured data science lifecycle tailored to the churn prediction and retention problem.")]
      }),
      new Paragraph({
        style: "Heading2",
        children: [new TextRun("6.1 Step-by-Step Outline")]
      }),
      new Paragraph({
        numbering: { reference: "numbered-steps", level: 0 },
        children: [new TextRun({ text: "Problem framing and success metrics definition. ", bold: true }), new TextRun("Finalize churn definition, prediction horizon, and business KPIs (e.g., precision at top decile, lift in retention, estimated CLV impact).")]
      }),
      new Paragraph({
        numbering: { reference: "numbered-steps", level: 0 },
        children: [new TextRun({ text: "Data sourcing and assessment. ", bold: true }), new TextRun("Identify available or proxy datasets; evaluate completeness, bias, and relevance to beauty & wellness behaviors.")]
      }),
      new Paragraph({
        numbering: { reference: "numbered-steps", level: 0 },
        children: [new TextRun({ text: "Exploratory data analysis. ", bold: true }), new TextRun("Profile distributions, missingness, correlations, and temporal patterns. Visualize RFM segments, engagement trajectories, and univariate relationships with the churn label.")]
      }),
      new Paragraph({
        numbering: { reference: "numbered-steps", level: 0 },
        children: [new TextRun({ text: "Data cleaning and preprocessing. ", bold: true }), new TextRun("Handle missing values, outliers, inconsistent formats, and create analysis-ready tables. Document all transformations for reproducibility.")]
      }),
      new Paragraph({
        numbering: { reference: "numbered-steps", level: 0 },
        children: [new TextRun({ text: "Feature engineering. ", bold: true }), new TextRun("Construct RFM-derived features, trend and velocity metrics, engagement ratios, interaction terms, and segment indicators. Explore time-window aggregations and sequence-based features where feasible.")]
      }),
      new Paragraph({
        numbering: { reference: "numbered-steps", level: 0 },
        children: [new TextRun({ text: "Model development and selection. ", bold: true }), new TextRun("Train and compare baseline (logistic regression) and advanced models (Random Forest, XGBoost/LightGBM, possibly neural nets if data volume supports). Use cross-validation and appropriate class-imbalance techniques.")]
      }),
      new Paragraph({
        numbering: { reference: "numbered-steps", level: 0 },
        children: [new TextRun({ text: "Evaluation and interpretation. ", bold: true }), new TextRun("Assess discrimination (AUC-ROC, PR-AUC), calibration, and business-oriented metrics (lift, precision@k). Use SHAP or similar methods for feature importance and local explanations.")]
      }),
      new Paragraph({
        numbering: { reference: "numbered-steps", level: 0 },
        children: [new TextRun({ text: "Intervention design linkage. ", bold: true }), new TextRun("Map risk scores and key drivers to candidate retention actions (replenishment reminders, personalized product suggestions, loyalty incentives, educational content). Outline a conceptual A/B or multi-armed bandit testing framework.")]
      }),
      new Paragraph({
        numbering: { reference: "numbered-steps", level: 0 },
        spacing: { after: 200 },
        children: [new TextRun({ text: "Documentation and iteration plan. ", bold: true }), new TextRun("Produce clear documentation of assumptions, pipeline, and limitations; define monitoring and retraining cadence.")]
      }),
      new Paragraph({
        style: "Heading2",
        children: [new TextRun("6.2 Anticipated Tools and Methods")]
      }),
      new Paragraph({
        spacing: { after: 120 },
        children: [new TextRun("Python ecosystem will be the primary environment:")]
      }),
      new Paragraph({
        numbering: { reference: "main-bullets", level: 0 },
        children: [new TextRun({ text: "Data handling: ", bold: true }), new TextRun("pandas, NumPy")]
      }),
      new Paragraph({
        numbering: { reference: "main-bullets", level: 0 },
        children: [new TextRun({ text: "Visualization: ", bold: true }), new TextRun("matplotlib, seaborn, plotly")]
      }),
      new Paragraph({
        numbering: { reference: "main-bullets", level: 0 },
        children: [new TextRun({ text: "Modeling: ", bold: true }), new TextRun("scikit-learn, XGBoost / LightGBM, potentially imbalanced-learn")]
      }),
      new Paragraph({
        numbering: { reference: "main-bullets", level: 0 },
        children: [new TextRun({ text: "Interpretation: ", bold: true }), new TextRun("SHAP, eli5, or built-in importance measures")]
      }),
      new Paragraph({
        numbering: { reference: "main-bullets", level: 0 },
        spacing: { after: 200 },
        children: [new TextRun({ text: "Workflow and reproducibility: ", bold: true }), new TextRun("Jupyter notebooks, version control, clear pipeline scripts")]
      }),
      new Paragraph({
        style: "Heading2",
        children: [new TextRun("6.3 Linkage to Marketing Insights")]
      }),
      new Paragraph({
        spacing: { after: 200 },
        children: [new TextRun("Model outputs will not remain purely technical. Risk scores and driver analyses will be translated into marketing language: which customer cohorts are most vulnerable, which behaviors signal disengagement, and which interventions are most likely to restore value. This bridges analytic rigor with practical CRM and loyalty program design—aligning with industry evidence that personalization and recognition are powerful levers for winning back or retaining clients.")]
      }),

      // 7. Relevance and Rationale
      new Paragraph({
        style: "Heading1",
        children: [new TextRun("7. Relevance and Rationale for the Chosen Problem")]
      }),
      new Paragraph({
        spacing: { after: 200 },
        children: [new TextRun("Selecting customer churn prediction and personalized retention as the focal problem is justified on multiple grounds:")]
      }),
      new Paragraph({
        numbering: { reference: "main-bullets", level: 0 },
        children: [new TextRun({ text: "Business impact: ", bold: true }), new TextRun("Retention improvements have well-documented multiplier effects on profitability. In a high-acquisition-cost environment, reducing churn is often more efficient than constant new-customer acquisition.")]
      }),
      new Paragraph({
        numbering: { reference: "main-bullets", level: 0 },
        children: [new TextRun({ text: "Data science maturity match: ", bold: true }), new TextRun("The problem is classic supervised learning with clear evaluation metrics, rich feature possibilities, and room for both simple and advanced techniques—ideal for a structured internship progression across data sourcing, cleaning, EDA, feature engineering, and modeling.")]
      }),
      new Paragraph({
        numbering: { reference: "main-bullets", level: 0 },
        children: [new TextRun({ text: "Industry alignment: ", bold: true }), new TextRun("Current trends emphasize personalization, AI, and relationship longevity. Predictive churn models directly support these priorities and can feed recommendation and loyalty systems.")]
      }),
      new Paragraph({
        numbering: { reference: "main-bullets", level: 0 },
        children: [new TextRun({ text: "Feasibility with public / proxy data: ", bold: true }), new TextRun("While proprietary CRM data would be ideal, the methodological pipeline can be developed and demonstrated using publicly available retail/churn datasets and carefully designed synthetic data that capture beauty- and wellness-relevant patterns.")]
      }),
      new Paragraph({
        numbering: { reference: "main-bullets", level: 0 },
        spacing: { after: 200 },
        children: [new TextRun({ text: "Foundation for subsequent weeks: ", bold: true }), new TextRun("The problem naturally cascades into data identification (Week 2), cleaning pipelines (Week 3), EDA and feature work (Week 4), and model selection/evaluation (Week 5).")]
      }),

      // 8. Anticipated Challenges and Mitigations
      new Paragraph({
        style: "Heading1",
        children: [new TextRun("8. Anticipated Challenges and Mitigations")]
      }),
      new Paragraph({
        numbering: { reference: "main-bullets", level: 0 },
        children: [new TextRun({ text: "Class imbalance: ", bold: true }), new TextRun("Churn rates may produce skewed labels. Mitigation: stratified sampling, class weights, SMOTE or related techniques, and focus on precision-recall metrics.")]
      }),
      new Paragraph({
        numbering: { reference: "main-bullets", level: 0 },
        children: [new TextRun({ text: "Data quality and missingness: ", bold: true }), new TextRun("Real-world transactional data often contain gaps. Mitigation: systematic missing-value analysis, domain-informed imputation or indicator variables, and robust documentation.")]
      }),
      new Paragraph({
        numbering: { reference: "main-bullets", level: 0 },
        children: [new TextRun({ text: "Concept drift: ", bold: true }), new TextRun("Consumer behavior and competitive offerings evolve. Mitigation: planned monitoring of performance metrics and periodic retraining.")]
      }),
      new Paragraph({
        numbering: { reference: "main-bullets", level: 0 },
        children: [new TextRun({ text: "Interpretability vs. complexity: ", bold: true }), new TextRun("Black-box models may be accurate but hard to action. Mitigation: emphasize explainable techniques and SHAP-style explanations alongside performance.")]
      }),
      new Paragraph({
        numbering: { reference: "main-bullets", level: 0 },
        spacing: { after: 200 },
        children: [new TextRun({ text: "Privacy and ethics: ", bold: true }), new TextRun("Personalization relies on customer data. Mitigation: adhere to privacy principles, minimize sensitive attributes, and design interventions that respect customer autonomy.")]
      }),

      // 9. Conclusion
      new Paragraph({
        style: "Heading1",
        children: [new TextRun("9. Conclusion")]
      }),
      new Paragraph({
        spacing: { after: 200 },
        children: [new TextRun("This Week 1 report establishes a clear, industry-grounded data science problem: predicting customer churn in the beauty and wellness sector and enabling personalized retention strategies. The problem is supported by current market dynamics—strong category growth, the rise of personalization and AI, and documented loyalty challenges. Research questions and hypotheses provide testable directions, while the outlined variables, data considerations, and step-by-step analytic plan create a coherent foundation for the subsequent weeks of data sourcing, cleaning, exploratory analysis, feature engineering, and predictive modeling.")]
      }),
      new Paragraph({
        spacing: { after: 200 },
        children: [new TextRun("By combining marketing insight with rigorous analytic methods, the proposed work aims to demonstrate how data science can move beauty and wellness organizations from reactive customer management toward proactive, evidence-based relationship building—ultimately supporting both business performance and more relevant, valued customer experiences.")]
      }),

      // References
      new Paragraph({
        style: "Heading1",
        children: [new TextRun("10. Selected References and Industry Sources")]
      }),
      new Paragraph({
        spacing: { after: 100 },
        children: [new TextRun({ text: "McKinsey & Company. State of Beauty and related insights on growth, personalization, and AI in beauty (2025–2026 publications).", size: 20 })]
      }),
      new Paragraph({
        spacing: { after: 100 },
        children: [new TextRun({ text: "NielsenIQ. State of Beauty 2025 – growth, digital surge, and wellness shift.", size: 20 })]
      }),
      new Paragraph({
        spacing: { after: 100 },
        children: [new TextRun({ text: "Global Wellness Institute / Global Wellness Summit. Future of Wellness trends and market valuation reports.", size: 20 })]
      }),
      new Paragraph({
        spacing: { after: 100 },
        children: [new TextRun({ text: "Zenoti. 2025 Wellness Loyalty Survey and related beauty & wellness benchmark reports on client retention and personalization.", size: 20 })]
      }),
      new Paragraph({
        spacing: { after: 100 },
        children: [new TextRun({ text: "Industry analyses on AI-driven personalization, med-spa trends, and beauty tech (BeautyMatter, Kearney, Coresight, and trade publications).", size: 20 })]
      }),
      new Paragraph({
        spacing: { after: 100 },
        children: [new TextRun({ text: "Academic and practitioner literature on customer churn modeling, RFM analysis, and retention economics in retail and subscription contexts.", size: 20 })]
      }),

      // Closing note
      new Paragraph({ spacing: { before: 400 }, children: [] }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: "— End of Week 1 Report —", italics: true, color: "666666", size: 20 })]
      })
    ]
  }]
});

Packer.toBuffer(doc).then(buffer => {
  const outputPath = "./Week1_Data_Science_Orientation_Beauty_Wellness_Report.docx";
  fs.writeFileSync(outputPath, buffer);
  console.log(`Document created successfully at ${outputPath}!`);
}).catch(err => {
  console.error("Error creating document:", err);
});