import numpy as np 
from timeit import default_timer as timer
from numba import vectorize, jit, cuda

class NDS():    
    # Comparison Matrix of nxn
    def comp_matrix(w):
        #w=np.array([0.9218, 0.7382, 0.1763 ,0.4057])
        a=sorted(w)
        a=np.array(a)
        # print(len(w))
        n=len(w)
        b=np.array([0 for i in range(n)])
        #w=np.append(w,[6])
        #print(w,a)
        for i in range(n):
            for j in range(n):
                if(a[i]==w[j]):
                    b[i]=j
        for i in range(n):
            b[i]=int(b[i])
        # print(b)

        # initial creation of comparison matrix
        c=np.zeros([m,m])
        # print(c,"\n")
        for j in range(m):
            c[b[0]][j]=1
        # print(c,"\n")
        for i in range(1,m):
            if(a[i]==a[i-1]):
                for j in range(m):
                    c[b[i]][j]=c[b[i-1]][j]
            else:
                for j in range(i,m):
                    c[b[i]][b[j]]=1
        # print(c)
        return c

    # Dominance Degree Matrix
    def dom_matrix(p,n,m):
        d=np.zeros([m,m])
        #let: m=3
        # Dom matrix d by summation of consecutive comparison matrix per objective of the solution
        for j in range(n):
            w=p[j]
            #print(w)
            c=NDS.comp_matrix(w)
            d=d+c
        # print(d)
        for i in range(m):
            for j in range(i,m):
                if(d[i][j]==n and d[j][i]==n):
                    d[i][j], d[j][i]=0,0
        # print(d)
        return d

    # ENS-DDA
    def ens_dda(n,m,p):
        # print(p)
        d=NDS.dom_matrix(p,n,m)
        # print(p)
        # sort p based on the 1st obj
        for i in range(m):
            for j in range(i,m):
                if(p[:,i][0]>p[:,j][0]):
                    p[:,[i,j]]=p[:,[j,i]]
        # print(p)
        c=0 #loop counter
        #insertion of fronts for all solutions
        for s in range(m):
            NDS.fr_insert(p[:,s],f,nf,d,n,m,c)
            c=c+1
        # print(f)
        return f

    def fr_insert(s,f,nf,d,n,m,c):
        isIn=False
        for k in range(nf+1):
            isDom=False
            #check if soln objs dominant
            for sd in f[k]:
                for sdd in range(m):
                    if(d[sdd][c]==n):
                        isDom=True
                        break
            #if not then insert to the fronts
            if(isDom==False):
                f[k].append([s])
                isIn=True
                break
        if(isIn==False):
            # print("Hello")
            nf=nf+1
            f.append([])
            f[nf].append([s]) 

# main
nf=0
n=50000
m=5
f=[[]]
# s=timer()
# p=np.random.rand(n,m)
# NDS.ens_dda(n,m,p)
# print(timer()-s)