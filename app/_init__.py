from flask import Flask

def create_app():
    app = Flask(__name__)

    # Importar el blueprint con las rutas del laberinto
    from app.routes.labetinto_api import universo_api

    # Registrar el blueprint en la app Flask
    app.register_blueprint(universo_api)

    return app
