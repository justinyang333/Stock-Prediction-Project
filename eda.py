import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import plotly.express as px


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
    data_status = {"Incomplete": 0, "Complete": 0}
    year_range = ["2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020"]
    for dir in os.listdir(path):
        if dir == '.DS_Store':
            continue
        complete_flag = True
        for y in year_range:
            complete_flag = complete_flag and (y + '.json') in os.listdir(path + dir)
        if complete_flag:
            data_status["Complete"] += 1
        elif not complete_flag:
            data_status["Incomplete"] += 1
    data_status = pd.DataFrame.from_dict(data_status, orient='index', columns=['count']).sort_index(axis=0)
    return px.bar(data_status, x=data_status.index, y='count', color=data_status.index, title='Count of Viable Stocks', labels={'count': 'Number of Stocks', 'index': 'Data Completeness'}, color_discrete_sequence=['green', 'red'])
            
            
            
    


