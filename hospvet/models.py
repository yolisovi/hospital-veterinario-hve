import uuid # <--- ¡IMPORTANTE!
from datetime import datetime, timezone
from hospvet.extensions import db

class Cita(db.Model):
    __tablename__ = 'citas'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    nombre = db.Column(db.String(50), nullable=False)
    apellido1 = db.Column(db.String(50), nullable=True)
    apellido2 = db.Column(db.String(50), nullable=True)
    telefono = db.Column(db.String(20), nullable=False)
    mascota = db.Column(db.String(100), nullable=False)
    edad = db.Column(db.Integer)
    especie = db.Column(db.String(20), nullable=False)
    dia_semana = db.Column(db.String(20), nullable=False)
    bloque_horario = db.Column(db.String(20), nullable=False)
    servicios = db.Column(db.String(500), nullable=False)
    costo_total = db.Column(db.Float, default=0.0)
    fecha_registro = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    comprobante_filename = db.Column(db.String(255))

    # --- NUEVA COLUMNA DE SEGURIDAD ---
    # Se genera un código único automático para cada registro
    unique_id = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
