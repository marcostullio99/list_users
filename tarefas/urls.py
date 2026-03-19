from django.urls import path

from .views import (
    TaskCreateView,
    TaskDeleteView,
    TaskDetailView,
    TaskListView,
    TaskUpdateView,
    toggle_task_status,
)


app_name = "tarefas"

urlpatterns = [
    path("", TaskListView.as_view(), name="lista"),
    path("nova/", TaskCreateView.as_view(), name="criar"),
    path("<int:pk>/", TaskDetailView.as_view(), name="detalhe"),
    path("<int:pk>/editar/", TaskUpdateView.as_view(), name="editar"),
    path("<int:pk>/excluir/", TaskDeleteView.as_view(), name="excluir"),
    path("<int:pk>/alternar-status/", toggle_task_status, name="alternar_status"),
]
