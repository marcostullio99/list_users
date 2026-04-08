from django import forms
from django.core.exceptions import ValidationError

from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["titulo", "descricao", "concluida"]
        labels = {
            "titulo": "Titulo",
            "descricao": "Descricao",
            "concluida": "Marcar como concluida",
        }
        help_texts = {
            "titulo": "Use um nome curto e objetivo para facilitar a leitura.",
            "descricao": "Opcional: adicione contexto para executar a tarefa.",
        }
        widgets = {
            "titulo": forms.TextInput(attrs={"placeholder": "Ex.: Revisar proposta comercial"}),
            "descricao": forms.Textarea(
                attrs={
                    "placeholder": "Descreva os detalhes importantes",
                    "rows": 4,
                }
            ),
        }

    def clean_titulo(self):
        titulo = self.cleaned_data["titulo"].strip()
        if len(titulo) < 3:
            raise ValidationError("O titulo deve ter pelo menos 3 caracteres.")
        return titulo

    def clean_descricao(self):
        descricao = self.cleaned_data.get("descricao", "")
        return descricao.strip()
