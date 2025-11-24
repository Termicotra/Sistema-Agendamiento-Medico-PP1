# Dockerfile para proyecto Django
FROM python:3.12-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de requerimientos e instala dependencias requeridas
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código fuente
COPY . .

# Crea los directorios necesarios
RUN mkdir -p staticfiles media

# Expone el puerto por defecto de Django
EXPOSE 8000

# Comando por defecto para correr el servidor de desarrollo
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
