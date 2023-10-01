import numpy as np
import matplotlib.pyplot as plt
import math
from Contexto import *
from Diferencas_finitas import *
from Calcula_momentos_por_trecho import *
from Vigahiperestatica import *

class Eq3momentos(Vigahiperestatica):
    def __init__(self,viga):
        self.viga= viga
        self.indice_mi_anterior = None
        self.indice_mi = None
        self.indice_mi_posterior = None
        self.Mi_anterior = None
        self.Mi = None
        self.Mi_posterior = None
        self.lista_incognitas_prencher = None
        self.matriz_incognitas = None
        self.M = None
        self.C = None
        self.Resultados_momentos = None
        self.lista_incognitas_vazia = None
        self.matriz_incognitas_vazia = None
        self.matriz_termo_inde = None
        self.linha_incognitas_quadrada = None
        self.matriz_incognitas_quadrada = None
        self.matriz_incognitas = None
        self.lista_momentos = None
        self.lista_reacoes = None
        self.lista_reacoes = None
        self.matriz_reacoes = None

        Vigahiperestatica.__init__(self, viga)
    def gera_matriz_cheia_de_zeros(self):
        self.matriz_incognitas_vazia = []
        # gera uma matriz com o número de termos com valores aij = 0
        for i in range(0, self.viga.numero_apoios- 2):
            self.lista_incognitas_vazia = []
            for j in range(0, self.viga.numero_apoios):
                x = 0
                self.lista_incognitas_vazia.append(x)
            print(self.lista_incognitas_vazia)
            self.matriz_incognitas_vazia.append(self.lista_incognitas_vazia)
    def adiciona_elementos_na_matriz_das_incognitas(self):
        print(self.lista_incognitas_prencher)
        self.lista_incognitas_prencher[self.indice_mi_anterior] = self.Mi_anterior
        self.lista_incognitas_prencher[self.indice_mi] = self.Mi
        self.lista_incognitas_prencher[self.indice_mi_posterior] = self.Mi_posterior
        self.matriz_incognitas.append(self.lista_incognitas_prencher)

    def resolve_sistema_equacoes(self):
        self.M = np.array(self.matriz_incognitas_quadrada)
        self.C = np.array(self.matriz_termo_inde)
        self.Resultados_momentos = np.linalg.solve(self.M, self.C)

    def gera_matriz_quadrada(self):
        print(self.matriz_incognitas)
        self.matriz_incognitas_quadrada = []
        for i in range(0, len(self.matriz_incognitas)):
            self.linha_incognitas_quadrada = []
            for j in range(0, len(self.matriz_incognitas[i])):
                if j > 0 and j < len(self.matriz_incognitas[i]) - 1:
                    self.linha_incognitas_quadrada.append(self.matriz_incognitas[i][j])
            self.matriz_incognitas_quadrada.append(self.linha_incognitas_quadrada)
    def gera_lista_momentos(self):
        self.lista_momentos = []
        for i in range(0, len(self.Resultados_momentos)):
            self.lista_momentos.append(self.Resultados_momentos[i][0])
        self.lista_momentos.insert(0,0)
        self.lista_momentos.insert(len(self.viga.lista_comprimentos),0)
        self.printa_momentos()
        #print(f'O vetor que representa os momentos nos apoios é: {self.lista_momentos}')
    def printa_momentos(self):
        print('----------MOMENTOS FLETORES NOS APOIOS-------------')
        for i in range(0, len(self.lista_momentos)):
            print(f'O momento no apoio {i+1} é {self.lista_momentos[i]} kNm')
            print(' ')


    def equacao_3_momentos(self):
        self.gera_matriz_cheia_de_zeros()
        self.matriz_termo_inde = []
        self.matriz_incognitas = []
        if self.viga.balanco_esquerdo == True:
            inicio = 1
        else:
            inicio =0
        if self.viga.balanco_direito == True:
            fim = len(self.viga.lista_comprimentos)-2
        else:
            fim = len(self.viga.lista_comprimentos)-1

        for i in range(inicio, fim):
            print(i)
            # pega uma lista com zeros
            print(self.matriz_incognitas_vazia[i-1])
            print(self.lista_incognitas_prencher)
            if self.viga.balanco_esquerdo == True:
                self.lista_incognitas_prencher = self.matriz_incognitas_vazia[i - 1]
                self.indice_mi_anterior = i-1
                self.indice_mi = i + 1 -1
                self.indice_mi_posterior = i + 2 -1
            else:
                self.lista_incognitas_prencher = self.matriz_incognitas_vazia[i]
                self.indice_mi_anterior = i
                self.indice_mi = i + 1
                self.indice_mi_posterior = i + 2
            lista_termo_ind =[]
            # controlas os indices de Mi-1, Mi e Mi+1
            # se i=0 e a viga tem mais de 3 apoios
            if i == inicio and self.viga.numero_apoios > 3:
                self.Mi = 2 * self.viga.lista_comprimentos[i] + 2 * self.viga.lista_comprimentos[i+1]
                self.Mi_posterior = self.viga.lista_comprimentos[i+1]
                if self.viga.balanco_esquerdo == True:
                    self.Mi_anterior = - self.viga.lista_comprimentos[0]**2* self.viga.lista_cargas_q[0]*self.viga.lista_comprimentos[i]/2
                else:
                    self.Mi_anterior = 0
                termo_inde = -6 * (self.viga.lista_cargas_q[i] * self.viga.lista_comprimentos[i] ** 3) / 24 - \
                             6 * (self.viga.lista_cargas_q[i + 1] * self.viga.lista_comprimentos[
                    i + 1] ** 3) / 24  - self.Mi_anterior

            # se i=0 e a viga tem apenas 3 apoios
            if i == inicio and self.viga.numero_apoios == 3:
                print('XXXXXXXXX')
                self.Mi = 2 * self.viga.lista_comprimentos[i] + 2 * self.viga.lista_comprimentos[i+1]
                if self.viga.balanco_direito == True:
                    self.Mi_posterior= - self.viga.lista_comprimentos[-1] ** 2 * self.viga.lista_cargas_q[-1] * self.viga.lista_comprimentos[i + 1] / 2
                else:
                    self.Mi_posterior = 0

                if self.viga.balanco_esquerdo == True:
                    self.Mi_anterior = - self.viga.lista_comprimentos[0]**2 * self.viga.lista_cargas_q[0]* self.viga.lista_comprimentos[i]/2
                else:
                    self.Mi_anterior = 0
                termo_inde = -6 * (self.viga.lista_cargas_q[i] * self.viga.lista_comprimentos[i] ** 3) / 24 - \
                             6 * (self.viga.lista_cargas_q[i + 1] * self.viga.lista_comprimentos[
                    i + 1] ** 3) / 24 - self.Mi_anterior - self.Mi_posterior
                print('o termo é', termo_inde)
            # se i> 0 e não é último apoio que estamos tratando
            if i > inicio and i <  fim-1 :
                self.Mi_anterior = self.viga.lista_comprimentos[i]
                self.Mi = 2 * self.viga.lista_comprimentos[i] + 2 * self.viga.lista_comprimentos[i+1]
                self.Mi_posterior = self.viga.lista_comprimentos[i + 1]
            # se i > 0 e estamos lidando com o último apoio
                termo_inde = -6 * (self.viga.lista_cargas_q[i] * self.viga.lista_comprimentos[i] ** 3) / 24 - \
                             6 * (self.viga.lista_cargas_q[i + 1] * self.viga.lista_comprimentos[i + 1] ** 3) / 24
            if  i == fim-1 and self.viga.numero_apoios > 3:
                self.Mi_anterior = self.viga.lista_comprimentos[i]
                self.Mi = 2 * self.viga.lista_comprimentos[i] + 2 * self.viga.lista_comprimentos[i+1]
                if self.viga.balanco_direito == True:
                    self.Mi_posterior = - self.viga.lista_comprimentos[-1]**2* self.viga.lista_cargas_q[-1]*self.viga.lista_comprimentos[i+1]/2
                else:
                    self.Mi_posterior = 0
                termo_inde = -6 * (self.viga.lista_cargas_q[i] * self.viga.lista_comprimentos[i] ** 3) / 24 - \
                             6 * (self.viga.lista_cargas_q[i + 1] * self.viga.lista_comprimentos[i + 1] ** 3) / 24 - self.Mi_posterior
            #calcula o termo independete e adiciona em uma matriz
            print(self.viga.lista_cargas_q[i])
            print(f'o termo inde é {termo_inde}')

            lista_termo_ind.append(termo_inde)
            self.matriz_termo_inde.append(lista_termo_ind)
            print(self.matriz_termo_inde)
            # adiciona os 'Momentos" na matriz de acordo com o indice
            self.adiciona_elementos_na_matriz_das_incognitas()
        # retira o primeiro e o último momento que são iguais a zero para obter a solução
        self.gera_matriz_quadrada()
        #resolve o sistema de equações
        self.resolve_sistema_equacoes()
        self.gera_lista_momentos()
        self.calcula_reacoes_apoio()


    def calcula_reacoes_apoio(self):
        self.lista_reacoes =[]
        self.matriz_reacoes =[]
        #CALCULA AS REAÇÕES DE APOIO POR TRECHO E ADICIONA EM UMA MATRIZ COM OS PARES
        for i in range( 0,len(self.viga.lista_comprimentos)):
            lista_reacoes_esquerda_direita =[]
            #MOMENTO GERADO PELA CARGA
            parcela_carga = self.viga.lista_cargas_q[i] * self.viga.lista_comprimentos[i]*self.viga.lista_comprimentos[i]/2
            #MOMENTO APOIO DA ESQUERDA
            parcela_momento_i = self.lista_momentos[i]
            #MOMENTO APOIO DA DIREITA
            parcela_momento_i_mais1 = -1*self.lista_momentos[i+1]

            # REAÇÃO DE APOIO DA DIREITA
            Ri_mais1 = (parcela_carga + parcela_momento_i +parcela_momento_i_mais1)/self.viga.lista_comprimentos[i]
            # REAÇÃO DE APOIO DA ESQUERDA
            Ri = self.viga.lista_cargas_q[i]*self.viga.lista_comprimentos[i] - Ri_mais1
            # ADICIONA OS PARES DE REAÇÃO
            lista_reacoes_esquerda_direita.append(Ri)
            lista_reacoes_esquerda_direita.append(Ri_mais1)

            self.matriz_reacoes.append(lista_reacoes_esquerda_direita)
        # SOMA A REAÇÃO DA ESQUERDA COM A REAÇÃO DA DIREITA

        for i in range(0, len(self.matriz_reacoes)):
            # SE I ==0 E A VIGA TEM MAIS DE 2 TRAMOS (MAIS DE 3 APOIOS)
            if i == 0 and len(self.viga.lista_comprimentos) >2:
                r_acumulado_i = self.matriz_reacoes[i][0]
                r_acumulado_i_mais_1 = self.matriz_reacoes[i][1] + self.matriz_reacoes[i + 1][0]
                self.lista_reacoes.append(r_acumulado_i)
                self.lista_reacoes.append(r_acumulado_i_mais_1)
            # SE ESTAMOS NO ÚLTIMO TRECHO DA VIGA
            elif i == len(self.matriz_reacoes)-1 and len(self.viga.lista_comprimentos) != 2:
                r_acumulado_i_mais_1 = self.matriz_reacoes[i][1]
                self.lista_reacoes.append(r_acumulado_i_mais_1)
            # SE I =0 E A VIGA TEM APENAS DOIS TRAMOS (3 APOIOS)
            elif  i == 0 and len(self.viga.lista_comprimentos) == 2:
                r_acumulado_i_menos_1 = self.matriz_reacoes[i][0]
                r_acumulado_i = self.matriz_reacoes[i][1] + self.matriz_reacoes[i + 1][0]
                r_acumulado_i_mais_1 = self.matriz_reacoes[i+1][1]
                self.lista_reacoes.append(r_acumulado_i_menos_1)
                self.lista_reacoes.append(r_acumulado_i)
                self.lista_reacoes.append(r_acumulado_i_mais_1)
            # SE I=1 E A VIGA TEM APENS DOIS TRAMOS
            elif i == len(self.matriz_reacoes) - 1 and len(self.viga.lista_comprimentos) == 2:
                pass

            else:
                r_acumulado_i = self.matriz_reacoes[i][1]+ self.matriz_reacoes[i+1][0]
                self.lista_reacoes.append(r_acumulado_i)
        self.viga.lista_reações =self.lista_reacoes
        self.printa_reacoes()
        #print( f' O vetor com as reações de apoio da viga é: {self.lista_reacoes}')
    def printa_reacoes(self):
        print('-----------REAÇÕES DE APOIO------------')
        for i in range(0, len(self.lista_reacoes)):
            print(f'A reação do apoio {i+1} é {self.lista_reacoes[i]} kN')
            print(' ')

    def apply(self):
        self.equacao_3_momentos()