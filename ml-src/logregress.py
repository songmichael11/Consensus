import numpy as np
import math

import pandas as pd

data = {
    'Hours_Studied': [1, 2, 3, 4, 5, 1, 2, 3, 4, 5],
    'Attendance':    [0, 0, 0, 1, 1, 1, 0, 1, 1, 1],
    'Passed':        [0, 0, 0, 1, 1, 0, 0, 1, 1, 1]
}

df = pd.DataFrame(data)

X = df[['Hours_Studied', 'Attendance']].to_numpy()
X = np.hstack((np.ones((X.shape[0], 1)), X))
y = df['Passed'].to_numpy()
w = [0,-1,1]

def logregress(X, y, w, alpha = 0.5, max_iter = 1000):
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

weights = logregress(X,y,w)
predictions = []
for i in range(len(y)):
    x = X[i]
    dot_prod = np.dot(x, weights)
    y_hat = 1 / (1 + np.exp(-dot_prod))
    if y_hat > 0.5:
        predictions.append(1)
    else:
        predictions.append(0)
print(predictions)
