🏠 House Price Prediction – Regression Project

📌 Project Overview

This project predicts the selling prices of residential homes in Ames, Iowa using machine learning regression techniques. The aim is to help real estate businesses and homebuyers estimate fair property prices based on key features such as size, location, quality, and amenities.


📊 Dataset

- Source: Kaggle – House Prices: Advanced Regression Techniques
- Rows: ~1,460
- Columns: 80 (categorical + numerical features)
- Target Variable: SalePrice


❓ Key Questions Answered in this Project

1. What problem are we solving?
    
    - Predicting house prices accurately using property features.

2. Why does this problem matter?

    - Helps buyers, sellers, and financial institutions estimate fair prices and avoid under/over-valuations.

3. What does the dataset look like?

    - Contains ~1,460 houses with 80 features (lot size, year built, quality ratings, etc.).

    - Target variable SalePrice ranges widely, with some outliers.

4. Which features affect house prices the most?

    - Does house size (GrLivArea, LotArea) have stronger influence than location or quality (OverallQual)?

    - SHAP analysis reveals which features drive price predictions.

5. How do different models perform?

    - Comparison between Linear Regression, Random Forest, and XGBoost.

    - Advanced models reduce RMSE significantly compared to baseline.

6. How do we evaluate performance?

    - Metrics used: RMSE, MAE, and R².

    - RMSE chosen as the primary metric since pricing errors need squared penalization.

7. How do we ensure interpretability?

    - Feature importance visualizations.

    - SHAP plots explaining both global feature influence and local predictions.

8. How can this be used in practice?

    - Real estate agents or buyers can input house details to get predicted prices.

    - Deployed version available via Streamlit.

9. What are the limitations of the model?

    - Trained on Ames data only — may not generalize to other cities.

    - Does not include external socioeconomic factors like neighborhood crime rates, schools, or future market trends.


🛠️ Tools & Libraries Used

- Python

    - pandas, numpy → Data cleaning & feature engineering

    - matplotlib, seaborn → Data visualization

    - scikit-learn → Modeling & evaluation

    - XGBoost → Advanced regression

    - SHAP → Model interpretability

    - Streamlit → Deployment as web app


🔎 Project Workflow

1. Exploratory Data Analysis (EDA)

    - Distribution of Sale Prices
    - Correlation heatmap of features
    - Outlier detection & handling

2. Data Preprocessing

    - Missing value imputation
    - Encoding categorical variables (OneHotEncoder)
    - Feature scaling (StandardScaler)
    - Train-test split

3. Modeling

    - Baseline: Linear Regression
    - Advanced: Random Forest Regressor, XGBoost Regressor
    - Model comparison using RMSE, MAE, R²

4. Hyperparameter Tuning
    - GridSearchCV & RandomizedSearchCV

5. Model Interpretability

    - Feature importance plots
    - SHAP summary plots (explain predictions at global & local level)

6. Deployment

    - Interactive Streamlit app to predict house price given input features


📈 Results


📊 Visualizations


🚀 How to Run the Project
1. Clone this Repo

    git clone https://github.com/Shreyak1999/Portfolio-Projects/Supervised_ML_Housing_Price_Analytics.git

    cd Supervised_ML_Housing_Price_Analytics

2. Install dependencies

    pip install -r requirements.txt

3. Run eda.ipynb

4. Deployment

    streamlit run app.py


🙌 Acknowledgments

    Dataset provided by Kaggle

    Inspired by Ames Housing dataset regression challenges
