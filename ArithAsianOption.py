import scipy.stats as sps
import numpy as np
import math


# n=step: the number of observation times for the geometric average
# m=path: the number of paths in the Monte Carlo simulation

class ArithAsianOption:
    def __init__(self, optionType=None, s0=0, sigma=0, r=0, t=0, k=0,
                 n=100, m=100000, cv=False):
        self.s0 = s0 * 1.0
        self.sigma = sigma
        self.r = r * 1.0
        self.t = t * 1.0
        self.k = k * 1.0
        self.n = n
        self.m = m
        self.optionType = optionType
        self.cv = cv
    def __repr__(self):
        return"AAO({}, {}, {}, {}, {}, {}, {},{},{})".\
        format(self.optionType,self.s0,self.sigma,self.r,self.t,self.k,self.n,self.m,self.cv)
        
    def cal(self):
        np.random.seed(20)
        n = self.n
        m = self.m
        dt = self.t/n
        Spath = np.zeros((m, n), order='F')
        rd = np.zeros((m, n), order='F')
        
        sigT = self.sigma*math.sqrt((n+1)*(2*n+1)/(6*n*n))
        muT = 0.5*sigT**2 + (self.r - 0.5*pow(self.sigma, 2))*(n+1)/(2*n)
        # (r-0.5*pow(sigma, 2))*(N+1)/(2*N)+0.5*pow(sigmaHat, 2)
        c1 = self.r - 0.5 * pow(self.sigma, 2)
        c2 = self.sigma * np.sqrt(dt)
        
        d1 = (np.log(self.s0/self.k) + (muT + 0.5*sigT))/np.sqrt(sigT)
        d2 = d1 - np.sqrt(self.t) * sigT
        
        N1 = sps.norm.cdf(d1)
        N2 = sps.norm.cdf(d2)
        
        for i in range(0, m):
            rd[i, :] = np.random.standard_normal(n)
            
        Spath[:, 0] = self.s0 * np.exp(c1 * dt + c2 * rd[:, 0])
          
        for j in range(1, n):
            ns = Spath[:, j-1]
            Spath[:, j] = ns * np.exp(c1 * dt + c2 * rd[:, j])
            
        #Arithmetic mean
        arithMean = Spath.mean(1)
        #Geometric mean
        geoMean = np.exp(1/float(n)*np.log(Spath).sum(1))
        
        if self.optionType == 'C':
            arithPayoff = np.exp(-self.r*self.t)*np.maximum(arithMean - self.k, 0)
            geoPayoff = np.exp(-self.r*self.t)*np.maximum(geoMean - self.k, 0)
            mean = np.mean(arithPayoff)
            std = np.std(arithPayoff)
            confmc_low = mean - (1.96*std/np.sqrt(m))
            confmc_high = mean + (1.96*std/np.sqrt(m))
            
        elif self.optionType == 'P':
            arithPayoff = np.exp(-self.r*self.t)*np.maximum(self.k - arithMean, 0)
            geoPayoff = np.exp(-self.r*self.t)*np.maximum(self.k - geoMean, 0)
            mean = np.mean(arithPayoff)
            std = np.std(arithPayoff)
            confmc_low = mean - (1.96*std/np.sqrt(m))
            confmc_high = mean + (1.96*std/np.sqrt(m))
        
        #Standard Monte Carlo
        if self.cv == 'MC':
            output = []
            output.append(mean)
            output.append(confmc_low)
            output.append(confmc_high)
            return output
        elif self.cv == 'CV':
        #Control Variate
            covXY = np.mean(arithPayoff * geoPayoff) - np.mean(arithPayoff)* np.mean(geoPayoff)
            theta = covXY/np.var(geoPayoff)
            output = []
        #control variate version
            if self.optionType == 'C':
                geo = math.exp(-self.r * self.t) * (self.s0 * np.exp(muT * self.t) * N1 - self.k * N2)
                Z = arithPayoff + theta * (geo - geoPayoff)
                mean = np.mean(Z)
                std = np.std(Z)
                confcv_low = mean - (1.96*std/np.sqrt(m))
                confcv_high = mean + (1.96*std/np.sqrt(m))
                output.append(mean)
                output.append(confmc_low)
                output.append(confmc_high)
                return output
            elif self.optionType == 'P':
                N1_ = sps.norm.cdf(-d1)
                N2_ = sps.norm.cdf(-d2)
                geo = math.exp(-self.r * self.t) * (-self.s0 * np.exp(muT * self.t) * N1_ + self.k * N2_)
                Z = arithPayoff + theta * (geo - geoPayoff)
                mean = np.mean(Z)
                std = np.std(Z)
                confcv_low = mean - (1.96*std/np.sqrt(m))
                confcv_high = mean + (1.96*std/np.sqrt(m))
                output.append(mean)
                output.append(confmc_low)
                output.append(confmc_high)
                return output
              

#if __name__ == '__main__':
#    option = ArithAsianOption(optionType='C', s0=100, sigma=0.3, r=0.05, t=3, k=100,
#                 n=50, m=100000, cv= 'Monte Carlo')
#    option2 = ArithAsianOption(optionType='C', s0=100, sigma=0.3, r=0.05, t=3, k=100,
#                 n=50, m=100000, cv= 'Control Variate')
#    option3 = ArithAsianOption(optionType='P', s0=100, sigma=0.3, r=0.05, t=3, k=100,
#                 n=50, m=100000, cv= 'Monte Carlo')
#    option4 = ArithAsianOption(optionType='P', s0=100, sigma=0.3, r=0.05, t=3, k=100,
#                 n=50, m=100000, cv= 'Control Variate')
#    answer = option.calc()
#    print(("The answer is: \n" + str(answer[0])\
#                                 + "\n" + "The 95% confidence interval is:\n"\
#                                 + str(answer[1]) + "," + str(answer[2])))
#    print(option.calc())
#    print(option2.calc())
#    print(option3.calc())
#    print(option4.calc())
        