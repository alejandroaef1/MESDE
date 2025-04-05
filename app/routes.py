from flask import Flask, Blueprint, render_template, request, session, redirect, url_for
from app.cerebro.BrownianoGeometrico import MovimientoBrownianoGeometrico
from app.cerebro.Euler import MetodoEuler

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/Probabilidades-de-transicion')
def Ptransicion():
    return render_template('Ptransicion.html')

@bp.route('/Método-de-Euler')
def Euler():
    return render_template('Euler.html')

@bp.route('/procesar', methods=['POST'])
def procesar():    
    
    # Obtener los datos del formulario y almacenarlos en la sesión
    pasos = int(request.form['pasos'])
    partida = float(request.form['partida'])
    tiempo = float(request.form['tiempo'])
    drift = float(request.form['drift'])
    volatilidad = float(request.form['volatilidad'])
    clave = request.form['clave']

    # Almacenar los valores en la sesión
    session['pasos'] = pasos
    session['partida'] = partida
    session['tiempo'] = tiempo
    session['drift'] = drift
    session['volatilidad'] = volatilidad
    session['clave'] = clave

    pasos = session.get('pasos')
    partida = session.get('partida')
    tiempo = session.get('tiempo')
    drift = session.get('drift')
    volatilidad = session.get('volatilidad')
    clave = session.get('clave')
    
    if clave =='transicion':

        browniano = MovimientoBrownianoGeometrico(pasos, partida, tiempo, drift, volatilidad)
        browniano.brownianoGeometrico()
        browniano.plot()

        return redirect(url_for('main.ptransicion')) 

    elif clave=='euler':    
        browniano = MetodoEuler(pasos, partida, tiempo, drift, volatilidad)
        browniano.brownianoEuler()
        browniano.plot()
    
        return redirect(url_for('main.meuler'))

@bp.route('/ptransicion')
def ptransicion():
    # Aquí se muestra el resultado del procesamiento
    return render_template('Ptransicion.html') 

@bp.route('/meuler')
def meuler():
    # Aquí se muestra el resultado del procesamiento
    return render_template('Euler.html')    

app = Flask(__name__)
app.register_blueprint(bp)

if __name__ == '__main__':
    app.run(debug=True)
