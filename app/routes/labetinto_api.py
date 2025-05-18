import json
import os
from flask import Blueprint, jsonify
from app.services.bckt import bckt_caminos

universo_api = Blueprint('universo_api', __name__)

@universo_api.route('/api/solve', methods=['GET'])
def encontrar_camino():
    # Ruta absoluta al archivo JSON
    file_path = os.path.join(os.path.dirname(__file__), '../../data/matriz_universo.json')

    try:
        with open(file_path, 'r') as f:
            data = json.load(f)

        required_keys = ['tamMatriz', 'origen', 'destino', 'agujerosNegros', 'estrellasGigantes', 'agujerosGusano', 'zonasRecarga', 'celdasCargaRequerida', 'cargaInicial', 'matrizInicial']
        if any(data.get(k) is None for k in required_keys):
            return jsonify({"error": "El archivo no contiene todos los datos requeridos"}), 400

        # Como las llaves del diccionario coinciden con los parametros recibidos por la función, este puede desempaquetarse con ** al enviarse
        caminos = bckt_caminos(**data)

        return jsonify({"caminos": caminos})

    except FileNotFoundError:
        return jsonify({"error": "Archivo matriz_universo.json no encontrado"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Error al leer el archivo JSON"}), 400
    except Exception as e:
        return jsonify({"error": f"Error inesperado: {str(e)}"}), 500
