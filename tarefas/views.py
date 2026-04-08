from urllib.parse import unquote

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import TaskForm
from .models import Task


def get_safe_next_url(request, fallback=""):
    raw_next_url = request.POST.get("next", "") or request.GET.get("next", "")
    if not raw_next_url:
        return fallback

    next_url = unquote(raw_next_url)
    if url_has_allowed_host_and_scheme(
        url=next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return next_url
    return fallback


class TaskListView(ListView):
    model = Task
    template_name = "tarefas/lista_tarefas.html"
    context_object_name = "tasks"
    paginate_by = 6

    def get_queryset(self):
        queryset = Task.objects.all()
        query = self.request.GET.get("q", "").strip()
        status = self.request.GET.get("status", "todas")

        if query:
            queryset = queryset.filter(titulo__icontains=query)

        if status == "concluidas":
            queryset = queryset.filter(concluida=True)
        elif status == "pendentes":
            queryset = queryset.filter(concluida=False)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("q", "").strip()
        status = self.request.GET.get("status", "todas")
        context["query"] = query
        context["status"] = status
        context["total_tasks"] = Task.objects.count()
        context["total_done"] = Task.objects.filter(concluida=True).count()
        context["total_pending"] = Task.objects.filter(concluida=False).count()
        context["result_count"] = context["paginator"].count

        query_params = self.request.GET.copy()
        query_params.pop("page", None)
        context["query_params"] = query_params.urlencode()
        return context


class FormFeedbackMixin:
    error_message = "Não foi possível salvar. Reveja os campos e tente novamente."

    def form_invalid(self, form):
        messages.error(self.request, self.error_message)
        return super().form_invalid(form)


class TaskCreateView(FormFeedbackMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tarefas/criar_tarefa.html"
    success_url = reverse_lazy("tarefas:lista")
    success_message = "Tarefa criada com sucesso."


class TaskDetailView(DetailView):
    model = Task
    template_name = "tarefas/detalhe_tarefa.html"
    context_object_name = "task"


class TaskUpdateView(FormFeedbackMixin, SuccessMessageMixin, UpdateView):
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["safe_next_url"] = get_safe_next_url(self.request)
        context["cancel_url"] = context["safe_next_url"] or str(self.success_url)
        return context

    def get_success_url(self):
        return get_safe_next_url(self.request, str(self.success_url))



@require_POST
def toggle_task_status(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.concluida = not task.concluida
    task.save(update_fields=["concluida"])

    if task.concluida:
        messages.success(request, "Tarefa marcada como concluída.")
    else:
        messages.success(request, "Tarefa marcada como pendente.")

    next_url = get_safe_next_url(request)
    if next_url:
        return redirect(next_url)
    return redirect("tarefas:lista")
