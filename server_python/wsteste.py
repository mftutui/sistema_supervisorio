#!/usr/bin/python
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from flask import url_for

app = Flask(__name__)

@app.route("/", methods=['GET'])
def hello():
    return "Hello World!"

@app.route ("/teste", methods =['GET'])
def caminho():
    return "Caminho"

@app.route ("/soma", methods=['GET'])
def soma():
    return "soma" 

if __name__ == "__main__":
    app.run()
