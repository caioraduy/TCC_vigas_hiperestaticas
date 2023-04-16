lista_comprimentos=[10,10,10]
lista_reações=[1,1,2,1]
carga_q=1
lista_L_acumulados = []
for i in range (0,len(lista_comprimentos)):
    if i ==0:
        comprimento_acumulado=0
    else:
        comprimento_acumulado = comprimento_acumulado + lista_comprimentos[i]
    lista_L_acumulados.append(comprimento_acumulado)

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

print(lista_eq_LE)