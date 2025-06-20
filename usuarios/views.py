from django.shortcuts import render, redirect
from .forms import RegistroForm, LoginForm
from django.contrib.auth import logout
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from conferencia.models import Conferencia
from conferencia.models import InvitacionRevisor
from django.shortcuts import get_object_or_404
from notificaciones.models import Notificacion


class CustomPasswordResetView(SuccessMessageMixin, PasswordResetView):
    """Vista personalizada para solicitar el restablecimiento de contraseña.

    Attributes:
        template_name (str): Plantilla del formulario de restablecimiento.
        email_template_name (str): Plantilla del correo enviado.
        subject_template_name (str): Plantilla del asunto del correo.
        success_url (str): Redirección al completarse la solicitud.
        success_message (str): Mensaje mostrado al enviar correctamente el correo.
    """
    template_name = 'registration/password_reset_form.html'
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')
    success_message = "Se han enviado las instrucciones para restablecer tu contraseña a tu correo electrónico."


class CustomPasswordResetDoneView(PasswordResetDoneView):
    """Vista que informa al usuario que el correo de restablecimiento fue enviado.

    Attributes:
        template_name (str): Plantilla HTML para mostrar el mensaje de éxito.
    """
    template_name = 'registration/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """Vista que permite al usuario ingresar una nueva contraseña tras recibir el enlace.

    Attributes:
        template_name (str): Plantilla para confirmar la nueva contraseña.
        success_url (str): URL de redirección al completarse el cambio de contraseña.
    """
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    """Vista mostrada tras completar exitosamente el restablecimiento de contraseña.

    Attributes:
        template_name (str): Plantilla HTML para el mensaje final.
    """
    template_name = 'registration/password_reset_complete.html'


def login_view(request):
    """Vista para iniciar sesión de usuario con redirección por rol.

    Si el inicio de sesión es exitoso, se redirige al usuario a la vista correspondiente
    a su grupo (Autor, Organizador, Revisor, Administrador).

    Args:
        request (HttpRequest): Petición HTTP entrante.

    Returns:
        HttpResponse: Página de login o redirección según el rol.
    """
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)

                if user.groups.filter(name='Autor').exists():
                    return redirect('vistaAutor')
                elif user.groups.filter(name='Organizador').exists():
                    return redirect('vistaOrganizador')
                elif user.groups.filter(name='Revisor').exists():
                    return redirect('vistaRevisor')
                elif user.groups.filter(name='Administrador').exists():
                    return redirect('vistaAdmin')
                else:
                    messages.error(request, "No tienes un rol asignado.")
                    return redirect('login')
            else:
                messages.error(request, "Usuario o contraseña incorrectos.")
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
    else:
        form = LoginForm()

    return render(request, 'usuarios/login.html', {'form': form})


def logout_view(request):
    """Cierra la sesión del usuario y redirige a la página de login.

    Args:
        request (HttpRequest): Petición HTTP.

    Returns:
        HttpResponse: Redirección a la vista de login.
    """
    logout(request)
    return redirect('login')


@login_required
def vistaAutor(request):
    """Vista del panel para usuarios con rol de Autor.

    Args:
        request (HttpRequest): Petición autenticada.

    Returns:
        HttpResponse: Renderiza la plantilla para el autor.
    """
    is_revisor = request.user.groups.filter(name='Revisor').exists()
    is_organizador = request.user.groups.filter(name='Organizador').exists()
    is_administrador = request.user.groups.filter(
        name='Administrador').exists()
    return render(request, 'usuarios/vistaAutor.html', {
        'is_organizador': is_organizador,
        'is_revisor': is_revisor,
        'is_administrador': is_administrador})


@login_required
def vistaOrganizador(request):
    """Vista del panel para usuarios con rol de Organizador.

    Args:
        request (HttpRequest): Petición autenticada.

    Returns:
        HttpResponse: Renderiza la plantilla del organizador.
    """
    is_revisor = request.user.groups.filter(name='Revisor').exists()
    is_organizador = request.user.groups.filter(name='Organizador').exists()
    is_administrador = request.user.groups.filter(
        name='Administrador').exists()
    return render(request, 'usuarios/vistaOrganizador.html', {
        'is_organizador': is_organizador,
        'is_revisor': is_revisor,
        'is_administrador': is_administrador})


@login_required
def vistaRevisor(request):
    """Vista del panel para usuarios con rol de Revisor.

    Args:
        request (HttpRequest): Petición autenticada.

    Returns:
        HttpResponse: Renderiza la plantilla del revisor.
    """
    is_revisor = request.user.groups.filter(name='Revisor').exists()
    is_organizador = request.user.groups.filter(name='Organizador').exists()
    is_administrador = request.user.groups.filter(
        name='Administrador').exists()
    return render(request, 'usuarios/vistaRevisor.html', {
        'is_organizador': is_organizador,
        'is_revisor': is_revisor,
        'is_administrador': is_administrador})


@login_required
def vistaAdmin(request):
    """Vista del panel para usuarios con rol de Administrador.

    Args:
        request (HttpRequest): Petición autenticada.

    Returns:
        HttpResponse: Renderiza la plantilla del administrador.
    """
    is_revisor = request.user.groups.filter(name='Revisor').exists()
    is_organizador = request.user.groups.filter(name='Organizador').exists()
    is_administrador = request.user.groups.filter(
        name='Administrador').exists()
    return render(request, 'usuarios/vistaAdmin.html', {
        'is_organizador': is_organizador,
        'is_revisor': is_revisor,
        'is_administrador': is_administrador})


def registro_view(request):
    """Vista para registrar un nuevo usuario en el sistema.

    Asigna automáticamente al usuario al grupo 'Autor' y lo autentica.

    Args:
        request (HttpRequest): Petición HTTP entrante.

    Returns:
        HttpResponse: Formulario de registro o redirección tras éxito.
    """
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = email

            if CustomUser.objects.filter(email=email).exists():
                form.add_error('email', 'Este correo ya está registrado.')
                return render(request,
                              'usuarios/registro.html',
                              {'form': form})

            user = form.save(commit=False)
            user.username = username
            user.set_password(form.cleaned_data['password1'])
            user.nombre = form.cleaned_data['nombre']
            user.apellidos = form.cleaned_data['apellidos']
            user.save()

            autor_group, _ = Group.objects.get_or_create(name='Autor')
            user.groups.add(autor_group)

            login(request, user)
            messages.success(
                request, '¡Registro exitoso! Ya puedes iniciar sesión.')
            return redirect('login')
    else:
        form = RegistroForm()

    return render(request, 'usuarios/registro.html', {'form': form})


@login_required
def admin_dashboard(request):
    """Vista del panel de administración que lista todos los usuarios.

    Args:
        request (HttpRequest): Petición autenticada.

    Returns:
        HttpResponse: Plantilla del panel de administración.
    """
    users = CustomUser.objects.all()
    return render(request, 'usuarios/admin_dashboard.html', {'users': users})


@login_required
def actualizar_roles(request):
    """Actualiza los roles de los usuarios desde el panel de administración.

    Envía notificaciones cuando se agregan o remueven roles.

    Args:
        request (HttpRequest): Petición autenticada.

    Returns:
        HttpResponse: Redirección al panel de administración.
    """
    if request.method == 'POST':
        users = CustomUser.objects.all()
        for user in users:
            for rol in ['Organizador', 'Revisor', 'Administrador']:
                checkbox_name = f'roles_{user.id}_{rol.lower()}'
                grupo, _ = Group.objects.get_or_create(name=rol)

                tiene_rol = grupo in user.groups.all()
                check_enviado = checkbox_name in request.POST

                if check_enviado and not tiene_rol:
                    user.groups.add(grupo)
                    Notificacion.objects.create(
                        usuario=user,
                        mensaje=f"Se te ha asignado el rol de {rol}."
                    )
                elif not check_enviado and tiene_rol:
                    user.groups.remove(grupo)
                    Notificacion.objects.create(
                        usuario=user,
                        mensaje=f"Se te ha removido el rol de {rol}."
                    )

        return redirect('admin_dashboard')


@login_required
def admin_dashboard_view(request):
    """Vista alternativa del panel de administración, con roles preprocesados.

    Args:
        request (HttpRequest): Petición autenticada.

    Returns:
        HttpResponse: Plantilla del panel con roles listados por usuario.
    """
    usuarios = CustomUser.objects.all().prefetch_related('groups')
    for user in usuarios:
        user.roles = list(user.groups.values_list('name', flat=True))

    return render(request, 'administrador/admin_dashboard.html', {
        'usuarios': usuarios
    })


@login_required
def vista_organizador(request):
    """Vista que muestra al organizador las conferencias que ha creado.

    Args:
        request (HttpRequest): Petición autenticada.

    Returns:
        HttpResponse: Plantilla con la lista de conferencias.
    """
    conferencias = Conferencia.objects.filter(organizador=request.user)
    return render(request,
                  'usuarios/vistaOrganizador.html',
                  {'conferencias': conferencias})


@login_required
def invitaciones_autor_view(request):
    """Vista que muestra al autor sus invitaciones para ser revisor.

    Args:
        request (HttpRequest): Petición autenticada.

    Returns:
        HttpResponse: Plantilla con la lista de invitaciones.
    """
    usuario = request.user
    invitaciones = InvitacionRevisor.objects.filter(autor=usuario)
    return render(request, 'usuarios/invitaciones.html',
                  {'invitaciones': invitaciones})


@login_required
def responder_invitacion_revisor_view(request, invitacion_id):
    """Permite al usuario responder a una invitación para ser revisor.

    Args:
        request (HttpRequest): Petición autenticada.
        invitacion_id (int): ID de la invitación.

    Returns:
        HttpResponse: Redirección a la vista de invitaciones.
    """
    invitacion = get_object_or_404(
        InvitacionRevisor, id=invitacion_id, autor=request.user)

    if request.method == 'POST':
        respuesta = request.POST.get('respuesta')
        if respuesta == 'aceptar':
            invitacion.estado = 'aceptado'
            grupo_revisor, _ = Group.objects.get_or_create(name='Revisor')
            if not request.user.groups.filter(name='Revisor').exists():
                request.user.groups.add(grupo_revisor)
        elif respuesta == 'rechazar':
            invitacion.estado = 'rechazado'

        invitacion.save()

    return redirect('invitaciones_autor')
