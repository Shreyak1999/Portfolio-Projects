#!/usr/bin/env python
# coding: utf-8

# # **Automatidata project**
# **Course 6 - The Nuts and bolts of machine learning**

# You are a data professional in a data analytics firm called Automatidata. Their client, the New York City Taxi & Limousine Commission (New York City TLC), was impressed with the work you have done and has requested that you build a machine learning model to predict if a customer will not leave a tip. They want to use the model in an app that will alert taxi drivers to customers who are unlikely to tip, since drivers depend on tips.
# 
# A notebook was structured and prepared to help you in this project. Please complete the following questions.

# # Course 6 End-of-course project: Build a machine learning model
# 
# In this activity, you will practice using tree-based modeling techniques to predict on a binary target class.  
# <br/>   
# 
# **The purpose** of this model is to find ways to generate more revenue for taxi cab drivers.  
#   
# **The goal** of this model is to predict whether or not a customer is a generous tipper.  
# <br/>  
# 
# *This activity has three parts:*
# 
# **Part 1:** Ethical considerations 
# * Consider the ethical implications of the request 
# 
# * Should the objective of the model be adjusted?
# 
# **Part 2:** Feature engineering
# 
# * Perform feature selection, extraction, and transformation to prepare the data for modeling
# 
# **Part 3:** Modeling
# 
# * Build the models, evaluate them, and advise on next steps
# 
# Follow the instructions and answer the questions below to complete the activity. Then, complete an Executive Summary using the questions listed on the PACE Strategy Document. 
# 
# Be sure to complete this activity before moving on. The next course item will provide you with a completed exemplar to compare to your own work. 
# 
# 

# # Build a machine learning model

# <img src="images/Pace.png" width="100" height="100" align=left>
# 
# # **PACE stages**
# 

# Throughout these project notebooks, you'll see references to the problem-solving framework PACE. The following notebook components are labeled with the respective PACE stage: Plan, Analyze, Construct, and Execute.

# <img src="images/Plan.png" width="100" height="100" align=left>
# 
# 
# ## PACE: Plan 
# 
# Consider the questions in your PACE Strategy Document to reflect on the Plan stage.
# 
# In this stage, consider the following questions:
# 
# 1.   What are you being asked to do?
# 
# 
# 2.   What are the ethical implications of the model? What are the consequences of your model making errors?
#   *   What is the likely effect of the model when it predicts a false negative (i.e., when the model says a customer will give a tip, but they actually won't)?
#   
#   *   What is the likely effect of the model when it predicts a false positive (i.e., when the model says a customer will not give a tip, but they actually will)?  
#   
#   
# 3.   Do the benefits of such a model outweigh the potential problems?
#   
# 4.   Would you proceed with the request to build this model? Why or why not?
#  
# 5.   Can the objective be modified to make it less problematic?
#  
# 

# #### Responses: 
# 1. Prediction of a customer's tipping behaviour.
# 2. a. Driver would be unhappy if the app says that the customer will tip, but he/she does not tip.
#        - If this happens frequently, driver loses confidence in the app. This leads to drivers uwilling to pick customers who  are predicted to not tip. Customers become unable to find rides and become dissatisfied with the taxi company.
#    b. Driver would not be happy as he/she would miss customers who would leave a tip. 
# 3. Penalizing drivers for picking up customers may discourage them from accepting rides and could trigger a negative response from customers. Overall, the drawbacks appear to outweigh any potential advantages.
# 4. No. Limiting equal access to taxis is ethically concerning and entails significant risks.
# 5. We can develop a model to identify the most generous tippers, helping taxi drivers maximize their earnings while ensuring fair and inclusive access to taxi services for all passengers.

# Suppose you were to modify the modeling objective so, instead of predicting people who won't tip at all, you predicted people who are particularly generous&mdash;those who will tip 20% or more? Consider the following questions:
# 
# 1.  What features do you need to make this prediction?
# 
# 2.  What would be the target variable?  
# 
# 3.  What metric should you use to evaluate your model? Do you have enough information to decide this now?
# 

# #### Responses
# 1. Ideally, we would have access to each customer’s behavioral history, including how much they tipped on previous taxi rides. Additionally, important features would include the time and date of the trip, pickup and dropoff locations, estimated fare, and the payment method used.
# 2. The target variable is a binary indicator (1 or 0) that represents whether a customer is expected to leave a tip of 20% or more.
# 3. Probably Accuracy, Precision, Recall, F1 and ROC. Others to be realised while building the model.

# 
# **_Complete the following steps to begin:_**

# ### **Task 1. Imports and data loading**
# 
# Import packages and libraries needed to build and evaluate random forest and XGBoost classification models.

# In[79]:


# Import packages and libraries
### YOUR CODE HERE ###
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

from sklearn.model_selection import train_test_split as tts
from sklearn.model_selection import GridSearchCV as gs
from sklearn.model_selection import PredefinedSplit as pds
from sklearn.ensemble import RandomForestClassifier as rfc
import sklearn.metrics as skm
from sklearn.metrics import mean_squared_error as mse
from sklearn.metrics import mean_absolute_error as mae
from sklearn.metrics import r2_score as r2
from sklearn.metrics import roc_auc_score as ras
from sklearn.metrics import roc_curve as roc

from xgboost import XGBClassifier as xgbc
from xgboost import plot_importance as pim


# In[48]:


# RUN THIS CELL TO SEE ALL COLUMNS 
# This lets us see all of the columns, preventing Juptyer from redacting them.
pd.set_option('display.max_columns', None)


# Begin by reading in the data. There are two dataframes: one containing the original data, the other containing the mean durations, mean distances, and predicted fares from the previous course's project called nyc_preds_means.csv.
# 
# **Note:** `Pandas` reads in the dataset as `df0`, now inspect the first five rows. As shown in this cell, the dataset has been automatically loaded in for you. You do not need to download the .csv file, or provide more code, in order to access the dataset and proceed with this lab. Please continue with this activity by completing the following instructions.

# In[49]:


# RUN THE CELL BELOW TO IMPORT YOUR DATA. 

# Load dataset into dataframe
df0 = pd.read_csv('2017_Yellow_Taxi_Trip_Data.csv')

# Import predicted fares and mean distance and duration from previous course
nyc_preds_means = pd.read_csv('nyc_preds_means.csv')


# Inspect the first few rows of `df0`.
# 

# In[50]:


# Inspect the first few rows of df0
### YOUR CODE HERE ###
df0.head()


# Inspect the first few rows of `nyc_preds_means`.

# In[51]:


# Inspect the first few rows of `nyc_preds_means`
### YOUR CODE HERE ###
nyc_preds_means.head()


# #### Join the two dataframes
# 
# Join the two dataframes using a method of your choice.

# In[52]:


# Merge datasets
### YOUR CODE HERE ###
df0 = df0.merge(nyc_preds_means,
                left_index=True,
                right_index=True)


# <img src="images/Analyze.png" width="100" height="100" align=left>
# 
# ## PACE: **Analyze**
# 
# Consider the questions in your PACE Strategy Documentto reflect on the Analyze stage.

# ### **Task 2. Feature engineering**
# 
# You have already prepared much of this data and performed exploratory data analysis (EDA) in previous courses. 
# 
# Call `info()` on the new combined dataframe.

# In[53]:


#==> ENTER YOUR CODE HERE
df0.info()


# You know from your EDA that customers who pay cash generally have a tip amount of $0. To meet the modeling objective, you'll need to sample the data to select only the customers who pay with credit card. 
# 
# Copy `df0` and assign the result to a variable called `df1`. Then, use a Boolean mask to filter `df1` so it contains only customers who paid with credit card.

# In[54]:


# Subset the data to isolate only customers who paid by credit card
#==> ENTER YOUR CODE HERE
df1 = df0.copy()
df1 = df0[df0['payment_type']==1]
df1.head()


# ##### **Target**
# 
# Notice that there isn't a column that indicates tip percent, which is what you need to create the target variable. You'll have to engineer it. 
# 
# Add a `tip_percent` column to the dataframe by performing the following calculation:  
# <br/>  
# 
# 
# $$tip\ percent = \frac{tip\ amount}{total\ amount - tip\ amount}$$  
# 
# Round the result to three places beyond the decimal. **This is an important step.** It affects how many customers are labeled as generous tippers. In fact, without performing this step, approximately 1,800 people who do tip ≥ 20% would be labeled as not generous. 
# 
# To understand why, you must consider how floats work. Computers make their calculations using floating-point arithmetic (hence the word "float"). Floating-point arithmetic is a system that allows computers to express both very large numbers and very small numbers with a high degree of precision, encoded in binary. However, precision is limited by the number of bits used to represent a number, which is generally 32 or 64, depending on the capabilities of your operating system. 
# 
# This comes with limitations in that sometimes calculations that should result in clean, precise values end up being encoded as very long decimals. Take, for example, the following calculation:
# 

# In[55]:


# Run this cell
1.1 + 2.2


# Notice the three that is 16 places to the right of the decimal. As a consequence, if you were to then have a step in your code that identifies values ≤ 3.3, this would not be included in the result. Therefore, whenever you perform a calculation to compute a number that is then used to make an important decision or filtration, round the number. How many degrees of precision you round to is your decision, which should be based on your use case. 
# 
# Refer to this [guide for more information related to floating-point arithmetic](https://floating-point-gui.de/formats/fp/).  

# In[56]:


# Create tip % col
#==> ENTER YOUR CODE HERE
df1['tip_percent'] = round((df1['tip_amount'])/(df1['total_amount'] - df1['tip_amount']),3)


# Now create another column called `generous`. This will be the target variable. The column should be a binary indicator of whether or not a customer tipped ≥ 20% (0=no, 1=yes).
# 
# 1. Begin by making the `generous` column a copy of the `tip_percent` column.
# 2. Reassign the column by converting it to Boolean (True/False).
# 3. Reassign the column by converting Boolean to binary (1/0).

# In[57]:


# Create 'generous' col (target)
#==> ENTER YOUR CODE HERE
df1['generous'] = df1['tip_percent']
df1['generous'] = (df1['generous'] >= 0.2)
df1['generous'] = df1['generous'].astype(int)


# <details>
#   <summary><h5>HINT</h5></summary>
# 
# To convert from Boolean to binary, use `.astype(int)` on the column.
# </details>

# #### Create day column

# Next, you're going to be working with the pickup and dropoff columns.
# 
# Convert the `tpep_pickup_datetime` and `tpep_dropoff_datetime` columns to datetime.

# In[58]:


# Convert pickup and dropoff cols to datetime
#==> ENTER YOUR CODE HERE
df1['tpep_pickup_datetime'] = pd.to_datetime(df1['tpep_pickup_datetime'], format='%m/%d/%Y %I:%M:%S %p')
df1['tpep_dropoff_datetime'] = pd.to_datetime(df1['tpep_dropoff_datetime'], format='%m/%d/%Y %I:%M:%S %p')


# Create a `day` column that contains only the day of the week when each passenger was picked up. Then, convert the values to lowercase.

# In[59]:


# Create a 'day' col
#==> ENTER YOUR CODE HERE
df1['day'] = df1['tpep_pickup_datetime'].dt.day_name().str.lower()


# 
# <details>
#   <summary><h5>HINT</h5></summary>
# 
# To convert to day name, use `dt.day_name()` on the column.
# </details>

# #### Create time of day columns

# Next, engineer four new columns that represent time of day bins. Each column should contain binary values (0=no, 1=yes) that indicate whether a trip began (picked up) during the following times:
# 
# `am_rush` = [06:00&ndash;10:00)  
# `daytime` = [10:00&ndash;16:00)  
# `pm_rush` = [16:00&ndash;20:00)  
# `nighttime` = [20:00&ndash;06:00)  
# 
# To do this, first create the four columns. For now, each new column should be identical and contain the same information: the hour (only) from the `tpep_pickup_datetime` column.

# In[60]:


# Create 'am_rush' col
#==> ENTER YOUR CODE HERE
df1['am_rush'] = df1['tpep_pickup_datetime'].dt.hour
# Create 'daytime' col
#==> ENTER YOUR CODE HERE
df1['daytime'] = df1['tpep_pickup_datetime'].dt.hour
# Create 'pm_rush' col
#==> ENTER YOUR CODE HERE
df1['pm_rush'] = df1['tpep_pickup_datetime'].dt.hour
# Create 'nighttime' col
#==> ENTER YOUR CODE HERE
df1['nighttime'] = df1['tpep_pickup_datetime'].dt.hour


# You'll need to write four functions to convert each new column to binary (0/1). Begin with `am_rush`. Complete the function so if the hour is between [06:00–10:00), it returns 1, otherwise, it returns 0.

# In[61]:


# Define 'am_rush()' conversion function [06:00–10:00)
    #==> ENTER YOUR CODE HERE
def am_rush(hour):
    if 6 <= hour['am_rush'] < 10:
        val = 1
    else:
        val = 0
    return val


# Now, apply the `am_rush()` function to the `am_rush` series to perform the conversion. Print the first five values of the column to make sure it did what you expected it to do.
# 
# **Note:** Be careful! If you run this cell twice, the function will be reapplied and the values will all be changed to 0.

# In[62]:


# Apply 'am_rush' function to the 'am_rush' series
#==> ENTER YOUR CODE HERE
df1['am_rush'] = df1.apply(am_rush, axis=1)
df1['am_rush'].head()


# Write functions to convert the three remaining columns and apply them to their respective series.

# In[63]:


# Define 'daytime()' conversion function [10:00–16:00)
#==> ENTER YOUR CODE HERE
def daytime(hour):
    if 10 <= hour['daytime'] < 16:
        val = 1
    else:
        val = 0
    return val


# In[64]:


# Apply 'daytime()' function to the 'daytime' series
#==> ENTER YOUR CODE HERE
df1['daytime'] = df1.apply(daytime, axis=1)
df1['daytime'].head()


# In[65]:


# Define 'pm_rush()' conversion function [16:00–20:00)
#==> ENTER YOUR CODE HERE
def pm_rush(hour):
    if 16 <= hour['pm_rush'] < 20:
        val = 1
    else:
        val = 0
    return val


# In[66]:


# Apply 'pm_rush()' function to the 'pm_rush' series
#==> ENTER YOUR CODE HERE
df1['pm_rush'] = df1.apply(pm_rush, axis=1)
df1['pm_rush'].head()


# In[67]:


# Define 'nighttime()' conversion function [20:00–06:00)
#==> ENTER YOUR CODE HERE
def nighttime(hour):
    if 6 <= hour['nighttime'] < 10:
        val = 1
    else:
        val = 0
    return val


# In[68]:


# Apply 'nighttime' function to the 'nighttime' series
#==> ENTER YOUR CODE HERE
df1['nighttime'] = df1.apply(nighttime, axis=1)
df1['nighttime'].head()


# #### Create `month` column

# Now, create a `month` column that contains only the abbreviated name of the month when each passenger was picked up, then convert the result to lowercase.

# <details>
#   <summary><h5>HINT</h5></summary>
# 
# Refer to the [strftime cheatsheet](https://strftime.org/) for help.
# </details>

# In[69]:


# Create 'month' col
#==> ENTER YOUR CODE HERE
df1['month'] = df1['tpep_pickup_datetime'].dt.strftime('%b').str.lower()


# Examine the first five rows of your dataframe.

# In[70]:


#==> ENTER YOUR CODE HERE
df1.head()


# #### Drop columns
# 
# Drop redundant and irrelevant columns as well as those that would not be available when the model is deployed. This includes information like payment type, trip distance, tip amount, tip percentage, total amount, toll amount, etc. The target variable (`generous`) must remain in the data because it will get isolated as the `y` data for modeling.

# In[71]:


# Drop columns
#==> ENTER YOUR CODE HERE
df1 = df1.drop(columns = ['Unnamed: 0', 'tpep_pickup_datetime', 'tpep_dropoff_datetime',
             'payment_type', 'trip_distance', 'store_and_fwd_flag', 'payment_type',
             'fare_amount', 'extra', 'mta_tax', 'tip_amount', 'tolls_amount',
             'improvement_surcharge', 'total_amount', 'tip_percent'])


# In[72]:


df1.info()


# #### Variable encoding

# Many of the columns are categorical and will need to be dummied (converted to binary). Some of these columns are numeric, but they actually encode categorical information, such as `RatecodeID` and the pickup and dropoff locations. To make these columns recognizable to the `get_dummies()` function as categorical variables, you'll first need to convert them to `type(str)`. 
# 
# 1. Define a variable called `cols_to_str`, which is a list of the numeric columns that contain categorical information and must be converted to string: `RatecodeID`, `PULocationID`, `DOLocationID`.
# 2. Write a for loop that converts each column in `cols_to_str` to string.
# 

# In[73]:


# 1. Define list of cols to convert to string
#==> ENTER YOUR CODE HERE
cols_to_str = ['RatecodeID', 'PULocationID', 'DOLocationID', 'VendorID']
# 2. Convert each column to string
#==> ENTER YOUR CODE HERE
for col in cols_to_str:
    df1[col] = df1[col].astype('str')


# In[74]:


df1.dtypes


# 
# <details>
#   <summary><h5>HINT</h5></summary>
# 
# To convert to string, use `astype(str)` on the column.
# </details>

# Now convert all the categorical columns to binary.
# 
# 1. Call `get_dummies()` on the dataframe and assign the results back to a new dataframe called `df2`.
# 

# In[75]:


# Convert categoricals to binary
#==> ENTER YOUR CODE HERE
df2 = pd.get_dummies(df1, drop_first = True)


# In[76]:


df2.info()


# ##### Evaluation metric
# 
# Before modeling, you must decide on an evaluation metric. 
# 
# 1. Examine the class balance of your target variable. 

# In[77]:


# Get class balance of 'generous' col
#==> ENTER YOUR CODE HERE
df2['generous'].value_counts(normalize=True)


# A little over half of the customers in this dataset were "generous" (tipped ≥ 20%). The dataset is very nearly balanced.
# 
# To determine a metric, consider the cost of both kinds of model error:
# * False positives (the model predicts a tip ≥ 20%, but the customer does not give one)
# * False negatives (the model predicts a tip < 20%, but the customer gives more)
# 
# False positives are worse for cab drivers, because they would pick up a customer expecting a good tip and then not receive one, frustrating the driver.
# 
# False negatives are worse for customers, because a cab driver would likely pick up a different customer who was predicted to tip more&mdash;even when the original customer would have tipped generously.
# 
# **The stakes are relatively even. You want to help taxi drivers make more money, but you don't want this to anger customers. Your metric should weigh both precision and recall equally. Which metric is this?**

# F1 Score

# <img src="images/Construct.png" width="100" height="100" align=left>
# 
# ## PACE: **Construct**
# 
# Consider the questions in your PACE Strategy Document to reflect on the Construct stage.

# ### **Task 3. Modeling**

# ##### **Split the data**
# 
# Now you're ready to model. The only remaining step is to split the data into features/target variable and training/testing data. 
# 
# 1. Define a variable `y` that isolates the target variable (`generous`).
# 2. Define a variable `X` that isolates the features.
# 3. Split the data into training and testing sets. Put 20% of the samples into the test set, stratify the data, and set the random state.

# In[80]:


# Isolate target variable (y)
#==> ENTER YOUR CODE HERE
y = df2['generous']
# Isolate the features (X)
#==> ENTER YOUR CODE HERE
X = df2.drop(['generous'], axis = 1)
# Split into train and test sets
#==> ENTER YOUR CODE HERE
X_train, X_test, y_train, y_test = tts(X, y, test_size = 0.2, stratify = y, random_state = 0)


# ##### **Random forest**
# 
# Begin with using `GridSearchCV` to tune a random forest model.
# 
# 1. Instantiate the random forest classifier `rf` and set the random state.
# 
# 2. Create a dictionary `cv_params` of any of the following hyperparameters and their corresponding values to tune. The more you tune, the better your model will fit the data, but the longer it will take. 
#  - `max_depth`  
#  - `max_features`  
#  - `max_samples` 
#  - `min_samples_leaf`  
#  - `min_samples_split`
#  - `n_estimators`  
# 
# 3. Define a set `scoring` of scoring metrics for GridSearch to capture (precision, recall, F1 score, and accuracy).
# 
# 4. Instantiate the `GridSearchCV` object `rf1`. Pass to it as arguments:
#  - estimator=`rf`
#  - param_grid=`cv_params`
#  - scoring=`scoring`
#  - cv: define the number of you cross-validation folds you want (`cv=_`)
#  - refit: indicate which evaluation metric you want to use to select the model (`refit=_`)
# 
# 
# **Note:** `refit` should be set to `'f1'`.<font/>
# </details>
#  
# 

# In[81]:


# 1. Instantiate the random forest classifier
#==> ENTER YOUR CODE HERE
rf = rfc(random_state = 0)

# 2. Create a dictionary of hyperparameters to tune 
#==> ENTER YOUR CODE HERE
cv_params = {'max_depth': [None], 'max_features': [1.0], 
             'max_samples': [0.7],
             'min_samples_leaf': [1],
             'min_samples_split': [2],
             'n_estimators': [300]}

# 3. Define a list of scoring metrics to capture
#==> ENTER YOUR CODE HERE
scoring = ['accuracy', 'precision', 'recall', 'f1']

# 4. Instantiate the GridSearchCV object
#==> ENTER YOUR CODE HERE
rf1 = gs(rf, cv_params, scoring=scoring, cv=5, refit='f1')


# Now fit the model to the training data. Note that, depending on how many options you include in your search grid and the number of cross-validation folds you select, this could take a very long time&mdash;even hours. If you use 4-fold validation and include only one possible value for each hyperparameter and grow 300 trees to full depth, it should take about 5 minutes. If you add another value for GridSearch to check for, say, `min_samples_split` (so all hyperparameters now have 1 value except for `min_samples_split`, which has 2 possibilities), it would double the time to ~10 minutes. Each additional parameter would approximately double the time. 

# In[82]:


get_ipython().run_cell_magic('time', '', '#==> ENTER YOUR CODE HERE\nrf1.fit(X_train, y_train)\n')


# Examine the best average score across all the validation folds. 

# In[83]:


# Examine best score
#==> ENTER YOUR CODE HERE
round(rf1.best_score_, 4)


# Examine the best combination of hyperparameters.

# In[84]:


#==> ENTER YOUR CODE HERE
rf1.best_params_


# Use the `make_results()` function to output all of the scores of your model. Note that it accepts three arguments. 

# <details>
#   <summary><h5>HINT</h5></summary>
# 
# To learn more about how this function accesses the cross-validation results, refer to the [`GridSearchCV` scikit-learn documentation](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GridSearchCV.html?highlight=gridsearchcv#sklearn.model_selection.GridSearchCV) for the `cv_results_` attribute.
# 
# </details>

# In[85]:


def make_results(model_name:str, model_object, metric:str):
    '''
    Arguments:
    model_name (string): what you want the model to be called in the output table
    model_object: a fit GridSearchCV object
    metric (string): precision, recall, f1, or accuracy

    Returns a pandas df with the F1, recall, precision, and accuracy scores
    for the model with the best mean 'metric' score across all validation folds.
    '''

    # Create dictionary that maps input metric to actual metric name in GridSearchCV
    metric_dict = {'precision': 'mean_test_precision',
                 'recall': 'mean_test_recall',
                 'f1': 'mean_test_f1',
                 'accuracy': 'mean_test_accuracy',
                 }

    # Get all the results from the CV and put them in a df
    cv_results = pd.DataFrame(model_object.cv_results_)

    # Isolate the row of the df with the max(metric) score
    best_estimator_results = cv_results.iloc[cv_results[metric_dict[metric]].idxmax(), :]

    # Extract Accuracy, precision, recall, and f1 score from that row
    f1 = best_estimator_results.mean_test_f1
    recall = best_estimator_results.mean_test_recall
    precision = best_estimator_results.mean_test_precision
    accuracy = best_estimator_results.mean_test_accuracy

    # Create table of results
    table = pd.DataFrame({'model': [model_name],
                        'precision': [precision],
                        'recall': [recall],
                        'F1': [f1],
                        'accuracy': [accuracy],
                        },
                       )

    return table


# Call `make_results()` on the GridSearch object.

# In[91]:


#==> ENTER YOUR CODE HERE
results = make_results('RF CV', rf1, 'f1')
results


# Your results should produce an acceptable model across the board. Typically scores of 0.65 or better are considered acceptable, but this is always dependent on your use case. Optional: try to improve the scores. It's worth trying, especially to practice searching over different hyperparameters.
# 
# <details>
#   <summary><h5>HINT</h5></summary>
# 
# For example, if the available values for `min_samples_split` were [2, 3, 4] and GridSearch identified the best value as 4, consider trying [4, 5, 6] this time.
# </details>

# Use your model to predict on the test data. Assign the results to a variable called `rf_preds`.

# <details>
#   <summary><h5>HINT</h5></summary>
#     
# You cannot call `predict()` on the GridSearchCV object directly. You must call it on the `best_estimator_`.
# </details>

# For this project, you will use several models to predict on the test data. Remember that this decision comes with a trade-off. What is the benefit of this? What is the drawback?

# Using multiple models to predict on the test data allows you to compare their performance on data that hasn’t been used during training or hyperparameter tuning. This helps reduce the risk of choosing a model that only performs well on the training set but poorly on new data.
# 
# However, selecting a model based on its performance on the final test set introduces bias. Since the test data is being used to make a decision about which model to choose, it effectively becomes part of the tuning process. As a result, you lose an unbiased estimate of how the model would perform on truly unseen data.

# In[89]:


# Get scores on test data
#==> ENTER YOUR CODE HERE
rf_pred = rf1.best_estimator_.predict(X_test)


# Use the below `get_test_scores()` function you will use to output the scores of the model on the test data.

# In[95]:


def get_test_scores(model_name:str, preds, y_test_data):
    '''
    Generate a table of test scores.

    In:
    model_name (string): Your choice: how the model will be named in the output table
    preds: numpy array of test predictions
    y_test_data: numpy array of y_test data

    Out:
    table: a pandas df of precision, recall, f1, and accuracy scores for your model
    '''
    accuracy = skm.accuracy_score(y_test_data, preds)
    precision = skm.precision_score(y_test_data, preds)
    recall = skm.recall_score(y_test_data, preds)
    f1 = skm.f1_score(y_test_data, preds)

    table = pd.DataFrame({'model': [model_name],
                        'precision': [precision],
                        'recall': [recall],
                        'F1': [f1],
                        'accuracy': [accuracy]
                        })

    return table


# 1. Use the `get_test_scores()` function to generate the scores on the test data. Assign the results to `rf_test_scores`.
# 2. Call `rf_test_scores` to output the results.

# ###### RF test results

# In[96]:


# Get scores on test data
#==> ENTER YOUR CODE HERE
rf_test_scores = get_test_scores('RF test', rf_pred, y_test)
results = pd.concat([results, rf_test_scores], axis=0)
results


# **Question:** How do your test results compare to your validation results?

# All scores increased by at most approximately 2%.

# ##### **XGBoost**
# 
#  Try to improve your scores using an XGBoost model.
# 
# 1. Instantiate the XGBoost classifier `xgb` and set `objective='binary:logistic'`. Also set the random state.
# 
# 2. Create a dictionary `cv_params` of the following hyperparameters and their corresponding values to tune:
#  - `max_depth`
#  - `min_child_weight`
#  - `learning_rate`
#  - `n_estimators`
# 
# 3. Define a set `scoring` of scoring metrics for grid search to capture (precision, recall, F1 score, and accuracy).
# 
# 4. Instantiate the `GridSearchCV` object `xgb1`. Pass to it as arguments:
#  - estimator=`xgb`
#  - param_grid=`cv_params`
#  - scoring=`scoring`
#  - cv: define the number of cross-validation folds you want (`cv=_`)
#  - refit: indicate which evaluation metric you want to use to select the model (`refit='f1'`)

# In[97]:


# 1. Instantiate the XGBoost classifier
#==> ENTER YOUR CODE HERE
xgb = xgbc(objective='binary:logistic', random_state=0)
# 2. Create a dictionary of hyperparameters to tune
#==> ENTER YOUR CODE HERE
cv_params = {'max_depth': [8],
             'min_child_weight': [2],
             'learning_rate': [0.1],             
             'n_estimators': [500]
             }
# 3. Define a list of scoring metrics to capture
#==> ENTER YOUR CODE HERE
scoring = ['accuracy', 'precision', 'recall', 'f1']
# 4. Instantiate the GridSearchCV object
#==> ENTER YOUR CODE HERE
xgb1 = gs(xgb, cv_params, scoring=scoring, cv=4, refit='f1')


# Now fit the model to the `X_train` and `y_train` data.

# In[98]:


get_ipython().run_cell_magic('time', '', '#==> ENTER YOUR CODE HERE\nxgb1.fit(X_train, y_train)\n')


# Get the best score from this model.

# In[100]:


# Examine best score
#==> ENTER YOUR CODE HERE
round(xgb1.best_score_,3)


# And the best parameters.

# In[101]:


# Examine best parameters
#==> ENTER YOUR CODE HERE
xgb1.best_params_


# ##### XGB CV Results
# 
# Use the `make_results()` function to output all of the scores of your model. Note that it accepts three arguments. 

# In[102]:


# Call 'make_results()' on the GridSearch object
#==> ENTER YOUR CODE HERE
xgb1_cv_results = make_results('XGB CV', xgb1, 'f1')
results = pd.concat([results, xgb1_cv_results], axis=0)
results


# Use your model to predict on the test data. Assign the results to a variable called `xgb_preds`.
# 
# <details>
#   <summary><h5>HINT</h5></summary>
#     
# You cannot call `predict()` on the GridSearchCV object directly. You must call it on the `best_estimator_`.
# </details>

# In[103]:


# Get scores on test data
#==> ENTER YOUR CODE HERE
xgb_pred = xgb1.best_estimator_.predict(X_test)


# ###### XGB test results
# 
# 1. Use the `get_test_scores()` function to generate the scores on the test data. Assign the results to `xgb_test_scores`.
# 2. Call `xgb_test_scores` to output the results.

# In[104]:


# Get scores on test data
#==> ENTER YOUR CODE HERE
xgb_test_scores = get_test_scores('XGB test', xgb_pred, y_test)
results = pd.concat([results, xgb_test_scores], axis=0)
results


# **Question:** Compare these scores to the random forest test scores. What do you notice? Which model would you choose?

# The F1 score of Random Forest model is approximately 1.4% higher as compared to the XGB model. Since the difference is very minute, any model can be chosen, however, higher preference may be given to the Random Forest model.

# Plot a confusion matrix of the model's predictions on the test data.

# In[110]:


# Generate array of values for confusion matrix
#==> ENTER YOUR CODE HERE
cm = skm.confusion_matrix(y_test, rf_pred, labels=rf1.classes_)
# Plot confusion matrix
#==> ENTER YOUR CODE HERE
disp = skm.ConfusionMatrixDisplay(confusion_matrix=cm,
                             display_labels=rf1.classes_, 
                             )
disp.plot(values_format='');


# **Question:** What type of errors are more common for your model?

# Type 1 error is most likely to be common here given that the probability of false negatives is lower than that of false positives. This is less ideal, as it's preferable for a driver to be pleasantly surprised by a generous tip they didn’t anticipate, rather than disappointed by a lower tip than expected. Nonetheless, the model's overall performance remains satisfactory.

# ##### Feature importance
# 
# Use the `feature_importances_` attribute of the best estimator object to inspect the features of your final model. You can then sort them and plot the most important ones.

# In[115]:


#==> ENTER YOUR CODE HERE
importances = rf1.best_estimator_.feature_importances_
rf_importances = pd.Series(importances, index=X_test.columns)
rf_importances = rf_importances.sort_values(ascending=False)[:15]

fig, ax = plt.subplots(figsize=(10,5))
rf_importances.plot.bar(ax=ax)
ax.set_title('Feature importances')
ax.set_ylabel('Mean decrease in impurity')
fig.tight_layout();


# <img src="images/Execute.png" width="100" height="100" align=left>
# 
# ## PACE: **Execute**
# 
# Consider the questions in your PACE Strategy Document to reflect on the Execute stage.

# ### **Task 4. Conclusion**
# 
# In this step, use the results of the models above to formulate a conclusion. Consider the following questions:
# 
# **Would you recommend using this model? Why or why not?**  
# Yes, this model performs reasonably well. It achieved an F1 score of 0.7235 and an overall accuracy of 0.6865. Notably, it correctly identified approximately 78% of actual responders in the test set—around 48% better than random guessing. It may be worthwhile to pilot the model with a selected group of taxi drivers to gather feedback.
# 
# **What was your model doing? Can you explain how it was making predictions?**   
# Random forest, while powerful, lacks transparency, making it difficult to interpret how individual features influence tipping behavior. We know that VendorID, predicted_fare, mean_duration, and mean_distance are the most important predictors, but the nature of their impact remains unclear and warrants deeper investigation. The prominence of VendorID is particularly noteworthy—it suggests that one vendor may consistently serve more generous tippers than the other. This observation could be explored further through statistical testing to assess whether tipping behavior significantly differs between the vendors.
# 

# In[ ]:




