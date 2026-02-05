from hospvet import create_app, db
from flask import url_for, redirect
import os

app = create_app()

with app.app_context():
    try:
        # ¡CUIDADO! Esto borrará los datos viejos de hace 8 días
        # Pero es la única forma de que se creen las columnas UUID y Nombre
        #
        db.create_all()
        print("Base de datos RECONSTRUIDA con éxito (UUID activo).")
    except Exception as e:
        print(f"Error al sincronizar BD: {e}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

@app.route('/')
def redirect_to_form():
    # Esto redirige la página principal al formulario de la campaña
    return redirect(url_for('campvacuna.campvacini'))
