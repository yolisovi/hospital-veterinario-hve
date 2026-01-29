import os
from flask import Flask, render_template, redirect, url_for, flash, request
from database import db
from flask_migrate import Migrate
from models import Cita
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, BooleanField, EmailField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Email
from forms import RegistroCitaForm


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'mi_llave_secreta_123')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Si estamos en Render, usará DATABASE_URL. Si no, usará SQLite local.
uri = os.environ.get('DATABASE_URL', 'sqlite:///camp_vacu_vet.db')
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = uri

# Inicializar db con la app
db.init_app(app)
migrate = Migrate(app, db) #2. Configurar

from models import Cita  # <--- Importar aquí es clave

# Crear tabla
with app.app_context():
    db.create_all()
    print("Tablas creadas en PostgreSQL con éxito")



class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


# --- RUTAS ---

@app.route('/', methods=['GET', 'POST'])
def index():

    # Si no hay nada en la URL, acceso_secreto valdrá None (vacío)
    acceso_secreto = request.args.get('acceso')

    # 1. Revisar si el mantenimiento está encendido en Render
    mantenimiento = os.environ.get('MODO_MANTENIMIENTO', 'OFF')

    # 2. Revisar si tú estás entrando con el link secreto, Ejemplo: tu-web.com/?acceso=hve2026
    # Solo si entras con un "token" secreto en la URL
    acceso_autorizado = request.args.get('token') == "mi_clave_privada"


    # 3. Bloqueo de seguridad
    if mantenimiento == 'ON' and acceso_secreto != "hve2026":
        return """
        <div style="text-align:center; margin-top:100px; font-family:sans-serif; color:#2c3e50;">
            <img src="https://cdn-icons-png.flaticon.com/512/3024/3024509.png" width="80">
            <h1>Sitio en Mantenimiento</h1>
            <p>Estamos preparando la Campaña de Vacunación 2026.</p>
            <p><strong>Vuelve pronto para agendar tu cita.</strong></p>
        </div>
        """, 503

    # 4. Si el mantenimiento está en 'OFF' o tienes el 'acceso', carga el formulario
        form = RegistroCitaForm()

    # O si la variable de entorno está activa
    if os.environ.get('MANTENIMIENTO') == 'ON' and not acceso_autorizado:
        return "<h1>Sitio en mantenimiento</h1><p>Próximamente más información.</p>", 503
    #return render_template('mantenimiento.html') #pagina temporal
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
            nombre=form.nombre.data,      # Nuevo
            apellido1=form.apellido1.data, # Nuevo
            apellido2=form.apellido2.data, # Nuevo
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
# Intento final
