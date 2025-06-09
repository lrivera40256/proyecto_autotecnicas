from flask import Flask, request, jsonify
from services.automata import procesar_archivo_placa, procesar_archivo_IP
import os
from flask import Flask, request, render_template, jsonify
import os
from werkzeug.utils import secure_filename
from services.bckt import bckt_caminos
from services.automata import procesar_archivo_placa
from utils.lector_json import lector_json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit
ALLOWED_EXTENSIONS = {'json'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Aseguramos que existe el directorio de uploads
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Ruta principal que muestra el HTML
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/backtracking')
def backtracking():
    return render_template('backtracking.html')

@app.route('/automata')
def automata():
    return render_template('automata.html')

@app.route('/upload-json', methods=['POST'])
def upload_json():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        try:
            matriz = lector_json(filepath)
            soluciones = []
            encontrado = bckt_caminos(matriz['tamMatriz'],
                                    matriz['origen'],
                                    matriz['destino'],
                                    matriz['agujerosNegros'],
                                    matriz['estrellasGigantes'],
                                    matriz['agujerosGusano'],
                                    matriz['zonasRecarga'],
                                    matriz['celdasCargaRequerida'],
                                    matriz['cargaInicial'],
                                    matriz['matrizInicial'],
                                    soluciones,
                                    [])
            return jsonify({
                'matriz': matriz,
                'soluciones': soluciones
            })
        finally:
            # Limpiamos el archivo después de usarlo
            if os.path.exists(filepath):
                os.remove(filepath)
    return jsonify({'error': 'Invalid file type'}), 400

# Ruta API que devuelve el laberinto y las soluciones
# @app.route('/lab-interestelar', methods=['GET'])
# def laberinto_data():
#     # Usar archivo por defecto si no hay uno subido
#     matriz = lector_json('data/test5x5.json')
#     print("Matriz cargada:", matriz)
    
#     # Mapa cargado
#     for fila in matriz['matrizInicial']:
#         print(' '.join(str(celda) for celda in fila)) 
        
#     soluciones = []
#     encontrado = bckt_caminos(matriz['tamMatriz'],
#                              matriz['origen'],
#                              matriz['destino'],
#                              matriz['agujerosNegros'],
#                              matriz['estrellasGigantes'],
#                              matriz['agujerosGusano'],
#                              matriz['zonasRecarga'],
#                              matriz['celdasCargaRequerida'],
#                              matriz['cargaInicial'],
#                              matriz['matrizInicial'],
#                              soluciones,
#                              [])
#     return jsonify({
#         'matriz': matriz,
#         'soluciones': soluciones
#     })

@app.route('/validar', methods=['POST'])
def validar():
    if 'archivo' not in request.files:
        return jsonify(['Error: No se envió ningún archivo']), 400
    
    archivo = request.files['archivo']
    tipo = request.form.get('tipo', 'placa')
    
    if archivo.filename == '':
        return jsonify(['Error: No se seleccionó ningún archivo']), 400
    
    # Guardar el archivo temporalmente
    temp_path = 'temp.txt'
    archivo.save(temp_path)
    
    try:
        if tipo == 'placa':
            resultados = procesar_archivo_placa(temp_path)
        else:
            resultados = procesar_archivo_IP(temp_path)
            
        return jsonify(resultados)
    
    finally:
        # Limpiar el archivo temporal
        if os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == "__main__":
    app.run(debug=True)