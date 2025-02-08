FROM python:3.9

# Crear y establecer el directorio de trabajo
WORKDIR /app

# Poner el requirements.txt junto al Dockerfile (fuera de /app)
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar la carpeta app/ y su contenido al directorio de trabajo
COPY app/ .

# Ejecutar la aplicación
CMD ["uvicorn", "main_ia:app", "--host", "0.0.0.0", "--port", "8000"]