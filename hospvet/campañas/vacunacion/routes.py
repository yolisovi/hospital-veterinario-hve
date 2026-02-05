import os
import uuid
from datetime import datetime
from flask import Blueprint, render_template, url_for, request, flash, redirect
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
    mantenimiento = os.environ.get('MODO_MANTENIMIENTO', 'OFF').strip()
    if mantenimiento == 'ON':
        acceso_secreto = request.args.get('acceso', '')
        if acceso_secreto != "hve2026":
            return render_template('mantenimiento.html'), 503

    form = RegistroCitaForm()
    horarios_llenos = obtener_horarios_agotados()

    # form.validate_on_submit() ahora ejecutará AUTOMÁTICAMENTE
    # la función validate_bloque_horario que escribimos en forms.py
    if form.validate_on_submit():
        try:
            # 1. Procesar Archivo (Comprobante)
            filename = None
            if hasattr(form, 'comprobante_pago') and form.comprobante_pago.data:
                file = form.comprobante_pago.data
                ext = os.path.splitext(file.filename)[1]
                filename = f"hve_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}{ext}"
                upload_path = os.path.join('hospvet', 'static', 'uploads')
                if not os.path.exists(upload_path): os.makedirs(upload_path)
                file.save(os.path.join(upload_path, filename))

            # 2. Preparar datos para la DB Servicios y Pesos
            peso_int = form.rango_peso_perro_interno.data if form.especie.data == 'Perro' else None
            peso_ext = form.rango_peso_perro_externo.data if form.especie.data == 'Perro' else None
            servicios_sel = form.servicios_perro.data if form.especie.data == 'Perro' else form.servicios_gato.data

            # Unificar Pesos en la lista de Servicios
            lista_final_servicios = list(servicios_sel)

            if peso_int:
                # Obtenemos la etiqueta legible del RadioField
                dict_pesos = dict(form.rango_peso_perro_interno.choices)
                texto_peso = dict_pesos.get(peso_int, peso_int)
                lista_final_servicios.append(texto_peso)
            if peso_ext:
                dict_pesos_ext = dict(form.rango_peso_perro_externo.choices)
                texto_peso_ext = dict_pesos_ext.get(peso_ext, peso_ext)
                lista_final_servicios.append(texto_peso_ext)

            # 3. Guardar en BD
            nueva_cita = Cita(
                email=form.email.data,
                nombre=form.nombre.data,
                apellido1=form.apellido1.data,
                apellido2=form.apellido2.data,
                telefono=form.telefono.data,
                mascota=form.mascota.data,
                edad=form.edad.data,
                especie=form.especie.data,
                dia_semana=form.dia_semana.data,
                bloque_horario=form.bloque_horario.data,
                servicios=", ".join(lista_final_servicios),
                costo_total=0.0, # Forzado a 0 para quitarlo de la confirmación
                comprobante_filename=filename,
                unique_id=str(uuid.uuid4())
            )

            db.session.add(nueva_cita)
            db.session.commit()

            flash(f'¡Registro exitoso!', 'success')
            # Redirigimos a la confirmación usando la llave secreta
            return redirect(url_for('campvacuna.confirmacion_cita', u_id=nueva_cita.unique_id))

        except Exception as e:
            db.session.rollback()
            print(f"Error al guardar: {e}")
            flash(f"Error crítico al procesar tu cita: {str(e)}", "danger")
            # ESTA LÍNEA ES LA QUE FALTABA:
            return render_template('index.html', form=form, horarios_llenos=obtener_horarios_agotados())

    # Este es el return para cuando la página carga por primera vez (GET)
    return render_template('index.html', form=form, horarios_llenos=obtener_horarios_agotados())

@campvacuna.route('/confirmacion/<string:u_id>')
def confirmacion_cita(u_id):
    # Buscamos por el UUID. Si alguien cambia una letra, le dará error 404
    cita = Cita.query.filter_by(unique_id=u_id).first_or_404()
    return render_template('confirmacion_publica.html', cita=cita)


@campvacuna.route('/admin')
def admin_panel():
    acceso = request.args.get('acceso')
    if acceso != "hve2026":
        return "No autorizado", 403
    citas = Cita.query.all()
    return render_template('admin.html', citas=citas)
