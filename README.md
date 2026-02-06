# Sistema de Gestión Veterinaria (HVE)

Este proyecto es una aplicación web para agendar citas veterinarias de forma segura utilizando identificadores únicos (UUID).

## 🚀 Características
- **Dockerizado**: Configurado para desplegarse fácilmente en cualquier servidor (Render, AWS, DigitalOcean).
- **Base de Datos Profesional**: Utiliza PostgreSQL para asegurar que los datos no se pierdan.
- **Seguridad**: Usa UUIDs en lugar de claves simples para proteger la privacidad de las citas.

## 🛠️ Requisitos para Despliegue (Render)
1. **GitHub**: Subir este repositorio.
2. **PostgreSQL**: Crear una base de datos en Render.
3. **Variables de Entorno**:
   - `DATABASE_URL`: La URL interna de tu base de datos PostgreSQL.
   - `SECRET_KEY`: Una clave secreta para la seguridad de la app.

## 📦 Instalación Local
Si quieres probarlo en tu computadora:
1. Tener instalado Docker.
2. Ejecutar: `docker-compose up --build`
