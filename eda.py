import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import plotly.express as px
import json


def plot_year_distribution(path: str):
    yearly_count = {}
    for dir in os.listdir(path):
        if dir == '.DS_Store':
            continue
        for file in os.listdir(path + dir):
            year = file.split('.')[0]
            if year in yearly_count.keys():
                yearly_count[year] += 1
            else:
                yearly_count[year] = 1
    yearly_count = pd.DataFrame.from_dict(yearly_count, orient='index', columns=['count']).sort_index(axis=0)
    return px.bar(yearly_count, x=yearly_count.index, y='count', title='Yearly Distribution of Stock Information')


def plot_data_viability(path: str):
    data_status = {"Complete" : 0, "Missing Years" : 0, "Missing Days Within Years" : 0}
    year_range = ["2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020"]
    for dir in os.listdir(path):
        if dir == '.DS_Store':
            continue
        complete_flag = True
        files = os.listdir(path + dir)
        for y in year_range:
            complete_flag = (complete_flag) and ((y + '.json') in files)
        if complete_flag:
            entry_count = 0
            for y in year_range:
                try:
                    entry_count += len(json.load(open(path + dir + '/' + y + '.json', 'r'))['o'])
                except KeyError as ke:
                    continue
            if entry_count == 3021:
                data_status["Complete"] += 1
            else:
                data_status["Missing Days Within Years"] += 1
        elif not complete_flag:
            data_status["Missing Years"] += 1
    data_status = pd.DataFrame.from_dict(data_status, orient='index', columns=['count']).sort_index(axis=0)
    return px.bar(data_status, x=data_status.index, y='count', color=data_status.index, title='Count of Viable Stocks', labels={'count': 'Number of Stocks', 'index': 'Data Completeness'}, color_discrete_sequence=['green', 'gold', 'red'])
            

def add_sector_and_industry(df: pd.DataFrame):
    stock_export = pd.read_csv('./data_collection/nasdaq_stock_export.csv')
    df['Sector'] = df['Symbol'].map(stock_export.set_index('Symbol')['Sector'])
    df['Industry'] = df['Symbol'].map(stock_export.set_index('Symbol')['Industry'])
    return df

def bound_data(data: pd.DataFrame, lower_bound: int, upper_bound: int):
    stock_groups = data.groupby('Symbol').describe()
    lower = stock_groups['Open']["min"] > lower_bound
    upper = stock_groups['Open']["max"] < upper_bound
    bounded = stock_groups[lower & upper]
    return data[data["Symbol"].isin(bounded.index.to_list())]

def plot_open_boxes(unbounded: pd.DataFrame, bounded: pd.DataFrame):
    fig, ax = plt.subplots(1, 2)
    ax[0] = unbounded.plot(kind='box', y='Open', ax=ax[0])
    ax[0].set_title('Open Price Distribution Before Bounding')
    ax[0].set_xlabel('Open Price')
    ax[0].set_ylabel('Frequency')
    ax[1] = bounded.plot(kind='box', y='Open', ax=ax[1])
    ax[1].set_title('Open Price Distribution After Bounding')
    ax[1].set_xlabel('Open Price')
    ax[1].set_ylabel('Frequency')
    return fig, ax


def plot_sector_distribution(df: pd.DataFrame):
    sector_group = df.groupby('Sector')['Symbol'].count() // 2769
    return px.bar(sector_group, x=sector_group.index, y='Symbol', title='Sector Distribution of Stocks')
            

def plot_sector_value_distribution(df: pd.DataFrame):
    sector_group = df.groupby(['Sector', 'Symbol']).agg({'Open': 'mean'}).reset_index()
    return sns.displot(sector_group, x='Open', hue='Sector', kind='kde', fill=True, height=10, aspect=1.5).set(title='Sector Distribution of Mean Open Prices ($)', xlabel='Average Stock Open Price ($)', ylabel='Density')

def create_daily_movements(df: pd.DataFrame):
    symbol_groups = df.groupby('Symbol')
    percent_changes = []
    for symbol, group in symbol_groups:
        print(symbol)
        percent_changes.append(pd.DataFrame({symbol : group['Open'].pct_change().reset_index(drop=True)}))
    return pd.concat(percent_changes, axis=1)

if __name__ == '__main__':
    path = './data/unprocessed/'
    # plot_year_distribution(path).show()
    plot_data_viability(path)
    
            
    


