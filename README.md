# Prueba Técnica - Desarrollador Django & Next.js Jr

Sistema web para la radicación y gestión de PQRS.

El proyecto está compuesto por un backend desarrollado con Django y un frontend desarrollado con Next.js.

## Tecnologías

### Backend

- Python 3.13.15
- Django 6.1
- Django REST Framework
- SQLite
- django-cors-headers

### Frontend

- Node.js 24.19.0
- npm 11.17.0
- Next.js 16.3.3
- React
- TypeScript
- Tailwind CSS

## Estructura del proyecto


prueba-sol-cielo/
│
├── backend/
│   ├── config/
│   ├── pqrs/
│   │   ├── migrations/
│   │   ├── admin.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── manage.py
│   └── requirements.txt
│
├── frontend/
│   ├── app/
│   ├── public/
│   ├── package.json
│   └── ...
│
├── .gitignore
└── README.md

## Instalación y ejecución

### Clonar el repositorio

cmd
"git clone https://github.com/ycantillomontes/prueba-sol-cielo.git


### El backend y el frontend se ejecutan como servicios independientes.

### 1. Backend - Django

Desde la raíz del proyecto:

cmd
"cd backend"


Crear el entorno virtual:

cmd
"py -m venv venv"


Activar el entorno virtual en Windows CMD:

cmd
"venv\Scripts\activate"

Instalar las dependencias:

cmd
"pip install -r requirements.txt"

Aplicar las migraciones de la base de datos:

cmd
"python manage.py migrate"


Verificar la configuración del proyecto:

cmd
"python manage.py check"


Para acceder al panel administrativo de Django:

1. Asegúrate de tener el entorno virtual activado.
2. Si aún no tienes un superusuario, créalo con:

cmd
" python manage.py createsuperuser"


Ejecutar el servidor:

cmd
"python manage.py runserver"


El backend estará disponible en:  http://127.0.0.1:8000/admin


### 2. Frontend - Next.js

Abrir una nueva ventana de CMD y ubicarse nuevamente en la raíz del proyecto:

cmd
"cd frontend"

Instalar las dependencias:

cmd
"npm install"


Ejecutar el servidor de desarrollo:

cmd
"npm run dev"


El frontend estará disponible en: http://localhost:3000
