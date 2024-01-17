from django.forms import ModelForm
from .models import Task
from django import forms

class TaskForm(ModelForm):
    class Meta:
        model = Task
        exclude = ['user', 'datecompleted']
        #widgets = {
        #    'datecompleted': forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'}),
        #}