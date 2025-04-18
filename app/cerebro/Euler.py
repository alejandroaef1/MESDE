import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')
import os

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
        Z = np.random.normal(0, 1,size=self.n-1)  
        Z_star = 1 + self.mu*self.dt + self.sigma*np.sqrt(self.dt)*Z
        trayectoria = self.inicio*np.cumprod(Z_star)
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