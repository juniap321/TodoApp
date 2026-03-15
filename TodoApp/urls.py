from django.urls import path
from .views import *

urlpatterns = [
    # HTML Page
    path('', todo_page, name="todo-page"),
    path("add/", AddTodoView.as_view(), name="add"),
    path('edit/<int:pk>/', EditTodoView.as_view(), name="update"),
    path('delete/<int:pk>/', DeleteTodoView.as_view(), name="delete"),


    # REST APIs
    path('api/todos/', TodoListCreateView.as_view()),
    path('api/tododetails/', TodoDetailView.as_view()),

    
    ]