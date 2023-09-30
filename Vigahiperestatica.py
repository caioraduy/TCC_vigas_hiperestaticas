import numpy as np
import matplotlib.pyplot as plt
import math
from Contexto import *
from Diferencas_finitas import *
from Eq3momentos import *
from Calcula_momentos_por_trecho import *

class Vigahiperestatica:
    def __init__(self, lista_comprimentos =None,lista_cargas_q= None, carga_q = None, lista_reações = None, b = None, h= None,
                 fck= None, balanco_esquerdo = False, balanco_direito= False,
                 q_balanco_esquerdo = None, q_balanco_direito = None):

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
        self.balanco_esquerdo = balanco_esquerdo
        self.balanco_direito = balanco_direito

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
