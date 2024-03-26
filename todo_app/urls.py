from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("register", views.register, name="register"),
    path("login", views.login, name="login"),
    path("save-task", views.save_task, name="save-task"),
    path("update-task/<int:task_id>", views.update_task, name="update-task"),
    path("toggle-completion/<int:task_id>", views.toggle_completion, name="toggle-completion"),
    path("delete-task/<int:task_id>", views.delete_task, name="delete-task"),
    path("create-list", views.create_new_list, name="create-list"),
    path("search-list", views.search_list, name="search-list"),
    path("delete-list/<int:list_id>", views.delete_list, name="delete-list"),
]