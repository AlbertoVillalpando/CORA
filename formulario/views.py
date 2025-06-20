from django.shortcuts import render, redirect, get_object_or_404
from conferencia.models import Conferencia
from .models import Pregunta, Evaluacion, Respuesta
from django.contrib.auth.decorators import login_required
from notificaciones.models import Notificacion


@login_required
def evaluar_conferencia(request, conferencia_id):
    """
    Permite a un usuario autenticado evaluar una conferencia específica.

    Obtiene o crea una evaluación para la conferencia y usuario actuales.
    Si el método HTTP es POST, actualiza la retroalimentación y las respuestas
    de la evaluación, y crea una notificación para el autor de la conferencia.

    Args:
        request (HttpRequest): Objeto con la información de la petición HTTP.
        conferencia_id (int): ID de la conferencia que se evaluará.

    Returns:
        HttpResponse: Renderiza el formulario de evaluación con preguntas y puntajes,
        o redirige a la vista de conferencias para revisores después de guardar.
    """
    conferencia = get_object_or_404(Conferencia, id=conferencia_id)
    preguntas = Pregunta.objects.filter(conferencia=conferencia)

    evaluacion, _ = Evaluacion.objects.get_or_create(
        conferencia=conferencia, revisor=request.user)

    # Diccionario pregunta.id -> puntaje
    respuestas = {
        r.pregunta.id: r.puntaje for r in evaluacion.respuestas.all()}

    if request.method == 'POST':
        evaluacion.retroalimentacion = request.POST.get(
            'retroalimentacion', '')
        evaluacion.save()

        evaluacion.respuestas.all().delete()

        for pregunta in preguntas:
            key = f'respuesta_{pregunta.id}'
            puntaje = request.POST.get(key)
            if puntaje:
                Respuesta.objects.create(
                    evaluacion=evaluacion,
                    pregunta=pregunta,
                    puntaje=int(puntaje)
                )

        # Crear notificación para el autor
        autor = conferencia.autor  # Cambia esto si es otra relación
        mensaje = f"Tu conferencia '{conferencia.nombre}' ha sido evaluada."
        Notificacion.objects.create(
            usuario=autor, mensaje=mensaje, leida=False)

        # Ajusta esta URL a la que uses
        return redirect('conferencias_revisor')

    # Pasamos las preguntas y los puntajes para marcar radios
    preguntas_con_puntajes = [
        (pregunta, respuestas.get(pregunta.id)) for pregunta in preguntas]

    return render(request, 'formulario/evaluar_conferencia.html', {
        'conferencia': conferencia,
        'preguntas_con_puntajes': preguntas_con_puntajes,
        'evaluacion': evaluacion,
    })


@login_required
def ver_evaluacion(request, conferencia_id):
    """
    Muestra todas las evaluaciones realizadas para una conferencia específica.

    Obtiene la conferencia por su ID y recupera todas las evaluaciones asociadas.
    Renderiza una plantilla con la información de la conferencia y sus evaluaciones.

    Args:
        request (HttpRequest): Objeto con la información de la petición HTTP.
        conferencia_id (int): ID de la conferencia cuyas evaluaciones se desean ver.

    Returns:
        HttpResponse: Página que muestra la conferencia y sus evaluaciones.
    """
    conferencia = get_object_or_404(Conferencia, id=conferencia_id)
    evaluaciones = conferencia.evaluacion_set.all()

    context = {
        'conferencia': conferencia,
        'evaluaciones': evaluaciones,
    }
    return render(request, 'formulario/ver_evaluacion.html', context)


@login_required
def crear_formulario(request, conferencia_id):
    """
    Permite crear y agregar preguntas a un formulario asociado a una conferencia.

    Si la petición es POST, crea nuevas preguntas vinculadas a la conferencia,
    ignorando preguntas vacías. Luego redirige a la vista principal de conferencias.
    Si la petición es GET, muestra las preguntas existentes para esa conferencia.

    Args:
        request (HttpRequest): Objeto con la información de la petición HTTP.
        conferencia_id (int): ID de la conferencia a la que se agregarán preguntas.

    Returns:
        HttpResponse: Renderiza la página para crear preguntas o redirige tras creación.
    """
    conferencia = get_object_or_404(Conferencia, id=conferencia_id)

    if request.method == 'POST':
        preguntas = request.POST.getlist('preguntas')
        for texto in preguntas:
            if texto.strip():
                Pregunta.objects.create(
                    conferencia=conferencia, texto=texto.strip())
        return redirect('home')

    preguntas_existentes = conferencia.preguntas.all()  # related_name

    return render(request, 'formulario/crear_formulario.html', {
        'conferencia': conferencia,
        'preguntas_existentes': preguntas_existentes
    })


@login_required
def ver_formulario(request, conferencia_id):
    """
    Muestra el formulario de preguntas para una conferencia y permite registrar respuestas.

    Si la petición es POST, guarda las respuestas enviadas para cada pregunta.
    Si es GET, simplemente muestra el formulario con las preguntas asociadas a la conferencia.

    Args:
        request (HttpRequest): Objeto con la información de la petición HTTP.
        conferencia_id (int): ID de la conferencia cuyo formulario se desea ver o responder.

    Returns:
        HttpResponse: Renderiza el formulario con las preguntas o redirige tras guardar respuestas.
    """
    conferencia = get_object_or_404(Conferencia, id=conferencia_id)
    preguntas = Pregunta.objects.filter(conferencia=conferencia)

    if request.method == 'POST':
        # Get or create an evaluation for this conference and current user
        evaluacion, created = Evaluacion.objects.get_or_create(
            conferencia=conferencia,
            revisor=request.user
        )

        for pregunta in preguntas:
            puntaje = request.POST.get(f"respuesta_{pregunta.id}")
            if puntaje:
                Respuesta.objects.create(
                    evaluacion=evaluacion,
                    pregunta=pregunta,
                    puntaje=int(puntaje)
                )
        return redirect('home')  # Redirige a donde prefieras

    return render(request, 'formulario/ver_formulario.html', {
        'conferencia': conferencia,
        'preguntas': preguntas
    })
