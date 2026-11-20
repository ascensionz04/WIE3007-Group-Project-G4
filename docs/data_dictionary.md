# Data Dictionary — Synthetic Malaysian SME Loan Applications

**Course:** WIE3007 Data Mining (2026/2027 Semester 1)  
**Contributor:** Member 2 — Tham Wing Shan  
**Dataset:** `data/raw/sme_loan_applications_synthetic.csv`  

**Unit of observation:** One fictitious Malaysian SME loan application.  
**Dataset size:** 1,500 records × 20 columns.  
**Prediction task:** Predict a *simulated* default within 12 months of the application.  
**Currency:** MYR (Malaysian ringgit).

> **Synthetic data only.** All businesses, amounts, narratives, review dates and outcomes are invented. The simulated default rate is **not** an observed rate for Malaysian SMEs. Do not use this dataset for real credit decisions.

## Field definitions

| Field name | Type | Description | Role |
|---|---|---|---|
| `application_id` | String | Unique fictitious identifier, `SME000001` through `SME001500`. | Identifier: exclude from model features |
| `application_date` | Date (`YYYY-MM-DD`) | Simulated loan application date, from 2024-07-01 through 2025-07-31. This is the prediction cut-off date. | Context; handle with care if modelled |
| `industry` | Categorical string | SME's operating sector, such as Retail, Logistics, or Manufacturing. | Predictor |
| `state` | Categorical string | Fictional location of the SME in Malaysia (13 represented locations). | Predictor |
| `years_in_business` | Integer | Years of business operation at the application date (1–30). | Predictor |
| `employee_count` | Integer | Employees at the application date (2–180). | Predictor |
| `annual_revenue_myr` | Float (MYR) | Estimated **gross annual sales revenue** at the application date. | Predictor |
| `profit_margin_pct` | Float (%) | Estimated business profit margin in percentage points; may be negative. | Predictor |
| `monthly_net_cash_flow_myr` | Float (MYR) | Estimated average monthly net business cash flow before the loan; may be negative. | Predictor |
| `existing_monthly_debt_payment_myr` | Float (MYR) | Monthly payments on existing debt, measured before this loan. | Predictor |
| `debt_to_revenue_ratio` | Float (0–1 range here) | **Existing monthly debt payments ÷ (`annual_revenue_myr` / 12)**, rounded to three decimal places. **This is *not* the conventional debt service coverage ratio (DSCR)**, whose denominator ordinarily uses cash flow available for debt service. Renamed from the previously ambiguous `debt_service_ratio`. | Predictor |
| `credit_score` | Integer | Fictitious creditworthiness score (360–850), measured before application. | Predictor |
| `late_payments_12m` | Integer | Count of late debt payments **in the 12 months preceding** application (0–9). | Predictor |
| `requested_loan_myr` | Float (MYR) | Amount of the new business loan requested. | Predictor |
| `loan_term_months` | Integer / discrete | Requested term: 12, 24, 36, 48 or 60 months. | Predictor |
| `collateral_available` | Categorical string | Whether the applicant indicates collateral is available (`Yes` / `No`). | Predictor |
| `loan_purpose` | Categorical string | Working Capital, Business Expansion, Equipment Purchase, Inventory Purchase, Digital Transformation, Marketing or Debt Refinancing. | Predictor |
| `owner_statement` | Free text | **Pre-application** SME owner narrative about operations, finances and the proposed use of funds. GenAI-authored language variants are selected and combined using only input attributes; no outcome label is consulted. | Text input for Member 3's LLM/SLM features |
| `customer_feedback` | Free text | **Historical, pre-application** synthetic customer-review summary. Every text contains an explicit fictional review date **7–90 days before** its row's `application_date`; no review after the application or after default is included. GenAI-authored review variants are combined using pre-application signals only. | Text input for Member 3's LLM/SLM features |
| `default_within_12m` | Binary integer | **TARGET:** `1` = generated default within 12 months after application; `0` = generated non-default. Not a real observed outcome. | Target; **never use as predictor or in LLM prompts** |

## GenAI-assisted simulation: provenance and method

**AI tool:** OpenAI ChatGPT (LLM). **Data assembly:** deterministic Python processing; the original numeric records were created with a seeded synthetic simulator (`20261119`).

1. **Numeric generation:** ChatGPT assisted with the scenario, column design, synthetic finance relationships and generator code. The simulator procedurally sampled fictitious borrower attributes and the binary target, rather than copying any real borrower dataset.
2. **LLM-authored language:** In response to an instruction to *draft realistic, varied Malaysian SME owner narratives and customer-review excerpts across industries and business conditions, without referring to a future loan outcome*, ChatGPT authored the narrative-language banks. These appear in `scripts/revise_member2_dataset.py` (`SECTOR_CONTEXT`, `OWNER_FINANCIAL`, `LOAN_PURPOSE`, `CUSTOMER_FEEDBACK` and `EXTRA_CONTEXT`).
3. **Record-level text assembly:** The script deterministically selects and combines LLM-authored passages using each record's **pre-application** industry, financing purpose and financial characteristics. A fixed seed generates distinct phrasings and a fictitious feedback date. **An LLM API was not called once for each of the 1,500 records.** This is a *hybrid LLM-written-content + procedural row-level assembly* method, not 1,500 independent LLM completions.
4. **Target independence:** The revision script does **not** read `default_within_12m` while writing either text field; its labels and numeric attributes are preserved from the original dataset. Both texts reflect only information available at or before the application cut-off.

**Example LLM-authored owner narrative fragment:** “Several invoices took longer to settle, making expense timing more important this quarter.”  
**Example LLM-authored customer-review fragment:** “Several reviewers praise the staff but want more accurate delivery estimates.”

**Reproducibility:** For a copy of this dataset, run `python scripts/revise_member2_dataset.py` from the repository root. It applies the same wording and date logic deterministically and is safe to rerun. The base numeric simulator's seed was `20261119` as well. No Python package or external API is required for the text revision.

## Pre-application timing and leakage controls

The **prediction time is `application_date`**. The following are known no later than that date: financial indicators, past repayment history, loan request information, the loan-owner statement, and earlier customer feedback. `customer_feedback` records show a fictional date 7–90 days before `application_date` inside the text itself (for example, `Customer review summary recorded 2025-05-20: ...`). These dates and review contents are fabricated for the exercise; they are not actual review records.

There are **no post-loan repayment events, future customer reviews, realised default information or target-dependent text** in the features. The row's `default_within_12m` is generated separately and is never allowed as a feature. Since simulated text and simulated outcome may share underlying pre-application risk drivers, unusually high model performance should be interpreted cautiously: it is **not** evidence of real-world lending performance.

**Avoid additional modelling leakage:** Split train/test before fitting scalers, text vectorisers, encoders, imputers, or feature-selection steps; do not include `application_id` or `default_within_12m` among inputs; do not put the target into LLM sentiment/risk-category prompts. Beware of evaluating models on duplicates of training records.

## Revision responding to GitHub peer review

| Feedback | Change |
|---|---|
| Text was overly template-based | Replaced both text fields with larger LLM-authored language banks and more varied record-specific assembly. The documentation clearly states that texts were **not** 1,500 independent API calls. |
| `debt_service_ratio` used a gross-revenue denominator | Renamed it to **`debt_to_revenue_ratio`**; kept the numerical values and explained the formula. |
| `customer_feedback` timing was unclear | Each review now includes an explicit artificial date **7–90 days before the application**, with timing and no-post-outcome policy stated here. |

**Schema notice for team members:** This revision changes one header from `debt_service_ratio` to `debt_to_revenue_ratio`. Update any notebook or pipeline that uses the old name. The dataset still has **20 columns**, and the numeric values, application IDs, dates and binary target outcomes are unchanged.

## Handoff and limitations

- **Member 1:** Use `default_within_12m` as the classification target, `debt_to_revenue_ratio` as the corrected numeric feature, and one shared train/test split for all models.
- **Member 3:** Apply LLM/SLM sentiment, risk or segmentation extraction to `owner_statement` and `customer_feedback` **without revealing default labels**; store engineered features outside the raw CSV.
- **Member 4:** EDA and interpretation should explicitly describe all observed relationships as **simulated**.
- **Member 2:** Logistic Regression is a later milestone; the current submission focuses on dataset simulation and documentation.

**Limitations:** This is synthetic, simplified text and financial data. The generated textual patterns and outcome relationships reflect modelling assumptions, not real-world evidence. Variables may share synthetic causes and the class balance may be easier to model than a real loan portfolio. Disclose all GenAI assistance in the final report.
