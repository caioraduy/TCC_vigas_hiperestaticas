import numpy as np
import matplotlib.pyplot as plt
import math
class Vigahiperestatica:
    def __init__(self, lista_comprimentos =None, carga_q = None, lista_reações = None, b = None, h= None, fck= None):
        self.b = b
        self.h = h
        self.lista_comprimentos = lista_comprimentos
        self.carga_q = carga_q
        self.lista_reações = lista_reações
        self.lista_eq_momento_por_trecho = None
        self.lista_comprimentos_acumulados_viga = None
        self.Ecs = 0
        self.fck = 30
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
        for i in range(0, len(self.viga.lista_comprimentos) - 1):
            self.lista_incognitas_vazia = []
            for j in range(0, len(self.viga.lista_comprimentos) + 1):
                x = 0
                self.lista_incognitas_vazia.append(x)
            #print(self.lista_incognitas_vazia)
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
            termo_inde = -6 * (self.viga.carga_q*self.viga.lista_comprimentos[i]**3)/24 -\
                         6* (self.viga.carga_q*self.viga.lista_comprimentos[i+1]**3)/24
            lista_termo_ind.append(termo_inde)
            self.matriz_termo_inde.append(lista_termo_ind)
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
            parcela_carga = self.viga.carga_q * self.viga.lista_comprimentos[i]*self.viga.lista_comprimentos[i]/2
            #MOMENTO APOIO DA ESQUERDA
            parcela_momento_i = self.lista_momentos[i]
            #MOMENTO APOIO DA DIREITA
            parcela_momento_i_mais1 = -1*self.lista_momentos[i+1]

            # REAÇÃO DE APOIO DA DIREITA
            Ri_mais1 = (parcela_carga + parcela_momento_i +parcela_momento_i_mais1)/self.viga.lista_comprimentos[i]
            # REAÇÃO DE APOIO DA ESQUERDA
            Ri = self.viga.carga_q*self.viga.lista_comprimentos[i] - Ri_mais1
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


if __name__== '__main__':
    # O USUÁRIO VAI ENTRAR COM OS COMPRIMENTOS DE CADA TRECHO E O VALOR DA CARGA DISTRIBUÍDA
    viga = Vigahiperestatica(lista_comprimentos=[10,10,10],carga_q=10, b= 0.2, h=0.3, fck = 30)
    #print(viga.I)
    contexto = Contexto(viga)
    contexto.apply()

