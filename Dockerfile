# Usamos una imagen ligera de Python
FROM python:3.11-slim

# Instalamos dependencias de Linux necesarias para PostgreSQL y compilación
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Definimos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalamos uv dentro del contenedor para que la instalación sea flash
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copiamos primero los archivos de dependencias para aprovechar el cache de Docker
COPY requirements.txt .
RUN uv pip install --system --no-cache -r requirements.txt

# Copiamos el resto de tu código
COPY . .

# Comando para arrancar tu app con Gunicorn
# "app:app" significa: busca el archivo app.py y la variable app = Flask(__name__)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
