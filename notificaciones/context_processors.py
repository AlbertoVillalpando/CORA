# notificaciones/context_processors.py


def notificaciones_usuario(request):
    """
    Context processor que provee las notificaciones del usuario autenticado.

    Si el usuario está autenticado, obtiene el conteo de notificaciones no leídas
    y las últimas 5 notificaciones ordenadas por fecha descendente.
    Si no está autenticado, retorna conteo cero y lista vacía.

    Args:
        request (HttpRequest): Objeto con la información de la petición HTTP.

    Returns:
        dict: Diccionario con dos claves:
            - 'notificaciones_no_leidas' (int): Número de notificaciones no leídas.
            - 'notificaciones_usuario' (QuerySet): Las últimas 5 notificaciones del usuario.
    """
    from .models import Notificacion
    if request.user.is_authenticated:
        no_leidas = Notificacion.objects.filter(
            usuario=request.user, leida=False).count()
        notificaciones = Notificacion.objects.filter(
            usuario=request.user).order_by('-fecha')[:5]  # últimas 5
    else:
        no_leidas = 0
        notificaciones = []
    return {
        'notificaciones_no_leidas': no_leidas,
        'notificaciones_usuario': notificaciones
    }
