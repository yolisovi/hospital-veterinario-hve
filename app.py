from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, BooleanField, EmailField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Email
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

# --- FORMS ---
class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class RegistroCitaForm(FlaskForm):
    email = EmailField('Correo electrónico *', validators=[DataRequired(), Email()])
    confirmacion = BooleanField('Confirmo condiciones', validators=[DataRequired()])
    tutor = StringField('Nombre Tutor', validators=[DataRequired()])
    telefono = StringField('Teléfono', validators=[DataRequired()])
    mascota = StringField('Nombre Mascota', validators=[DataRequired()])
    edad = StringField('Edad', validators=[DataRequired()])
    especie = SelectField('Especie', choices=[('', 'Seleccione...'), ('Perro', 'Perro'), ('Gato', 'Gato')], validators=[DataRequired()])

    servicios_perro = MultiCheckboxField('Servicios Perros', choices=[
        ('v_multiple', 'Vacuna múltiple: $450'), ('v_antirrabica', 'Vacuna antirrábica: $200'),
        ('desp_int_menor', 'Despar. Interna <10kg: $240'), ('desp_int_mayor', 'Despar. Interna >10kg: $280')
    ])
    horario_perro = SelectField('Horario Perros', choices=[('Lun24_12pm', 'Lunes 24 - 12 p.m.'), ('Mar25_9pm', 'Martes 25 - 9 p.m.')])

    servicios_gato = MultiCheckboxField('Servicios Gatos', choices=[
        ('v_antirrabica_gato', 'Vacuna antirrábica: $200'), ('desp_int_gato', 'Desparasitación interna: $240')
    ])
    horario_gato = SelectField('Horario Gatos', choices=[('Mar25_12pm', 'Martes 25 - 12 p.m.'), ('Mie26_10am', 'Miércoles 26 - 10 a.m.')])

    submit = SubmitField('Registrar Cita')

# --- RUTAS ---
@app.route('/', methods=['GET', 'POST'])
def index():
    form = RegistroCitaForm()
    if form.validate_on_submit():
        # Lógica para elegir servicios según especie
        if form.especie.data == 'Perro':
            servicios_list = form.servicios_perro.data
            horario_seleccionado = form.horario_perro.data
        else:
            servicios_list = form.servicios_gato.data
            horario_seleccionado = form.horario_gato.data

        # GUARDAR USANDO SQLAlchemy (Mucho más fácil)
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

        db.session.add(nueva_cita)
        db.session.commit()

        flash('¡Cita registrada con éxito!')
        return redirect(url_for('admin'))

    return render_template('index.html', form=form)

@app.route('/admin')
def admin():
    todas_las_citas = Cita.query.all()
    return render_template('admin.html', citas=todas_las_citas)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
