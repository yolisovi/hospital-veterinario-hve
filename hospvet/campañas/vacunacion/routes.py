import csv
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
    agotados = []


    conteo_db = db.session.query(
        Cita.especie,
        Cita.dia_semana,
        Cita.bloque_horario,
        func.count(Cita.id)
    ).group_by(Cita.especie, Cita.dia_semana, Cita.bloque_horario).all()


    dict_citas = {(e, d, h): c for e, d, h, c in conteo_db}

    try:

        ruta_csv = os.path.join(os.path.dirname(__file__), 'cupos.csv')

        with open(ruta_csv, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:

                esp_csv = (row.get('especie') or '').strip()
                dia_csv = (row.get('dia_semana') or '').strip()
                hor_csv = (row.get('bloque_horario') or '').strip()


                try:
                    limite = int(row.get('cupo', 0))
                except (ValueError, TypeError):
                    continue


                if not esp_csv or not dia_csv or not hor_csv:
                    continue


                total_actual = dict_citas.get((esp_csv, dia_csv, hor_csv), 0)

                if total_actual >= limite:
                    agotados.append(f"{esp_csv}|{dia_csv}|{hor_csv}")

    except Exception as e:
        print(f"Error procesando cupos: {e}")


    return agotados


def calcular_costo(especie, servicios_seleccionados, peso_interno=None, peso_externo=None):

    total = 0.0

    return total

# ==========================================
# RUTAS
# ==========================================

@campvacuna.route('/', methods=['GET', 'POST'])
def campvacini():
    # 1. Mantenimiento
    mantenimiento = os.environ.get('MODO_MANTENIMIENTO', 'OFF').strip()
    if mantenimiento == 'ON':

        if request.args.get('acceso') != "UUIDs":
            return render_template('mantenimiento.html'), 503

    form = RegistroCitaForm()

    lista_de_bloqueados = obtener_horarios_agotados()

    if form.validate_on_submit():
        try:

            conteo_actual = Cita.query.filter_by(
                especie=form.especie.data,
                dia_semana=form.dia_semana.data,
                bloque_horario=form.bloque_horario.data
            ).count()


            cupo_maximo = 0
            ruta_csv = os.path.join(os.path.dirname(__file__), 'cupos.csv')

            with open(ruta_csv, mode='r', encoding='utf-8') as file:

                reader = csv.DictReader(file, skipinitialspace=True)


                reader.fieldnames = [name.strip() for name in reader.fieldnames]

                for row in reader:

                    csv_especie = row.get('especie')
                    csv_dia = row.get('dia_semana')
                    csv_horario = row.get('bloque_horario')

                    if csv_especie == form.especie.data and \
                        csv_dia == form.dia_semana.data and \
                        csv_horario == form.bloque_horario.data:
                        cupo_maximo = int(row.get('cupo', 0))
                        break


            if conteo_actual >= cupo_maximo:
                flash(f'¡Lo sentimos! El cupo para {form.especie.data} en este horario está lleno.', 'danger')
                return render_template('formulario_vacunacion_2026.html', form=form, horarios_llenos=obtener_horarios_agotados())    # ------------------------------------------------------------


            filename = None
            if form.comprobante_pago.data:
                file = form.comprobante_pago.data
                ext = os.path.splitext(file.filename)[1]
                filename = f"{uuid.uuid4().hex}{ext}"
                upload_path = os.path.join(current_app.root_path, 'static', 'uploads')
                if not os.path.exists(upload_path): os.makedirs(upload_path)
                file.save(os.path.join(upload_path, filename))



            especie = form.especie.data
            if especie == 'Perro':
                lista_final_servicios = list(form.servicios_perro.data)
                # Sumamos los radio buttons si tienen selección
                if form.rango_peso_perro_interno.data:
                    lista_final_servicios.append(form.rango_peso_perro_interno.data)
                if form.rango_peso_perro_externo.data:
                    lista_final_servicios.append(form.rango_peso_perro_externo.data)
            else:
                lista_final_servicios = list(form.servicios_gato.data)


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


    return render_template('formulario_vacunacion_2026.html', form=form, horarios_llenos=obtener_horarios_agotados())

@campvacuna.route('/confirmacion/<string:u_id>')
def confirmacion_cita(u_id):

    cita = Cita.query.filter_by(unique_id=u_id).first_or_404()
    return render_template('confirmacion_publica.html', cita=cita)
