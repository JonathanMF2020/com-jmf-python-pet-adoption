FROM python:3.9-slim

# Instalar Poetry
RUN pip install poetry

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el archivo pyproject.toml
COPY pyproject.toml /app/

# Instalar dependencias usando Poetry
RUN poetry install --no-root

# Copiar el contenido del proyecto al contenedor
COPY . /app/

# Exponer el puerto 8000
EXPOSE 8000

# Comando para esperar a que MySQL esté listo y luego ejecutar FastAPI con uvicorn
CMD ["./wait-for-it.sh", "mysql_db:3306", "--", "poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]