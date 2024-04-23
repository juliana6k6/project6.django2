from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from blog.models import Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ("title", "body")
    success_url = reverse_lazy("blog:post_list")

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class PostListView(ListView):
    model = Post


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("blog:post_list")

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if user != self.object.owner:
            raise Http404("Вы можете удалить только свои посты")
        return self.object


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ("title", "body", "preview")

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if not user.is_superuser or user != self.object.owner:
            raise Http404("Вы можете редактировать только свои посты")
        return self.object

    def get_success_url(self):
        return reverse("blog:post_view", args=[self.kwargs.get("pk")])


def published_activity(request, pk):
    post_item = get_object_or_404(Post, pk=pk)
    if post_item.published:
        post_item.published = False
    else:
        post_item.published = True
    post_item.save()
    return redirect(reverse_lazy("blog:post_list"))
