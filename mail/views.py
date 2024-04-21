from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)

from blog.models import Post
from mail.forms import ClientForm, MailingForm, MessageForm
from mail.models import Client, MailAttempt, Mailing, Message


def index(request):
    return render(request, "mail/index.html")


class MailingListView(LoginRequiredMixin, ListView):
    """Просмотр списка рассылок"""

    model = Mailing


class MailingDetailView(LoginRequiredMixin, DetailView):
    """Просмотр рассылки по id"""

    model = Mailing


class MailingCreateView(LoginRequiredMixin, CreateView):
    """Создание рассылки"""

    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("mail:mailing_list")

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    form = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("mail:mailing_list")

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if user.groups.filter(name="Менеджер").exists() or user.is_superuser:
            return self.object
        if user != self.object.author:
            raise Http404("Вы можете редактировать только свои рассылки")
        return self.object


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy("mail:mailing_list")

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if user.is_superuser:
            return self.object
        if user != self.object.author:
            raise Http404("Вы можете удалить только свою подписку")
        return self.object


class ClientListView(LoginRequiredMixin, ListView):
    """Просмотр списка клиентов"""

    model = Client


class ClientCreateView(LoginRequiredMixin, CreateView):
    """Создание нового клиента"""

    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("mail:client_list")


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование клиента"""

    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("mail:client_list")

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if user.groups.filter(name="Модератор").exists() or user.is_superuser:
            return self.object
        if user != self.object.author:
            raise Http404("Вы можете редактировать только своих клиентов")
        return self.object


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление клиента"""

    model = Client
    success_url = reverse_lazy("mail:client_list")

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if user.is_superuser:
            return self.object
        if user != self.object.author:
            raise Http404("Вы можете удалять только своих клиентов")
        return self.object


class MessageListView(LoginRequiredMixin, ListView):
    """Просмотр списка сообщений"""

    model = Message


class MessageCreateView(LoginRequiredMixin, CreateView):
    """Создание сообщения"""

    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mail:message_list")


class MailAttemptListView(LoginRequiredMixin, ListView):
    """Просмотр списка попыток отправки"""

    model = MailAttempt

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data["all"] = context_data["object_list"].count()
        context_data["success"] = (
            context_data["object_list"].filter(attempt_status=True).count()
        )
        context_data["non-success"] = (
            context_data["object_list"].filter(attempt_status=False).count()
        )
        return context_data


class MainPageView(TemplateView):
    """Отображение главной страницы сервиса"""

    template_name = "mail/main_page.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["mailing_count"] = Mailing.objects.all().count()
        # количество рассылок всего
        context_data["active_mailing_count"] = Mailing.objects.filter(
            is_active=True,
        ).count()
        # количество активных рассылок
        context_data["unique_clients_count"] = Client.objects.all().distinct().count()
        # количество уникальных клиентов для рассылок
        context_data["random_posts"] = Post.objects.all()[:3]
        # три случайные статьи из блога
        return context_data

    def toggle_status(request, pk):
        """Позволяюет отключать и активировать рассылку"""
        mailing = get_object_or_404(Mailing, pk=pk)
        message_service = MessageService(mailing)
        if mailing.status == "STARTED" or mailing.status == "CREATED":
            delete_task(mailing)
            mailing.status = "COMPLETED"
        else:
            message_service.create_task()
            mailing.status = "STARTED"

        mailing.save()

        return redirect(reverse("mail:mailing_list"))
