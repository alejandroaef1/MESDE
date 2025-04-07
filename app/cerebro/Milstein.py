import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')
import os

class MetodoMilstein:
    def __init__(self, n, inicio, t_final, mu, sigma):

        self.n = n          
        self.t_final = t_final  
        self.dt = t_final / n  
        self.tiempos = np.linspace(0, t_final, n) 
        self.inicio = inicio 
        self.mu = mu 
        self.sigma =sigma 
       
        
    def brownianoMilstein(self):
        
        trayectoria = np.zeros(self.n)
        trayectoria[0] = self.inicio
        for i in range(1, self.n):
          Z = np.random.normal(0, np.sqrt(self.dt))
          trayectoria[i] = trayectoria[i-1] + self.mu * trayectoria[i-1] * self.dt + self.sigma * trayectoria[i-1] * Z + 0.5 * self.sigma**2 * trayectoria[i-1] * (Z**2 - self.dt)

        return self.tiempos, trayectoria

    def plot(self):

        tiempos, trayectoria = self.brownianoMilstein()
        plt.plot(tiempos, trayectoria)
        plt.title(f'Simulación método Milstein')
        plt.xlabel('Tiempo')
        plt.ylabel('Posición')
        
        image_path = os.path.join(os.path.abspath('app/static/images'), 'milstein.png')
        plt.savefig(image_path)  
        plt.close()