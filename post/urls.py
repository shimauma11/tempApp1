from django.urls import path
from .views import HomeView, CreatePostView, PostDetailView, DeletePostView, ProfileView

app_name = "post"
urlpatterns = [
    path("home/", HomeView.as_view(), name="home"),
    path("create/", CreatePostView.as_view(), name="create"),
    path("detail/<int:pk>/", PostDetailView.as_view(), name="detail"),
    path("delete/<int:pk>/", DeletePostView.as_view(), name="delete"),
    path("profile/", ProfileView.as_view(), name="profile"),
]
