from datetime import date

from django.core.management.base import BaseCommand

from gestion.models import Proyecto, Tarea


PROYECTOS = [
    {
        "nombre": "Sistema de Gestión Escolar",
        "descripcion": "Plataforma para administrar estudiantes, docentes y calificaciones.",
        "fecha_inicio": date(2026, 2, 3),
        "tareas": [
            ("Diseñar la base de datos", True),
            ("Implementar el módulo de matrículas", False),
        ],
    },
    {
        "nombre": "Portal de Ventas Online",
        "descripcion": "Tienda virtual con catálogo de productos y pagos en línea.",
        "fecha_inicio": date(2026, 4, 15),
        "tareas": [
            ("Diseñar el catálogo de productos", True),
            ("Integrar la pasarela de pagos", False),
        ],
    },
    {
        "nombre": "Aplicación de Control de Inventario",
        "descripcion": "Herramienta para registrar productos, entradas y salidas de almacén.",
        "fecha_inicio": date(2026, 6, 1),
        "tareas": [
            ("Registrar los productos iniciales", True),
            ("Generar el reporte de existencias", False),
        ],
    },
]


class Command(BaseCommand):
    help = "Crea tres proyectos de ejemplo con dos tareas cada uno."

    def handle(self, *args, **options):
        Proyecto.objects.all().delete()
        for datos in PROYECTOS:
            proyecto = Proyecto.objects.create(
                nombre=datos["nombre"],
                descripcion=datos["descripcion"],
                fecha_inicio=datos["fecha_inicio"],
            )
            Tarea.objects.bulk_create([
                Tarea(proyecto=proyecto, titulo=titulo, completada=completada)
                for titulo, completada in datos["tareas"]
            ])
        self.stdout.write(self.style.SUCCESS(
            f"Proyectos: {Proyecto.objects.count()} | Tareas: {Tarea.objects.count()}"
        ))
