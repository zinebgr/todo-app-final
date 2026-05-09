from django import forms
from .models import Task
from django.utils.translation import gettext_lazy as _

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'completed', 'due_date']
        labels = {
            'title': _('Title'),
            'description': _('Description'),
            'completed': _('Completed'),
            'due_date': _('Due Date'),
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Enter task title...')
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': _('Task description (optional)')
            }),
            'completed': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'due_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
        }