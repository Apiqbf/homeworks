from flask import Flask,jsonify
from flasgger import Swagger

app=Flask(__name__)
swagger=Swagger(app)

@app.route("/")
def home():
    return "WELCOME"

@app.route('/sum')
def sum(a:int=5,b:int=7):
    return str(a+b)

@app.route("/huesos")
def h():
    return "HUESOS"

def my_task():
    result = sum(range(1, 1000000))
    return result

@app.route('/run-task')
def run_task():
    return jsonify({"status": "ok", "result": my_task()})

if __name__ == "__main__":
    app.run(port=5000)

