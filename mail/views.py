from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, \
    TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from mail.models import Mailing, Client, Message, Mail_attempt
from blog.models import Post
from mail.forms import MailingForm
from django.urls import reverse_lazy, reverse
def index(request):
    return render(request, 'mail/index.html')


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
    success_url = reverse_lazy('mailing:mailing_list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    form = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')

  def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if user.groups.filter(name='Менеджер').exists() or user.is_superuser:
            return self.object
        if user != self.object.author:
            raise Http404("Вы можете редактировать только свои рассылки")
        return self.object


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('mail:mailing_list')

class MainPageView(TemplateView):
    """Отображение главной страницы сервиса"""
    template_name = 'mail/main_page.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['mailing_count'] = Mailing.objects.all().count()
        # количество рассылок всего
        context_data['active_mailing_count'] = Mailing.objects.filter(is_active=True, ).count()
        # количество активных рассылок
        context_data['unique_clients_count'] = Client.objects.all().distinct().count()
        # количество уникальных клиентов для рассылок
        context_data['random_posts'] = Post.objects.all()[:3]
        # три случайные статьи из блога
        return context_data