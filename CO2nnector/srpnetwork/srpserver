import tablib as tablib
from flask_web_log import Log
from flask import Flask
import os

app = Flask(__name__)
app.config["LOG_TYPE"] = "CSV"
app.config
Log(app)

app = Flask(__name__)
dataset = tablib.Dataset()
with open(os.path.join(os.path.dirname(__file__), 'flask-web-log.csv')) as f:
    dataset.csv = f.read()


@app.route('/sensor', methods=["POST"])
def sensor():
    return


@app.route("/data")
def data():
    return dataset.html


if __name__ == "__main__":
    app.run()
