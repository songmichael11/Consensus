import numpy as np
import math

import pandas as pd


def log_regress(X, y, w, alpha = 0.5, max_iter = 1000):
    runalg = True
    i = 0
    iter = 0

    while runalg:
        x = X[i]
        dot_prod = np.dot(x, w)
        y_hat = 1 / (1 + np.exp(-dot_prod))
        gradient = (y_hat - y[i]) * x
        w = w - alpha * gradient
        i += 1
        if i >= len(y):
            i = 0
            iter += 1
        if iter > max_iter:
            print(iter)
            runalg = False
            break
    
    return w
