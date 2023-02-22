# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 17:38:38 2023

@author: Alex b
"""
from multiprocessing import Process
from multiprocessing import current_process
from multiprocessing import Value, BoundedSemaphore, Lock
import time
import random


def merge(v,inicio,mitad,fin):
    i=inicio
    j=mitad+1
    k=0
    aux=[]
    while i<=mitad and j<=fin:
        if v[i]<v[j]:
            aux.append(v[i])
            i+=1
        else:
            aux.append(v[j])
            j+=1
        k+=1
    while i<=mitad:
        aux.append(v[i])
        i+=1
        k+=1
    while j<=fin:
        aux.append(v[j])
        j+=1
        k+=1
    for i in range(inicio,fin+1):
        v[i]=aux[i-inicio]
        
        

def m(v,inicio,fin): # Ordenación por el método mergesort
    sem
    if inicio<fin:
        mitad=(inicio+fin)//2
        m(v,inicio,mitad)
        m(v,mitad+1,fin)
        merge(v,inicio,mitad,fin)
    sem.release()
def mergeSort(v):
    m(v,0,len(v)-1)

def main():
    v=[5,4,2,1,3]
    m(v,0,len(v)-1)
    sem=Lock()

    print ("fin")
if __name__ == "__main__":
    main()