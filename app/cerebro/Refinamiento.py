import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

class Refinamiento:

    def __init__(self, DataFrame, segmentos):
        
        self.datos = DataFrame
        self.segmentos = segmentos

    def segmentacion(self):

        distribucion = pd.cut(self.datos, bins=self.segmentos)
        distribucion = distribucion.value_counts(normalize=True).sort_index()
        distribucion_transicion = pd.DataFrame({'Intervalo':distribucion.index, 'Probabilidad':distribucion.values})

        self.datos.plot.hist(bins=self.segmentos)  # bins=10 para el número de barras, alpha=0.7 para la transparencia
        plt.title('Histograma')  # Título del gráfico
        plt.xlabel('Valor')  # Etiqueta del eje X
        plt.ylabel('Frecuencia')  # Etiqueta del eje Y
        image_path = os.path.join(os.path.abspath('app/static/images'), 'histograma.png')
        plt.savefig(image_path) 
        plt.close()


        return distribucion_transicion