from flask import Blueprint, render_template, request
from hospvet.models import Cita

inicio = Blueprint('inicio', __name__)

@inicio.route('/tabla-de-registros')
def tabla_citas():
    acceso = request.args.get('acceso')
    if acceso != "UUIDs":
        return "No autorizado.", 403

    try:
        todas_las_citas = Cita.query.order_by(Cita.dia_semana.asc(), Cita.bloque_horario.asc()).all()
        # Flask buscará 'admin.html' en la carpeta templates general
        return render_template('admin.html', citas=todas_las_citas)
    except Exception as e:
        return f"Error: {e}"
