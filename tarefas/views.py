from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import TaskForm
from .models import Task


class TaskListView(ListView):
    model = Task
    template_name = "tarefas/lista_tarefas.html"
    context_object_name = "tasks"


class TaskCreateView(SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tarefas/criar_tarefa.html"
    success_url = reverse_lazy("tarefas:lista")
    success_message = "Tarefa criada com sucesso."


class TaskDetailView(DetailView):
    model = Task
    template_name = "tarefas/detalhe_tarefa.html"
    context_object_name = "task"


class TaskUpdateView(SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tarefas/editar_tarefa.html"
    success_url = reverse_lazy("tarefas:lista")
    success_message = "Tarefa atualizada com sucesso."


class TaskDeleteView(SuccessMessageMixin, DeleteView):
    model = Task
    template_name = "tarefas/confirmar_exclusao.html"
    success_url = reverse_lazy("tarefas:lista")

    def form_valid(self, form):
        messages.success(self.request, "Tarefa removida com sucesso.")
        return super().form_valid(form)


@require_POST
def toggle_task_status(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.concluida = not task.concluida
    task.save(update_fields=["concluida"])

    if task.concluida:
        messages.success(request, "Tarefa marcada como concluida.")
    else:
        messages.success(request, "Tarefa marcada como pendente.")

    return redirect("tarefas:lista")
