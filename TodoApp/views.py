from django.shortcuts import render
from django.views import View
from rest_framework.views import APIView
from .serializers import *
from .models import *
from rest_framework import status
from rest_framework.response import Response
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404

def todo_page(request):
    todos = Todo.objects.all()
    return render(request, "index.html", {"todos": todos})

class AddTodoView(View):
    def post(self, request):
        title = request.POST.get("title")
        if not title:
            return HttpResponse(status=400)
        todo = Todo.objects.create(title=title)
        return render(request, "forms/todo.html", {"todo": todo})
    
class EditTodoView(View):
    def get(self, request, pk):
        todo = get_object_or_404(Todo, pk=pk)
        return render(request, "forms/todo.html", {
            "todo": todo,
            "editing": True
        })

    def post(self, request, pk):
        todo = get_object_or_404(Todo, pk=pk)
        todo.title = request.POST.get("title")
        todo.save()

        return render(request, "forms/todo.html", {
            "todo": todo,
            "editing": False
        })

class DeleteTodoView(View):
    def delete(self, request, pk):
        todo = Todo.objects.get(pk=pk)
        todo.delete()
        return HttpResponse()    


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


class TodoDetailView(APIView):

    def get(self, request, pk):
        todo = get_object_or_404(Todo, pk=pk)
        serializer = TodoSerializer(todo)
        return Response(serializer.data)

    def put(self, request, pk):
        todo = get_object_or_404(Todo, pk=pk)
        serializer = TodoSerializer(todo, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        todo = get_object_or_404(Todo, pk=pk)
        serializer = TodoSerializer(todo, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        todo = get_object_or_404(Todo, pk=pk)
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)       