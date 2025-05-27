import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')
import os
from app.cerebro.browniano import MovimientoBrowniano

class MetodoEuler:
    def __init__(self, n, inicio, t_final, mu, sigma):

        self.n = n          
        self.t_final = t_final  
        self.dt = t_final / n  
        self.tiempos = np.linspace(0, t_final, n) 
        self.inicio = inicio 
        self.mu = mu 
        self.sigma =sigma 
       
        
    def brownianoEuler(self):
        B = MovimientoBrowniano(self.n,self.t_final)
        _, W = B.browniano()
        DW = np.diff(W)  
        trayectoria = 1 + self.mu*self.dt + self.sigma*(DW)
        trayectoria = self.inicio*np.cumprod(trayectoria)
        trayectoria = np.insert(trayectoria, 0, self.inicio)
        return self.tiempos, trayectoria

    def plot(self):
        
        tiempos, trayectoria = self.brownianoEuler()
        plt.plot(tiempos, trayectoria)
        plt.title(f'Simulación método Euler')
        plt.xlabel('Tiempo')
        plt.ylabel('Posición')
        
        image_path = os.path.join(os.path.abspath('app/static/images'), 'euler.png')
        plt.savefig(image_path)  
        plt.close()

    def plot_wc(self):
        
        tiempos, trayectoria = self.brownianoEuler()
        plt.plot(tiempos, trayectoria)
        plt.xlabel('Tiempo en n° de días')
        plt.ylabel('Posición')
        plt.grid(True)
        plt.xticks(rotation=45)  # O usa 90 para vertical
        plt.tight_layout() 
        
        image_path = os.path.join(os.path.abspath('app/static/images'), 'euler_wc.png')
        plt.savefig(image_path)    