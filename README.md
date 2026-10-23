# Backend Django: proyectos y tareas

Aplicación académica construida con Django y SQLite.

## Requisitos

Python compatible con Django 6.1.1, según `requirements.txt`.

## Preparar la base de datos

```powershell
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
```

El comando `seed_data` crea tres proyectos y dos tareas relacionadas por proyecto.
Para entrar al administrador, usa `python manage.py runserver` y abre
`http://127.0.0.1:8000/admin/`. El usuario y la contraseña de entrega están en
`credenciales.txt`.

La aplicación `gestion` define `Proyecto` y `Tarea`, los registra en el admin y
relaciona cada tarea con su proyecto mediante `ForeignKey`.

## Entrega

- `db.sqlite3`: base SQLite con migraciones aplicadas y registros.
- `credenciales.txt`: acceso al superusuario y estado/enlace del repositorio.
- `capturas/`: vistas del administrador para proyectos y tareas.
