FROM python:3.9-slim

# Establecer el directorio de trabajo en /app
WORKDIR /app

# Copiar el archivo requirements.txt
COPY requirements.txt /app/

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el contenido del proyecto al contenedor
COPY . /app/


# Exponer el puerto 8000
EXPOSE 8000

# Comando para esperar a que MySQL esté listo y luego ejecutar FastAPI con uvicorn
CMD ["./wait-for-it.sh", "mysql_db:3306", "--", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
