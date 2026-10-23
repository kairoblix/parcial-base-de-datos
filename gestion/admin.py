from django.contrib import admin

from .models import Proyecto, Tarea


@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "fecha_inicio")
    search_fields = ("nombre", "descripcion")
    ordering = ("id",)


@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ("id", "titulo", "proyecto", "completada")
    list_filter = ("completada", "proyecto")
    search_fields = ("titulo",)
    ordering = ("id",)
