import json
import os

def probar_carga_json():
    file_path = os.path.join(os.path.dirname(__file__), '../../data/matriz_universo.json')
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        print("JSON cargado correctamente:")
        print(data)
    except FileNotFoundError:
        print("Archivo no encontrado:", file_path)
    except json.JSONDecodeError:
        print("Error al decodificar el JSON")
    except Exception as e:
        print("Error inesperado:", e)

if __name__ == "__main__":
    probar_carga_json()
