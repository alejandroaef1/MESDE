import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

class MovimientoBrowniano:
    def __init__(self, n, t_final):

        self.n = n           
        self.t_final = t_final  
        self.dt = t_final / n  
        self.tiempos = np.linspace(0, t_final, n)  

    def browniano(self):
  
        # Simulación del movimiento Browniano utilizando la ecuación:
        # W(t) = W(t-1) + sqrt(dt)*Z
        Z = np.random.normal(0, 1, self.n -1) 
        pasos = np.sqrt(self.dt) * Z
        trayectoria = np.insert(pasos,0,0)
        trayectoria = np.cumsum(trayectoria) 
    
        return self.tiempos, trayectoria

    def plot(self):

        tiempos, trayectoria = self.browniano()
        plt.plot(tiempos, trayectoria)
        plt.title(f'Movimiento Browniano')
        plt.xlabel('Tiempo')
        plt.ylabel('Posición')
        
        image_path = os.path.join(os.path.abspath('app/static/images'), 'graph.png')
        plt.savefig(image_path)  
        plt.close()

