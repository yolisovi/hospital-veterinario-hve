import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY', 'mi_llave_secreta_123')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # agregado para verlo en render
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

class Produccion(Config):
    uri = os.environ.get('DATABASE_URL')

    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = uri

class Desarrollo(Config):
    db_path = "/home/yola/Personal/veterinaria/vet_form/instance/camp_vacu_vet.db"

    SQLALCHEMY_DATABASE_URI = 'sqlite:////' + db_path

    uri = os.environ.get('DATABASE_URL', SQLALCHEMY_DATABASE_URI)
    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DATABASE_URI = uri
