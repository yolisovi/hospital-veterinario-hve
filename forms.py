from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, BooleanField, EmailField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Email


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


# ... (imports iguales) ...

class RegistroCitaForm(FlaskForm):
    email = EmailField('Correo electrónico *', validators=[DataRequired(), Email()])
    confirmacion = BooleanField('Confirmo condiciones', validators=[DataRequired()])
    tutor = StringField('Nombre Tutor', validators=[DataRequired()])
    telefono = StringField('Teléfono', validators=[DataRequired()])
    mascota = StringField('Nombre Mascota', validators=[DataRequired()])
    edad = StringField('Edad', validators=[DataRequired()])
    especie = SelectField('Especie', choices=[('', 'Seleccione...'), ('Perro', 'Perro'), ('Gato', 'Gato')], validators=[DataRequired()])

    # Quitamos DataRequired de estos porque son condicionales
    servicios_perro = MultiCheckboxField('Servicios Perros', choices=[...])
    horario_perro = SelectField('Horario Perros', choices=[...]) # Sin DataRequired

    servicios_gato = MultiCheckboxField('Servicios Gatos', choices=[...])
    horario_gato = SelectField('Horario Gatos', choices=[...]) # Sin DataRequired

    submit = SubmitField('Registrar Cita')
