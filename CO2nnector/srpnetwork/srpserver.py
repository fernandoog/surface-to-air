# import tablib as tablib
# from flask_web_log import Log
from flask import Flask
from flask import request
import os
import json
import sqlite3

app = Flask(__name__)
app.config["LOG_TYPE"] = "CSV"
app.config
# Log(app)



app = Flask(__name__)







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

    # Guardar en base de datos
    return ''


# curl http://localhost:8888/data -H 'Content-Type: application/json' -d '{"from":1502402400.0, "to":1502405400.0}'  
@app.route('/data', methods=["GET", "POST"])
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


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8888, debug=True)
