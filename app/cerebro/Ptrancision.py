import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')
import os
from scipy.stats import lognorm

class MetodoPtransicion:
    def __init__(self, n, inicio, t_final, mu, sigma):

        self.n = n           
        self.t_final = t_final  
        self.dt = t_final / n  
        self.tiempos = np.linspace(0, t_final, n)  
        self.inicio = inicio 
        self.mu = mu 
        self.sigma =sigma       
        self.forma = self.sigma*np.sqrt(self.dt)

    def brownianoTransicion(self):
        s = self.inicio
        trayectoria = np.zeros(self.n)
        trayectoria[0] = s
        for i in range(1,self.n):
            escala = s*np.exp((self.mu - (self.sigma**2)*0.5)*self.dt)
            s = lognorm.rvs(self.forma,scale=escala) 
            trayectoria[i] = s 

        return self.tiempos, trayectoria

    def plot(self):

        tiempos, trayectoria = self.brownianoTransicion()
        plt.plot(tiempos, trayectoria)
        plt.title(f'Simulación con probabilidades de transición')
        plt.xlabel('Tiempo')
        plt.ylabel('Posición')
        
        image_path = os.path.join(os.path.abspath('app/static/images'), 'transicion.png')
        plt.savefig(image_path)  
        plt.close()


