import json

def lector_json(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Archivo no encontrado:", file_path)
    except json.JSONDecodeError:
        print("Error al decodificar el JSON")
    except Exception as e:
        print("Error inesperado:", e)
        
    return data
