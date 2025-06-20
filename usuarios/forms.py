from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser  # Asegúrate de importar CustomUser


class LoginForm(AuthenticationForm):
    """
    Formulario de autenticación personalizado que usa el correo electrónico como username.

    Attributes:
        username (EmailField): Campo para el correo electrónico.
        password (CharField): Campo para la contraseña con widget PasswordInput.
    """

    username = forms.EmailField()  # Usamos 'username' pero representará el correo
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        """
        Metadatos para el formulario LoginForm.

        Attributes:
            model (CustomUser): Modelo de usuario personalizado.
            fields (list[str]): Campos incluidos en el formulario.
        """
        model = CustomUser  # Usamos CustomUser en lugar de User
        fields = ['username', 'password']

    def clean_username(self):
        """
        Valida que el correo ingresado exista en la base de datos.

        Raises:
            forms.ValidationError: Si no existe un usuario con el correo dado.

        Returns:
            str: El correo electrónico validado.
        """
        email = self.cleaned_data.get('username')
        try:
            CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise forms.ValidationError(
                "No se encuentra un usuario con ese correo.")
        return email


AREAS = [
    ('Ingenieria', 'Ingenieria'),
    ('Medicina', 'Medicina'),
    ('Letras', 'Letras'),
    ('Contabilidad', 'Contabilidad'),
]


class RegistroForm(UserCreationForm):
    """
    Formulario para el registro de usuarios con campos personalizados.

    Attributes:
        email (EmailField): Campo para el correo electrónico.
        area_conocimiento (ChoiceField): Campo para seleccionar área de conocimiento.
    """

    email = forms.EmailField()

    area_conocimiento = forms.ChoiceField(
        choices=[('', 'Seleccionar área')] + AREAS
    )

    class Meta:
        """
        Metadatos para el formulario RegistroForm.

        Attributes:
            model (CustomUser): Modelo de usuario personalizado.
            fields (list[str]): Campos incluidos en el formulario.
        """
        model = CustomUser
        fields = ['nombre', 'apellidos', 'email',
                  'password1', 'password2', 'area_conocimiento']

    def save(self, commit=True):
        """
        Guarda una nueva instancia de usuario asegurando que el correo se use como username y sea único.

        Args:
            commit (bool): Si es True, guarda el usuario en la base de datos.

        Raises:
            forms.ValidationError: Si ya existe un usuario con el mismo correo.

        Returns:
            CustomUser: El usuario creado.
        """
        user = super().save(commit=False)
        # Usamos el correo como username
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']

        # Validación para asegurarnos de que no haya duplicados de correo
        if CustomUser.objects.filter(email=user.email).exists():
            raise forms.ValidationError(
                "Ya existe un usuario con este correo electrónico.")

        if commit:
            user.save()
        return user
