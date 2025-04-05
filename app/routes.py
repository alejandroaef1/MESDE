from flask import Flask, Blueprint, render_template, request, session
from app.cerebro.browniano import MovimientoBrowniano

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/procesar', methods=['POST'])
def procesar():    
    
    # Obtener los datos del formulario y almacenarlos en la sesión
    pasos = int(request.form['pasos'])
    tiempo = float(request.form['tiempo'])
    
    # Almacenar los valores en la sesión
    session['pasos'] = pasos
    session['tiempo'] = tiempo

    pasos = session.get('pasos')
    tiempo = session.get('tiempo')
    
    
    # Usar los valores para el cálculo
    browniano = MovimientoBrowniano(pasos, tiempo)
    browniano.browniano()
    browniano.plot()

    return render_template('index.html')

app = Flask(__name__)
app.register_blueprint(bp)

if __name__ == '__main__':
    app.run(debug=True)
