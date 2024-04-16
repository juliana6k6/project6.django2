from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView
from mail.models import Mailing, Client, Message, Mail_attempt
from blog.models import Post
def index(request):
    return render(request, 'mail/index.html')


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