from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Herramienta, UsuarioBombero, NotaHerramienta, EventoCalendario, ParteGuardia, UnidadMovil

class HerramientaForm(forms.ModelForm):
    class Meta:
        model = Herramienta
        fields = ['codigo', 'nombre', 'estado', 'disponibilidad', 'ubicacion', 'unidad']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 001', 'readonly': 'readonly'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la herramienta'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'disponibilidad': forms.Select(attrs={'class': 'form-control'}),
            'ubicacion': forms.Select(attrs={'class': 'form-control'}),
            'unidad': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['unidad'].queryset = UnidadMovil.objects.select_related('sitio').order_by('sitio__nombre', 'nombre')
        self.fields['unidad'].required = False
        self.fields['unidad'].label = 'Unidad (opcional)'

class RegistroBomberoForm(UserCreationForm):
    class Meta:
        model = UsuarioBombero
        fields = ('username', 'email', 'documento', 'rol')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rol'].label = 'Tipo de acceso'
        self.fields['rol'].help_text = 'Elegí el rol con el que vas a operar en el sistema.'

class NotaHerramientaForm(forms.ModelForm):
    class Meta:
        model = NotaHerramienta
        fields = ['detalle']
        widgets = {
            'detalle': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describa la falla, rotura o novedad de la herramienta...'}),
        }

class EventoCalendarioForm(forms.ModelForm):
    class Meta:
        model = EventoCalendario
        fields = ['fecha', 'titulo']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Revisión de mangueras'}),
        }

class ParteAsignarForm(forms.ModelForm):
    class Meta:
        model = ParteGuardia
        fields = ['fecha', 'turno', 'unidad', 'bombero']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'turno': forms.Select(attrs={'class': 'form-control'}),
            'unidad': forms.Select(attrs={'class': 'form-control'}),
            'bombero': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bombero'].queryset = UsuarioBombero.objects.filter(
            rol='rescatista', is_approved=True
        ).order_by('username')
        self.fields['bombero'].label = 'Bombero asignado'


class UnidadMovilForm(forms.ModelForm):
    class Meta:
        model = UnidadMovil
        fields = ['sitio', 'nombre', 'clasificacion', 'funcion', 'modelo', 'capacidad_personal', 'capacidad_agua', 'equipamiento', 'estado_operativo']
        widgets = {
            'sitio': forms.Select(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Unidad 1, Unidad 21...'}),
            'clasificacion': forms.Select(attrs={'class': 'form-control'}),
            'funcion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Función detallada de la unidad'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Mercedes-Benz 1620'}),
            'capacidad_personal': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 6'}),
            'capacidad_agua': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 3500 (en litros)'}),
            'equipamiento': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Equipamiento técnico de la unidad...'}),
            'estado_operativo': forms.Select(attrs={'class': 'form-control'}),
        }