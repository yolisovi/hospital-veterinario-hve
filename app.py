import os
from flask import redirect, url_for
from hospvet import create_app, db

app = create_app()

# Eliminamos el @app.route('/') de aquí porque está chocando.
# La ruta raíz debe controlarse desde el Blueprint de la campaña.

with app.app_context():
    try:
        db.create_all()
        print("Base de datos sincronizada con UUIDs.")
    except Exception as e:
        print(f"Error en BD: {e}")

if __name__ == "__main__":
    # Cambiamos a 8000 para local, pero Render usará su propio puerto
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=True)
