from django.shortcuts import render
from django.views import View
from rest_framework.views import APIView
from .serializers import *
from .models import *
from rest_framework import status
from rest_framework.response import Response
from django.http.response import HttpResponse


class TodoListCreateView(APIView):
    def get(self,request):
        todos = Todo.objects.all()
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

def todo_page(request):
    todos = Todo.objects.all()
    return render(request, "index.html", {"todos": todos})

class AddTodoView(View):
    def post(self, request):
        title = request.POST.get("title")
        if title:
            todo = Todo.objects.create(title=title)
        return render(request, "forms/todo.html", {"todo": todo})
    
class UpdateTodoView(View):
    def put(self, request, pk):
        todo = Todo.objects.get(pk=pk)
        todo.is_done = True
        todo.save()
        return render(request, "forms/todo.html", {"todo": todo})

class DeleteTodoView(View):
    def delete(self, request, pk):
        todo = Todo.objects.get(pk=pk)
        todo.delete()
        return HttpResponse(status=204)      