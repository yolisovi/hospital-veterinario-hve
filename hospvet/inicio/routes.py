from flask import Blueprint

inicio = Blueprint('inicio', __name__)

@inicio.route('/informacion-general')
def index():
    return "Página de inicio movida para dar paso al formulario."
