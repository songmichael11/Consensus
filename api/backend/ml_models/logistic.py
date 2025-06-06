import numpy as np
import pandas as pd
from flask import Blueprint, jsonify, request, current_app

# from models import log_regress
# from models import lin_regress
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import r2_score
# from sklearn.metrics import mean_squared_error
# from datetime import datetime

# megaframe = pd.read_csv('datasets/MEGAFRAME_CLEANEDV2.csv')


# X_df = pd.get_dummies(megaframe, columns=['Region'], dtype=int)
# X_df = X_df.drop(labels=['TIME_PERIOD', 'Reference area', 'REF_AREA', 'Gini index'], axis=1)
# describe = X_df.describe().loc[['mean', 'std']].to_numpy()

# # Assume X is your full NumPy array
# num_exclude = 4

# # Split the array
# X_main = X[:, :-num_exclude]   # Columns to standardize
# X_last = X[:, -num_exclude:]   # Columns to leave untouched

# # Standardize the first part
# mean = X_main.mean(axis=0)
# std = X_main.std(axis=0)
# std[std == 0] = 1  # Avoid division by zero
# X_main_standardized = (X_main - mean) / std

# # Concatenate back together
# X = np.hstack([X_main_standardized, X_last])
# print(X)

# X = np.array([78.699997,28.0,0.0734319847255705,0.0631525528524754,0.0057497428086187,0.0025634702523358,5.1075,5.825,8895960.0,27259.4806735435,2.40595834145438,0,1,0,0])

def predict_gini(X, describe, weights, model='logistic'):
    """
    Make predictions using the logistic regression model.
    
    Args:
        X: list of feature values in the same order as FEATURE_VARIABLES
        describe: numpy array of shape (2, n_features) containing mean and std for standardization
        weights: numpy array of weights in the same order as FEATURE_VARIABLES
        model: either 'logistic' or 'linear'
    
    Returns:
        float: predicted Gini index value
    """
    try:
        # Convert inputs to numpy arrays
        X = np.array(X, dtype=float)
        describe = np.array(describe, dtype=float)
        weights = np.array(weights, dtype=float)
        
        # Validate shapes
        if len(X) != len(weights):
            raise ValueError(f"Feature vector length {len(X)} doesn't match weights length {len(weights)}")
        
        if describe.shape[0] != 2:
            raise ValueError(f"Describe array must have shape (2, n_features), got {describe.shape}")
        
        # Standardize features (except last 4 which are region indicators)
        X_standardized = np.zeros_like(X)
        for i in range(len(X)-4):
            std = describe[1,i]
            if std == 0:  # Handle zero standard deviation
                X_standardized[i] = 0  # If std is 0, all values are the same, so standardized value is 0
            else:
                X_standardized[i] = (X[i] - describe[0,i]) / std
        
        X_standardized[-4:] = X[-4:]  # Keep region indicators as is
        
        # Make prediction
        if model == 'linear':
            gini = np.dot(X_standardized, weights)
        elif model == 'logistic':
            dot_prod = np.dot(X_standardized, weights)
            # Handle potential overflow in exp
            if dot_prod > 100:  # exp(100) is already a very large number
                gini = 1.0
            elif dot_prod < -100:  # exp(-100) is very close to 0
                gini = 0.0
            else:
                gini = 1 / (1 + np.exp(-dot_prod))
        else:
            raise ValueError("Model must be 'linear' or 'logistic'")
        
        # Ensure gini is between 0 and 1
        gini = np.clip(gini, 0.0, 1.0)
        
        return float(gini)
        
    except Exception as e:
        current_app.logger.error(f"Error in predict_gini: {str(e)}")
        raise

# print(predict_gini(X, describe))