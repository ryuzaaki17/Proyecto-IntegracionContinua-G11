# Imagen base de Python 3.13.4 en su versión "slim" (ligera), ideal para producción
FROM python:3.13.4-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instala netcat (versión openbsd) para esperar conexión a PostgreSQL
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

# Copia el script antes de usarlo
COPY wait_for_postgres.sh ./

# Copia el archivo de requisitos al contenedor
COPY requisitos.txt ./

# Instala las dependencias especificadas en el archivo (NOTA: hay un error aquí, se debe usar 'requirements.txt' en lugar de 'requisitos.txt' si el archivo copiado es el mismo)
RUN pip install -r requisitos.txt

# Copia el contenido del proyecto actual al contenedor
COPY . .

# Asegurar permisos de ejecución
RUN chmod +x wait_for_postgres.sh

# Expone el puerto 4000 para que Flask sea accesible desde fuera del contenedor
EXPOSE 4000

# Usa el script como punto de entrada
CMD ["./wait_for_postgres.sh", "flask", "run", "--host=0.0.0.0", "--port=4000"]

# Comando por defecto para ejecutar la aplicación Flask
#CMD ["flask", "run", "--host=0.0.0.0", "--port=4000"]