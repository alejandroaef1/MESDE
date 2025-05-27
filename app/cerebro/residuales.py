import numpy as np
import pandas as pd
from app.cerebro.Euler import MetodoEuler
from scipy.stats import kstest

class Residuales:
    def __init__(self,n,inicio,t_final,mu,sigma,nsimulaciones):

        self.n=n
        self.inicio=inicio
        self.t_final=t_final
        self.mu=mu
        self.sigma=sigma
        self.dt = t_final / n 
        self.s = nsimulaciones

    def residuales(self): 
        # Muestra método Euler
        lista_muestrario_1 = []
        simulacion1 = MetodoEuler(self.n, self.inicio, self.t_final, self.mu, self.sigma)
        
        for i in range(self.n):
             _, trayectoria = simulacion1.brownianoEuler()
             trayectoriaA = (1/self.sigma)*(np.log(trayectoria))
             trayectoriaB = ((self.mu/self.sigma)-(0.5*self.sigma))*self.dt
             #trayectoriaB = trayectoriaB[1:]
             trayectoriaA = np.diff(trayectoriaA) - trayectoriaB
             lista_muestrario_1.append(trayectoriaA) 

        muestrario_1 = pd.DataFrame(lista_muestrario_1)
        muestrario = muestrario_1.iloc[:,round(0.5*self.n)]
        statistic, pvalue = kstest(muestrario, 'norm', args=(0,self.dt))
        print(pvalue)

        return muestrario, pvalue
    
        
        

