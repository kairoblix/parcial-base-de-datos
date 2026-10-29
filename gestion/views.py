import json

from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_date
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_protect

from .models import Proyecto


def _proyecto_a_json(proyecto):
    return {
        "id": proyecto.pk,
        "nombre": proyecto.nombre,
        "descripcion": proyecto.descripcion,
        "fecha_inicio": proyecto.fecha_inicio.isoformat(),
    }


def _leer_datos(request):
    """Lee y valida el objeto JSON requerido para crear o reemplazar un proyecto."""
    try:
        datos = json.loads(request.body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None, JsonResponse(
            {"error": "El cuerpo debe ser un objeto JSON válido."}, status=400
        )

    if not isinstance(datos, dict):
        return None, JsonResponse(
            {"error": "El cuerpo JSON debe ser un objeto."}, status=400
        )

    campos = ("nombre", "descripcion", "fecha_inicio")
    faltantes = [campo for campo in campos if campo not in datos]
    if faltantes:
        return None, JsonResponse(
            {"error": "Faltan campos obligatorios.", "campos": faltantes},
            status=400,
        )

    fecha_inicio = datos["fecha_inicio"]
    if not isinstance(fecha_inicio, str) or parse_date(fecha_inicio) is None:
        return None, JsonResponse(
            {"error": "fecha_inicio debe tener el formato AAAA-MM-DD."},
            status=400,
        )

    return {
        "nombre": datos["nombre"],
        "descripcion": datos["descripcion"],
        "fecha_inicio": fecha_inicio,
    }, None


def _errores_validacion(exc):
    if hasattr(exc, "message_dict"):
        return exc.message_dict
    return {"error": exc.messages}


@method_decorator(csrf_protect, name="dispatch")
class ProyectoEndpoint(View):
    """Endpoint JSON de ejemplo para listar, crear, reemplazar y borrar proyectos."""

    http_method_names = ["get", "post", "put", "delete", "options"]

    def get(self, request, pk=None):
        if pk is None:
            proyectos = Proyecto.objects.all()
            return JsonResponse(
                [_proyecto_a_json(proyecto) for proyecto in proyectos],
                safe=False,
            )

        proyecto = get_object_or_404(Proyecto, pk=pk)
        return JsonResponse(_proyecto_a_json(proyecto))

    def post(self, request, pk=None):
        if pk is not None:
            return HttpResponseNotAllowed(["GET", "PUT", "DELETE"])

        datos, error = _leer_datos(request)
        if error:
            return error

        proyecto = Proyecto(**datos)
        try:
            proyecto.full_clean()
        except ValidationError as exc:
            return JsonResponse(_errores_validacion(exc), status=400)

        proyecto.save()
        return JsonResponse(_proyecto_a_json(proyecto), status=201)

    def put(self, request, pk=None):
        if pk is None:
            return HttpResponseNotAllowed(["GET", "POST"])

        proyecto = get_object_or_404(Proyecto, pk=pk)
        datos, error = _leer_datos(request)
        if error:
            return error

        for campo, valor in datos.items():
            setattr(proyecto, campo, valor)

        try:
            proyecto.full_clean()
        except ValidationError as exc:
            return JsonResponse(_errores_validacion(exc), status=400)

        proyecto.save()
        return JsonResponse(_proyecto_a_json(proyecto))

    def delete(self, request, pk=None):
        if pk is None:
            return HttpResponseNotAllowed(["GET", "POST"])

        proyecto = get_object_or_404(Proyecto, pk=pk)
        proyecto.delete()
        return HttpResponse(status=204)
