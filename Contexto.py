
from Diferencas_finitas import *
from Eq3momentos import *
from Vigahiperestatica import *
from Calcula_momentos_por_trecho import *



class Contexto:
    def __init__(self,viga):
        self.viga= viga
    def apply(self):
        #print(self.viga.I)
        self.viga.apply()
        reações = Eq3momentos(self.viga)
        reações.apply()
        momentos = Calcula_momentos_por_trecho(self.viga)
        momentos.apply()
        diferenças_finitas = Diferencas_finitas(self.viga)
        diferenças_finitas.apply()