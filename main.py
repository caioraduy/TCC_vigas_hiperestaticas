from Contexto import *
from Diferencas_finitas import *
from Eq3momentos import *
from Vigahiperestatica import *
if __name__== '__main__':
    # O USUÁRIO VAI ENTRAR COM OS COMPRIMENTOS DE CADA TRECHO E O VALOR DA CARGA DISTRIBUÍDA
    #viga = Vigahiperestatica(lista_comprimentos=[10,10,10,10],lista_cargas_q=[10,10,10,10]
                             #, b= 0.2, h=0.3, fck = 30)

    viga1 = Vigahiperestatica(lista_comprimentos=[10, 10, 10,10], lista_cargas_q=[10, 10,10,10], balanco_esquerdo=True,
                             balanco_direito =True, b=0.2, h=0.3, fck=30)

    #print(viga.I)
    #contexto = Contexto(viga)
    #contexto.apply()
    contexto = Contexto(viga1)
    contexto.apply()