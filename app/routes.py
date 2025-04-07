from flask import Flask, Blueprint, render_template, request, session, redirect, url_for
import pandas as pd
from app.cerebro.Ptrancision import MetodoPtransicion
from app.cerebro.Euler import MetodoEuler
from app.cerebro.Milstein import MetodoMilstein
from app.cerebro.Estimacion import estimadorTransicion
from app.cerebro.Refinamiento import Refinamiento

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/simulaciones')
def simulaciones():
    return render_template('simulaciones.html') 

@bp.route('/transicion')
def transicion():
    return render_template('transicion.html')

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
    segmentos = int(request.form['segmentos'])

    transiciones = estimadorTransicion(simulaciones, corte, pasos, partida, tiempo, drift, volatilidad)
    probabilidades = transiciones.calculoDistribucion()
    segmentacion = Refinamiento(probabilidades, segmentos)
    transiciones_calculadas = segmentacion.segmentacion()
    tabla_html = transiciones_calculadas.to_html()

    return render_template('transicion.html', tabla_html=tabla_html)



app = Flask(__name__)
app.register_blueprint(bp)

if __name__ == '__main__':
    app.run(debug=True)
