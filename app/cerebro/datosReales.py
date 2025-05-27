from datetime import datetime
import os
import matplotlib
import matplotlib.pyplot as plt
import csv
import pandas as pd
import numpy as np
matplotlib.use('Agg')

class SerieTiempo():

    def __init__(self):
        pass
    
    def serieTemporal(self):
        # Método que toma el archivo csv y lo deja listo para usar en el resto de la librería.  
        tabla = []
        datos = 'C:\\Users\\aaesf\\Documents\\App SDE\\SDE\\app\\static\\docs\\stiempo.csv'
        with open(datos, newline='', encoding='utf-8') as archivo:
            lector = csv.reader(archivo)
            for fila in lector:
                tabla.append(fila)

        valores = [float(fila[0].replace(',','').replace('.',''))/100 for fila in tabla[1:]] 
        fechas = [fila[2] for fila in tabla[1:]]
        fechas = [datetime.strptime(f, '%d/%m/%Y') for f in fechas]
        #numeracion = list(range(1, len(valores) + 1))

        return fechas, valores

    def grafica(self,fechas,valores):
        # Método que grfíca la serie temporal.
        plt.plot(fechas,valores)
        plt.xlabel('Fecha')
        plt.ylabel('Precio')
        plt.grid(True)
        plt.xticks(rotation=45)  # O usa 90 para vertical
        plt.tight_layout() 

        image_path = os.path.join(os.path.abspath('app/static/images'), 'stiempo.png')
        plt.savefig(image_path)  
        plt.close()

    def serieTemporalSegmentada(self,fechas,valores):
        # Método que grafíca la segmentación
        inicio = datetime.strptime('2005-01-01', '%Y-%m-%d')  
        final = datetime.strptime('2017-02-01', '%Y-%m-%d')  
        segmentacion_fechas  = [f for f in fechas if f > inicio and f < final]
        
        posicion_i = fechas.index(segmentacion_fechas[0])
        posicion_f = fechas.index(segmentacion_fechas[-1])
        segmentacion_valores = valores[posicion_i:posicion_f+1]

        plt.plot(segmentacion_fechas,segmentacion_valores)
        plt.xlabel('Fecha')
        plt.ylabel('Precio')
        plt.grid(True)
        plt.xticks(rotation=45)  # O usa 90 para vertical
        plt.tight_layout() 

        image_path = os.path.join(os.path.abspath('app/static/images'), 'stiempoParcial.png')
        plt.savefig(image_path)  
        plt.close()

        return segmentacion_fechas, segmentacion_valores

    def serieTemporal_pandas(self):
        # Método que toma el archivo csv y lo deja listo para usar en el resto de la librería.  
        tabla = []
        datos = 'C:\\Users\\aaesf\\Documents\\App SDE\\SDE\\app\\static\\docs\\stiempo.csv'
        df = pd.read_csv(datos)
        df['VIGENCIADESDE'] = pd.to_datetime(df['VIGENCIADESDE'], format='%d/%m/%Y')
        df['Fechas'] = df['VIGENCIADESDE']
        df['VIGENCIAHASTA'] = pd.to_datetime(df['VIGENCIAHASTA'], format='%d/%m/%Y')
        df = df.sort_values(by='Fechas', ascending=True)
        df['VALOR'] = df['VALOR'].str.replace(',','',regex=False).str.replace('.','',regex=False).astype(float)/100
        df = df.set_index('VIGENCIADESDE')
        #df_mensual = df.resample('M').last()
        df_segmentado = df.loc[(df['Fechas'] >= '2005-01-01') & (df['Fechas'] <= '2017-02-01')]
        df_segmentado['log_return'] = np.log(df_segmentado['VALOR'] / df_segmentado['VALOR'].shift(1))
        fechas = df_segmentado['Fechas'].to_list()
        valores = df_segmentado['VALOR'].to_list()

        return fechas, valores

