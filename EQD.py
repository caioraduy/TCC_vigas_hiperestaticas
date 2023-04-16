import numpy as np
class Vigahiperestatica:
    def __init__(self, lista_comprimentos =None, carga_q = None, lista_reações = None):
        self.lista_comprimentos = lista_comprimentos
        self.carga_q = carga_q
        self.lista_reações = lista_reações
class Calcula_momentos_por_trecho(Vigahiperestatica):
    def __init__(self,viga):
        self.viga = viga
        self.x_acumulado = None
        self.lista_L_acumulados = None
        self.comprimento_acumulado = None
        self.termo_inde_acumulado = None
        self.lista_eq_momento = None
        Vigahiperestatica.__init__(self, viga)
    def calcula_comprimentos_acumulados(self):
        self.lista_L_acumulados = []
        print(self.viga.lista_comprimentos)
        for i in range (0,len(self.viga.lista_comprimentos)):
            if i ==0:
                self.comprimento_acumulado=0
            else:
                self.comprimento_acumulado = self.comprimento_acumulado + self.viga.lista_comprimentos[i]
            self.lista_L_acumulados.append(self.comprimento_acumulado)
        print(self.lista_L_acumulados)
    def gera_equacoes_momentos_por_trecho(self):
        self.lista_eq_LE=[]
        L = 0
        V = len(self.viga.lista_comprimentos)-1
        # for de traz para frente, começando no número de elementos da lista com os comprimentos
        for i in range(len(self.viga.lista_comprimentos),0,-1 ):
            LE=[]
            #variável que acumula o termo independente
            self.termo_inde_acumulado = 0
            #variável que acumula x^1
            self.x_acumulado = 0
            k = 0
            for j in range(L, len(self.viga.lista_comprimentos)):
                #combina a reação de apoio com o comprimento acumulado
                termo_inde =self.viga.lista_reações[k]*self.lista_L_acumulados[-j-1]
                #o x é a reação
                x = self.viga.lista_reações[k]
                #acumula os valores
                self.x_acumulado += x
                self.termo_inde_acumulado += termo_inde
                # aumenta o K para que no próxima iteração seja obtido o valor correto da reação
                k=k+1
            #calcula o termo da carga
            termo_inde_carga = self.viga.carga_q * self.lista_L_acumulados[V]**2/2
            x_carga = self.viga.carga_q * self.lista_L_acumulados[V]
            x_2 = -self.viga.carga_q/2
            # o L aumenta, cada vez o número de reações é maior
            L=L+1
            # o V diminui para combinar a maior reação com o menor valor de comprimento acumulado
            V=V-1
            self.x_acumulado -= x_carga
            self.termo_inde_acumulado -= termo_inde_carga
            LE.append(self.termo_inde_acumulado)
            LE.append(self.x_acumulado)
            LE.append(x_2)
            self.lista_eq_LE.append(LE)
        print(self.lista_eq_LE)
    def apply(self):
        self.calcula_comprimentos_acumulados()
        self.gera_equacoes_momentos_por_trecho()
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

        Vigahiperestatica.__init__(self, viga)
    def gera_matriz_cheia_de_zeros(self):
        self.matriz_incognitas_vazia = []
        # gera uma matriz com o número de termos com valores aij = 0
        for i in range(0, len(self.viga.lista_comprimentos) - 1):
            self.lista_incognitas_vazia = []
            for j in range(0, len(self.viga.lista_comprimentos) + 1):
                x = 0
                self.lista_incognitas_vazia.append(x)
            print(self.lista_incognitas_vazia)
            self.matriz_incognitas_vazia.append(self.lista_incognitas_vazia)
    def adiciona_elementos_na_matriz_das_incognitas(self):
        self.lista_incognitas_prencher[self.indice_mi_anterior] = self.Mi_anterior
        self.lista_incognitas_prencher[self.indice_mi] = self.Mi
        self.lista_incognitas_prencher[self.indice_mi_posterior] = self.Mi_posterior
        self.matriz_incognitas.append(self.lista_incognitas_prencher)

    def resolve_sistema_equacoes(self):
        self.M = np.array(self.matriz_incognitas_quadrada)
        self.C = np.array(self.matriz_termo_inde)
        self.Resultados_momentos = np.linalg.solve(self.M, self.C)

    def gera_matriz_quadrada(self):
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
        print(self.lista_momentos)

    def equacao_3_momentos(self):
        self.gera_matriz_cheia_de_zeros()
        self.matriz_termo_inde = []
        self.matriz_incognitas = []
        for i in range(0, len(self.viga.lista_comprimentos)-1):
            # pega uma lista com zeros
            self.lista_incognitas_prencher = self.matriz_incognitas_vazia[i]
            lista_termo_ind =[]
            # controlas os indices de Mi-1, Mi e Mi+1
            self.indice_mi_anterior = i
            self.indice_mi = i + 1
            self.indice_mi_posterior = i + 2
            # se i=0 e a viga tem mais de 3 apoios
            if i == 0 and len(self.viga.lista_comprimentos) > 2:
                self.Mi_anterior = 0
                self.Mi = 2 * self.viga.lista_comprimentos[i] + 2 * self.viga.lista_comprimentos[i+1]
                self.Mi_posterior = self.viga.lista_comprimentos[i+1]
            # se i=0 e a viga tem apenas 3 apoios
            if i == 0 and len(self.viga.lista_comprimentos) == 2:
                self.Mi_anterior = 0
                self.Mi = 2 * self.viga.lista_comprimentos[i] + 2 * self.viga.lista_comprimentos[i+1]
                self.Mi_posterior = 0
            # se i> 0 e não é último apoio que estamos tratando
            if i > 0 and i <  len(self.viga.lista_comprimentos)-2:
                #print('arromba')
                self.Mi_anterior = self.viga.lista_comprimentos[i]
                self.Mi = 2 * self.viga.lista_comprimentos[i] + 2 * self.viga.lista_comprimentos[i+1]
                self.Mi_posterior = self.viga.lista_comprimentos[i + 1]
            # se i > 0 e estamos lidando com o último apoio
            if  i == len(self.viga.lista_comprimentos)-2:
                self.Mi_anterior = self.viga.lista_comprimentos[i]
                self.Mi = 2 * self.viga.lista_comprimentos[i] + 2 * self.viga.lista_comprimentos[i+1]
                self.Mi_posterior = 0
                #print(Mi_anterior)
                #print(Mi)
            #calcula o termo independete e adiciona em uma matriz
            termo_inde = -6 * (self.viga.carga_q*self.viga.lista_comprimentos[i])/24 -\
                         6* (self.viga.carga_q*self.viga.lista_comprimentos[i+1])/24
            lista_termo_ind.append(termo_inde)
            self.matriz_termo_inde.append(lista_termo_ind)
            # adiciona os 'Momentos" na matriz de acordo com o indice
            self.adiciona_elementos_na_matriz_das_incognitas()
        # retira o primeiro e o último momento que são iguais a zero para obter a solução
        self.gera_matriz_quadrada()
        #resolve o sistema de equações
        self.resolve_sistema_equacoes()
        print(self.Resultados_momentos)
        self.gera_lista_momentos()

    def calcula_reacoes_apoio(self):
        pass




    def apply(self):
        self.equacao_3_momentos()






class Contexto:
    def __init__(self,viga):
        self.viga= viga
    def apply(self):
        momentos = Calcula_momentos_por_trecho(self.viga)
        momentos.apply()
        reações = Eq3momentos(self.viga)
        reações.apply()

if __name__== '__main__':
    viga = Vigahiperestatica(lista_comprimentos=[10,10,10],carga_q=1
                             ,lista_reações=[1,1,2,1]
    )
    contexto = Contexto(viga)
    contexto.apply()

