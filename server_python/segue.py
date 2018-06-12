# Import the EV3-robot library
from ev3dev.ev3 import *
import ev3dev.ev3 as ev3
from time import sleep
from threading import Thread

luz = ev3.ColorSensor();      assert luz.connected
cor = ev3.ColorSensor();      assert cor.connected

luz.mode = 'COL-REFLECT'  # intensidade da luz
cor.mode= 'COL-COLOR' # deteccao de cores
cores=('unknown','black','blue','green','yellow','red','white','brown')

# motors
me = ev3.LargeMotor('outB');  assert me.connected  # motor esquerdo
md = ev3.LargeMotor('outC');  assert md.connected  # motor direito

class segueLinha:

    def esquerda(self):
        me.run_timed(time_sp=3350, speed_sp=-90)
        sleep(2)

    def direita(self):
        md.run_timed(time_sp=3350, speed_sp=90)
        sleep(2)

    # Main method
    def segue(self):

        speed = 360/4  # deg/sec, [-1000, 1000]
        dt = 500       # milliseconds
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

            print(cores[cor.value()]) # printa a cor no console

            if (cores[cor.value()] == 'green'):
                sleep(2) # degub
                self.esquerda()
            elif (cores[cor.value()] == 'yellow'):
                Sound.speak(cores[cor.value()]).wait() # debug
                self.direita()

# Main
if __name__ == "__main__":
    robot = segueLinha()
    robot.segue()
