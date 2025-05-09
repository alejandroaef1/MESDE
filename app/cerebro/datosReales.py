
import os
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
matplotlib.use('Agg')

class SerieTiempo():

    def __init__(self):
        pass
    
    def serieTemporal(self):
        df = pd.read_csv('C:\\Users\\aaesf\\Documents\\App SDE\\SDE\\app\\static\\docs\\stiempo.csv')
        df['VIGENCIADESDE'] = pd.to_datetime(df['VIGENCIADESDE'], dayfirst=True)
        df['VALOR'] = df['VALOR'].str.replace(',', '', regex=False).str.replace('.', '', regex=False)
        df['VALOR'] = df['VALOR'].astype(float)
        df['VALOR'] = df['VALOR']/100

        df.set_index('VIGENCIADESDE', inplace=True)

        df['VALOR'].plot(title='Tiempo total')
        plt.xlabel('Fecha')
        plt.ylabel('Precio')
        plt.grid(True)

        image_path = os.path.join(os.path.abspath('app/static/images'), 'stiempo.png')
        plt.savefig(image_path)  
        plt.close()

    def serieTemporalSegmentada(self):
        
        df = pd.read_csv('C:\\Users\\aaesf\\Documents\\App SDE\\SDE\\app\\static\\docs\\stiempo.csv')
        inicio = '2017-03-01'    
        final = '2017-12-01'
        print(df)
        df['VIGENCIADESDE'] = pd.to_datetime(df['VIGENCIADESDE'], format='%d/%m/%Y')
        print(df)
        df.set_index('VIGENCIADESDE', inplace=True)
        print(df)
        df = df[df.index.to_series().between(inicio, final)]
        print(df)
        df['VALOR'] = df['VALOR'].str.replace(',', '', regex=False).str.replace('.', '', regex=False)
        df['VALOR'] = df['VALOR'].astype(float)
        df['VALOR'] = df['VALOR']/100
        df['VALOR'].plot(title='Ventana de tiempo del experimento')
        plt.xlabel('Fecha')
        plt.ylabel('Precio')
        plt.grid(True)

        image_path = os.path.join(os.path.abspath('app/static/images'), 'stiempoParcial.png')
        plt.savefig(image_path)  
        plt.close()



