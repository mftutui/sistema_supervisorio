# Import the EV3-robot library
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ev3dev.ev3 import *
import ev3dev.ev3 as ev3
from time import sleep
from threading import Thread
from time import sleep
import threading
from math import sqrt
import sys

cor = ev3.ColorSensor();      assert cor.connected
cor.mode = 'COL-COLOR'  # intensidade da luz

# motors
me = ev3.LargeMotor('outB');  assert me.connected  # motor esquerdo
md = ev3.LargeMotor('outC');  assert md.connected  # motor direito

lcd = Screen()
smile = True

class Jogo:

    def __init__ (self):
        self.lista_inicial = ["1:3,5", "2:3,3", "3:5,3", "4:5,5", "5:2,3"]
        self.cores = ('unknown','black','blue','green','yellow','red','white','brown')

    def tela():
        lcd = Screen()
        smile = True

        while True:
            lcd.clear()
            # lcd.draw returns a PIL.ImageDraw handle
            lcd.draw.ellipse(( 20, 20,  60, 60))
            lcd.draw.ellipse((118, 20, 158, 60))
            lcd.draw.arc((20, 80, 158, 100), 0, 180)
            # Update lcd display
            lcd.update()
            sleep(1)

    def esquerda(self):
        md.run_timed(time_sp=3700, speed_sp=90)
        sleep(3)

    def direita(self):
        me.run_timed(time_sp=1500, speed_sp=90)
        md.run_timed(time_sp=1500, speed_sp=90)
        sleep(3)
        me.run_timed(time_sp=3500, speed_sp=90)
        sleep(3)

    def meia_direita(self):
        me.run_timed(time_sp=3500, speed_sp=90)
        sleep(3)

    def giro(self):
        me.run_timed(time_sp=4000, speed_sp=-400)
        md.run_timed(time_sp=4000, speed_sp=400)
        sleep(2)
        me.run_timed(time_sp=4000, speed_sp=400)
        md.run_timed(time_sp=4000, speed_sp=-400)

    def segue_preto(self):
        cor.mode = 'COL-COLOR'
        while True:
            if cor.value() != 3: #nao esta no verde
                target_value = cor.value()
                Kp = 15
                area_branca = 6
                area_preta = 1
                bPower = (area_branca - target_value) * Kp
                cPower =  (target_value - area_preta) * Kp
                me.run_timed(time_sp=200, speed_sp=cPower)
                md.run_timed(time_sp=200, speed_sp=bPower)
                sleep(0.2)
            else: break
                #para de andar!

    def toca_musica(self):
            while True:
                Sound.play('tokyo.wav').wait()
                sleep(1)

    def verifica_cor(self):
        cor.mode = 'COL-COLOR'
        while True:
            print(cor.value())
            sleep(0.2)

    def lista_cacas(self):
        aux = 0

        # Controle X,Y
        girou_direita = 0
        girou_esquerda = 0

        indice_anterior = 0

        # Ponto de partida do robo
        xA = 0
        yA = 0

        # Ainda têm caças a serem pegas
        while len(self.lista_inicial) != 0:

            # Tirar uma caça no meio da partida
            #if aux == 3:
                #self.lista_inicial = ["1:3,5", "2:3,3", "3:5,3", "4:5,5"]
                #print("A caca 5 ja foi pega!")
                #print("--------------------------------------")

            # Zerando a lista com as distancias entre o robô e as caças e a ordenada
            lista_distancias = []
            lista_ordenada = []

            # Cria uma lista com as distancias a partir da primeira lista recebida
            for item in self.lista_inicial:

                # Separa as informacoes das linhas da lista_inicial passada pelo SS
                #indice_lista = int(item.split(":")[0])
                ponto = str(item.split(":")[1])
                sxB = int(ponto.split(",")[0])
                syB = int(ponto.split(",")[1])

                # Distancia em int por pitagoras
                distAB = str(round(sqrt(((sxB - xA)**2) + ((syB - yA)**2)), 1))

                # Cria uma nova lista lista_distancias
                # onde o primeiro parametro é a distancia entre o ponto inicial os demais pontos
                if lista_distancias == []:
                    lista_distancias = [distAB + "." + item]
                else:
                    lista_distancias.append(distAB + "." + item)

                # Ordena essa lista da menor distância para a maior
                lista_ordenada = sorted(lista_distancias)

            # Separa a primeira linha da lista lista_ordenada
            # a primeira linha contém o ponto mais proximo do ponto inicial
            linha_lista = lista_ordenada[0]

            # Separo as informacoes da linha 0 para poder determinar o quanto é necessário andar
            # para chegar no ponto mais proximo
            indice = str(linha_lista[4])
            pontoxy = linha_lista.split(":")[1]
            xB = int(pontoxy.split(",")[0])
            yB = int(pontoxy.split(",")[1])

            # Tratando das caças
            # Já é a segunda rodada e já tenho um indice anterior
            if aux != 0:
                # Se tratando de uma nova caça
                if indice != indice_anterior:
                    # Se girou pra direita, volta pra esquerda
                    if girou_direita == 1:
                        robot.esquerda()
                        print("Voltou para a esquerda!")
                        girou_direita = 0
                    # Se girou pra esquerda, volta pra direita
                    elif girou_esquerda ==1:
                        robot.direita()
                        print("Voltou para a direita!")
                        girou_esquerda = 0

            indice_anterior = indice
            # Debug
            print("A caca " + indice + " e a caca mais proxima e esta no ponto " + pontoxy)
            print("-----------------------------------------------------------------------")

            # Repassando
            yAinicio = yA
            xAinicio = xA

            # Andar somente uma casa e depois verificar tudo outra vez

            # Anda pra cima/baixo
            anda_em_y = yB - yA

            # Vira pra direita/esquerda
            anda_em_x = xB - xA

            # If para andar em y
            if anda_em_y != 0:
                # Se maior ou igual a 1, anda para frente
                if anda_em_y >= 1:
                    print("Anda  1 casa pra frente")
                    yA = yA + 1
                    print("Estava no ponto " + str(xAinicio) + "," + str(yAinicio))
                    print("Ponto atual do robo " + str(xA) + "," + str(yA))
                    robot.segue_preto()
                    sleep(1)

                # Se menor que 1, anda para tras
                else:
                    print("Anda 1 casa pra tras")
                    yA = yA - 1
                    print("Estava no ponto " + str(xAinicio) + "," + str(yAinicio))
                    print("Ponto atual do robo " + str(xA) + "," + str(yA))
                    #robot.re()
                    robot.diteita()
                    robot.meia_direita()
                    robot.segue_preto()
                    sleep(1)

            # Caso a diferença em y seja igual a zero, anda em x
            else:
                # Se a diferença for diferente de 0
                if anda_em_x != 0:
                    # Se maior ou igual a 1, gira pra a direita e anda pra frente
                    if anda_em_x >= 1:
                        xA = xA + 1

                        # Controle do giro, que tem que ser "desfeito" ao fim da procura da caça
                        # Já girou = 1 ---- Não girou ainda = 0

                        # Se não girei, giro e ando
                        if girou_direita == 0:
                            print("Vai pra direita e pra frente")
                            girou_direita = 1
                            robot.direita()
                            sleep(2)
                            #robot.frente()
                            robot.segue_preto()
                            sleep(1)
                        # se ja girei, só ando
                        else:
                            #robot.frente()
                            robot.segue_preto()
                            sleep(1)
                            print("So anda pra frente")

                        print("Estava no ponto " + str(xAinicio) + "," + str(yAinicio))
                        print("Ponto atual do robo " + str(xA) + "," + str(yA))

                    # Se menor que 1, gira para a esquerda e anda pra frente
                    else:
                        print("Anda 1 casa pra esquerda")
                        xA = xA - 1

                        # Controle do giro, que tem que ser "desfeito" ao fim da procura da caça
                        # Já girou = 0 ---- Não girou ainda = 1

                        # Se não girei, giro e ando
                        if girou_esquerda == 0:
                            girou_esquerda = 1
                            print("Vai pra esquerda e pra frente")
                            robot.esquerda()
                            sleep(2)
                            #robot.frente()
                            robot.segue_preto()
                            sleep(1)

                        # Se ja girou, anda para frente
                        else:
                            print("So anda pra frente")
                            #robot.frente()
                            robot.segue_preto()
                            sleep(1)

                        print("Estava no ponto " + str(xAinicio) + "," + str(yAinicio))
                        print("Ponto atual do robo " + str(xA) + "," + str(yA))

                # Se a diferença em x seja 0 o robô chegou a caça procurada
                else:
                    print("Chegou na caca " + indice)
                    #print("Estava no ponto " + str(xAinicio) + "," + str(yAinicio))
                    print("Ponto atual do robo " + pontoxy)

                    # Remove a caça que acabou de encontrar da lista
                    # (Envia para o SS que envia para o SA e confirma)
                    self.lista_inicial.remove(indice + ":" + pontoxy)

                    print("--------------------------------------")

            # Tira a linha usada ??
            #lista_ordenada.pop(0)

            # Não tirar pq está sendo usado para outro fim além da gambiarra
            aux = aux + 1

        print("Acabou o jogo, todas as cacas foram pegas")

if __name__ == "__main__":
    robot = Jogo()

    t1 = threading.Thread(target=robot.lista_cacas)
    t2 = threading.Thread(target=robot.segue_preto)
    t3 = threading.Thread(target=robot.toca_musica)
    t4 = threading.Thread(target=robot.verifica_cor)
    t5 = threading.Thread(target=robot.tela)

    t1.start()  #lista_cacas
    #t2.start()  #segue_preto
    t3.start() #toca_musica
    #t4.start()  #verifica_cor --- degug
    t5.start()  #tela

    t1.join()
    #t2.join()
    t3.join()
    #t4.join()
    t5.join()
