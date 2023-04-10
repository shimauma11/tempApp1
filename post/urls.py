from django.urls import path
from .views import HomeView

app_name = "post"
urlpatterns = [
    path("home/", HomeView, name="home")
]
