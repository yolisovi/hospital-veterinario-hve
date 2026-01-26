from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email

class CitaForm(FlaskForm):
    mascota = StringField('Nombre de la Mascota', validators=[DataRequired()])
    edad = StringField('Edad', validators=[DataRequired()])
    especie = SelectField('Especie', choices=[('Perro', 'Perro'), ('Gato', 'Gato')])
    tutor = StringField('Nombre del Tutor', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    telefono = StringField('Teléfono', validators=[DataRequired()])
    servicios = StringField('Servicios')
    horario = StringField('Horario Sugerido')
    submit = SubmitField('Registrar Cita')
