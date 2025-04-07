import numpy as np
import pandas as pd
from app.cerebro.Euler import MetodoEuler

class estimadorTransicion:

    def __init__(self, nsim, corte, n, t_final, inicio, mu, sigma):
       
        self.nsimulaciones = nsim
        self.n = n          
        self.t_final = t_final  
        self.dt = t_final / n  
        self.tiempos = np.linspace(0, t_final, n) 
        self.inicio = inicio 
        self.mu = mu 
        self.sigma =sigma 
        self.corte = corte 

    def generadorSimulaciones(self):

        lista_muestrario = []
        simulacion = MetodoEuler(self.n, self.t_final, self.inicio, self.mu, self.sigma)
        
        for i in range(self.nsimulaciones):
             _, trayectoria = simulacion.brownianoEuler()
             lista_muestrario.append(trayectoria)

        muestrario = pd.DataFrame(lista_muestrario)
        muestrario.columns = [f'C_{i+1}' for i in range(muestrario.shape[1])]
        
        return muestrario

    def calculoDistribucion(self):

        muestrario = self.generadorSimulaciones()
        posicion_corte = self.corte
        probabilidades = muestrario[f'C_{posicion_corte}']
        
        return probabilidades

        

