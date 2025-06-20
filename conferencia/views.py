import os
from pyexpat.errors import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Conferencia
from .forms import ConferenciaForm
from django.contrib.auth.models import Group
from django.http import JsonResponse
from usuarios.models import CustomUser
from notificaciones.models import Notificacion
from .models import InvitacionRevisor, Conferencia
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
import json
from django.contrib import messages


@login_required
def conferencias_administrador(request):
    """
    Muestra todas las conferencias para el administrador.

    Args:
        request (HttpRequest): Objeto de la solicitud HTTP.

    Returns:
        HttpResponse: Página con la lista de todas las conferencias y flags de roles.
    """
    conferencias = Conferencia.objects.all()
    return render(request, 'conferencia/conferencias_administrador.html', {
        'conferencias': conferencias,
        'es_autor': False,
        'es_revisor': False,
    })


@login_required
def conferencias_autor(request):
    """
    Muestra las conferencias filtradas por el autor actual.

    Args:
        request (HttpRequest): Objeto de la solicitud HTTP.

    Returns:
        HttpResponse: Página con las conferencias donde el usuario es autor.
    """
    conferencias = Conferencia.objects.filter(autor=request.user)
    return render(request,
                  'conferencia/conferencias_autor.html',
                  {'conferencias': conferencias})


@login_required
def conferencias_revisor(request):
    """
    Muestra las conferencias donde el usuario es revisor.

    Args:
        request (HttpRequest): Objeto de la solicitud HTTP.

    Returns:
        HttpResponse: Página con conferencias donde el usuario es revisor.
    """
    conferencias = request.user.conferencias_como_revisor
    return render(request,
                  'conferencia/conferencias_revisor.html',
                  {'conferencias': conferencias})


@login_required
def conferencias_organizador(request):
    """
    Muestra todas las conferencias para organizadores con posibles filtros.

    Args:
        request (HttpRequest): Objeto de la solicitud HTTP.

    Returns:
        HttpResponse: Página con lista de conferencias para organizadores.
    """
    conferencias = Conferencia.objects.all()  # o con más filtros según permisos
    return render(request,
                  'conferencia/conferencias_organizador.html',
                  {'conferencias': conferencias})


@login_required
def evaluar_conferencia(request, conferencia_id):
    """
    Muestra la vista para evaluar una conferencia específica.

    Args:
        request (HttpRequest): Objeto de la solicitud HTTP.
        conferencia_id (int): ID de la conferencia a evaluar.

    Returns:
        HttpResponse: Página con la conferencia y sus preguntas para evaluación.
    """
    conferencia = get_object_or_404(Conferencia, id=conferencia_id)
    preguntas = conferencia.preguntas.all()  # si usas related_name='preguntas'

    return render(request, 'conferencia/evaluar_conferencia.html', {
        'conferencia': conferencia,
        'preguntas': preguntas,
    })


@login_required
def subir_documentos_view(request, pk):
    """
    Permite subir un archivo ZIP para la conferencia indicada.

    Args:
        request (HttpRequest): Objeto de la solicitud HTTP.
        pk (int): Clave primaria de la conferencia.

    Returns:
        HttpResponse: Renderiza la página para subir documentos o redirige tras la subida.
    """
    conferencia = get_object_or_404(Conferencia, pk=pk)

    if request.method == 'POST':
        archivo = request.FILES.get('archivo')

        if not archivo:
            return redirect(request.path)

        if not archivo.name.endswith('.zip'):
            return redirect(request.path)

        conferencia.archivo_zip = archivo
        conferencia.save()

        return redirect('conferencias_autor')

    return render(request,
                  'conferencia/subir_documentos.html',
                  {'conferencia': conferencia})


@login_required
def crear_conferencia_view(request):
    """
    Vista para crear una nueva conferencia mediante formulario.

    Args:
        request (HttpRequest): Objeto de la solicitud HTTP.

    Returns:
        HttpResponse: Renderiza el formulario o redirige tras creación exitosa.
    """
    if request.method == 'POST':
        form = ConferenciaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('conferencias_administrador')
    else:
        form = ConferenciaForm()

    return render(request,
                  'conferencia/crear_conferencia.html',
                  {'form': form})


@login_required
def editar_conferencia(request, pk):
    """
    Edita una conferencia existente identificada por pk.

    Args:
        request (HttpRequest): Objeto de la solicitud HTTP.
        pk (int): Clave primaria de la conferencia.

    Returns:
        HttpResponse: Renderiza formulario con datos de conferencia o redirige tras guardar.
    """
    conferencia = get_object_or_404(Conferencia, pk=pk)
    if request.method == 'POST':
        form = ConferenciaForm(request.POST, instance=conferencia)
        if form.is_valid():
            form.save()
            return redirect('conferencias_administrador')
    else:
        form = ConferenciaForm(instance=conferencia)
    return render(request, 'conferencia/editar.html', {'form': form})


@login_required
def eliminar_conferencia(request, pk):
    """
    Elimina la conferencia especificada por pk.

    Args:
        request (HttpRequest): Objeto de la solicitud HTTP.
        pk (int): Clave primaria de la conferencia.

    Returns:
        HttpResponseRedirect: Redirige a la vista de conferencias administrador.
    """
    conferencia = get_object_or_404(Conferencia, pk=pk)
    conferencia.delete()
    return redirect('conferencias_administrador')


@login_required
def autores_disponibles(request, conferencia_id):
    """
    Devuelve en JSON los autores que no han sido invitados a una conferencia.

    Args:
        request (HttpRequest): Objeto de la solicitud HTTP.
        conferencia_id (int): ID de la conferencia.

    Returns:
        JsonResponse: Lista de autores disponibles con id, nombre y email.
    """
    autores = CustomUser.objects.filter(groups__name='Autor')
    invitados_ids = InvitacionRevisor.objects.filter(
        conferencia_id=conferencia_id).values_list('autor_id', flat=True)
    disponibles = autores.exclude(id__in=invitados_ids)

    data = [
        {"id": autor.id, "nombre": f"{autor.nombre} {autor.apellidos}",
            "email": autor.email}
        for autor in disponibles
    ]
    return JsonResponse(data, safe=False)


@login_required
def ver_invitaciones_conferencia(request, conferencia_id):
    """
    Muestra las invitaciones enviadas para una conferencia y autores disponibles.

    Args:
        request (HttpRequest): Objeto de la solicitud HTTP.
        conferencia_id (int): ID de la conferencia.

    Returns:
        HttpResponse: Renderiza la página con invitaciones y autores disponibles.
    """
    conferencia = get_object_or_404(Conferencia, id=conferencia_id)
    invitaciones = InvitacionRevisor.objects.filter(conferencia=conferencia)

    # Filtrar autores disponibles (que no hayan sido invitados aún)
    autores_disponibles = CustomUser.objects.exclude(
        id__in=invitaciones.values('autor_id'))

    return render(request, 'conferencia/invitaciones_conferencia.html', {
        'conferencia': conferencia,
        'invitaciones': invitaciones,
        'autores_disponibles': autores_disponibles,
    })


@login_required
def responder_invitacion(request, invitacion_id, accion):
    """
    Permite a un autor aceptar o rechazar una invitación como revisor.

    Args:
        request (HttpRequest): Objeto de la solicitud HTTP.
        invitacion_id (int): ID de la invitación.
        accion (str): Acción a realizar ('aceptar' o 'rechazar').

    Returns:
        HttpResponseRedirect: Redirige a la vista de invitaciones para la conferencia.
    """
    invitacion = get_object_or_404(
        InvitacionRevisor, id=invitacion_id, autor=request.user)

    accion_lower = accion.lower()
    if accion_lower == 'aceptar':
        invitacion.estado = 'aceptado'
        invitacion.save()

        autor = invitacion.autor
        revisor_group, _ = Group.objects.get_or_create(name='Revisor')
        autor.groups.add(revisor_group)

    elif accion_lower == 'rechazar':
        invitacion.estado = 'rechazado'
        invitacion.save()

    return redirect('invitaciones_conferencia',
                    conferencia_id=invitacion.conferencia.id)


@login_required
def invitar_autor(request, conferencia_id):
    """
    Vista para invitar a un autor a ser revisor de una conferencia.

    Args:
        request (HttpRequest): Objeto de la solicitud HTTP.
        conferencia_id (int): ID de la conferencia.

    Returns:
        HttpResponse: Renderiza formulario o redirige tras crear invitación.
    """
    conferencia = get_object_or_404(Conferencia, id=conferencia_id)

    if request.method == 'POST':
        autor_id = request.POST.get('autor')

        if not autor_id:
            messages.error(
                request,
                "Debe seleccionar un autor antes de invitar.",
                extra_tags='danger')
            return redirect(
                'invitaciones_conferencia',
                conferencia_id=conferencia.id)

        autor = get_object_or_404(CustomUser, id=autor_id)

        # Crear la invitación para el autor
        invitacion = InvitacionRevisor(conferencia=conferencia, autor=autor)
        invitacion.save()

        messages.success(request, f"Autor {autor.nombre} {autor.apellidos} invitado exitosamente.")
        return redirect(
            'invitaciones_conferencia',
            conferencia_id=conferencia.id)

    autores_disponibles = CustomUser.objects.filter(
        rol='Autor')  # Solo autores
    invitaciones = InvitacionRevisor.objects.filter(conferencia=conferencia)

    return render(request, 'conferencia/invitar_autor.html', {
        'conferencia': conferencia,
        'autores_disponibles': autores_disponibles,
        'invitaciones': invitaciones
    })


@login_required
@require_http_methods(["POST"])
def enviar_revision_conferencia(request):
    """
    Recibe vía POST la decisión sobre la revisión de una conferencia y notifica al autor.

    Args:
        request (HttpRequest): Objeto de la solicitud HTTP con cuerpo JSON.

    Returns:
        JsonResponse: Estado de la decisión o error si método no permitido.
    """
    if request.method == "POST":
        data = json.loads(request.body)
        conferencia_id = data.get("conferencia_id")
        decision = data.get("decision")

        conferencia = Conferencia.objects.get(id=conferencia_id)
        conferencia.estado_revision = decision  # campo nuevo en el modelo
        conferencia.save()

        # Crear notificación
        mensaje = f"Tu conferencia '{conferencia.nombre}' ha sido {decision}."
        Notificacion.objects.create(
            usuario=conferencia.autor,
            mensaje=mensaje,
            leida=False
        )

        return JsonResponse({"estado": decision})
    return JsonResponse({"error": "Método no permitido"}, status=405)


@require_http_methods(["POST"])
def reportar_trabajo(request):
    """
    Marca una conferencia como trabajo reportado vía POST.

    Args:
        request (HttpRequest): Objeto de la solicitud HTTP con cuerpo JSON.

    Returns:
        JsonResponse: Estado OK o error.
    """
    if request.method == "POST":
        data = json.loads(request.body)
        conferencia_id = data.get("conferencia_id")
        conferencia = Conferencia.objects.get(id=conferencia_id)
        conferencia.trabajo_reportado = True
        conferencia.save()
        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "error"})


def eliminar_trabajo(request, conf_id):
    """
    Elimina el archivo ZIP de una conferencia si está reportado y existe.

    Args:
        request (HttpRequest): Objeto de la solicitud HTTP.
        conf_id (int): ID de la conferencia.

    Returns:
        HttpResponseRedirect: Redirige a la vista de conferencias administrador.
    """
    conferencia = Conferencia.objects.get(id=conf_id)
    if conferencia.trabajo_reportado and conferencia.archivo_zip:
        path = conferencia.archivo_zip.path
        if os.path.exists(path):
            os.remove(path)
        conferencia.archivo_zip = None
        conferencia.trabajo_reportado = False
        conferencia.save()
    # Ajusta si tu nombre de URL es diferente
    return redirect('conferencias_administrador')
