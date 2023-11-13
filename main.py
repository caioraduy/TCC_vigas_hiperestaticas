from Contexto import *
from Diferencas_finitas import *
from Eq3momentos import *
from Vigahiperestatica import *
if __name__== '__main__':
    # O USUÁRIO VAI ENTRAR COM OS COMPRIMENTOS DE CADA TRECHO E O VALOR DA CARGA DISTRIBUÍDA
    #viga = Vigahiperestatica(lista_comprimentos=[10,10,10,10],lista_cargas_q=[10,10,10,10]
                           #  , b= 0.2, h=0.3, fck = 30)

    viga1 = Vigahiperestatica(lista_comprimentos=[10,8,8,5,9,6
                                                  ], lista_cargas_q=[8,9,7,5,4,3], balanco_esquerdo=False,
                             balanco_direito =False, b=0.2, h=0.3, fck=30 )

    #print(viga.I)
    #contexto = Contexto(viga)
    #contexto.apply()
    contexto = Contexto(viga1)
    contexto.apply()