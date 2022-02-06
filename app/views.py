import datetime
from django.shortcuts import render

# Create your views here.

from rest_framework.generics import ListCreateAPIView, UpdateAPIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Task
from .serializers import TaskSerializer


class ListCreateTasks(ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.all()

    def list(self, request):
        queryset = self.get_queryset().filter(owner=request.user).order_by("-created_at", "-updated_at")
        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(data=request.DATA)

        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        task = Task.objects.create(
            owner=request.user,
            name=serializer.data['name'],
            description=serializer.data['description'],
            is_done=serializer.data['is_done'],
            created_at = datetime.datetime.now(),
            updated_at = datetime.datetime.now())
        result = TaskSerializer(task)
        return Response(result.data, status=status.HTTP_201_CREATED)


class MarkTaskAsDone(APIView):

    def post(self, request, pk):
        task = Task.objects.filter(owner=request.user).get(id=pk)
        serialized_task = TaskSerializer(task)
        if task:
            task.is_done = True
            task.save()
            return Response(status=status.HTTP_202_ACCEPTED, data=serialized_task.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

