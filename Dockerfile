FROM python:3.11-slim

# Instalar uv para velocidad
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copiamos requerimientos
COPY requirements.txt .
RUN uv pip install --system -r requirements.txt

# Copiamos todo el proyecto
COPY . .

# Variables de entorno por defecto (Render las sobreescribirá)
ENV PORT=8080

# Comando para arrancar usando Python directamente
CMD ["python", "app.py"]
