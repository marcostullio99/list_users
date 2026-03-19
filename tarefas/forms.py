from django import forms

from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["titulo", "descricao", "concluida"]
        widgets = {
            "titulo": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Titulo da tarefa"}
            ),
            "descricao": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Descreva a tarefa",
                    "rows": 4,
                }
            ),
        }
