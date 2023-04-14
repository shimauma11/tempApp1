from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponseBadRequest

from .models import Post
from registration.models import FriendShip

# Create your views here.
User = get_user_model()


class HomeView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "post/home.html"
    context_object_name = "postList"
    queryset = model.objects.prefetch_related("user").order_by("-created_at")


class ProfileView(LoginRequiredMixin, ListView):
    model = User
    template_name = "post/profile.html"
    context_object_name = "profile"
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, **kwargs):
        ctxt = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        target_user = get_object_or_404(User, pk=pk)
        request_user = self.request.user
        can_follow = not FriendShip.objects.filter(
            request_user=request_user, follower=target_user
        )
        postList = target_user.posts.order_by("-created_at")
        ctxt = {
            "postList": postList,
            "can_follow": can_follow,
            "request_user": request_user,
            "target_user": target_user
        }
        return ctxt


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
    context_object_name = "post"

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.user


class FollowView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        username = self.kwargs["username"]
        pk = self.kwargs["pk"]
        target_user = get_object_or_404(User, pk=pk)
        request_user = request.user
        if target_user == request_user:
            messages.add_message(
                request, messages.ERROR, "you can't do this action"
            )
            return HttpResponseBadRequest("you can't do this action")

        if FriendShip.objects.filter(
            request_user=request_user, follower=target_user
        ).exists():
            messages.add_message(
                request, messages.ERROR, "you can't do this action"
            )
            return HttpResponseBadRequest("you can't do this action")
        FriendShip.objects.create(
            request_user=request_user, follower=target_user
        )
        return redirect("post:profile", username=username, pk=pk)


class UnFollowView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        username = self.kwargs["username"]
        pk = self.kwargs["pk"]
        request_user = self.request.user
        target_user = get_object_or_404(User, pk=pk)
        target_friendship = FriendShip.objects.filter(
            request_user=request_user, follower=target_user
        )
        if request_user == target_user:
            messages.add_message(
                request, messages.ERROR, "you can't do this action"
            )
            return HttpResponseBadRequest("you can't do this action")
        if not target_friendship.exists():
            messages.add_message(
                request, messages.ERROR, "you can't do this action"
            )
            return HttpResponseBadRequest("you can't do this action")
        target_friendship.delete()
        return redirect("post:profile", username=username, pk=pk)

        
