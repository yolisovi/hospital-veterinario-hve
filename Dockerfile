# Imagen base de Python
FROM python:3.11-slim

# Instalamos uv para que la instalación sea ultra rápida
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Directorio de trabajo
WORKDIR /app

# Copiamos solo el archivo de requerimientos primero
COPY requirements.txt .

# Instalamos las librerías necesarias
RUN uv pip install --system -r requirements.txt

# Copiamos todo el código (el .dockerignore filtrará lo que no sirve)
COPY . .

# Comando para arrancar. Usamos 0.0.0.0 para que Render pueda entrar al contenedor
CMD ["python", "app.py"]
