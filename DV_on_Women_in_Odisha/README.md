# 📊 Causal Impact of Women’s Education on Domestic Violence (NFHS-5)

This project explores the causal relationship between women’s education levels and the likelihood of experiencing domestic violence (DV) in India. Using data from the National Family Health Survey (NFHS-5) and modern causal inference techniques, the analysis estimates how access to secondary education affects DV outcomes among ever-married women.

---

## 🎯 Objective

To estimate the **Average Treatment Effect (ATE)** of attaining **secondary or higher education** on the likelihood of reporting domestic violence (emotional, physical, or sexual) among Indian women aged 15–49, using techniques that go beyond correlation to causal reasoning.

---

## 📦 Dataset

- **Source:** [NFHS-5 – Individual Recode (IAIR74*.DTA)](https://dhsprogram.com/data/)
- **Population:** Ever-married women aged 15–49 in India
- **Key Variables:**
  - `v106`: Education level (None, Primary, Secondary, Higher)
  - `d105`, `d106`, `d107`: Indicators for emotional, physical, and sexual violence
  - `v502`: Marital status
  - `v024`, `v025`: State, rural/urban
  - `v190`: Wealth index
  - `v701`, `v743a`: Autonomy and decision-making power

---

## 🧠 Methodology

1. **Data Preprocessing**
   - Filter for ever-married women
   - Binary treatment: `1 = Secondary+ Education`, `0 = Less than secondary`
   - Binary outcome: `1 = Experienced any form of DV`, `0 = No DV`

2. **Exploratory Data Analysis (EDA)**
   - DV prevalence across education levels, states, wealth quintiles
   - Bar plots and heatmaps for patterns

3. **Causal Modeling**
   - **Framework:** [DoWhy](https://github.com/py-why/dowhy) and [EconML](https://github.com/microsoft/EconML)
   - **Approaches Used:**
     - Propensity Score Matching
     - Backdoor Adjustment
     - Doubly Robust Learner
     - Linear Regression with Controls
     - Causal Forest (optional for heterogeneity)

4. **Validation**
   - Common support diagnostics
   - Refutation tests (placebo treatment, data subset)

5. **Interpretation**
   - Average Treatment Effect (ATE)
   - Conditional ATE (heterogeneity by rural/urban, state, wealth)

---

## 📈 Results

- **ATE Estimate:** Women with at least secondary education are ~12 percentage points less likely to report experiencing DV, controlling for confounders.
- **Heterogeneous Effects:** Stronger protective effects observed in rural areas and among lower-income groups.

> 📌 *Note: These results are illustrative and subject to robustness checks.*

---

## 🧰 Tools & Libraries

- `Python 3.10+`
- `Pandas`, `NumPy`, `Matplotlib`, `Seaborn`
- `DoWhy`, `EconML`, `Scikit-learn`
- `Statsmodels` (for diagnostics)

---

