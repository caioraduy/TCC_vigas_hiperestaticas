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
        for i in range(len(self.viga.lista_comprimentos),0,-1 ):
            LE=[]
            self.termo_inde_acumulado = 0
            self.x_acumulado = 0
            k = 0
            for j in range(L, len(self.viga.lista_comprimentos)):
                termo_inde =self.viga.lista_reações[k]*self.lista_L_acumulados[-j-1]
                x = self.viga.lista_reações[k]
                self.x_acumulado += x
                self.termo_inde_acumulado += termo_inde
                k=k+1
            termo_inde_carga = self.viga.carga_q * self.lista_L_acumulados[V]**2/2
            x_carga = self.viga.carga_q * self.lista_L_acumulados[V]
            x_2 = -self.viga.carga_q/2
            L=L+1
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
class Contexto:
    def __init__(self,viga):
        self.viga= viga
    def apply(self):
        momentos = Calcula_momentos_por_trecho(self.viga)
        momentos.apply()

if __name__== '__main__':
    viga = Vigahiperestatica(lista_comprimentos=[10,10,10],carga_q=1
                             ,lista_reações=[1,1,2,1]
    )
    contexto = Contexto(viga)
    contexto.apply()

