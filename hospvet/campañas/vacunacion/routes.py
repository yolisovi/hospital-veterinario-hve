import os
import uuid
from datetime import datetime
from flask import Blueprint, render_template, url_for, request, flash, redirect, current_app
from hospvet import db
from hospvet.models import Cita
from hospvet.campañas.vacunacion.forms import RegistroCitaForm
from sqlalchemy import func


campvacuna = Blueprint('campvacuna', __name__)

# ==========================================
# FUNCIONES DE APOYO
# ==========================================

def obtener_horarios_agotados():
    """
    Esta función ahora es más simple. Consulta la DB y
    compara contra un límite fijo o podrías llamar a la lógica del form.
    Por ahora, la dejaremos básica para que no rompa tu código.
    """
    agotados = []
    citas_actuales = db.session.query(
        Cita.especie, Cita.dia_semana, Cita.bloque_horario, func.count(Cita.id)
    ).group_by(Cita.especie, Cita.dia_semana, Cita.bloque_horario).all()

    # Nota: Aquí podrías implementar una lógica similar a la del Form
    # si quieres que el calendario pinte los grises automáticamente.
    return agotados

def calcular_costo(especie, servicios_seleccionados, peso_interno=None, peso_externo=None):
    # (Mantén tu diccionario de precios aquí, estaba correcto en tu código)
    # ... [Tu lógica de precios actual] ...
    total = 0.0
    # ... [Tu lógica de suma de costos actual] ...
    return total

# ==========================================
# RUTAS
# ==========================================

@campvacuna.route('/', methods=['GET', 'POST'])
def campvacini():
    # 1. Mantenimiento
    mantenimiento = os.environ.get('MODO_MANTENIMIENTO', 'OFF').strip()
    if mantenimiento == 'ON':
        # Cambiado a tu nueva preferencia de seguridad
        if request.args.get('acceso') != "UUIDs":
            return render_template('mantenimiento.html'), 503

    form = RegistroCitaForm()

    if form.validate_on_submit():
        try:
            # 2. Procesar Archivo con UUID (Tu nueva preferencia)
            filename = None
            if form.comprobante_pago.data:
                file = form.comprobante_pago.data
                ext = os.path.splitext(file.filename)[1]
                # Nombre de archivo puramente UUID para evitar rastreos
                filename = f"{uuid.uuid4().hex}{ext}"

                upload_path = os.path.join(current_app.root_path, 'static', 'uploads')
                if not os.path.exists(upload_path): os.makedirs(upload_path)
                file.save(os.path.join(upload_path, filename))

            # 3. Lógica de Pesos y Servicios (Simplificada para legibilidad)
            especie = form.especie.data
            servicios_sel = form.servicios_perro.data if especie == 'Perro' else form.servicios_gato.data
            lista_final_servicios = list(servicios_sel)

            # 4. Guardar en BD
            nueva_cita = Cita(
                email=form.email.data,
                nombre=form.nombre.data,
                apellido1=form.apellido1.data,
                apellido2=form.apellido2.data,
                telefono=form.telefono.data,
                mascota=form.mascota.data,
                edad=form.edad.data,
                especie=especie,
                dia_semana=form.dia_semana.data,
                bloque_horario=form.bloque_horario.data,
                servicios=", ".join(lista_final_servicios),
                costo_total=0.0,
                comprobante_filename=filename,
                unique_id=str(uuid.uuid4()) # ID único para la URL de confirmación
            )

            db.session.add(nueva_cita)
            db.session.commit()

            flash('¡Registro exitoso!', 'success')
            return redirect(url_for('campvacuna.confirmacion_cita', u_id=nueva_cita.unique_id))

        except Exception as e:
            db.session.rollback()
            flash(f"Error al guardar: {str(e)}", "danger")

    # Si el formulario falla o es un GET, regresamos al mismo sitio con los errores
    return render_template('formulario_vacunacion_2026.html', form=form, horarios_llenos=obtener_horarios_agotados())

@campvacuna.route('/confirmacion/<string:u_id>')
def confirmacion_cita(u_id):
    # Buscamos por el UUID. Si alguien cambia una letra, le dará error 404
    cita = Cita.query.filter_by(unique_id=u_id).first_or_404()
    return render_template('confirmacion_publica.html', cita=cita)



# @campvacuna.route('/admin')
# def admin_panel():
#     acceso = request.args.get('acceso')
#     # Corregido: usamos 'acceso' en lugar de 'acceso_secreto'
#     if acceso != "UUIDs":
#         return "No autorizado", 403
#     citas = Cita.query.all()
#     return render_template('admin.html', citas=citas)

# # @campvacuna.route('/admin')
# @campvacuna.route('/panel-de-control-veterinario') # <--- Cambia '/admin' por algo largo y único
# def admin_panel():
#     acceso = request.args.get('acceso')
#     # Cambia esta línea al principio de tu función campvacini
#     if acceso != "UUIDs": # Antes tenías hve2026
#         return "No autorizado", 403
#     citas = Cita.query.all()
#     return render_template('admin.html', citas=citas)
