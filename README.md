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
