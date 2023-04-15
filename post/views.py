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
        following = get_object_or_404(User, pk=pk)
        follower = self.request.user
        can_follow = not FriendShip.objects.filter(
            follower=follower, following=following
        )
        postList = following.posts.order_by("-created_at")
        ctxt = {
            "postList": postList,
            "can_follow": can_follow,
            "following": following,
            "follower": follower,
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
        following = get_object_or_404(User, pk=pk)
        follower = request.user
        if follower == following:
            messages.add_message(
                request, messages.ERROR, "you can't do this action"
            )
            return HttpResponseBadRequest("you can't do this action")

        if FriendShip.objects.filter(
            follower=follower, following=following
        ).exists():
            messages.add_message(
                request, messages.ERROR, "you can't do this action"
            )
            return HttpResponseBadRequest("you can't do this action")
        FriendShip.objects.create(follower=follower, following=following)
        return redirect("post:profile", username=username, pk=pk)


class UnFollowView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        username = self.kwargs["username"]
        pk = self.kwargs["pk"]
        follower = self.request.user
        following = get_object_or_404(User, pk=pk)
        friendship = FriendShip.objects.filter(
            follower=follower, following=following
        )
        if follower == following:
            messages.add_message(
                request, messages.ERROR, "you can't do this action"
            )
            return HttpResponseBadRequest("you can't do this action")
        if not friendship.exists():
            messages.add_message(
                request, messages.ERROR, "you can't do this action"
            )
            return HttpResponseBadRequest("you can't do this action")
        friendship.delete()
        return redirect("post:profile", username=username, pk=pk)
