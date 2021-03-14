
import numpy as np
import scipy.stats as sps
import math


class EuroOption:
    def __init__(self, typ, s0, k, t, r,q):
        self.typ = typ              
        self.s0 = s0 
        self.k = k 
        self.t = t 
        self.r = r 
        self.q = q
   
    def __repr__(self):
        return"EuroOption({}, {}, {}, {}, {}, {}, {})".format(self.typ,self.s0,self.k,self.t,self.r,self.sigma,self.q)
    

    def Op(self,sigma): 
        self.d1 = (np.log(self.s0/self.k) + (self.r - self.q) * self.t)/(sigma * np.sqrt(self.t)) + 0.5 * sigma * np.sqrt(self.t)
        self.d2 = (np.log(self.s0/self.k) + (self.r - self.q) * self.t)/(sigma * np.sqrt(self.t)) - 0.5 * sigma * np.sqrt(self.t)
        if self.typ == 'C':
            op = (self.s0*np.exp(-self.q*self.t)*sps.norm.cdf(self.d1,0.0,1.0)) - \
                 (self.k*np.exp(-self.r*self.t)*sps.norm.cdf(self.d2,0.0,1.0))
        if self.typ == 'P':        
            op = (self.k*np.exp(-self.r*self.t)*sps.norm.cdf(-self.d2,0.0,1.0)) - \
                 (self.s0*np.exp(-self.q*self.t)*sps.norm.cdf(-self.d1,0.0,1.0))
        return op


    def vega(self,sigma): 
                  
        d = ((math.log(self.s0/self.k) + (self.r-self.q)*self.t) / \
             (sigma*math.sqrt(self.t))) + 0.5*sigma*math.sqrt(self.t)
            
        vega =  self.s0*np.exp(-self.q*self.t)*math.sqrt(self.t)*sps.norm.pdf(d,0.0,1.0)
        return vega

    def getSigma(self, option_premium):
        sigmahat = np.sqrt(2 * abs((np.log(self.s0/self.k) + (self.r - self.q) * self.t)/self.t))
        tol = 1e-8
        nmax = 100
        sigmadiff = 1
        n = 1
        while (sigmadiff >= tol and n < nmax):
            O = self.Op(sigmahat)           
            Ovega = self.vega(sigmahat)
            increment = (O - option_premium)/Ovega
            sigmahat = sigmahat - increment
            n = n + 1
            sigmadiff = abs(increment)            
        return sigmahat
    



