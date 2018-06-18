#!/usr/bin/env python3
from math import sqrt

class Pit:

    def demais_cacas(self, novo_xA, novo_yA, lista_ordenada):
        novo_lista_distancias = []

        # Proximas caças
        while len(lista_ordenada) != 0: # Tem que receber da funcao primeira_caca

            # Ordena a lista com -1 posicao
            for item in lista_ordenada:
                # Separa as informacoes da(s) linha(s)
                novo_indice = str(item[4])

                novo_ponto = str(item.split(":")[1])
                novo_item = (novo_indice + ":" + novo_ponto)
                novo_sxB = int(novo_ponto.split(",")[0])
                novo_syB = int(novo_ponto.split(",")[1])

                # Calcula a(s) distancia(s)
                novo_distAB = str(round(sqrt(((novo_sxB - novo_xA)**2) + ((novo_syB - novo_yA)**2)), 1))
                nova_linha = (novo_distAB + "." + novo_item)

                # Cria uma nova lista com a(s) distancas(s), incice(s) e ponto(s)
                if novo_lista_distancias == []:
                    novo_lista_distancias = [nova_linha]
                else:
                    novo_lista_distancias.append(nova_linha)

                # Ordena esta nova lista
                novo_lista_ordenada = sorted(novo_lista_distancias)

            # Separa a primeira linha da nova lista
            nova_linha = novo_lista_ordenada[0]


            # Manipula as informacoes para da linha
            novo_indice = str(nova_linha[4])
            novo_pontoxy = nova_linha.split(":")[1]
            pontox2 = int(novo_pontoxy.split(",")[0])
            pontoy2 = int(novo_pontoxy.split(",")[1])

            pontox1 = novo_xA # Tem que receber da funcao primeira_caca
            pontoy1 = novo_yA

            # Anda pra cima/baixo
            anda_em_y = pontoy2 - pontoy1

            if anda_em_y != 0:
                if anda_em_y >= 1:
                    anda_em_y = str(anda_em_y)
                    print("Anda " + anda_em_y + " casas pra cima")
                else:
                    anda_em_y = str(anda_em_y * (-1))
                    print("Anda " + anda_em_y + " casas pra baixo")
            else:
                print("Não anda nada em y")

            # Anda pra direita/esquerda
            anda_em_x = pontox2 - pontox1

            if anda_em_x != 0:
                if anda_em_x >= 1:
                    anda_em_x = str(anda_em_x)
                    print("Anda " + anda_em_x + " casas pra direita")
                else:
                    anda_em_x = str(anda_em_x * (-1))
                    print("Anda " + anda_em_x + " casas pra esquerda")
            else:
                print("Não anda nada em x")

            novo_xA = pontox2
            novo_yA = pontoy2

            print("Ponto atual do robo " + str(novo_xA) + "," + str(novo_yA))

            print("Chegou na caça " + novo_indice)

            novo_lista_ordenada.pop(0)

            lista_ordenada = novo_lista_ordenada

            novo_lista_distancias = []


    def primeira_caca(self):

        lista_inicial = ["1:3,5", "2:3,3", "3:5,3", "4:5,5", "5:2,3"]
        lista_distancias = []

        # Ponto de partida do robo
        xA = 1
        yA = 3

        # Cria uma lista ordenada a partir da primeira lista recebida
        for item in lista_inicial:

            # Separa as informacoes das linhas da lista_inicial passada pelo SS
            indice = int(item.split(":")[0])
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

        # Separo as informacoes da linha 0
        # para poder determinar o quanto é necessário andar
        # para chegar no ponto mair proximo
        indice = str(linha_lista[4])
        pontoxy = linha_lista.split(":")[1]
        pontox2 = int(pontoxy.split(",")[0])
        pontoy2 = int(pontoxy.split(",")[1])

        pontox1 = xA
        pontoy1 = yA

        # Anda pra cima/baixo
        anda_em_y = pontoy2 - pontoy1
        if anda_em_y != 0:
            if anda_em_y >= 1:
                anda_em_y = str(anda_em_y)
                print("Anda " + anda_em_y + " casas pra cima")
            else:
                anda_em_y = str(anda_em_y * (-1))
                print("Anda " + anda_em_y + " casas pra baixo")
        else:
            print("Não anda nada em y")

        # Anda pra direita/esquerda
        anda_em_x = pontox2 - xA
        if anda_em_x != 0:
            if anda_em_x >= 1:
                anda_em_x = str(anda_em_x)
                print("Anda " + anda_em_x + " casas pra direita")
            else:
                anda_em_x = str(anda_em_x * (-1))
                print("Anda " + anda_em_x + " casas pra esquerda")
        else:
            print("Não anda nada em x")

        # Novo ponto atual
        ponto_atual_x = pontox1 + int(anda_em_x)
        ponto_atual_y = pontoy1 + int(anda_em_y)
        print("Ponto atual do robo " + str(ponto_atual_x) + "," + str(ponto_atual_y))

        # Chehou na caça X
        print("Chegou na caça " + indice)

        # Tira a linha usada
        lista_ordenada.pop(0)

        # tem que retornar a lista e o novo ponto X e Y
        self.demais_cacas(ponto_atual_x, ponto_atual_y, lista_ordenada)

if __name__ == "__main__":
    robot = Pit()
    robot.primeira_caca()
