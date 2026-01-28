#Este archivo solo sirve para que tanto app.py como models.py puedan compartir la base de datos sin errores de "importación circular
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
