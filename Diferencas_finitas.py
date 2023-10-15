import numpy as np
import matplotlib.pyplot as plt
import math
from Contexto import *
from Calcula_momentos_por_trecho import *
from Eq3momentos import *
from Vigahiperestatica import *

class Diferencas_finitas(Vigahiperestatica):
    def __init__(self, viga):
        self.viga = viga
        self.passo = 0.001
        self.matriz_segunda_derivada = None
        self.matriz_momento_dividido_por_EI = None
        self.resultados_deformação = None
        self.deflexoes = []
        self.eixo_x = None
        self.lista_deslocamentos_igual_zero = None
        self.lista_deflexoes = None
        self.c = None
        Vigahiperestatica.__init__(self, viga)
    def gera_linha_cheia_de_zeros(self):
        # CRIA A LISTA VAZIA COM O NÚMERO DE INCÓGNICAS (Y/DEFLEXOES AO LONGO DA VIGA)
        self.linha_vazia =[]
        c=int(1/self.passo)*len(self.viga.lista_comprimentos)+1
        self.c =c
        for i in range(0, c):
            self.linha_vazia.append(0)



    def resolve_sistema_para_descobrir_deformaçao_nos_pontos(self):
        # RESOLVE SISTEMA DE EQUAÇÕES
        M = np.array(self.matriz_segunda_derivada)
        C = np.array(self.matriz_momento_dividido_por_EI)
        self.resultados_deformação = np.linalg.solve(M, C)

    def gera_lista_vazia(self):
        for i in range(1, len(self.viga.lista_comprimentos)+1):
            x = int(i/self.passo)
            self.lista_deslocamentos_igual_zero.append(x)
    def remove_apoios_da_matriz_com_o_indice_dos_y(self):
        # REMOVE OS APOIOS POIS JÁ SABEMOS QUE NELES Y=0 E DESSA FORMA A MATRIZ SE TORNA QUADRADA
        for i in range(0, len(self.matriz_segunda_derivada)):
            for y in range(len(self.lista_deslocamentos_igual_zero) - 1, -1, -1):
                self.matriz_segunda_derivada[i].pop(self.lista_deslocamentos_igual_zero[y])
    def cria_lista_deflexoes(self):
        # PEGA A SAÍDA NO NUMPY E TRANSFORMA EM UM LISTA NORMAL
        self.lista_deflexoes = []
        for i in range(0, len(self.resultados_deformação)):
            self.lista_deflexoes.append(self.resultados_deformação[i])
    def adiciona_o_x_das_posicoes_de_apoio(self):
        #ADICIONA OS APOIOS COM DEFLEXÃO IGUAL A ZERO EM TODOS E A POSIÇÃO X
        for i in range(0, len(self.viga.lista_comprimentos)+1):
            self.lista_deflexoes.append(0)
            if i ==0:
                posicao_apoio = 0
            else:
                posicao_apoio = posicao_apoio +self.viga.lista_comprimentos[i-1]
            self.eixo_x.append(posicao_apoio)
    def gera_grafico_deflexoes(self):
        print(self.lista_deflexoes)
        plt.scatter(self.eixo_x, self.lista_deflexoes, s= 0.1)
        plt.plot()
        plt.title('Deflexão ao longo da viga ')
        plt.xlabel('x (m)')
        plt.ylabel('Deflexão (mm)')
        plt.show()

    def apply(self):
        # CÁLCULA O NÚMERO DE ITERAÇÕES A PARTIR DO PASSO
        i = int(1/self.passo +1)
        # CRIA UMA LISTA PARA O EIXO X (X AO LONGO DA VIGA)
        self.eixo_x =[]
        self.lista_deslocamentos_igual_zero = [0]
        comprimento_acumulado =0
        self.gera_lista_vazia()
        #ESSA MATRIZ VAI ARMAZENAR OS Ys (Y1, Y2,..., Yn-1, Yn) OBTIDOS PARA O SISTEMA DE EQUAÇÃO
        self.matriz_segunda_derivada = []
        # ESSA MATRIZ VAI ARMAZENAR O LAMBDA = M(X). PASSO²/EI
        self.matriz_momento_dividido_por_EI = []
        # A VIGA COMEÇA SER ANALISADA EM 1, POIS 0 SERÁ A EXTREMIDADE ONDE A DEFLEXÃO SERÁ ZERO
        indice = 1
        # CONTROLA O INDICE DAS EQUAÇÕES DO MOMENTO QUE ESTÃO DO ÚLTIMO TRECHO PARA O PRIMEIRO
        EqM = len(self.viga.lista_eq_momento_por_trecho) - 1
        # FAZ O FOR EM TODOS OS TRECHOS DA VIGA
        for x in range(0,len(self.viga.lista_eq_momento_por_trecho)):
            #print('xxxxxxxxxxxxxx', i)
            if x ==0:
                # SE O X==0, ENTÃO O X COMEÇA EM 0
                eixo_x = self.passo*self.viga.lista_comprimentos[x]
                x_atual = self.passo * self.viga.lista_comprimentos[x]
            else:
                # SE O X>0. TEMOS QUE CONSIDERAR QUE JÁ EXISTE UM COMPRIMENTO DE VIGA AMULADO
                eixo_x = comprimento_acumulado + self.viga.lista_comprimentos[x]*self.passo
                x_atual = self.passo * self.viga.lista_comprimentos[x-1]
            # A VIGA VAI ATÉ O NUMÉRO DE DIVISÕES -1, POIS O ÚLTIMO PONTO SERÁ O APOIO ONDE O DESLOCAMENTO
            # SERÁ ZERO
            fim = int(1 / self.passo) -1
            print('--------o passo é-------------')
            h= (self.passo)*self.viga.lista_comprimentos[x]
            print(h)
            # FAZ O FOR DENTRO DO TRECHO COM AS ITERAÇÕES DO MÉTODO DAS DIFERENÇAS FINITAS
            for y in range (0, fim):
                # CÁLCULA O MOMENTO NO PONTO
                #print(self.viga.Ecs)
                #print(self.viga.I)
                #print(self.passo)
                momento_no_ponto = ((self.viga.lista_eq_momento_por_trecho[EqM][0] +self.viga.lista_eq_momento_por_trecho[EqM][1]*x_atual
                                     +self.viga.lista_eq_momento_por_trecho[EqM][2]*x_atual**2) * (h**2))/(self.viga.Ecs * self.viga.I )

                self.gera_linha_cheia_de_zeros()
                # SE ALGUM DOS INDICES (INDICE -1, INDICE, INDICE +1) FOR IGUAL A INDICE QUE REPRESENTE O APOIO O Y SERÁ ZERO
                # SE FOR DIFERENTE SEGUE A SEGUINTE LÓGICA 1.Yn-1 - 2 Yn + 1. Yn+1
                if indice+1 in self.lista_deslocamentos_igual_zero:
                    self.linha_vazia[indice + 1] = 0
                else:
                    self.linha_vazia[indice + 1] = 1

                if indice in self.lista_deslocamentos_igual_zero:
                    self.linha_vazia[indice] = 0
                else:
                    self.linha_vazia[indice] = -2

                if indice-1 in self.lista_deslocamentos_igual_zero:
                    self.linha_vazia[indice-1] = 0
                else:
                    self.linha_vazia[indice - 1] = 1
                if y == fim-1:
                    indice = indice + 2
                else:
                    indice = indice + 1
                self.eixo_x.append(eixo_x)
                #print(eixo_x)
                #FAZ O INCREMENTO NO X_ATUAL ( QUE SEMPRE SERÁ TERÁ X=0 NO COMEÇO DO TRECHO)
                # E O EIXO_X ACUMULA OS VALORES
                x_atual = x_atual + self.passo*self.viga.lista_comprimentos[x]
                eixo_x = eixo_x + self.passo * self.viga.lista_comprimentos[x]
                self.matriz_segunda_derivada.append(self.linha_vazia)
                self.matriz_momento_dividido_por_EI.append(momento_no_ponto)

            EqM = EqM - 1
            #print(x)
            #print(self.viga.lista_comprimentos[x])
            comprimento_acumulado += self.viga.lista_comprimentos[x]
            #print('O comprimento acumulado é,',comprimento_acumulado)


        self.remove_apoios_da_matriz_com_o_indice_dos_y()
        self.resolve_sistema_para_descobrir_deformaçao_nos_pontos()
        self.cria_lista_deflexoes()
        self.adiciona_o_x_das_posicoes_de_apoio()
        self.gera_grafico_deflexoes()