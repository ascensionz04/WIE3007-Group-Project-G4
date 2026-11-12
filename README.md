# WIE3007 Data Mining Group Project (Group 4)

AI-enhanced data mining on a simulated financial/business dataset: GenAI dataset simulation, LLM-based feature extraction, and predictive modelling (Decision Tree baseline + 4 models).

## Members and Roles
| Member | Role | Model(s) |
|---|---|---|
| Member 1 | Repo lead, shared pipeline, model comparison | Decision Tree (baseline), XGBoost |
| Member 2 | GenAI dataset simulation, data dictionary | Logistic Regression |
| Member 3 | LLM/SLM feature extraction, preprocessing | Random Forest |
| Member 4 | EDA, feature importance interpretation | Neural Network (MLP) |

## Repository Structure
```
data/raw/          simulated dataset (Member 2)
data/processed/    feature-engineered dataset (Member 3)
notebooks/         main.ipynb (shared notebook)
src/               shared code: data loading, split, evaluation
models/            one notebook/script per model
```

## Setup
```bash
pip install -r requirements.txt
```

## Workflow Rules
1. Never commit directly to `main`. Create your own branch: `feature/<name>-<task>` (e.g. `feature/ali-random-forest`).
2. Make small, frequent commits with clear messages (e.g. `Add Random Forest grid search`). Minimum 6 commits per member (Weeks 5–13).
3. Open a pull request into `main`; at least one other member must review before merging.
4. Every model must use `src.data_utils.split_data()` and `src.evaluation.evaluate_classifier()` so results are comparable.
