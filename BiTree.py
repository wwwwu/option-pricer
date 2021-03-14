import numpy as np

class BiTree:
    def __init__(self, optionType=None, s0=0, sigma=0, r=0, t=0, k=0,
                 n=100):
        self.s0 = s0 * 1.0
        self.sigma = sigma
        self.r = r * 1.0
        self.t = t * 1.0
        self.k = k * 1.0
        self.n = n
        self.optionType = optionType
    
    def calc(self):
        n = self.n
        dt = self.t/n
        tp = self.optionType
        u = np.exp(self.sigma * np.sqrt(dt))
        d = np.exp(-self.sigma * np.sqrt(dt))
        p = (np.exp(self.r * dt) - d) / (u - d)
        DF = np.exp(-self.r * dt)
        st = np.asarray([0.0 for i in range(n + 1)]) 
        st2 = np.asarray([(self.s0 * pow(u, j) * pow(d,(n - j))) for j in range(n + 1)])
        st3 = [float(self.k)]*(n+1)
               
        if tp == 'C':
            st[:] = np.maximum(st2-st3, 0.0)
            for i in range(n-1, -1, -1):
                st[:-1]= DF * (p * st[1:] + (1-p) * st[:-1])
                st2[:]=st2[:] * u
                st[:]=np.maximum(st[:],st2[:]-st3[:])
        elif tp =='P':
            st[:] = np.maximum(st3-st2, 0.0)
            for i in range(n-1, -1, -1):
                st[:-1]= DF * (p * st[1:] + (1-p) * st[:-1])
                st2[:]=u * st2[:]
                st[:]=np.maximum(st[:],-st2[:]+st3[:])
            
        return st[0]
    
option = BiTree(optionType='P', s0=50, sigma=0.4, r=0.1, t=2, k=70,
                 n=200)
