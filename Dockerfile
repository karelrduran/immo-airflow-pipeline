# Usar la imagen oficial de Python
FROM python:3.9-slim

# Instalar las dependencias de tu proyecto
RUN apt-get update && apt-get install -y \
    postgresql \
 && rm -rf /var/lib/apt/lists/*

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar los archivos de tu proyecto al directorio de trabajo
COPY . .

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Comando por defecto para ejecutar tu proyecto
CMD ["python", "app.py"]