📦 Automatidata Machine Learning Project

Overview

This project was completed as part of the "The Nuts and Bolts of Machine Learning" course at Automatidata.

The objective was to build a machine learning model that predicts whether a customer taking a taxi ride in New York City would be a generous tipper (defined as tipping ≥ 20% of the fare).

This model is intended to help taxi drivers maximize their earnings by identifying passengers likely to leave higher tips, while maintaining fairness and minimizing bias.

Project Structure

The project follows the PACE (Plan, Analyze, Construct, Execute) framework:

    Plan: Identify the business problem, assess ethical considerations, define the modeling objective.

    Analyze: Conduct feature engineering, data preprocessing, and exploratory data analysis.

    Construct: Build Random Forest and XGBoost models, tune hyperparameters using GridSearchCV.

    Execute: Evaluate model performance and derive conclusions based on metrics and feature importance.

Dataset

    Source: NYC Taxi and Limousine Commission datasets (2017 Yellow Taxi Trip Data).

    Size: 1+ million rides (filtered down to credit card transactions).

    Target Variable: generous (binary: 1 if tip ≥ 20% of the fare, 0 otherwise).

Features Used:

    Trip metadata (pickup/dropoff location, day of the week, time of day)

    Fare predictions and trip averages (mean distance, mean duration, predicted fare)

    Vendor and Rate Codes

Key Steps

    Filtered only credit card paying customers.

    Engineered features like:

    Tip percentage

    Time bins (AM rush, PM rush, Daytime, Nighttime)

    Day of the week and month indicators

    Encoded categorical variables via one-hot encoding.

    Handled ethical concerns by adjusting the modeling target (predict generous tippers instead of non-tippers).

Models Built

    Random Forest Classifier

    XGBoost Classifier

    Both models were optimized using cross-validation and hyperparameter tuning.

Results

    Model	               |  Precision    |   Recall |   F1 Score |   Accuracy
    ----------------------------------------------------------------------
    Random Forest (Test) |      0.7251	 |  0.7235 |   0.7235	 |   0.6865
    Random Forest (Test) |      0.7251	 |  0.7235 |   0.7235	 |   0.6865
    XGBoost (Test)	     |      0.7108	 |  0.7064 |   0.7073  |    0.6731

    Random Forest slightly outperformed XGBoost.

    F1 Score and accuracy suggest reasonable predictive power.

Feature Importance (Top Predictors)

    Vendor ID

    Predicted Fare

    Mean Duration

    Mean Distance

    Pickup Location ID

Ethical Considerations: 

    Instead of penalizing customers predicted to tip poorly, the model highlights potential high tippers.

    Ensures equitable access to taxi services while helping drivers maximize earnings.

Care taken to avoid model biases that could worsen customer discrimination.

Conclusion
The model shows solid performance for identifying generous tippers and can be piloted in a limited deployment with taxi drivers for further validation. Future enhancements could involve deep model explainability (SHAP values) and real-time feature updates.
