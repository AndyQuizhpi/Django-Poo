# Django Notes

Aplicación web de gestión de tareas (to-do list) construida con **Django 4.1**, con
autenticación de usuarios, protección de datos por usuario, interfaz con **Bootstrap 5**
y lista para desplegarse en **Render** usando **PostgreSQL** y **WhiteNoise**.

## ✨ Funcionalidades

- Registro, inicio y cierre de sesión de usuarios.
- CRUD completo de tareas: crear, editar, completar y eliminar.
- Cada usuario solo puede ver y modificar sus propias tareas.
- Historial de tareas completadas, ordenado por fecha.
- Búsqueda de tareas y filtro por "importantes".
- Contador de tareas pendientes/completadas.
- Mensajes de éxito/error (Django messages) para cada acción.
- Interfaz responsive con Bootstrap 5 e íconos de Bootstrap Icons.
- Páginas de error 404 y 500 personalizadas.
- Configuración lista para producción (variables de entorno, PostgreSQL, WhiteNoise, Gunicorn).

## 🧱 Stack

- Python / Django 4.1
- SQLite (desarrollo) / PostgreSQL (producción)
- Bootstrap 5 + Bootstrap Icons (CDN)
- Gunicorn + WhiteNoise (servidor de producción / estáticos)
- python-decouple + dj-database-url (configuración por variables de entorno)

## 🚀 Instalación local

1. **Clonar el repositorio**
   ```bash
   git clone <url-del-repositorio>
   cd django-notes-master
   ```

2. **Crear y activar un entorno virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate   # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**

   Copia el archivo de ejemplo y ajusta los valores:
   ```bash
   cp .env.example .env
   ```
   En desarrollo puedes dejar `DEBUG=True` y omitir `DATABASE_URL` (usará SQLite).

5. **Aplicar migraciones**
   ```bash
   python manage.py migrate
   ```

6. **Crear un superusuario** (para acceder al panel de administración)
   ```bash
   python manage.py createsuperuser
   ```

7. **Ejecutar el servidor de desarrollo**
   ```bash
   python manage.py runserver
   ```
   La aplicación estará disponible en `http://127.0.0.1:8000/`.

## 📦 Estructura del proyecto

```
django-notes-master/
├── djangocrud/          # Configuración del proyecto (settings, urls, wsgi/asgi)
├── tasks/                # App principal: modelos, vistas, formularios, templates
│   ├── templates/        # base.html, home, signin, signup, tasks, task_detail, etc.
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── admin.py
├── static/               # css/, js/, img/ propios del proyecto
├── requirements.txt
├── build.sh              # Script de build para Render
├── Procfile              # Comando de arranque (gunicorn) para Render
├── .env.example
└── .gitignore
```

## ☁️ Despliegue en Render

1. Sube el proyecto a un repositorio de GitHub.
2. Crea un nuevo **Web Service** en [Render](https://render.com) apuntando al repositorio.
3. Configura:
   - **Build command:** `./build.sh`
   - **Start command:** `gunicorn djangocrud.wsgi:application` (ya definido en `Procfile`)
4. Crea una base de datos **PostgreSQL** en Render (o usa una existente) y copia su `DATABASE_URL`.
5. Configura las variables de entorno en Render (pestaña *Environment*):
   - `SECRET_KEY`
   - `DEBUG=False`
   - `ALLOWED_HOSTS` (incluye el dominio `.onrender.com` que te asigne Render)
   - `DATABASE_URL`
6. Despliega. `build.sh` instalará dependencias, recolectará estáticos (`collectstatic`)
   y aplicará las migraciones automáticamente.

## 🔒 Notas de seguridad

- Todas las vistas privadas están protegidas con `@login_required`.
- Todas las consultas de tareas usan `get_object_or_404(Task, pk=..., user=request.user)`
  para evitar que un usuario acceda o modifique tareas ajenas.
- Todos los formularios incluyen `{% csrf_token %}`.
- Completar y eliminar tareas solo se permite mediante `POST`.

## 📄 Licencia

Proyecto con fines educativos, basado en un curso de Django CRUD.
