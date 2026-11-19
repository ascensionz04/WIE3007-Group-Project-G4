# Data Dictionary — Synthetic Malaysian SME Loans

**Course:** WIE3007 Data Mining | **Owner:** Group 4 

**Dataset:** `data/raw/sme_loan_applications_synthetic.csv`

**Unit of observation:** One fictional Malaysian SME loan application  
**Size:** 1,500 records × 20 fields  
**Task:** Binary classification of simulated 12-month loan default  
**Currency:** Malaysian ringgit (MYR)

> All records and outcomes are fully synthetic. They are not actual Malaysian loan applicants, transactions, or observed default rates. This dataset must not be used for real lending decisions.

## Field definitions

| Field name | Type | Description | Role |
|---|---|---|---|
| `application_id` | String | Unique fictional application ID (SME000001–SME001500). | Identifier; exclude from features |
| `application_date` | Date (YYYY-MM-DD) | Fictional application date in 2024-07-01 to 2025-07-31. | Input/context |
| `industry` | Categorical string | Business sector, e.g., Retail, Manufacturing, E-commerce. | Input |
| `state` | Categorical string | Malaysian business location (13 locations in the dataset). | Input |
| `years_in_business` | Integer | Years in operation before applying (1–30). | Input |
| `employee_count` | Integer | Number of staff at time of application (2–180). | Input |
| `annual_revenue_myr` | Float | Annual gross sales revenue, in MYR. | Input |
| `profit_margin_pct` | Float | Business profit margin, in percentage points; may be negative. | Input |
| `monthly_net_cash_flow_myr` | Float | Average monthly business net cash flow; may be negative, in MYR. | Input |
| `existing_monthly_debt_payment_myr` | Float | Monthly repayment obligations on debts existing at application, in MYR. | Input |
| `debt_service_ratio` | Float | Existing monthly debt payment divided by estimated monthly **gross revenue** (`annual_revenue_myr / 12`), stored to 3 decimal places. | Input |
| `credit_score` | Integer | Fictional credit score (360–850; higher means stronger credit). | Input |
| `late_payments_12m` | Integer | Number of late debt payments in the **prior** 12 months (0–9). | Input |
| `requested_loan_myr` | Float | Amount of new business loan requested, in MYR. | Input |
| `loan_term_months` | Integer / categorical | Requested repayment period: 12, 24, 36, 48, or 60 months. | Input |
| `collateral_available` | Categorical string | Whether collateral is available: Yes or No. | Input |
| `loan_purpose` | Categorical string | Requested financing purpose: Working Capital, Business Expansion, Equipment Purchase, Inventory Purchase, Digital Transformation, Marketing, or Debt Refinancing. | Input |
| `owner_statement` | Text | GenAI-assisted synthetic, pre-application owner narrative about business conditions and intended use of funds. | NLP input (Member 3) |
| `customer_feedback` | Text | GenAI-assisted synthetic customer comments about product/service and customer experience. | NLP input (Member 3) |
| `default_within_12m` | Binary integer | **Target**: 1 = simulated default within 12 months; 0 = simulated no default. | TARGET — never use as feature |

## Simulation design and validity

ChatGPT (GenAI) assisted the scenario design, numerical relationship assumptions, field descriptions, and narrative template wording. The included Python program then **procedurally samples** 1,500 rows using a fixed seed (`20261119`). It does *not* call an LLM API once for each row. No real borrowers or personal information were used.

The simulated outcome is sampled from a probability function influenced by pre-application credit score, repayment history, profitability, existing debt ratio, sector, collateral, and cash flow. The owner statements and customer feedback reflect business conditions **before** the outcome is generated; they are not written by looking up the target. The outcome is therefore a fictional label, not a validated bank default model or a Malaysian default statistic.

## Handoff for other members

- **Member 1:** Use `default_within_12m` as classification target. Exclude `application_id`; create one shared train/test split and fit all preprocessing on training only. For Logistic Regression and other models, encode categorical features and scale numeric variables as appropriate.
- **Member 3:** Derive sentiment, risk category, or customer segment from `owner_statement` and `customer_feedback` via LLM/SLM. **Never include target labels in the extraction prompt.** Save engineered features separately from the raw CSV.
- **Member 4:** Perform EDA and interpret model performance as patterns in *simulated* data only.

## Verification

1,500 distinct IDs; no missing fields; both classes present (1,078 non-default, 422 default, ~28.1% synthetic default). The generator enforces and checks data types, score ranges, debt ratio calculation, and target classes. Limitations: template language is simpler than real text; numerical distributions and default likelihood are invented for coursework and not externally calibrated. Correlated revenue/debt fields should not be assumed independent.
