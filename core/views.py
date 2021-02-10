from django.views import View
from django.http import HttpResponse, JsonResponse
from core.models import ToDo, ToDoSchema
from django.shortcuts import get_object_or_404
import time

class ToDoView(View):
    def options(self, request):
        response = HttpResponse()
        print(request.headers.get("Origin"))
        response['Access-Control-Allow-Origin'] = request.headers.get("Origin") or '*'
        response['Access-Control-Allow-Methods'] = "GET, POST, PATCH, DELETE, OPTIONS"
        return response

    def get(self, request):
        todos = [
            ToDoSchema.from_orm(todo).dict() for todo in ToDo.objects.all()
        ]
        response = JsonResponse(todos, safe=False)
        print(todos)
        response['Access-Control-Allow-Origin'] = request.headers.get("Origin") or '*'
        response['Access-Control-Allow-Methods'] = "GET, POST, PATCH, DELETE, OPTIONS"
        return response

    def post(self, request):
        todo_data = ToDoSchema.parse_raw(request.body)
        todo_data.id = None
        ToDo.objects.create(**todo_data.dict())

        response = HttpResponse(status=201)
        response['Access-Control-Allow-Origin'] = request.headers.get("Origin") or '*'
        response['Access-Control-Allow-Methods'] = "GET, POST, PATCH, DELETE, OPTIONS"
        return response

    def patch(self, request):
        todo_data = ToDoSchema.parse_raw(request.body)
        todo = get_object_or_404(ToDo, id=todo_data.id)
        todo.complete = todo_data.complete
        todo.task = todo_data.task
        todo.save()
        response = HttpResponse(status=202)
        response['Access-Control-Allow-Origin'] = request.headers.get("Origin") or '*'
        response['Access-Control-Allow-Methods'] = "GET, POST, PATCH, DELETE, OPTIONS"
        return response

    def delete(self, request):
        ToDo.objects.filter(complete=True).delete()
        response = HttpResponse(status=204)
        response['Access-Control-Allow-Origin'] = request.headers.get("Origin") or '*'
        response['Access-Control-Allow-Methods'] = "GET, POST, PATCH, DELETE, OPTIONS"
        return response
