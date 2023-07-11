import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error


def get_dataset():
    data = pd.read_csv('./data/dataset.csv')
    data = data[data['Symbol'] == 'AAPL']
    data = data[0:200].reset_index(drop=True)
    data = data[["Date", "Open", "High", "Low", "Close", "Volume"]]
    data["Date"] = pd.to_datetime(data["Date"]).astype('category')
    X, y = data[["Date", "High", "Low", "Close", "Volume"]], data[["Open"]]
    print(X)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, train_size=0.8, shuffle=False)
    return X_train, X_test, y_train, y_test


def run_xgboost(X_train, X_test, y_train):
    print(1)
    dtrain_reg = xgb.DMatrix(X_train, label=y_train, enable_categorical=True)
    print(2)
    xgb_model = xgb.train({'objective': 'reg:squarederror'}, dtrain_reg, num_boost_round=100)
    print(3)
    y_pred = xgb_model.predict(X_test)
    return y_pred


def plot_rmse():
    boost_nums = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    rmses = {"AAPL" : [], "AMD" : [], "INTC" : []}

    for symbol in list(rmses.keys()):
        for n in boost_nums:
            X_train, X_test, y_train, y_test = get_dataset(symbol)
            predictions = run_xgboost(X_train, X_test, y_train, y_test, num_boost_round=n)
            rmses[symbol].append(mean_squared_error(predictions, y_test))

    df = pd.DataFrame(data=rmses)
    df["Boost Nums"] = boost_nums
    df.plot(kind="line", x="Boost Nums", y=["AAPL", "AMD", "INTC"], figsize=(15, 5), ylim=(0, 1), xlabel="Number of Boost Rounds", ylabel="Root Mean Squared Error", title="RMSE Against Number of Boost Rounds")
    
    

    