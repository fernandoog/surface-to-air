# Regression Example With Boston Dataset: Standardized and Larger
from pandas import read_csv
from keras.models import Sequential
from keras.layers import Dense
# from keras.wrappers.scikit_learn import KerasRegressor
from keras.models import load_model
# from sklearn.model_selection import cross_val_score
# from sklearn.model_selection import KFold
# from sklearn.preprocessing import StandardScaler
# from sklearn.pipeline import Pipeline

import sqlite3
import pandas as pd



loaded_model = load_model('my_model_pruebas.h5')

df2 = pd.DataFrame([[651984,1.00222,-3.6474747575],[0.3,1.6,-7.8]])

df3 = pd.read_csv('file_m.csv')

import pdb; pdb.set_trace()