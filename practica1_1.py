# -*- coding: utf-8 -*-
"""
Spyder Editor

"""

from multiprocessing import Process, BoundedSemaphore, Semaphore, Lock, Value, Array
from multiprocessing import Manager
from time import sleep
from random import randint, random
import math

N = 4
NPROD = 4
tam = NPROD * N  # tamaño de cada buffer

#En esta version tratamos de usar un array lineal para los buffers de los productores         	 
#Obtenemos el mínimo valor de un buffer              	 
def get_minvalues(producidos_aux):
    menor = math.inf
    for i in range(NPROD):
        if (producidos_aux[i] !=-1) and (producidos_aux[i] < menor) and (producidos_aux[i] !=-2):
            pmenor = i
            menor = producidos_aux[i]
    return (pmenor,menor)

#Obtenemos el mínimo de los valores minimos de cada buffer
def get_min(producidos, pos_c):
    posibles=[]
    for i in range(NPROD):
        if pos_c[i]<tam:
            posibles.append(producidos[i][pos_c[i]])
    (pmenor,menor)=get_minvalues(posibles)
    return pos_c[pmenor],pmenor,menor


#Nos determina si todos los buffers están vacíos
def acabar(producidos, pos_c):
    for i in range(NPROD):
        if producidos[i][pos_c[i] % tam] != -1:
            return False
    return True

def producer(producidos, pos_c, pos_p, pos_aux, empty, non_empty, pid):
    for i in range(N):
        print(f'productor {pid} produciendo')
        pos_aux.value = pos_aux.value + randint(1, 20)
        producidos[pos_p] = pos_aux.value
        pos_p += 1
        print(f"Productor {pid} ha producido", producidos[i % tam], flush=True)
        non_empty.release()
        if pos_p == pos_c: # si el productor y el consumidor están en la misma posición activamos el semáforo
            empty.acquire()
    print(f'Productor {pid} ha producido todos sus productos')
    producidos[pos_p] = -1
    non_empty.release()


def anadir(pos,minP,menor,producidos,resultados,pos_c):
    resultados.append(menor)
    producidos[minP][pos] = -2
    pos_c[minP] += 1


def consumer(producidos, pos_c, empty, non_empty, resultados):
    print ('entra en consumer')
    for i in range(NPROD):
        non_empty[i].acquire()
    while (not acabar(producidos, pos_c)):
        pid = 0
        for i in producidos:
            print(f'productos del productor {pid}')
            print(list(producidos[pid]), flush=True)
            pid += 1         
        pos, minP, menor = get_min(producidos,pos_c)
        anadir(pos,minP,menor,producidos,resultados,pos_c)
        print(resultados[:])
        print(f"Consumer  consumiendo {menor}", flush=True)
        if producidos[minP][pos_c[minP]] == -2:
            empty[minP].release()
            non_empty[minP].acquire()
    print("Consumer  ha consumido todos los productos")

def main():
    producidos = [Array('i', tam) for _ in range(NPROD)] # buffer de cada productor
    pos_aux = [Value('i', 0) for _ in range(NPROD)]  # posición auxiliar de cada productor
    pos_c = Array('i', NPROD) # posición de consumo de cada productor
    pos_p = Array('i', NPROD) # posición de producción de cada productor
    resultados=Manager().list() # lista de resultados
    for i in range(NPROD): # inicialización de los buffers
        pos_c[i] = 0 
        pos_p[i] = 0
        for j in range(tam):
            producidos[i][j] = -2


    non_empty = [] # Creamos 2 semaforos para controlar la producción y no haya ningún tipo de problema		
    empty = [] 

    for i in range(NPROD):
        empty.append(Semaphore(0))
        non_empty.append(Semaphore(0))


    prodlst = [Process(target=producer, name=f'prod_{i}',args=(producidos[i], pos_c[i], pos_p[i], pos_aux[i], empty[i], non_empty[i], i))
                for i in range(NPROD)]

    conslst = [Process(target=consumer, name=f"cons_{i}",
                args=(producidos, pos_c, empty, non_empty, resultados))]

    for p in prodlst+conslst:
        p.start()
    for p in prodlst+conslst:
        p.join()

if __name__ == '__main__':
    main()

