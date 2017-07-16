# -*- encoding:utf8 -*-

from random import randrange,random
import numpy as np
from datetime import datetime

class AliasTable():
    def __init__(self,probs):
        self.probs=probs
        probs=np.array(probs)
        self.bins=len(probs) 
        probs=probs*self.bins/np.sum(probs)    
        self.p_table=np.ones(self.bins,dtype=np.float64)
        self.b_table=np.zeros(self.bins,dtype=np.int64)
        p=1/self.bins
        L,H=[],[]
        for i in range(self.bins):
            if probs[i]<1:
                L.append(i)
            else:
                H.append(i)
        
        while len(L)>0 and len(H)>0:
            l=L.pop()
            h=H.pop()
            self.p_table[l]=probs[l]
            self.b_table[l]=h
            probs[h]=probs[h]-(1-probs[l])
            if probs[h]<1:
                L.append(h)
            else:
                H.append(h)

        while len(L)>0:
            l=L.pop()
            self.p_table[l]=1

        while len(H)>0:
            h=H.pop()
            self.p_table[H]=1
            
    def sample(self):  
        b=randrange(self.bins)
        if random()<self.p_table[b]:
            return b
        else:
            return self.b_table[b]


if __name__=='__main__':
    test=[0,1,2]
    at=AliasTable(test)
    t=at.sample()    
    
    

    
