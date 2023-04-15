class Vigahiperestatica:
    def __init__(self, lista_comprimentos =None, carga_q = None, lista_reacoes = None):
        self.lista_comprimentos = lista_comprimentos
        self.carga_q = carga_q
        self.lista_reacoes = lista_reacoes
class Calcula_momentos_por_trecho:
    def __init__(self,viga):
        self.viga = viga
        self.x_acumulado = None
        self.lista_L_acumulados = None
        self.comprimento_acumulado = None
        self.termo_inde_acumulado = None
        self.lista_eq_momento = None
    def calcula_documentos_acumulados(self):
        self.lista_L_acumulados = []
        for i in range (0,len(self.viga.lista_comprimentos)):
            if i ==0:
                self.comprimento_acumulado=0
            else:
                self.comprimento_acumulado = self.comprimento_acumulado + self.viga.lista_comprimentos[i]
        self.lista_L_acumulados.append(self.comprimento_acumulado)
    def gera_equacoes_momentos_por_trecho(self):
        lista_eq_LE=[]
L = 0
V = len(lista_comprimentos)-1
for i in range(len(lista_comprimentos),0,-1 ):
    LE=[]
    termo_inde_acumulado = 0
    x_acumulado = 0
    print(f'------------------{i}')
    k = 0
    for j in range(L, len(lista_comprimentos)):
        if j==0 and i == 1:
            print(lista_reações[k])
            #termo_inde = lista_reações[k] * lista_L_acumulados[0]
        else:
            print(lista_reações[k])
            print(lista_L_acumulados[-j-1])

            termo_inde =lista_reações[k]*lista_L_acumulados[-j-1]


        x = lista_reações[k]
        x_acumulado += x
        termo_inde_acumulado += termo_inde
        k=k+1
    termo_inde_carga = carga_q*lista_L_acumulados[V]**2/2
    x_carga = carga_q * lista_L_acumulados[V]
    x_2 = -carga_q/2
    L=L+1
    V=V-1
    x_acumulado -= x_carga
    termo_inde_acumulado -= termo_inde_carga
    LE.append(termo_inde_acumulado)
    LE.append(x_acumulado)
    LE.append(x_2)
    lista_eq_LE.append(LE)

if __name__== '__main__':
