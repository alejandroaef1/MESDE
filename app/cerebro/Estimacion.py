import numpy as np
import pandas as pd
from app.cerebro.Euler import MetodoEuler
from app.cerebro.Ptrancision import MetodoPtransicion
from app.cerebro.Milstein import MetodoMilstein

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

        # Muestra método Euler
        lista_muestrario_1 = []
        simulacion1 = MetodoEuler(self.n, self.t_final, self.inicio, self.mu, self.sigma)
        
        for i in range(self.nsimulaciones):
             _, trayectoria = simulacion1.brownianoEuler()
             lista_muestrario_1.append(trayectoria)

        muestrario_1 = pd.DataFrame(lista_muestrario_1)
        muestrario_1.columns = [f'C_{i+1}' for i in range(muestrario_1.shape[1])]
        
        # Muestra método Ptransición
        lista_muestrario_2 = []
        simulacion2 = MetodoPtransicion(self.n, self.t_final, self.inicio, self.mu, self.sigma)
        
        for i in range(self.nsimulaciones):
             _, trayectoria = simulacion2.brownianoTransicion()
             lista_muestrario_2.append(trayectoria)

        muestrario_2 = pd.DataFrame(lista_muestrario_2)
        muestrario_2.columns = [f'C_{i+1}' for i in range(muestrario_2.shape[1])]

        # Muestra método Milstein
        lista_muestrario_3 = []
        simulacion3 = MetodoMilstein(self.n, self.t_final, self.inicio, self.mu, self.sigma)
        
        for i in range(self.nsimulaciones):
             _, trayectoria = simulacion3.brownianoMilstein()
             lista_muestrario_3.append(trayectoria)

        muestrario_3 = pd.DataFrame(lista_muestrario_3)
        print(muestrario_3)
        muestrario_3.columns = [f'C_{i+1}' for i in range(muestrario_3.shape[1])]
        

        return muestrario_1, muestrario_2, muestrario_3

    def calculoDistribucion(self):

        muestrario_1, muestrario_2, muestrario_3 = self.generadorSimulaciones()
        posicion_corte = self.corte
        probabilidades_1 = muestrario_1[f'C_{posicion_corte}']
        probabilidades_2 = muestrario_2[f'C_{posicion_corte}']
        probabilidades_3 = muestrario_3[f'C_{posicion_corte}']
        
        return probabilidades_1, probabilidades_2, probabilidades_3
    

        

