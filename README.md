# Diagrama de Arquitectura

El siguiente diagrama ilustra la arquitectura por capas del sistema de agendamiento médico, mostrando la interacción entre el usuario, el frontend, el backend y la base de datos, así como los principales endpoints y servicios involucrados:

![Diagrama de Arquitectura](https://user-images.githubusercontent.com/placeholder/arquitectura.png)

> **Nota:** El diagrama muestra el flujo desde el usuario hasta la base de datos, incluyendo los endpoints REST.
# Sistema de Agendamiento Médico

Este sistema es una aplicación web desarrollada con Django para la gestión de turnos médicos y administración de una clínica.

## Descripción
El sistema permite gestionar turnos médicos, pacientes, profesionales de la salud, facturación e inventario en una clínica médica.

## Funcionalidades Principales
- Gestión de turnos médicos
- Administración de pacientes
- Registro de profesionales de la salud
- Sistema de facturación
- Control de inventario
- Sistema de comunicación interna

## Requisitos del Sistema
- Python 3.12 o superior
- Django (última versión estable)
- SQLite3 (incluido en Python)

## Estructura del Proyecto
El proyecto está organizado en las siguientes aplicaciones:
- `paciente`: Gestión de pacientes
- `profesional`: Gestión de profesionales de la salud
- `turno`: Gestión de turnos médicos
- `facturacion`: Sistema de facturación
- `inventario`: Control de inventario
- `comunicacion`: Sistema de comunicación interna
- `empleado`: Gestión de empleados

## Instalación

1. Clonar el repositorio:
```bash
git clone [URL_DEL_REPOSITORIO]
```

2. Crear un entorno virtual:
```bash
python -m venv venv
```

3. Activar el entorno virtual:
```bash
# En Windows
.\venv\Scripts\activate
```

4. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

5. Realizar las migraciones:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Crear un superusuario (opcional):
```bash
python manage.py createsuperuser
```

7. Iniciar el servidor:
```bash
python manage.py runserver
```

## Ejecución con Docker

1. Asegúrate de tener Docker instalado en tu sistema.
2. En la raíz del proyecto, ejecuta:

```powershell
docker-compose up --build
```

Esto construirá y levantará los contenedores de la base de datos y la aplicación.

3. Ejecuta las migraciones de la base de datos dentro del contenedor web:

```powershell
docker-compose exec web python manage.py makemigrations

docker-compose exec web python manage.py migrate
```

4. Accede a la aplicación en tu navegador en:
- Admin panel: `http://localhost:8080/admin/`
- Aplicación web: `http://localhost:8080/`

5. Para detener los contenedores, presiona `Ctrl+C` en la terminal o ejecuta:

```powershell
docker-compose down
```

## Uso
Una vez iniciado el servidor, puedes acceder a:
- Admin panel: `http://localhost:8000/admin/`
- Aplicación web: `http://localhost:8000/`

## Tecnologías Utilizadas
- Django
- SQLite
- HTML/CSS
- JavaScript

## Contribución
Si deseas contribuir al proyecto:
1. Haz un Fork del repositorio
2. Crea una rama para tu funcionalidad (`git checkout -b feature/NuevaFuncionalidad`)
3. Realiza tus cambios y haz commit (`git commit -am 'Agrega nueva funcionalidad'`)
4. Sube los cambios a tu Fork (`git push origin feature/NuevaFuncionalidad`)
5. Crea un Pull Request

## Licencia
Este proyecto está bajo la licencia [MIT](https://opensource.org/licenses/MIT)

## Actualización: Autenticación con JWT

Se ha implementado un sistema de autenticación basado en JSON Web Tokens (JWT) utilizando la biblioteca SimpleJWT. Esto incluye las siguientes características:

### Características
- **Inicio de sesión con JWT**: Los usuarios pueden autenticarse y recibir un par de tokens (access y refresh).
- **Cierre de sesión**: Los tokens de acceso y de actualización se invalidan al cerrar sesión.
- **Lista negra de tokens**: Los tokens de acceso y actualización se almacenan en una lista negra para evitar su reutilización.
- **Autenticación personalizada**: Se ha añadido una clase de autenticación personalizada para manejar tokens en lista negra.

### Uso
1. **Inicio de sesión**:
   - Endpoint: `auth/api/login/`
   - Método: `POST`
   - Cuerpo:
     ```json
     {
       "username": "usuario",
       "password": "contraseña"
     }
     ```
   - Respuesta:
     ```json
     {
       "refresh": "<refresh_token>",
       "access": "<access_token>"
     }
     ```

2. **Cierre de sesión**:
   - Endpoint: `auth/api/logout/`
   - Método: `POST`
   - Encabezado: `Authorization: Bearer <access_token>`
   - Cuerpo:
     ```json
     {
       "refresh": "<refresh_token>"
     }
     ```

### Requisitos Adicionales
Asegúrate de tener las siguientes dependencias instaladas:
- `djangorestframework-simplejwt`

Instalación:
```bash
pip install djangorestframework-simplejwt
```
