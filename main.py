from hospvet import create_app

app = create_app()

if __name__ == "__main__":
    # Escucha en todas las interfaces y puerto 8000
    app.run(host='0.0.0.0', port=8000, debug=True)
