import scipy.stats as sps
import numpy as np
import sys
import math


# n=step: the number of observation times for the geometric average
# m=path: the number of paths in the Monte Carlo simulation

class GeoAsianOption:
    def __init__(self, optionType=None, s0=0, sigma=0, r=0, t=0, k=0,
                 n=100):
        self.s0 = s0 * 1.0
        self.sigma = sigma * 1.0
        self.r = r * 1.0
        self.t = t * 1.0
        self.k = k * 1.0
        self.n = n
        self.optionType = optionType
    
    def calc(self):
        n = self.n
        tp = self.optionType
        sigT = self.sigma*math.sqrt((n+1)*(2*n+1)/(6*n*n))
        muT = 0.5*sigT**2 + (self.r - 0.5*pow(self.sigma, 2))*(n+1)/(2*n)
        d1 = (np.log(self.s0/self.k) + (muT + 0.5*sigT))/np.sqrt(sigT)
        d2 = d1 - np.sqrt(self.t) * sigT
        N1 = sps.norm.cdf(d1)
        N2 = sps.norm.cdf(d2)
        N1_ = sps.norm.cdf(-d1)
        N2_ = sps.norm.cdf(-d2)
        
        geoCall = math.exp(-self.r * self.t) * (self.s0 * np.exp(muT * self.t) * N1 - self.k * N2)
        geoPut = math.exp(-self.r * self.t) * (-self.s0 * np.exp(muT * self.t) * N1_ + self.k * N2_)
        
        if tp == 'C':
            return geoCall
        elif tp == 'P':
            return geoPut
        else:
            return 'Error'
        
option = GeoAsianOption(optionType='C', s0=100, sigma=0.3, r=0.05, t=3, k=100,
                 n=50)
