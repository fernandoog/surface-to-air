# import tablib as tablib
# from flask_web_log import Log
from flask import Flask
from flask import request
from flask import render_template
import os
import json
import sqlite3
from flask_cors import CORS, cross_origin
import datetime
from keras.models import load_model
import numpy as np
import pandas as pd

app = Flask(__name__)
app.config["LOG_TYPE"] = "CSV"
app.config
# Log(app)



app = Flask(__name__)
CORS(app, support_credentials=True)



loaded_model = load_model('../prediction/my_model.h5')
loaded_model._make_predict_function()

# dataset = tablib.Dataset()
# with open(os.path.join(os.path.dirname(__file__), 'flask-web-log.csv')) as f:
#     dataset.csv = f.read()


@app.route("/")
def root():
    print('hola')
    # return


# curl http://localhost:8888/sensor -H 'Content-Type: application/json' -d '{"time":1502402400.0, "latitude":1502505400.0, "longitud":5555, "value":11.2}'
@app.route('/sensor', methods=["POST"])
def sensor():
    data_received = request.get_json()


    print(data_received)

    # conn = sqlite3.connect("../data/database.db")
    # cursor = conn.cursor()
    # query_str = "SELECT * FROM VisualData WHERE time BETWEEN {f} AND {t};".format(f=from_ts, t=to_ts)
    # query = cursor.execute(query_str)

    # Guardar en base de datos
    return ''


# curl http://localhost:8888/data -H 'Content-Type: application/json' -d '{"from":1502402400.0, "to":1502405400.0}' 
@app.route('/data', methods=["GET", "POST", "OPTIONS"])
@cross_origin(supports_credentials=True)
def data():

    data_received = request.get_json()

    from_ts = data_received['from']
    to_ts = data_received['to']

    conn = sqlite3.connect("../data/database.db")
    cursor = conn.cursor()
    query_str = "SELECT * FROM VisualData WHERE time BETWEEN {f} AND {t};".format(f=from_ts, t=to_ts)
    query = cursor.execute(query_str)
    data = query.fetchall()
    
    return json.dumps(data)


@app.route('/data_prediction', methods=["GET", "POST", "OPTIONS"])
@cross_origin(supports_credentials=True)
def data_prediction():

    data_received = request.get_json()
    data = []

    if 'positions' in data_received:

        # {'lat': 33.58487928182987, 'lng': -117.79541015625001}]}

        time = data_received['to']
        # from_str = data_received['from']
        positions = data_received['positions']


        x = []

        for i in range(len(positions)):
            x.append([time, positions[i]['lat'], positions[i]['lng']])

        # x = np.array(x)
        

        df2 = pd.DataFrame(x)

        str_csv = 'csvdatos{}'.format(datetime.datetime.now().timestamp())
        df2.to_csv('{}'.format(str_csv))



        df3 = pd.read_csv(str_csv)

        x_final = df3[['0','1','2']].values
        # x = df[['time', 'latitude', 'longitude']].values

        # print(data_received['from'])

        import pdb; pdb.set_trace()

        # print(data_received)
        # Cargamos modelo

        print("Realizando predicciones")
        
        # predecimos
        # loaded_model.predict(df2[[0,1,2]].values)
        predictions = loaded_model.predict(x)
        print("hechas")

    
        # data = []
        for i in range(len(predictions)):
            data.append([to_str, positions[i]['lat'], positions[i]['lng'], predictions[i]])

    # numpy.ndarray

    # import pdb; pdb.set_trace()

    return json.dumps(data)



@app.route('/sensor_to_view')
def sensor_to_view():

    # data_received = request.get_json()

    # from_ts = data_received['from']
    # to_ts = data_received['to']

    # conn = sqlite3.connect("../data/database.db")
    # cursor = conn.cursor()
    # query_str = "SELECT * FROM VisualData WHERE time BETWEEN {f} AND {t};".format(f=from_ts, t=to_ts)
    # query = cursor.execute(query_str)

    conn = sqlite3.connect("../data/database.db")
    cursor = conn.cursor()



     # Hasta que inserte los datos el sensor

    import random

    query_str = "INSERT INTO VisualData_Sensor VALUES({time}, {latitude}, {longitude}, {value});".format(time=datetime.datetime.now().timestamp(),latitude=0,longitude=0,value=random.randrange(200, 250)/10)
    query = cursor.execute(query_str)
    conn.commit()


    query_str = "SELECT value FROM VisualData_Sensor ORDER BY time DESC LIMIT 10;"
    query = cursor.execute(query_str)

    data = query.fetchall()
    y = data[::-1]
    x = [x for x in range(len(y))]

    print(data)
    data = {'x':x, 'y':y}


    # data = query.fetchall()
    
    return json.dumps(data)



@app.route('/view')
def view():
    return render_template("index.html")




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8888, debug=True)


