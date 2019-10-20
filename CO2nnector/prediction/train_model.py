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

# load dataset
dataframe = read_csv("housing.data", delim_whitespace=True, header=None)
dataset = dataframe.values
# split into input (X) and output (Y) variables
X1 = dataset[:,0:13]
Y1 = dataset[:,13]





conn = sqlite3.connect("../data/database.db")
# cursor = conn.cursor()
query_str = "SELECT * FROM VisualData;"
# query = cursor.execute(query_str)
# data = query.fetchall()

df = pd.read_sql_query(query_str, conn)
X = df[['time', 'latitude', 'longitude']].values
Y = df.value.values

import pdb; pdb.set_trace()
# Creamos modelo
model = Sequential()
model.add(Dense(3, input_dim=3, kernel_initializer='normal', activation='relu'))
model.add(Dense(2, kernel_initializer='normal', activation='relu'))
model.add(Dense(1, kernel_initializer='normal'))
model.compile(loss='mean_squared_error', optimizer='adam')


#Entrenamos
model.fit(X, Y, batch_size=5, epochs=10, verbose=1)



# https://jovianlin.io/saving-loading-keras-models/
# Guardamos modelo
model.save('my_model.h5')

# Deletes the existing model
del model  


# # Cargamos modelo
# loaded_model = load_model('my_model.h5')
# # predecimos
# predictions = loaded_model.predict(X)
