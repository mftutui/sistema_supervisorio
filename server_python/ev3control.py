#ev3control.py
from ev3dev.ev3 import *
from time import sleep

m_esq = LargeMotor('outA')
m_dir = LargeMotor('outD')
class EV3Manual(object):
    #def __init__(self, motor1, motor2):
     #   m_esq = LargeMotor(motor1)
      #  m_dir = LargeMotor(motor2)

    def re(self):
        m_esq.run_timed(time_sp=3000, speed_sp=-400)
        m_dir.run_timed(time_sp=3000, speed_sp=-400)
        sleep(2)

    def frente(self):
        m_esq.run_timed(time_sp=3000, speed_sp=400)
        m_dir.run_timed(time_sp=3000, speed_sp=400)
        sleep(2)

    def direita(self):
        m_esq.run_timed(time_sp=3350, speed_sp=90)
        sleep(2)

    def esquerda(self):
        m_dir.run_timed(time_sp=3350, speed_sp=90)
        sleep(2)
