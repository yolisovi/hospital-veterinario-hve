import os
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, BooleanField, EmailField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Email
from forms import RegistroCitaForm


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'mi_llave_secreta_123')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# --- CONFIGURACIÓN DINÁMICA DE BASE DE DATOS ---
# Si estamos en Render, usará DATABASE_URL. Si no, usará SQLite local.
uri = os.environ.get('DATABASE_URL', 'sqlite:///camp_vacu_vet.db')
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = uri

db = SQLAlchemy(app)


# --- MODELO ---
class Cita(db.Model):
    __tablename__ = 'citas'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    tutor = db.Column(db.String(100))
    telefono = db.Column(db.String(20))
    mascota = db.Column(db.String(100))
    edad = db.Column(db.String(20))
    especie = db.Column(db.String(20))
    servicios = db.Column(db.String(500))
    horario = db.Column(db.String(100))

# Crear tabla
with app.app_context():
    db.create_all()
    print("Base de datos y tablas creadas con éxito")

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


# --- RUTAS ---
@app.route('/', methods=['GET', 'POST'])

@app.route('/', methods=['GET', 'POST'])
def index():
    form = RegistroCitaForm()

    if form.validate_on_submit():
        # Selección de datos según especie
        if form.especie.data == 'Perro':
            servicios_list = form.servicios_perro.data
            horario_seleccionado = form.horario_perro.data
        else:
            servicios_list = form.servicios_gato.data
            horario_seleccionado = form.horario_gato.data

        # IMPORTANTE: Usamos la clase Cita (SQLAlchemy se encarga del nombre de la tabla)
        nueva_cita = Cita(
            email=form.email.data,
            tutor=form.tutor.data,
            telefono=form.telefono.data,
            mascota=form.mascota.data,
            edad=form.edad.data,
            especie=form.especie.data,
            servicios=", ".join(servicios_list) if servicios_list else "Sin servicios",
            horario=horario_seleccionado
        )

        try:
            db.session.add(nueva_cita)
            db.session.commit()
            flash('¡Cita registrada con éxito!')
            return redirect(url_for('admin'))
        except Exception as e:
            db.session.rollback()
            # Este mensaje te dirá el error real si persiste
            return f"Error de Base de Datos: {e}"

    if request.method == 'POST' and not form.validate():
        return f"Error de validación: {form.errors}"

    return render_template('index.html', form=form)

@app.route('/admin')
def admin():
    try:
        # Esto buscará específicamente la tabla 'citas'
        todas_las_citas = Cita.query.all()
    except Exception as e:
        return f"Error al leer la base de datos: {e}"

    return render_template('admin.html', citas=todas_las_citas)


if __name__ == '__main__':
    app.run(debug=True, port=8000)
