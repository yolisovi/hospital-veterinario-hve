from hospvet import create_app

app = create_app() #los parentesis ejecutan la aplicación


import os

if __name__ == "__main__":
    # Esto es vital para que Render pueda "ver" tu app
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

#arrancamos la aplicación
# if __name__ == "__main__":
#     #app.run(port=8000, debug=True, host="0.0.0.0") #cambiar debug = false
#     app.run(port=8000, debug=True) #cambiar debug = false
