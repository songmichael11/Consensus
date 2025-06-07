import numpy as np
import pandas as pd
from flask import Blueprint, jsonify, request, current_app

def predict_gini(X, describe, weights, model='logistic'):
    # current_app.logger.info(X.size)
    # current_app.logger.info(describe.size)
    # current_app.logger.info(weights.size)

    X = np.hstack([[(X[i] - describe[0,i]) / describe[1,i] for i in range(len(X)-4)], X[-4:]])
    if model == 'linear':
        gini = np.dot(X, weights)
    elif model == 'logistic':
        gini = 1 / (1 + np.exp(-np.dot(X, weights)))
    return gini

# print(predict_gini(X, describe))