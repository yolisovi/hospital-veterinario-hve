from flask import Blueprint, render_template, url_for, request, flash, redirect
from hospvet.models import Cita #permite acceder a la clase que apunta a la clase de datos

inicio = Blueprint('inicio', __name__)

@inicio.route('/')
def index():
    try:
        # Esto buscará específicamente la tabla 'citas'
        todas_las_citas = Cita.query.all()
    except Exception as e:
        return f"Error al leer la base de datos: {e}"

    return render_template('admin.html', citas=todas_las_citas)
