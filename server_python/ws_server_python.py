#!/usr/bin/python3
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from flask import url_for

from ev3dev.ev3 import *
from time import sleep

m_esq = LargeMotor('outA')
m_dir = LargeMotor('outD')

app = Flask(__name__)

@app.route("/re", methods=['GET'])
def re():

    m_esq.run_timed(time_sp=3000, speed_sp=-100)
    m_dir.run_timed(time_sp=3000, speed_sp=-100)
    print ('re')

    sleep(2)   # Give the motor time to move
    return "re"

@app.route ("/frente", methods =['GET'])
def frente():
    m_esq.run_timed(time_sp=3000, speed_sp=100) #ver se o 40 ta bom
    m_dir.run_timed(time_sp=3000, speed_sp=100)
    print ('frente')

    sleep(2)   # Give the motor time to move

    return "frente"

@app.route("/direita", methods = ['GET'])
def direita():
   m_esq.run_timed(time_sp=4000, speed_sp=90)
  # m_dir.run_timed(time_sp=3000, speed_sp=10)
   print ('direita')
   sleep(2)
   return "direita"


@app.route("/esquerda", methods = ['GET'])
def esquerda():
  # m_esq.run_timed(time_sp=3000, speed_sp=10)
   m_dir.run_timed(time_sp=4000, speed_sp=90)
   print ('esquerda')
   sleep(2)
   return "esquerda"


@app.route ("/", methods=['GET'])
def first_page():
    return "bem vindo"

if __name__ == "__main__":
    app.run('10.1.1.5')
