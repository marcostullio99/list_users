from urllib.parse import quote

from django.test import TestCase
from django.urls import reverse

from .models import Task


class TaskModelTest(TestCase):
    def test_str_retorna_titulo(self):
        task = Task(titulo="Estudar Django")
        self.assertEqual(str(task), "Estudar Django")


class TaskListViewTest(TestCase):
    def test_lista_filtrada_mantem_metricas_globais_e_resultados_filtrados(self):
        Task.objects.create(titulo="Planejar sprint", concluida=False)
        Task.objects.create(titulo="Revisar entrega", concluida=True)
        Task.objects.create(titulo="Planejar retro", concluida=False)

        response = self.client.get(reverse("tarefas:lista"), {"q": "Planejar", "status": "pendentes"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["total_tasks"], 3)
        self.assertEqual(response.context["total_done"], 1)
        self.assertEqual(response.context["total_pending"], 2)
        self.assertEqual(response.context["result_count"], 2)
        self.assertEqual(response.context["paginator"].count, 2)

    def test_lista_e_paginada_em_seis_itens(self):
        for index in range(7):
            Task.objects.create(titulo=f"Tarefa {index}")

        response = self.client.get(reverse("tarefas:lista"))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(response.context["page_obj"].paginator.num_pages, 2)
        self.assertEqual(len(response.context["tasks"]), 6)


class TaskActionViewTest(TestCase):
    def test_toggle_status_redireciona_para_next_url_valida(self):
        task = Task.objects.create(titulo="Atualizar status")
        next_url = f"{reverse('tarefas:lista')}?status=pendentes&q=Atualizar"

        response = self.client.post(
            reverse("tarefas:alternar_status", args=[task.pk]),
            {"next": next_url},
        )

        task.refresh_from_db()
        self.assertTrue(task.concluida)
        self.assertRedirects(response, next_url)

    def test_toggle_status_aceita_next_url_codificada(self):
        task = Task.objects.create(titulo="Atualizar status com next codificada")
        next_url = f"{reverse('tarefas:lista')}?status=pendentes&q=Atualizar"

        response = self.client.post(
            reverse("tarefas:alternar_status", args=[task.pk]),
            {"next": quote(next_url, safe="")},
        )

        self.assertRedirects(response, next_url)

    def test_toggle_status_ignora_next_url_insegura(self):
        task = Task.objects.create(titulo="Atualizar status sem sair da app")

        response = self.client.post(
            reverse("tarefas:alternar_status", args=[task.pk]),
            {"next": "//example.com/fora"},
        )

        self.assertRedirects(response, reverse("tarefas:lista"))

    def test_excluir_mostra_cancelamento_seguro_quando_next_e_invalida(self):
        task = Task.objects.create(titulo="Excluir sem redirecionamento externo")

        response = self.client.get(
            reverse("tarefas:excluir", args=[task.pk]),
            {"next": "//example.com/fora"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["safe_next_url"], "")
        self.assertEqual(response.context["cancel_url"], reverse("tarefas:lista"))

    def test_excluir_redireciona_para_next_url_valida(self):
        task = Task.objects.create(titulo="Excluir e voltar para a lista filtrada")
        next_url = f"{reverse('tarefas:lista')}?status=pendentes"

        response = self.client.post(
            reverse("tarefas:excluir", args=[task.pk]),
            {"next": next_url},
        )

        self.assertRedirects(response, next_url)
        self.assertFalse(Task.objects.filter(pk=task.pk).exists())
