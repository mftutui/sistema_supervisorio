# Import the EV3-robot library
from ev3dev.ev3 import *
import ev3dev.ev3 as ev3
from time import sleep
import threading
import sys
import time

luz = ev3.ColorSensor();      assert luz.connected
cor = ev3.ColorSensor();      assert cor.connected
me = ev3.LargeMotor('outA');  assert me.connected  # motor esquerdo
md = ev3.LargeMotor('outD');  assert md.connected  # motor direito

gy = GyroSensor()
assert gy.connected, "Connect a single gyro sensor to any sensor port"

luz.mode = 'COL-REFLECT'  # intensidade da luz
cor.mode = 'COL-COLOR'    # deteccao de cores
cores = ('unknown','black','blue','green','yellow','red','white','brown')

gy.mode = 'GYRO-ANG'
gy.mode = 'GYRO-RATE'
gy.mode = 'GYRO-ANG'
units = gy.units

#class segueLinha:
#angle_u = 0

#class WorkerThread(threading.Thread):

#    def __init__(self):
#        super(WorkerThread, self).__init__()
#        self._is_interrupted = False
#
#    def stop(self):
#         self._is_interrupted = True
#
#    def run(self):
#
#    def __init__(self, broker):
#        self.thread = WorkerThread()
#        self.thread.start()

def esquerda():
    md.run_timed(time_sp=3700, speed_sp=90)
    sleep(2)
def direita():
    me.run_timed(time_sp=1500, speed_sp=90)
    md.run_timed(time_sp=1500, speed_sp=90)
    sleep(2)
    me.run_timed(time_sp=3500, speed_sp=90)
    sleep(2)

    # Main method
def alinha():
    while True:
        time.sleep(0.3)
        angle_u = gy.value()
        print(angle_inicial)

        angle = gy.value()
        print(angle)


        if (angle != angle_u):
            while (angle > angle_u):
                print(str(angle))
                md.run_timed(time_sp=80,speed_sp=80)
                angle = gy.value()
                if angle == angle_inicial:
                    print("Alinhou!")
                    break

            while (angle < angle_u):
                print(str(angle))
                me.run_timed(time_sp=80,speed_sp=80)
                angle = gy.value()
                if angle == angle_inicial:
                  print("Alinhou!")
                  break

def segue():
    speed = 360/4  # deg/sec, [-1000, 1000]
    dt = 80       # milliseconds
    stop_action = "coast"

    # PID tuning
    Kp = 1  # proportional gain
    Ki = 0  # integral gain
    Kd = 0  # derivative gain

    integral = 0
    previous_error = 0

    # primeiro valor lido pelo sensor
    target_value = luz.value()

    while True:

        # calculando a direção com PID
        error = target_value - luz.value()
        integral += (error * dt)
        derivative = (error - previous_error) / dt

        # u zero:     on target,  drive forward
        # u positive: too bright, turn right
        # u negative: too dark,   turn left

        u = (Kp * error) + (Ki * integral) + (Kd * derivative)
        #angle_u = gy.value()
        print(u)

        # limit u to safe values: [-1000, 1000] deg/sec
        if speed + abs(u) > 1000:
            if u >= 0:
                u = 1000 - speed
            else:
                u = speed - 1000

        # run motors
        if u >= 0:
            me.run_timed(time_sp=dt, speed_sp=speed + u, stop_action=stop_action)
            md.run_timed(time_sp=dt, speed_sp=speed - u, stop_action=stop_action)
            sleep(dt / 1000)
        else:
            me.run_timed(time_sp=dt, speed_sp=speed - u, stop_action=stop_action)
            md.run_timed(time_sp=dt, speed_sp=speed + u, stop_action=stop_action)
            sleep(dt / 1000)

        previous_error = error

            #print(cores[cor.value()]) # printa a cor no console

            #if (cores[cor.value()] == 'green'):
            #    print("verde")
            #    #self.esquerda()
            #    sleep(2)
            #elif (cores[cor.value()] == 'yellow'):
            #    #self.direita()
            #    print("amarelo")
            #    sleep(2)
            #time.sleep(0.3)

def sai():
    while True:
        if (cores[cor.value()] == 'green'):
            print("verde")
            sys.exit()
        time.sleep(0.3)

t1 = threading.Thread(target=segue)
t2 = threading.Thread(target=alinha)
t3 = threading.Thread(target=sai)

t1.start()
t2.start()
t3.start()

t1.join()
t2.join()
t3.join()

# Main
#if __name__ == "__main__":
#    robot = segueLinha()
#    robot.segue()
