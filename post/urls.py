from django.urls import path
from .views import (
    HomeView,
    CreatePostView,
    PostDetailView,
    DeletePostView,
    ProfileView,
    FollowView,
    UnFollowView,
    FollowListView,
    FollowerListView,
    LikeView,
    UnLikeView,
    CommentView,
)

app_name = "post"
urlpatterns = [
    path("home/", HomeView.as_view(), name="home"),
    path("create/", CreatePostView.as_view(), name="create"),
    path("detail/<int:pk>/", PostDetailView.as_view(), name="detail"),
    path("delete/<int:pk>/", DeletePostView.as_view(), name="delete"),
    path(
        "profile/<str:username>/<int:pk>",
        ProfileView.as_view(),
        name="profile",
    ),
    path(
        "follow/<str:username>/<int:pk>/", FollowView.as_view(), name="follow"
    ),
    path(
        "unfollow/<str:username>/<int:pk>/",
        UnFollowView.as_view(),
        name="unfollow",
    ),
    path(
        "followList/<str:username>/<int:pk>/",
        FollowListView.as_view(),
        name="followList",
    ),
    path(
        "followerList/<str:username>/<int:pk>/",
        FollowerListView.as_view(),
        name="followerList",
    ),
    path("<int:pk>/like/", LikeView.as_view(), name="like"),
    path("<int:pk>/unlike/", UnLikeView.as_view(), name="unlike"),
    path("comment/<int:pk>/", CommentView.as_view(), name="comment"),
]
