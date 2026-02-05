# Usa una imagen ligera de Python
FROM python:3.11-slim

# Instala uv para gestionar dependencias rápido
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de dependencias primero (para aprovechar el cache)
COPY requirements.txt .

# Instala las dependencias
RUN uv pip install --system -r requirements.txt

# Copia TODO el contenido de tu carpeta actual al contenedor
COPY . .

# Comando para arrancar la app
CMD ["python", "app.py"]
