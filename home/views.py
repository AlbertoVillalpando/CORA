from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def home_view(request):
    """
    Renderiza la página principal para usuarios autenticados.

    Args:
        request (HttpRequest): Objeto que contiene la información de la solicitud HTTP.

    Returns:
        HttpResponse: Renderiza la plantilla 'home.html'.
    """
    return render(request, 'home.html')
