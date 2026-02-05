import os

# Definimos la ruta base del proyecto
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY', 'mi_llave_secreta_123')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class Produccion(Config):
    # En producción, DATABASE_URL es obligatoria.
    # Si no existe, fallará al arrancar, lo cual es preferible a conectar a una DB equivocada.
    # En Docker, esto vendrá del environment en docker-compose.yml
    uri = os.environ.get('DATABASE_URL')

    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = uri

class Desarrollo(Config):
    # Usamos la ruta absoluta que me pasaste
    # Importante: sqlite://// (4 barras) es para rutas absolutas en Linux/Mac
    db_path = "/home/yola/Personal/veterinaria/vet_form/instance/camp_vacu_vet.db"

    SQLALCHEMY_DATABASE_URI = 'sqlite:////' + db_path

    # Mantenemos esto por si acaso cambias de entorno
    uri = os.environ.get('DATABASE_URL', SQLALCHEMY_DATABASE_URI)
    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DATABASE_URI = uri
