from django.shortcuts import render
from django.http import HttpResponse
from app.serializers import *
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from app.models import *

# Create your views here.


class UserLoginView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        # return token with user type admin, teacher, student
        if user.is_superuser:
            return Response({'token': token.key, 'user_type': 'admin'}, status=status.HTTP_200_OK)
        else:
            if Teacher.objects.filter(user=user).exists():
                return Response({'token': token.key, 'user_type': 'teacher'}, status=status.HTTP_200_OK)
            elif Student.objects.filter(user=user).exists():
                return Response({'token': token.key, 'user_type': 'student'}, status=status.HTTP_200_OK)
            else:
                return Response({'token': token.key, 'user_type': 'unknown'}, status=status.HTTP_200_OK)
        
class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class Class_nameViewSet(viewsets.ModelViewSet):
    queryset = Class_name.objects.all()
    serializer_class = Class_nameSerializer

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class ParentViewSet(viewsets.ModelViewSet):
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer

class MarkViewSet(viewsets.ModelViewSet):
    queryset = Mark.objects.all()
    serializer_class = MarkSerializer