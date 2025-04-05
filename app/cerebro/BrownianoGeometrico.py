import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')
import os

class MovimientoBrownianoGeometrico:
    def __init__(self, n, inicio, t_final, mu, sigma):

        self.n = n           
        self.t_final = t_final  
        self.dt = t_final / n  
        self.tiempos = np.linspace(0, t_final, n)  
        self.inicio = inicio 
        self.mu = mu 
        self.sigma =sigma       
        self.eta = np.log(self.inicio) + (self.mu - (self.sigma**2)/2)*self.dt
        self.nu = (self.sigma**2)*self.dt

    def brownianoGeometrico(self):

        trayectoria = np.zeros(self.n)
        trayectoria[0] = self.inicio
        for i in range(1,self.n):
            increment = np.random.lognormal((self.mu - 0.5 * self.sigma**2) * self.dt, self.sigma * np.sqrt(self.dt))
            trayectoria[i] = trayectoria[i-1] * increment

        return self.tiempos, trayectoria

    def plot(self):

        tiempos, trayectoria = self.brownianoGeometrico()
        plt.plot(tiempos, trayectoria)
        plt.title(f'Simulación con probabilidades de transición')
        plt.xlabel('Tiempo')
        plt.ylabel('Posición')
        
        image_path = os.path.join(os.path.abspath('app/static/images'), 'geometrico.png')
        plt.savefig(image_path)  
        plt.close()


