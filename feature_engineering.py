import pandas as pd
import numpy as np
import sklearn
import matplotlib.pyplot as plt


def log_volume(data):
    data['log_volume'] = np.log(data['Volume'])
    return data

