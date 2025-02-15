Pet Adoption API
Bienvenido al proyecto Pet Adoption API, una plataforma web para facilitar la adopción de perritos. Este proyecto está construido utilizando FastAPI, una herramienta moderna y rápida para desarrollar APIs con Python 3.7+.

Descripción
Este sistema tiene como objetivo permitir que los usuarios busquen, adopten y evalúen perritos disponibles para adopción. Además, los administradores pueden gestionar usuarios, perros y sus evaluaciones.

Características principales:
Registro de usuarios: Los usuarios pueden registrarse, iniciar sesión y ver los perritos disponibles para adopción.
Perfiles de perritos: Información detallada sobre cada perrito, incluyendo fotos, descripciones y características.
Evaluaciones de adopción: Los administradores pueden agregar evaluaciones a los perros según su comportamiento, energía y otras características.
Administración de usuarios y perros: Los administradores pueden gestionar tanto a los perros como a los usuarios en la plataforma.
Autenticación segura: Implementación de JWT (JSON Web Tokens) para garantizar un acceso seguro y controlado.
Tecnologías
Backend: FastAPI
Base de Datos: MySQL
ORM: SQLAlchemy
Autenticación: JWT (JSON Web Tokens)
Validación de datos: Pydantic
Cargar imágenes: Utiliza el almacenamiento de archivos para subir imágenes de los perros disponibles para adopción.
Instalación
Sigue los siguientes pasos para instalar y ejecutar el proyecto localmente.

Clonar el repositorio:
bash
Copiar
Editar
git clone https://github.com/JonathanMF2020/com-jmf-python-pet-adoption.git
Instalar dependencias:
bash
Copiar
Editar
cd com-jmf-python-pet-adoption
pip install -r requirements.txt
Configurar base de datos:
Asegúrate de tener MySQL instalado y configurado. Crea una base de datos llamada pet_adoption (o la que prefieras) y actualiza el archivo de configuración con tus credenciales de base de datos.

Ejecutar el servidor:
bash
Copiar
Editar
uvicorn app.main:app --reload
Esto iniciará el servidor de desarrollo. Puedes acceder a la API en http://localhost:8000/docs.

Contribuir
¡Tu ayuda es bienvenida! Si deseas contribuir al proyecto, por favor sigue estos pasos:

Haz un fork del repositorio.
Crea una nueva rama para tus cambios (git checkout -b feature/nueva-caracteristica).
Realiza tus cambios y haz commit (git commit -am 'Añadir nueva funcionalidad').
Haz push a la rama (git push origin feature/nueva-caracteristica).
Abre un Pull Request.
Licencia
Distribuido bajo la licencia MIT. Ver LICENSE para más detalles.