from hospvet import create_app, db
from flask import redirect, url_for
import os

app = create_app()

# ESTO FUERZA A QUE LA RAÍZ (/) SIEMPRE VAYA AL FORMULARIO
@app.route('/')
def home():
    return redirect(url_for('campvacuna.campvacini'))

with app.app_context():
    try:
        # Asegúrate de haber borrado db.drop_all() para no perder datos nuevos
        db.create_all()
        print("Base de datos lista.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
