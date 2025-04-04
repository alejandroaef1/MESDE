import numpy as np
import matplotlib.pyplot as plt

class MovimientoBrownianoGeometrico:
    def __init__(self, n, t_final, inicio, mu, sigma):
        """
        Inicializa los parámetros del Movimiento Browniano
        :param n: número de pasos en la simulación
        :param t_final: tiempo final de la simulación
        :param mu: Media 
        :param sigma: Volatilidad
        """
        self.n = n           # Número de pasos
        self.t_final = t_final  # Tiempo final
        self.dt = t_final / n  # El tamaño del paso de tiempo
        self.tiempos = np.linspace(0, t_final, n)  # Vector de tiempos
        self.inicio = inicio # Punto de partida del movimiento
        self.mu = mu # Media
        self.sigma =sigma # Volatilidad
        
    def brownianoGeometrico(self):

        for t in self.tiempos:
         pass    

