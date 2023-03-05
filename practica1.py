from multiprocessing import Process, BoundedSemaphore, Semaphore, Lock, Value, Array
from time import sleep
from random import randint, random
import math

N = 4
NPROD = 4
K = NPROD * N


def delay(factor = 3):
    sleep(random()/factor)

def anadir(resultados, v, mutex, index):
    mutex.acquire()
    try:
        resultados[index.value] = v
        m=index.value+1
        index.value =m
    finally:
        mutex.release()
                        

def add(producidos, v, mutex, pid):
    mutex.acquire()
    try:
        producidos[pid] = v
    finally:
        mutex.release()
                    
                    
def get_minvalues(producidos, mutex):
    mutex.acquire()
    try:
        menor = math.inf
        for i in range(NPROD):
            if (producidos[i] !=-1) and (producidos[i] < menor):
                pmenor = i
                menor = producidos[i]
    finally:
        mutex.release()
    return (pmenor,menor)
            
            
def producer(l, producidos, empty, nonEmpty, mutex, pid):
    x = 0
    for i in range(l):
        print (f'productor {pid} produciendo')
        delay(6)
        empty.acquire()
        x += randint(1,20)
        add(producidos,x, mutex, pid)
        print(f"Productor {pid} ha producido", x, flush=True)
        delay(15)
        nonEmpty.release()  
    empty.acquire()
    producidos[pid] = -1
    nonEmpty.release()
 
def consumer(producidos, resultados, empty, non_empty, mutex, index):
    print ('entra en consumer')
    for i in range(NPROD):
        non_empty[i].acquire()
    print("c1", list(producidos), flush=True)
    while (-1) in resultados:
        (minP,menor) = get_minvalues(producidos, mutex)
        anadir(resultados, menor, mutex, index)
        print(resultados[:])
        empty[minP].release()
        print (f"consumer  consumiendo {producidos[minP]} de {minP}", flush=True)
        non_empty[minP].acquire()


def main():
    resultados = Array('i', K)
    producidos = Array('i', NPROD)
    index = Value('i', 0)
    
    for i in range(NPROD):
        producidos[i] = -2
   
    for i in range(K):
        resultados[i] = -1
        
    non_empty = []			
    empty = []				
    mutex = Lock()
    
    for i in range(NPROD):
        empty.append(BoundedSemaphore(1))
        non_empty.append(Semaphore(0))

    prodlst = [ Process(target=producer,
                        name=f'prod_{i}',
                        args=(N, producidos, empty[i], non_empty[i], mutex, i))
                for i in range(NPROD) ]

    conslst = [Process(target=consumer,
                      name=f"cons_{i}",
                      args=(producidos, resultados, empty, non_empty, mutex, index)) ]
          
    for p in prodlst + conslst:
        p.start()

    for p in prodlst + conslst:
        p.join()

if __name__ == '__main__':
    main()

