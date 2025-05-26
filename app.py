from flask import Flask, render_template, jsonify
from services.bckt import bckt_caminos
from utils.lector_json import lector_json

app = Flask(__name__)

# Ruta principal que muestra el HTML
@app.route('/')
def index():
    return render_template('index.html')

# Ruta API que devuelve el laberinto y las soluciones
@app.route('/lab-interestelar', methods=['GET'])
def laberinto_data():
    matriz = lector_json('data/test5x5.json')
    print("Matriz cargada:", matriz)
    
    # Mapa cargado
    for fila in matriz['matrizInicial']:
        print(' '.join(str(celda) for celda in fila)) 
        
    soluciones = bckt_caminos(matriz['tamMatriz'],
                             matriz['origen'],
                             matriz['destino'],
                             matriz['agujerosNegros'],
                             matriz['estrellasGigantes'],
                             matriz['agujerosGusano'],
                             matriz['zonasRecarga'],
                             matriz['celdasCargaRequerida'],
                             matriz['cargaInicial'],
                             matriz['matrizInicial'],
                             [],
                             [])
    return jsonify({
        'matriz': matriz,
        'soluciones': soluciones
    })

if __name__ == "__main__":
    app.run(debug=True)