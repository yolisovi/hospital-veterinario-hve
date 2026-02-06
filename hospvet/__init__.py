from flask import Flask
from hospvet.config import Desarrollo as configuracion
# Importamos las extensiones desde el nuevo archivo que creaste
from hospvet.extensions import db, csrf, bcrypt, migrate
from hospvet.campañas.vacunacion.routes import campvacuna
from hospvet.inicio.routes import inicio


def create_app():
    app = Flask(__name__)
    app.config.from_object(configuracion)

    # Inicializamos las extensiones
    db.init_app(app)
    csrf.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app)

    # IMPORTANTE: Los imports de rutas van AQUÍ ADENTRO
    # para evitar el error circular que te salió antes
    from hospvet.inicio.routes import inicio
    from hospvet.campañas.vacunacion.routes import campvacuna

    # Registramos los Blueprints (Campaña manda en la raíz '/')

    app.register_blueprint(campvacuna, url_prefix='/')
    # app.register_blueprint(inicio, url_prefix='/web-inicio')
    #  app.register_blueprint(inicio, url_prefix='/inicio')

    return app
