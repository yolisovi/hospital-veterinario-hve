from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, BooleanField, EmailField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Email
from forms import RegistroCitaForm
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mi_llave_secreta_123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///veterinaria.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- MODELO ---
class Cita(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    tutor = db.Column(db.String(100))
    telefono = db.Column(db.String(20))
    mascota = db.Column(db.String(100))
    edad = db.Column(db.String(20))
    especie = db.Column(db.String(20))
    servicios = db.Column(db.String(500)) # Subí el tamaño por los checkboxes
    horario = db.Column(db.String(100))

# Crear tabla
with app.app_context():
    db.create_all()

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


# --- RUTAS ---
@app.route('/', methods=['GET', 'POST'])
def index():
    form = RegistroCitaForm()
    if form.validate_on_submit():
        # 1. Determinamos servicios y horario según la especie
        if form.especie.data == 'Perro':
            servicios_list = form.servicios_perro.data
            horario_seleccionado = form.horario_perro.data
        else:
            servicios_list = form.servicios_gato.data
            horario_seleccionado = form.horario_gato.data

        # 2. CREAMOS EL OBJETO usando el modelo 'Cita'
        # Nota: Asegúrate de usar los nombres de columna de tu clase Cita
        nueva_cita = Cita(
            email=form.email.data,
            tutor=form.tutor.data,
            telefono=form.telefono.data,
            mascota=form.mascota.data,
            edad=form.edad.data,
            especie=form.especie.data,
            servicios=", ".join(servicios_list),
            horario=horario_seleccionado
        )

        # 3. GUARDAMOS en la base de datos de forma profesional
        try:
            db.session.add(nueva_cita)
            db.session.commit()
            flash('¡Cita registrada con éxito!')
            return redirect(url_for('admin'))
        except Exception as e:
            db.session.rollback()
            return f"Error al guardar: {e}"

    return render_template('index.html', form=form)

@app.route('/admin')
def admin():
    todas_las_citas = Cita.query.all()
    return render_template('admin.html', citas=todas_las_citas)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
