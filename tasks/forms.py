from django.forms import ModelForm, TextInput, Textarea, CheckboxInput
from .models import Task


class TaskForm(ModelForm):
    """Formulario para crear y actualizar tareas, estilizado con Bootstrap 5."""

    class Meta:
        model = Task
        fields = ['title', 'description', 'important']
        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título de la tarea',
            }),
            'description': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe la tarea (opcional)',
                'rows': 4,
            }),
            'important': CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }
