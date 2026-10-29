# Taller: peticiones HTTP en Django

## Objetivo

Este taller implementa un endpoint JSON para el modelo `Proyecto` de la aplicación
`gestion`, usando únicamente Django y módulos incluidos en Python. El endpoint
acepta `GET`, `POST`, `PUT` y `DELETE` y separa la colección del recurso individual.

## Métodos HTTP y operaciones CRUD

| Método | Uso en este endpoint | Operación CRUD | Respuesta habitual |
| --- | --- | --- | --- |
| `GET /api/proyectos/` | Consultar todos los proyectos | Read | `200 OK` con una lista JSON |
| `GET /api/proyectos/{id}/` | Consultar un proyecto | Read | `200 OK` o `404 Not Found` |
| `POST /api/proyectos/` | Crear un proyecto | Create | `201 Created` con el objeto creado |
| `PUT /api/proyectos/{id}/` | Reemplazar los datos de un proyecto | Update | `200 OK` o `404 Not Found` |
| `DELETE /api/proyectos/{id}/` | Borrar un proyecto | Delete | `204 No Content` o `404 Not Found` |

`PUT` reemplaza los tres campos del proyecto y por eso exige `nombre`,
`descripcion` y `fecha_inicio`. Para una modificación parcial normalmente se
utiliza `PATCH`; el taller solicita `PUT`, así que no se implementa `PATCH`.

## Cuerpo JSON para crear o reemplazar

```json
{
  "nombre": "Huerta comunitaria",
  "descripcion": "Organización del espacio y sus actividades.",
  "fecha_inicio": "2026-10-28"
}
```

La fecha debe seguir el formato `AAAA-MM-DD`. Los cuerpos JSON inválidos, los
campos faltantes y los valores que no superan la validación del modelo devuelven
`400 Bad Request`. Las rutas admiten únicamente las operaciones correspondientes;
los demás métodos responden `405 Method Not Allowed`.

## Archivos, módulos, funciones y decoradores

- `gestion/views.py`: define `ProyectoEndpoint`, una subclase de
  `django.views.View`. Sus métodos `get()`, `post()`, `put()` y `delete()` atienden
  cada verbo HTTP. `dispatch()` selecciona el método según la petición.
- `gestion/urls.py`: declara las rutas con `django.urls.path` y conecta la clase
  mediante `ProyectoEndpoint.as_view()`.
- `config/urls.py`: incorpora las rutas de la aplicación con `include()` bajo el
  prefijo `/api/`.
- `gestion/models.py`: aporta el modelo `Proyecto`; `objects.all()`, `save()` y
  `delete()` consultan, crean, actualizan y eliminan registros usando el ORM.
- `django.http.JsonResponse`: construye respuestas JSON y permite indicar el
  código HTTP. `HttpResponse` devuelve la respuesta vacía `204` y
  `HttpResponseNotAllowed` comunica los métodos permitidos.
- `django.shortcuts.get_object_or_404`: busca un proyecto y responde `404` cuando
  no existe.
- `json.loads`: decodifica el cuerpo de la petición; `parse_date` valida la fecha;
  `full_clean()` comprueba los valores contra los campos del modelo antes de
  guardar.
- `@method_decorator(csrf_protect, name="dispatch")`: aplica la protección CSRF de
  Django a la vista basada en clase. Los clientes autenticados por sesión deben
  enviar el token CSRF en las peticiones que cambian datos.

La clase base `View` ofrece el despacho por método HTTP; por ello no se necesita
un decorador `require_http_methods` adicional. No se usa Django REST Framework ni
otra biblioteca externa.

## Protección y alcance

La protección CSRF se mantiene activa para `POST`, `PUT` y `DELETE`. No se usa
`csrf_exempt`. Este ejemplo no añade autenticación ni autorización por usuario;
antes de exponer datos reales, se debe limitar quién puede leer y modificar los
proyectos y desplegar la aplicación con la configuración de seguridad apropiada.
El modelo `Tarea` tiene una relación `ForeignKey` con `on_delete=models.CASCADE`,
por lo que borrar un proyecto también elimina sus tareas relacionadas.

## Fuentes consultadas

- [Vistas basadas en clases de Django](https://docs.djangoproject.com/en/6.1/topics/class-based-views/): clase `View`, despacho de métodos y `as_view()`.
- [Objetos de petición y respuesta](https://docs.djangoproject.com/en/6.1/ref/request-response/): respuestas HTTP y `JsonResponse`.
- [Atajos de Django](https://docs.djangoproject.com/en/6.1/topics/http/shortcuts/): uso de `get_object_or_404`.
- [Protección CSRF de Django](https://docs.djangoproject.com/en/6.1/howto/csrf/): protección de peticiones que cambian estado y uso de tokens.
- [Seguridad en Django](https://docs.djangoproject.com/en/6.1/topics/security/): consideraciones para no desactivar CSRF sin necesidad.
