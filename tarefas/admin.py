from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("titulo", "concluida", "criada_em")
    list_filter = ("concluida", "criada_em")
    search_fields = ("titulo", "descricao")
