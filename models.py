from database import db
   # --- MODELO ---
class Cita(db.Model):
    __tablename__ = 'citas'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    nombre = db.Column(db.String(50))
    apellido1 = db.Column(db.String(50))
    apellido2 = db.Column(db.String(50))
    telefono = db.Column(db.String(20))
    mascota = db.Column(db.String(100))
    edad = db.Column(db.String(20))
    especie = db.Column(db.String(20))
    servicios = db.Column(db.String(500))
    horario = db.Column(db.String(100))
