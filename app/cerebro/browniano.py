import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

class MovimientoBrowniano:
    def __init__(self, n, t_final):
        """
        Inicializa los parámetros del Movimiento Browniano
        :param n: número de pasos en la simulación
        :param t_final: tiempo final de la simulación
        :param mu: media (por defecto 0)
        :param sigma: desviación estándar (por defecto 1)
        """
        self.n = n           # Número de pasos
        self.t_final = t_final  # Tiempo final
        self.dt = t_final / n  # El tamaño del paso de tiempo
        self.tiempos = np.linspace(0, t_final, n)  # Vector de tiempos

    def browniano(self):
        """
        Genera el Movimiento Browniano
        :return: trayectorias del movimiento Browniano
        """
        # Simulación del movimiento Browniano utilizando la ecuación:
        # W(t) = W(t-1) + sqrt(dt)*Z
        Z = np.random.normal(0, 1, self.n)  # Generación de ruido blanco
        pasos = np.sqrt(self.dt) * Z
        trayectoria = np.cumsum(pasos)  # Acumulando los pasos para obtener el movimiento

        return self.tiempos, trayectoria

    def plot(self):
        """
        Genera la gráfica
        """

        tiempos, trayectoria = self.browniano()
        plt.plot(tiempos, trayectoria)
        plt.title(f'Movimiento Browniano')
        plt.xlabel('Tiempo')
        plt.ylabel('Posición')
        
        image_path = os.path.join(os.path.abspath('app/static/images'), 'graph.png')
        plt.savefig(image_path)  
        plt.close()

