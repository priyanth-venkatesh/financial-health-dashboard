from sklearn.linear_model import LinearRegression
import numpy as np


def simple_forecast(values):
    X = np.arange(len(values)).reshape(-1, 1)
    y = np.array(values)

    model = LinearRegression().fit(X, y)

    future_x = np.array([[len(values)]])
    prediction = model.predict(future_x)[0]

    return float(prediction)