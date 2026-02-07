#!/bin/bash
echo "🚀 Reiniciando Hospital Veterinario (HVE)..."

# Detiene los contenedores actuales
docker-compose down

# Levanta y construye (por si hubo cambios en Python o carpetas)
# El -d es para que corra "detached" (en el fondo)
docker-compose up --build -d

echo "✅ ¡Servidor reiniciado con éxito!"
echo "📺 Mostrando logs (Presiona Ctrl+C para dejar de verlos, la app seguirá corriendo):"

# Te muestra los logs para ver si Flask truena al arrancar
docker-compose logs -f --tail=50
