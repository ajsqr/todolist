from django.urls import path

from .views import ListCreateTasks, MarkTaskAsDone

urlpatterns = [
     path("list_create_tasks", ListCreateTasks.as_view()),
     path("mark_as_done", MarkTaskAsDone.as_view()),
]
