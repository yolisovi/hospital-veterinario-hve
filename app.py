from hospvet import create_app, db  # Importamos también 'db'
import os

app = create_app() #los parentesis ejecutan la aplicación

# Bloque de auto-reparación de base de datos
with app.app_context():
    try:
        db.create_all()
        print("Base de datos sincronizada con éxito.")
    except Exception as e:
        print(f"Error al sincronizar BD: {e}")

if __name__ == "__main__":
    # Esto es vital para que Render pueda "ver" tu app
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
