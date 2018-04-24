#!/usr/bin/python3
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from flask import url_for
from ev3control import *


motor = EV3Manual()

app = Flask(__name__)

@app.route("/re", methods=['GET'])
def re():

        motor.re()
        return "re"

@app.route ("/frente", methods =['GET'])
def frente():
        motor.frente()
        return "frente"

@app.route("/direita", methods = ['GET'])
def direita():
        motor.direita()
        return "direita"


@app.route("/esquerda", methods = ['GET'])
def esquerda():
        motor.esquerda()
        return "esquerda"


@app.route ("/", methods=['GET'])
def first_page():
        return "bem vindo"

if __name__ == "__main__":
    app.run('192.168.1.14')
