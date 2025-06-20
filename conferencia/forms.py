from django import forms
from .models import Conferencia
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()


class ConferenciaForm(forms.ModelForm):
    """Formulario para crear y editar instancias del modelo Conferencia.

    Este formulario utiliza widgets personalizados para mejorar la presentación en el frontend.
    Además, filtra los campos 'organizador' y 'autor' para que solo se muestren usuarios
    pertenecientes a los grupos correspondientes.

    Attributes:
        Meta (class): Define el modelo asociado y los campos incluidos, así como los widgets personalizados.
    """

    class Meta:
        """Metadatos del formulario.

        Attributes:
            model (Model): Modelo al que está vinculado el formulario (Conferencia).
            fields (list): Lista de campos que serán utilizados en el formulario.
            widgets (dict): Diccionario de widgets personalizados para cada campo.
        """
        model = Conferencia
        fields = ['nombre', 'meses', 'dias', 'horas',
                  'minutos', 'organizador', 'autor', 'categoria']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'meses': forms.NumberInput(attrs={'class': 'form-control'}),
            'dias': forms.NumberInput(attrs={'class': 'form-control'}),
            'horas': forms.NumberInput(attrs={'class': 'form-control'}),
            'minutos': forms.NumberInput(attrs={'class': 'form-control'}),
            'organizador': forms.Select(attrs={'class': 'form-control'}),
            'autor': forms.Select(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        """Inicializa el formulario y personaliza los queryset de los campos 'organizador' y 'autor'.

        Filtra los usuarios que pueden ser seleccionados como organizadores o autores,
        según pertenezcan a los grupos 'Organizador' y 'Autor', respectivamente.

        Args:
            *args: Argumentos posicionales para el constructor del formulario.
            **kwargs: Argumentos con nombre para el constructor del formulario.
        """
        super().__init__(*args, **kwargs)
        try:
            grupo_organizadores = Group.objects.get(name='Organizador')
            self.fields['organizador'].queryset = grupo_organizadores.user_set.all()
        except Group.DoesNotExist:
            self.fields['organizador'].queryset = User.objects.none()

        try:
            self.fields['autor'].queryset = Group.objects.get(
                name='Autor').user_set.all()
        except Group.DoesNotExist:
            self.fields['autor'].queryset = User.objects.none()
