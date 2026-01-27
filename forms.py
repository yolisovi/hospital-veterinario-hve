from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, BooleanField, EmailField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Email


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
