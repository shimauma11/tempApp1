from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponseBadRequest, JsonResponse

from .models import Post, Like

# Create your views here.
User = get_user_model()


class HomeView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "post/home.html"
    context_object_name = "postList"
    queryset = model.objects.prefetch_related("user").order_by("-created_at")

    def get_context_data(self, **kwargs):
        ctxt = super().get_context_data(**kwargs)
        liked_post_list = Like.objects.filter(
            user=self.request.user
        ).values_list("post", flat=True)
        ctxt["liked_post_list"] = liked_post_list
        return ctxt


class ProfileView(LoginRequiredMixin, ListView):
    model = User
    template_name = "post/profile.html"
    context_object_name = "profile"
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, **kwargs):
        ctxt = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        user = get_object_or_404(User, pk=pk)
        follower = self.request.user
        can_follow = not follower.following.filter(pk=pk).exists()
        postList = user.posts.order_by("-created_at")
        liked_post_list = Like.objects.filter(user=follower).values_list(
            "post", flat=True
        )
        ctxt = {
            "postList": postList,
            "can_follow": can_follow,
            "following": user,
            "follower": follower,
            "following_count": user.following.count(),
            "follower_count": user.follower.count(),
            "liked_post_list": liked_post_list,
        }
        return ctxt


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = "post/detail.html"

    def get_context_data(self, **kwargs):
        ctxt = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        post = get_object_or_404(Post, pk=pk)
        user = self.request.user
        is_liked = Like.objects.filter(user=user, post=post).exists()
        ctxt["is_liked"] = is_liked
        ctxt["post"] = post
        return ctxt


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
        user = get_object_or_404(User, pk=pk)
        follower = self.request.user
        if follower == user:
            messages.add_message(
                request, messages.ERROR, "you can't do this action"
            )
            return HttpResponseBadRequest("you can't do this action")

        if follower.following.filter(username=username).exists():
            messages.add_message(
                request, messages.ERROR, "you can't do this action"
            )
            return HttpResponseBadRequest("you can't do this action")
        follower.following.add(user)
        return redirect("post:profile", username=username, pk=pk)


class UnFollowView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        username = self.kwargs["username"]
        pk = self.kwargs["pk"]
        user = get_object_or_404(User, pk=pk)
        follower = self.request.user
        if follower == user:
            messages.add_message(
                request, messages.ERROR, "you can't do this action"
            )
            return HttpResponseBadRequest("you can't do this action")
        if not follower.following.filter(username=username).exists():
            messages.add_message(
                request, messages.ERROR, "you can't do this action"
            )
            return HttpResponseBadRequest("you can't do this action")
        follower.following.remove(user)
        return redirect("post:profile", username=username, pk=pk)


class FollowListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "post/followList.html"

    def get_context_data(self, **kwargs):
        ctxt = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        user = get_object_or_404(User, pk=pk)
        followList = user.following.all()
        ctxt = {
            "followList": followList,
            "target_user": user,
        }
        return ctxt


class FollowerListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "post/followerList.html"

    def get_context_data(self, **kwargs):
        ctxt = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        user = get_object_or_404(User, pk=pk)
        followerList = user.follower.all()
        ctxt = {
            "followerList": followerList,
            "target_user": user,
        }
        return ctxt


class LikeView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        pk = self.kwargs["pk"]
        post = get_object_or_404(Post, pk=pk)
        user = self.request.user
        Like.objects.create(post=post, user=user)
        like_count = post.likes.count()
        ctxt = {
            "like_count": like_count,
        }
        return JsonResponse(ctxt)


class UnLikeView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        pk = self.kwargs["pk"]
        post = get_object_or_404(Post, pk=pk)
        user = self.request.user
        Like.objects.filter(post=post, user=user).delete()
        like_count = post.likes.count()
        ctxt = {
            "like_count": like_count,
        }
        return JsonResponse(ctxt)
