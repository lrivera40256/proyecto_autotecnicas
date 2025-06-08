from flask import Flask, request, render_template, jsonify
import os
from werkzeug.utils import secure_filename
from services.bckt import bckt_caminos
from services.automata import procesar_archivo
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

@app.route('/validar-placas', methods=['POST'])
def validar_placas():
    if 'archivo' not in request.files:
        return jsonify({'error': 'No se envió ningún archivo'}), 400

    archivo = request.files['archivo']
    if archivo.filename == '':
        return jsonify({'error': 'Nombre de archivo vacío'}), 400

    nombre_seguro = secure_filename(archivo.filename)
    ruta_temporal = os.path.join('data', nombre_seguro)
    archivo.save(ruta_temporal)

    resultados = procesar_archivo(ruta_temporal)
    os.remove(ruta_temporal)

    return jsonify({'resultado': resultados})

if __name__ == "__main__":
    app.run(debug=True)