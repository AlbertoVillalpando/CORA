# notificaciones/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Notificacion
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse


@login_required
def dropdown_notificaciones(request):
    """
    Renderiza un fragmento HTML con las últimas 5 notificaciones del usuario para un dropdown.

    Obtiene las notificaciones del usuario autenticado ordenadas por fecha descendente
    y las pasa al template parcial para mostrarlas en un menú desplegable.

    Args:
        request (HttpRequest): Objeto con la información de la petición HTTP.

    Returns:
        HttpResponse: Renderiza el template '_dropdown.html' con las notificaciones.
    """
    notificaciones = Notificacion.objects.filter(
        usuario=request.user).order_by('-fecha')[:5]
    return render(request, 'notificaciones/_dropdown.html', {
        'notificaciones': notificaciones
    })


@login_required
@require_http_methods(["POST"])
def marcar_notificaciones_leidas(request):
    """
    Marca todas las notificaciones no leídas del usuario autenticado como leídas.

    Solo acepta peticiones POST. Actualiza el campo 'leida' a True para todas las
    notificaciones pendientes y responde con un JSON de estado.

    Args:
        request (HttpRequest): Objeto con la información de la petición HTTP.

    Returns:
        JsonResponse: Respuesta JSON indicando éxito o error.
            - {'status': 'ok'} si la actualización fue exitosa.
            - {'error': 'Método no permitido'} con código 405 si no es POST.
    """
    if request.method == 'POST':
        Notificacion.objects.filter(
            usuario=request.user, leida=False).update(leida=True)
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'error': 'Método no permitido'}, status=405)
