import numpy as np
from scipy import stats
from app.cerebro.Estimacion import estimadorTransicion

class PruebaHipotesis:
    def __init__(self,d1,d2):
        
        self.d1 = d1
        self.d2 = d2

    def prueba(self):

        estadistico, p_valor = stats.ks_2samp(self.d1, self.d2)
        return estadistico, p_valor

        

