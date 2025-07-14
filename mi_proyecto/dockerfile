# Usa una imagen base ligera de Python 3.11
FROM python:3.11-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de dependencias
COPY requirements.txt .

# Instala dependencias del sistema necesarias para pandas y SQLite
RUN pip install --no-cache-dir -r requirements.txt
# Copia el resto de la aplicación
COPY . .

# Expone el puerto de Flask (por defecto 5000)
EXPOSE 8000

# Comando para arrancar la API
CMD ["python", "app.py"]
