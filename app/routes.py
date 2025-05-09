from flask import Flask, Blueprint, render_template, request, session, redirect, url_for
import pandas as pd
from app.cerebro.Ptrancision import MetodoPtransicion
from app.cerebro.Euler import MetodoEuler
from app.cerebro.Milstein import MetodoMilstein
from app.cerebro.Estimacion import estimadorTransicion
from app.cerebro.PHipotesis import PruebaHipotesis
from app.cerebro.EstimadoresML import EstimadoresMl
from app.cerebro.graficaMu import graficaMu
from app.cerebro.datosReales import SerieTiempo

bp = Blueprint('main', __name__)

###############################################################
"""""
Templates para las páginas del sitio
"""
################################################################

# Home
@bp.route('/')
def index():
    #Grafica serie de tiempo
    serie = SerieTiempo()
    serie.serieTemporal()
    serie.serieTemporalSegmentada()
    return render_template('index.html')

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
"""""
Acciones
"""
###########################################################################

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
    mu, sigma = estimadores.estimaciones()
    
    tabla2 = pd.DataFrame(data=[mu, sigma], index=['μ', 'σ'])
    tabla_html2 = tabla2.to_html()

    graficaDrift = graficaMu(pasos, partida, tiempo, drift)
    graficaDrift.calculos()

    return render_template('estimaciones.html', tabla_html2=tabla_html2)

app = Flask(__name__)
app.register_blueprint(bp)

if __name__ == '__main__':
    app.run(debug=True)
