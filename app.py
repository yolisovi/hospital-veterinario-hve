import sqlite3 # Librería nativa de Python
from flask import Flask, render_template, request, redirect, url_for, flash
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, SubmitField, EmailField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Email

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345' # Necesario para CSRF, cambiar por un aleatorio


# Función para conectar a la BD
def conectar_bd():
    conn = sqlite3.connect('hospital_veterinario.db')
    conn.row_factory = sqlite3.Row
    return conn


# Crear la tabla al iniciar (Ejecutar esto una vez)
def crear_tabla():
    conn = conectar_bd()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS citas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            tutor TEXT NOT NULL,
            telefono TEXT NOT NULL,
            mascota TEXT NOT NULL,
            edad TEXT NOT NULL,
            especie TEXT NOT NULL,
            servicios TEXT,
            horario TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# --- FORMS ---
# Clase para los checkboxes de servicios
class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class RegistroCitaForm(FlaskForm):
    email = EmailField('Correo electrónico *', validators=[DataRequired(), Email()])
    confirmacion = BooleanField('Confirmo haber leído las condiciones de presentación del animal.', validators=[DataRequired()])
    tutor = StringField('Nombre Completo del Tutor *', validators=[DataRequired()])
    telefono = StringField('Teléfono de contacto *', validators=[DataRequired()])
    mascota = StringField('Nombre de la mascota *', validators=[DataRequired()])
    edad = StringField('Edad de la mascota *', validators=[DataRequired()])

    especie = SelectField('Especie *', choices=[
        ('', 'Seleccione...'),
        ('Perro', 'Perro'),
        ('Gato', 'Gato')
    ], id="especie", validators=[DataRequired()])

    # Campos específicos para Perros
    #Se agregaron tuplas ('valor', 'texto')
    servicios_perro = MultiCheckboxField('Servicios para Perros', choices=[
        ('v_multiple', 'Vacuna múltiple: $450 incluye: consulta hemograma y urianálisis'),
        ('v_antirrabica', 'Vacuna antirrábica: $200 incluye: consulta'),
        ('desp_int_menor', 'Desparasitación interna (perro peso menor a 10Kg) : $240 incluye: consulta'),
        ('desp_int_mayor', 'Desparasitación interna (perro peso mayor a 10Kg) : $280 incluye: consulta'),
        ('desp_ext_menor_1', 'Desparasitación externa (perro peso menor a 10Kg): $200 incluye: consulta'),
        ('desp_ext_menor_2', 'Desparasitación externa (perro peso menor a 10Kg): $250 incluye: consulta')
    ])
    horario_perro = SelectField('Horario para Perros *', choices=[('Lun24_12pm', 'Lunes 24 - 12 p.m.'),
        ('Lun24_2pm', 'Lunes 24 - 2 p.m.'),
        ('Mar25_9pm', 'Martes 25 - 9 p.m.'),
        ('Mar25_12pm', 'Martes 25 - 12 p.m.'),
        ('Mie26_9am', 'Miércoles 26 - 9 a.m.'),
        ('Mie26_12pm', 'Miércoles 26 - 12 p.m.'),
        ('Mie26_2pm', 'Miércoles 26 - 2 p.m.'),
        ('Mie26_4pm', 'Miércoles 26 - 4 p.m.'),
        ('Jue27_12pm', 'Jueves 27 - 12 p.m.'),
        ('Jue27_1pm', 'Jueves 27 - 1 p.m.')

    ])

    # Campos específicos para Gatos
    servicios_gato = MultiCheckboxField('Servicios para Gatos', choices=[
        ('v_antirrabica_gato', 'Vacuna antirrábica: $200'),
        ('desp_int_gato', 'Desparasitación interna: $240 incluye: consulta'),
        ('desp_ext_gato', 'Desparasitación externa: $200 incluye: consulta')
    ])

    horario_gato = SelectField('Horario para Gatos *', choices=[
        ('Mar25_12pm', 'Martes 25 - 12 p.m.'),
        ('Mie26_10am', 'Miércoles 26 - 10 a.m.'),
        ('Jue27_9am', 'Jueves 27 - 9 a.m.'),
        ('Jue27_10am', 'Jueves 27 - 10 a.m.'),
        ('Jue27_12pm', 'Jueves 27 - 12 p.m.'),
        ('Jue27_1pm', 'Jueves 27 - 1 p.m.')
    ])

    submit = SubmitField('Registrar Cita')

#--- RUTAS ---
@app.route('/', methods=['GET', 'POST'])
def index():
    # . . . lógica de registro . . .
    form = RegistroCitaForm()

    if form.validate_on_submit():
        # Extraer datos del formulario
        email = form.email.data
        tutor = form.tutor.data
        telefono = form.telefono.data
        mascota = form.mascota.data
        edad = form.edad.data
        especie = form.especie.data

        # Determinar qué servicios y horario guardar según la especie
        if especie == 'Perro':
            servicios = ", ".join(form.servicios_perro.data)
            horario = form.horario_perro.data
        else:
            servicios = ", ".join(form.servicios_gato.data)
            horario = form.horario_gato.data

        # Guardar en SQLite
        try:
            conn = conectar_bd()
            conn.execute('''
                INSERT INTO citas (email, tutor, telefono, mascota, edad, especie, servicios, horario)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (email, tutor, telefono, mascota, edad, especie, servicios, horario))
            conn.commit()
            conn.close()
            return "<h1>¡Cita guardada en la Base de Datos!</h1><a href='/'>Volver</a>"
        except Exception as e:
            return f"Error al guardar: {e}"

    return render_template('index.html', form=form)

@app.route('/admin')
def ver_citas():
    conn = conectar_bd()
    citas = conn.execute('SELECT * FROM citas').fetchall()
    conn.close()
    return render_template('admin.html', citas=citas)

    # --- FIN DE RUTAS ---

if __name__ == '__main__':
    crear_tabla() # Llamada aquí a la creación de la tabla
    app.run(debug=True, port=8000)
