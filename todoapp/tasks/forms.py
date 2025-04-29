from .models import Task
from django.forms import ModelForm
from django import forms


class Taskform(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date']


        
