from flask import Flask, Blueprint, render_template, request, session, redirect, url_for, jsonify
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')
import os
from app.cerebro.Ptrancision import MetodoPtransicion
from app.cerebro.Euler import MetodoEuler
from app.cerebro.Milstein import MetodoMilstein
from app.cerebro.Estimacion import estimadorTransicion
from app.cerebro.PHipotesis import PruebaHipotesis
from app.cerebro.EstimadoresML import EstimadoresMl
from app.cerebro.graficaMu import graficaMu
from app.cerebro.datosReales import SerieTiempo
from app.cerebro.residuales  import Residuales

bp = Blueprint('main', __name__)

################################################################
################## PESTAÑAS ####################################
################################################################

# Home
@bp.route('/')
def index():
    #Grafica serie de tiempo
    serie = SerieTiempo()
    fechas, valores = serie.serieTemporal_pandas()
    serie.grafica(fechas,valores)
    # Estimadores en serie de tiempo
    numeracion = list(range(0, len(fechas)))
    numeracion = [x/len(numeracion) for x in numeracion]
    T = len(numeracion)
    

    estimadores = EstimadoresMl(T,valores)
    mu, sigma, dicc = estimadores.estimaciones()
    graficaE = MetodoEuler(dicc['Número de pasos'],dicc['Precio inicial'],dicc['Horizonte de tiempo'],dicc['μ'],dicc['σ'])
    
    for i in [0,1,2]:
       graficaE.plot_wc()

    tabla = pd.DataFrame(data=[mu, sigma], index=['μ', 'σ'])
    tabla_html = tabla.to_html()
                              

    return render_template('index.html', tabla_html=tabla_html)

# Simulaciones
@bp.route('/simulaciones')
def simulaciones():
    return render_template('simulaciones.html') 

# Pruebas de hipótesis
@bp.route('/transicion')
def transicion():
    return render_template('transicion.html')

# Estimación de parámetros
@bp.route('/estimaciones')
def estimaciones():
    return render_template('estimaciones.html')

###########################################################################
#################  ACCIONES ###############################################
###########################################################################

############################
"""""
Acciones en página de inicio
"""
############################
@bp.route('/test', methods=['POST'])
def test():
    #Grafica serie de tiempo
    serie = SerieTiempo()
    fechas, valores = serie.serieTemporal_pandas()
    serie.grafica(fechas,valores)
    # Estimadores en serie de tiempo
    numeracion = list(range(0, len(fechas)))
    numeracion = [x/len(numeracion) for x in numeracion]
    T = len(numeracion)

    estimadores = EstimadoresMl(T,valores)
    mu, sigma, dicc = estimadores.estimaciones()
    muestra = Residuales(dicc['Número de pasos'],dicc['Precio inicial'],dicc['Horizonte de tiempo'],mu,sigma,10000)
    muestrario, pvalor = muestra.residuales()

    muestrario.plot.hist(bins=100, alpha=0.7, color='skyblue', edgecolor='black')
    plt.title("Histograma")
    plt.xlabel("Valor")
    plt.ylabel("Frecuencia")
    image_path = os.path.join(os.path.abspath('app/static/images'), 'hist_muestrario.png')
    plt.savefig(image_path)  
    plt.close()
    
    pasos = dicc['Número de pasos']
    tiempo = dicc['Horizonte de tiempo']
    pinicial = dicc['Precio inicial']

    return jsonify({'pvalor': pvalor,'pasos': pasos,'tiempo': tiempo,'pinicial': pinicial})

# Acción de la pestaña simulaciones
@bp.route('/procesar', methods=['POST'])
def procesar():        
    
    # Obtener los datos del formulario y almacenarlos en la sesión
    pasos = int(request.form['pasos'])
    partida = float(request.form['partida'])
    tiempo = float(request.form['tiempo'])
    drift = float(request.form['drift'])
    volatilidad = float(request.form['volatilidad'])
 
    browniano = MetodoPtransicion(pasos, partida, tiempo, drift, volatilidad)
    browniano.brownianoTransicion()
    browniano.plot()
    
    browniano = MetodoEuler(pasos, partida, tiempo, drift, volatilidad)
    browniano.brownianoEuler()
    browniano.plot()

    browniano = MetodoMilstein(pasos, partida, tiempo, drift, volatilidad)
    browniano.brownianoMilstein()
    browniano.plot()
    
    return redirect(url_for('main.simulaciones'))   

# Acción de la prueba de hipótesis
@bp.route('/calculoTransicion', methods=['POST'])     
def calculoTransicion():
    
    # Parametros del BG y sus simulaciones
    simulaciones = int(request.form['simulaciones'])
    corte = int(request.form['corte'])
    pasos = int(request.form['pasos'])
    partida = float(request.form['partida'])
    tiempo = float(request.form['tiempo'])
    drift = float(request.form['drift'])
    volatilidad = float(request.form['volatilidad'])

    # Parámetros de la transición

    transiciones = estimadorTransicion(simulaciones, corte, pasos, partida, tiempo, drift, volatilidad)
    probabilidades1, probabilidades2, probabilidades3 = transiciones.calculoDistribucion()
    hipotesis1 = PruebaHipotesis(probabilidades1,probabilidades2)
    _, p_valor1 = hipotesis1.prueba()
    hipotesis2 = PruebaHipotesis(probabilidades2,probabilidades3)
    _, p_valor2 = hipotesis2.prueba()
    p_valor1 = {'p valor':p_valor1}
    p_valor2 = {'p valor':p_valor2}
    tabla = pd.DataFrame(data=[p_valor1,p_valor2])
    tabla_html = tabla.to_html()

    return render_template('transicion.html', tabla_html=tabla_html)

# Acción de la estimación de parámetros
@bp.route('/procesar2', methods=['POST'])
def procesar2():

    # Obtener los datos del formulario y almacenarlos en la sesión
    pasos = int(request.form['pasos'])
    partida = float(request.form['partida'])
    tiempo = float(request.form['tiempo'])
    drift = float(request.form['drift'])
    volatilidad = float(request.form['volatilidad'])

    browniano = MetodoEuler(pasos, partida, tiempo, drift, volatilidad)
    _, trayectoria =  browniano.brownianoEuler()
    browniano.plot()

    estimadores = EstimadoresMl(tiempo,trayectoria)
    mu, sigma, _ = estimadores.estimaciones()
    
    tabla2 = pd.DataFrame(data=[mu, sigma], index=['μ', 'σ'])
    tabla_html2 = tabla2.to_html()

    graficaDrift = graficaMu(pasos, partida, tiempo, drift)
    graficaDrift.calculos()

    return render_template('estimaciones.html', tabla_html2=tabla_html2)


app = Flask(__name__)
app.register_blueprint(bp)

if __name__ == '__main__':
    app.run(debug=True)
