import random
import secrets

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView, ListView

from config import settings
from users.forms import RecoverForm, RegistrationForm, UserForm
from users.models import User


# Create your views here.
class RegisterView(CreateView):
    model = User
    form_class = RegistrationForm

    def get_success_url(self):
        return reverse("users:login")

    def form_valid(self, form):
        user = form.save()
        token = secrets.token_hex(16)
        user.token = token
        user.is_active = False
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/verify/{token}"
        message = f"Привет, для подтверждения почты тебе нужно перейти по ссылке: {url}"
        send_mail("Верификация почты", message, settings.EMAIL_HOST_USER, [user.email])
        return super().form_valid(form)


def verify(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


def restore_access(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user = User.objects.get(email=email)
        new_password = "".join([str(random.randint(0, 9)) for _ in range(8)])

        message = f"Ваш новый пароль : {new_password}"
        send_mail(
            "Восстановление доступа", message, settings.EMAIL_HOST_USER, [user.email]
        )
        user.set_password(new_password)
        user.save()
        return redirect(reverse("users:login"))
    else:
        form = RecoverForm
        context = {"form": form}
        return render(request, "users/restore.html", context)


class UserListView(LoginRequiredMixin, ListView):
    model = User

    def get_queryset(self):
        customer_list = super().get_queryset()
        if self.request.user.is_bloked == True:
            raise Http404("Вы заблокрованы")
        else:
            return customer_list


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy("users:list_users")

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if user.is_superuser:
            return self.object
        if user != self.object.pk:
            raise Http404("Вы не можете удалить другого пользователя")
        return self.object
