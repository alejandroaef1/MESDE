import numpy as np
from app.cerebro.EstimadoresML import EstimadoresMl
from app.cerebro.Euler import MetodoEuler
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')
import os

class graficaMu:
    def __init__(self,pasos, partida,tiempo,drift):
        self.n = pasos
        self.i = partida
        self.T = tiempo
        self.mu = drift
      
    def calculos(self):
        volatilidad = np.linspace(0,10,1000)
        drift = []
        for i in range(1000):
            browniano = MetodoEuler(self.n,self.i,self.T,self.mu,volatilidad[i])
            _, trayectoria = browniano.brownianoEuler()
            estimadores = EstimadoresMl(self.T,trayectoria)
            mu, _, _ = estimadores.estimaciones()
            drift.append(mu)

        plt.plot(volatilidad,drift)
        plt.title(f'Volatilidad vs Drift')
        plt.xlabel('Volatilidad')
        plt.ylabel('drift')

        image_path = os.path.join(os.path.abspath('app/static/images'), 'drift.png')
        plt.savefig(image_path)  
        plt.close()


        





