from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from .models import Post

# Create your views here.
User = get_user_model()


class HomeView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "post/home.html"
    context_object_name = "postList"
    queryset = model.objects.prefetch_related("user").order_by("-created_at")


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = "post/detail.html"
    context_object_name = "post"


class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "post/create.html"
    fields = ["title", "content"]
    success_url = reverse_lazy("post:home")

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super().form_valid(form)


class DeletePostView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "post/delete.html"
    success_url = reverse_lazy("post:home")

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.user
