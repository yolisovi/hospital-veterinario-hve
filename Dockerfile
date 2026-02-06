FROM python:3.11-slim

# Instalamos uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copiamos el archivo (el punto indica la raíz donde estamos parados)
COPY ./requirements.txt /app/requirements.txt

# Instalamos
RUN uv pip install --system -r requirements.txt

# Luego el resto
COPY . .

CMD ["python", "app.py"]
