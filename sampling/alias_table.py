# -*- encoding:utf8 -*-

from random import randrange,random
import numpy as np

class AliasTable():
    def __init__(self,probs):
        probs=np.array(probs)
        self.probs=probs/np.sum(probs)
        self.bins=len(probs)        
        self.A=np.zeros((self.bins,3))
        p=1/self.bins
        L,H=[],[]
        for i in range(self.bins):
            if self.probs[i]<=p:
                L.append(i)
                self.A[i,1]=self.A[i,2]=i
            else:
                H.append(i)
                self.A[i,1]=self.A[i,2]=i
        
        while len(L)>0 and len(H)>0:
            l=L.pop()
            h=H.pop()
            self.A[l,0]=self.probs[l]
            self.A[l,1]=l
            self.A[l,2]=h
            self.probs[h]=self.probs[h]+self.probs[l]-p
            self.probs[l]=p
            if self.probs[h]>p:
                H.append(h)
            else:
                L.append(h)
    def sample(self):  
        b=randrange(self.bins)
        (p,i,h)=self.A[b]
        if self.bins*p<=random():
            return int(h)
        else:
            return int(i)

if __name__=='__main__':
    at=AliasTable([1,10])
    test=np.zeros(2)
    for i in range(100000):
        t=at.sample()    
        test[t]+=1
    print(test)
