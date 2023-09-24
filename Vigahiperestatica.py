import numpy as np
import matplotlib.pyplot as plt
import math
from Contexto import *
from Diferencas_finitas import *
from Eq3momentos import *
from Calcula_momentos_por_trecho import *

class Vigahiperestatica:
    def __init__(self, lista_comprimentos =None,lista_cargas_q= None, carga_q = None, lista_reações = None, b = None, h= None, fck= None):
        self.b = b
        self.h = h
        self.lista_comprimentos = lista_comprimentos
        self.carga_q = carga_q
        self.lista_reações = lista_reações
        self.lista_eq_momento_por_trecho = None
        self.lista_comprimentos_acumulados_viga = None
        self.Ecs = 0
        self.fck = 30
        self.lista_cargas_q = lista_cargas_q
        self.I = None
    def calcula_momento_de_inercia(self):
        I = (self.b * (self.h **3) )/ 12
        #print(I)
        self.I = I
    def calculo_modulo_elasticidade(self):
        # de 20 até 50 MPa
        Eci = 0.9 * 5600 * math.sqrt(self.fck)
        alfa =  0.8 + 0.2 * self.fck/80
        self.Ecs = (Eci * alfa)
        print(f'O Ecs é {self.Ecs}')
        #print(self.Ecs)
    def apply(self):
        self.calcula_momento_de_inercia()
        self.calculo_modulo_elasticidade()
class Calcula_momentos_por_trecho(Vigahiperestatica):
    def __init__(self,viga):
        self.viga = viga
        self.x_acumulado = None
        self.lista_L_acumulados = None
        self.comprimento_acumulado = None
        self.termo_inde_acumulado = None
        self.lista_eq_momento = None
        self.acumulado_l = None
        self.comprimento_acumulado_invertido = None
        self.lista_comprimento_acumulado_vaos_meio = []
        self.lista_comprimento_acumulado_invertido = []
        self.scatter_x = []
        self.scatter_y_momento = []
        self.scatter_y_cortante = []
        Vigahiperestatica.__init__(self, viga)
    def calcula_comprimentos_acumulados(self):
        self.lista_L_acumulados = []
        self.acumulado_L=[]
        for i in range(0, len(self.viga.lista_comprimentos)):
            if i == 0:
                self.comprimento_acumulado = 0
            else:
                self.comprimento_acumulado = self.comprimento_acumulado + self.viga.lista_comprimentos[i]
            self.lista_L_acumulados.append(self.comprimento_acumulado)
        self.viga.lista_comprimentos_acumulados_viga = self.lista_L_acumulados
        # print(self.lista_L_acumulados)


        for i in range(0, len(self.viga.lista_comprimentos)+1):
            acumulado = 0
            for y in range(0,i):
                #print('------------------')
                #print(y)
                #print(self.viga.lista_comprimentos[y])
                acumulado = acumulado + self.viga.lista_comprimentos[y]
            #print(acumulado)
            self.acumulado_L.append(acumulado)


        L= 0
        for i in range (0,len(self.viga.lista_comprimentos)-1):
            x = 0
            for y in range (L,len(self.viga.lista_comprimentos)-1):
                #print(y)
                x += self.viga.lista_comprimentos[y]
            L += 1
            self.lista_comprimento_acumulado_invertido.append(x)
        self.lista_comprimento_acumulado_invertido.append(0)
        #print(self.lista_comprimento_acumulado_invertido)
        L = len(self.viga.lista_comprimentos)
        for i in range(0, len(self.viga.lista_comprimentos)):
            x = 0
            for y in range(0, L):
                # print(y)
                x += self.viga.lista_comprimentos[y]
            L -= 1
            self.lista_comprimento_acumulado_vaos_meio.append(x)
        self.lista_comprimento_acumulado_vaos_meio.append(0)

    def imprime_equações_momentos(self):
        print('-------EQUAÇÕES DOS MOMENTOS POR TRECHO-------')
        for i in range(0, len(self.viga.lista_comprimentos)):
            X = len(self.viga.lista_comprimentos) -i

            print(f'Equação do momento no trecho {X} é:')
            print(f'{self.lista_eq_LE[i][2]}x² + {self.lista_eq_LE[i][1]}x + 1.({self.lista_eq_LE[i][0]})')
            print('      ')


    def gera_equacoes_momentos_por_trecho(self):
        self.lista_eq_LE=[]
        L = 0
        V = len(self.viga.lista_comprimentos)-1
        x_acumulado = 0
        # for de traz para frente, começando no número de elementos da lista com os comprimentos
        # for da equação
        for i in range(len(self.viga.lista_comprimentos),0,-1 ):
            #print(i)
            LE=[]
            #variável que acumula o termo independente
            self.termo_inde_acumulado = 0
            #variável que acumula x^1
            self.x_acumulado = 0
            k = 0
            L_acumulado_trecho = 0
            fim = -1
            # for das reações
            for j in range(L, len(self.viga.lista_comprimentos)):
                # o X1 é a posição do último trecho antes do trecho analisado, pois o comprimento no trecho analisado será X
                X1 = len(self.viga.lista_comprimentos)-L-2

                L_acumulado_trecho = 0
                # calcula o comprimento acumulado que deve ser multiplicado pela reação
                # a reação vai da esquerda da direita (começa no primeiro apoio e vai até o último)
                # o comprimento deve ser o analisado da direita para a esquerda
                # somando o L de cada trecho até a reação
                # então o comprimento acumulado é a soma dos comprimentos do trecho analisado até o trecho da reação
                # isso deve ser feito para toda reação por isso mais um for
                # FOR DA REAÇÃO
                # O X1 é o trecho analisado e o fim é a reação. O X1 se mantém para o trecho e o fim aumenta a cada reação
                for _k in range(X1,fim,-1):
                    L_acumulado_trecho+=self.viga.lista_comprimentos[_k]
                fim = fim +1

                termo_inde = self.viga.lista_reações[k] * L_acumulado_trecho
                #o x é a reação
                x = self.viga.lista_reações[k]
                #acumula os valores
                self.x_acumulado += x
                self.termo_inde_acumulado += termo_inde
                # aumenta o K para que no próxima iteração seja obtido o valor correto da reação
                k=k+1
            #calcula o termo da carga

            termo_inde_carga = self.viga.carga_q * self.acumulado_L[V]**2/2
            #print('---------------------------------')
            #print(self.acumulado_L)
            #print(self.acumulado_L[V])
            #print(V)
            x_carga = self.viga.carga_q * self.acumulado_L[V]
            x_2 = -self.viga.carga_q/2
            # o L aumenta, cada vez o número de reações é maior
            L=L+1
            # o V diminui para combinar a carga distribuída com o comprimento toral
            V=V-1
            self.x_acumulado -= x_carga
            self.termo_inde_acumulado -= termo_inde_carga
            LE.append(self.termo_inde_acumulado)
            LE.append(self.x_acumulado)
            LE.append(x_2)
            self.lista_eq_LE.append(LE)
        self.viga.lista_eq_momento_por_trecho = self.lista_eq_LE

        self.imprime_equações_momentos()

        #print("Os polinômios que representam a equação dos momentos por trecho são")
        #print("(do último para o primeiro trecho):",self.lista_eq_LE)
    def gera_diagrama_momento_fletor(self):


        EqM = 0

        for i in range(len(self.viga.lista_comprimentos)-1,-1,-1):
            for j in range(0, (self.viga.lista_comprimentos[EqM]+1)):

                momento_fletor = self.lista_eq_LE[i][0] + self.lista_eq_LE[i][1]*j +self.lista_eq_LE[i][2]*(j**2)
                cortante = self.lista_eq_LE[i][1] + self.lista_eq_LE[i][2]*2*j

                j = j +self.acumulado_L[EqM]
                #print(self.acumulado_L)
                #print(j)
                self.scatter_x.append(j)
                self.scatter_y_momento.append(momento_fletor)
                self.scatter_y_cortante.append(cortante)
            EqM += 1
        #print(self.scatter_x)
        plt.gca().invert_yaxis()
        plt.plot(self.scatter_x, self.scatter_y_momento)
        plt.plot()
        plt.title('Momento fletor ao longo da viga ')
        plt.xlabel('x (m)')
        plt.ylabel('Momento fletor (kNm)')
        plt.show()
        plt.plot(self.scatter_x, self.scatter_y_cortante)
        plt.title('Força cortante ao longo da viga ')
        plt.xlabel('x (m)')
        plt.ylabel('Força cortante (kN)')
        plt.plot()
        plt.show()

    def apply(self):
        self.calcula_comprimentos_acumulados()
        self.gera_equacoes_momentos_por_trecho()
        self.gera_diagrama_momento_fletor()