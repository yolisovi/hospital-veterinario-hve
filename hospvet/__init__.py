from flask import Flask
from hospvet.config import Desarrollo as configuracion
from hospvet.extensions import db, csrf, bcrypt, migrate




def create_app():
    app = Flask(__name__)
    app.config.from_object(configuracion)


    db.init_app(app)
    csrf.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app)


    from hospvet.inicio.routes import inicio
    from hospvet.campañas.vacunacion.routes import campvacuna


    app.register_blueprint(inicio, url_prefix='/admin')

    app.register_blueprint(campvacuna, url_prefix='/')

    return app
