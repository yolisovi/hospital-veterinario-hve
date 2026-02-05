from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, RadioField, SelectField, SelectMultipleField, StringField, SubmitField, widgets, FileField
from wtforms.validators import DataRequired, Email, Regexp, ValidationError
import os
import csv
from hospvet.models import Cita # Asegúrate de que la ruta a tu modelo sea correcta

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class RegistroCitaForm(FlaskForm):
    # --- DATOS DEL DUEÑO ---
    email = StringField('Correo Electrónico', validators=[DataRequired(message="El correo es obligatorio"), Email(message="Ingresa un correo válido")])
    nombre = StringField('Nombre del Dueño', validators=[DataRequired()])
    apellido1 = StringField('Primer Apellido', validators=[DataRequired()])
    apellido2 = StringField('Segundo Apellido')
    telefono = StringField('Teléfono de contacto', validators=[DataRequired(message="El teléfono es obligatorio"), Regexp(r'^\d{10}$', message="El teléfono debe tener exactamente 10 dígitos numéricos.")])

    # --- DATOS DE LA MASCOTA ---
    mascota = StringField('Nombre de la Mascota', validators=[DataRequired()])
    edad = IntegerField('Edad de la Mascota (Años)', validators=[DataRequired()])
    especie = SelectField('Especie', choices=[('', 'Seleccione especie'), ('Perro', 'Perro'), ('Gato', 'Gato')], validators=[DataRequired()])

# --- AGENDA ---# --- AGENDA ---
    dia_semana = SelectField('Día', choices=[
        ('Lunes 16', 'Lunes 16 de Febrero'),
        ('Martes 17', 'Martes 17 de Febrero'),
        ('Miércoles 18', 'Miércoles 18 de Febrero'),
        ('Jueves 19', 'Jueves 19 de Febrero'),
        ('Viernes 20', 'Viernes 20 de Febrero'),
        ('Lunes 23', 'Lunes 23 de Febrero'),
        ('Martes 24', 'Martes 24 de Febrero'),
        ('Miércoles 25', 'Miércoles 25 de Febrero'),
        ('Jueves 26', 'Jueves 26 de Febrero'),
        ('Viernes 27', 'Viernes 27 de Febrero')
    ], validators=[DataRequired()])

    bloque_horario = SelectField('Hora', choices=[
        ('', 'Seleccione un horario'),
        ('10:00 - 11:00', '10:00 AM - 11:00 AM (Solo Perros)'),
        ('11:00 - 12:00', '11:00 AM - 12:00 PM (Solo Perros)'),
        ('12:00 - 13:00', '12:00 PM - 01:00 PM (Solo Gatos)'),
        ('13:00 - 14:00', '01:00 PM - 02:00 PM (Solo Gatos)'),
        ('15:00 - 16:00', '03:00 PM - 04:00 PM (Perros y Gatos)'),
        ('16:00 - 17:00', '04:00 PM - 05:00 PM (Perros y Gatos)'),
        ('17:00 - 18:00', '05:00 PM - 06:00 PM (Perros y Gatos)')
    ], validators=[DataRequired()])

    # --- SERVICIOS ---
    servicios_perro = MultiCheckboxField('Servicios para Perros', choices=[
        ('v_multiple_desp_externa', 'Vacuna múltiple y Desparasitación Externa'),
        ('v_multiple_desp_interna', 'Vacuna múltiple y Desparasitación Interna'),
        ('v_rabia_desp_interna_externa', 'Vacuna Rabia, Desparasitación Interna y Externa'),
        ('desp_interna_externa', 'Desparasitación Interna y Externa'),
        ('v_multiple_y_rabia', 'Vacuna múltiple y Rabia'),
        ('v_cuadruple_multiple_y_rabia', 'Vacuna cuádruple, Vacuna múltiple y Rabia'),
        ('v_cuadruple_multiple_rabia_desp_int_ext', 'Vacuna cuádruple, Vacuna múltiple y Rabia, Desparasitación Interna y Externa'),
        ('v_bordetella', 'Vacuna Bordetella'),
        ('v_antirrabica', 'Vacuna Rabia'),
        ('v_sextuple', 'Vacuna Séxtuple'),
        ('v_cuadruple', 'Vacuna Cuádruple'),
    ])

    rango_peso_perro_interno = RadioField('Desparasitación interna según peso', choices=[
        ('desp_int_menor_10kg', 'Desparasitación interna (Perro < 10Kg)'),
        ('desp_int_10kg_20kg', 'Desparasitación interna (Perro 10Kg - 20Kg)'),
        ('desp_int_mayor_20kg', 'Desparasitación interna (Perro > 20Kg)')
    ])

    rango_peso_perro_externo = RadioField('Desparasitación externa según peso', choices=[
        ('desp_ext_menor_10kg', 'Desparasitación externa (Perro < 10Kg)'),
        ('desp_ext_10kg_20kg', 'Desparasitación externa (Perro 10Kg - 20Kg)'),
        ('desp_ext_mayor_20kg', 'Desparasitación externa (Perro > 20Kg)')
    ])

    servicios_gato = MultiCheckboxField('Servicios para Gatos', choices=[
        ('v_cuadruple_desparacitacion_completa', 'Vacuna cuádruple felina y Desparasitación Interna/Externa'),
        ('prueba_v_leucemia', 'Prueba Leucemia y Vacuna Leucemia'),
        ('v_rabia_desparacitacion_completa', 'Vacuna contra Rabia y Desparasitación Interna/Externa'),
        ('desparacitacion_interna_externa', 'Desparasitación Interna y Externa'),
        ('v_cuadruple_felina', 'Vacuna Cuádruple felina (Feligen CRP)'),
        ('desparacitacion_interna', 'Desparasitación Interna'),
        ('v_antirrabica_gato', 'Vacuna Rabia (Imrab 3 TF)')
    ])


    confirmacion = BooleanField('Acepto las indicaciones y confirmo que los datos son correctos', validators=[DataRequired()])
    comprobante_pago = FileField('Comprobante de Pago')
    submit = SubmitField('Registrar Cita')

    # --- VALIDACIÓN DE CUPO ---
    def validate_bloque_horario(self, field):
        import csv
        import os
        from hospvet.models import Cita

        limite = None # Empezamos en None para saber si realmente lo encontró
        ruta_csv = os.path.join(os.path.dirname(__file__), 'cupos.csv')

        if os.path.exists(ruta_csv):
            with open(ruta_csv, mode='r', encoding='utf-8-sig') as f:
                lector = csv.DictReader(f)
                for fila in lector:
                    # El CSV ahora tiene una columna 'especie' donde dice si es Perro o Gato
                    if (fila['especie'].strip() == self.especie.data and
                        fila['dia'].strip() == self.dia_semana.data and
                        fila['bloque'].strip() == field.data):
                        limite = int(fila['limite'])
                        break

        # --- PLAN DE RESCATE ---
        # Si limite sigue siendo None, significa que NO encontró la combinación en el CSV
        if limite is None:
            print(f"DEBUG: No se encontró en CSV: {self.especie.data} | {self.dia_semana.data} | {field.data}")
            limite = 10 # Le damos un margen para que no te bloquee mientras pruebas

        # 2. Contar citas actuales en la DB
        from hospvet.models import Cita
        citas_existentes = Cita.query.filter_by(
            especie=self.especie.data,
            dia_semana=self.dia_semana.data,
            bloque_horario=field.data
        ).count()

        if citas_existentes >= limite:
            raise ValidationError(f'¡Cupo agotado! El horario {field.data} para {self.especie.data}s ya no tiene lugares (Límite: {limite}).')
