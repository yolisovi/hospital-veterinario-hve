from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from hospvet.config import Desarrollo as configuracion #importar cuando vaya a clase Produccion

db = SQLAlchemy()
csrf = CSRFProtect() #PARA PORTEGER LOS FORMULARIOS
bcrypt = Bcrypt() #encriptar el ID del registro que se va a enviar.
migrate = Migrate()

def create_app(): #función que genra la aplicación
    app = Flask(__name__) #aquí se genra la aplicación
    app.config.from_object(configuracion) #parametros de configuración de la aplicaion, se tomaran del objeto llamado desarrollo

    db.init_app(app) #enlazamos ya sea con sqlite o postgresSQL
    csrf.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app)

    from hospvet import models #traemos los modelos se crea después de que db se crea para que no hay probelma cicular.

    from hospvet.inicio.routes import inicio #es el bluprint de routes inicio
    from hospvet.campañas.vacunacion.routes import campvacuna

    app.register_blueprint(inicio)
    app.register_blueprint(campvacuna, url_prefix='/vacunacion')

    return app
