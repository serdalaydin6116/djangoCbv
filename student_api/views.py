from email.policy import HTTP
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, HttpResponse, get_object_or_404

from .models import Student, Path

from .serializers import StudentSerializer, PathSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, mixins, ListCreateAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView


# Create your views here.


### CBV ###
def home(request):
    return HttpResponse('<h1>API Page</h1>')


class StudentList(APIView):
    def get(self, request):
        students=Student.objects.all()
        serializer=StudentSerializer(students, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer=StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # data = {
            # "message": f"Student {data.last_name} created successfully"
            # }
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentDetail(APIView): 
    def get_obj(self, pk):
        return get_object_or_404(Student, pk=pk)

    def get(self, request, pk):
        student=self.get_obj(pk)
        serializer=StudentSerializer(student)
        return Response(serializer.data)    

    def put(self, request, pk):
        student=self.get_obj(pk)
        serializer=StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            new_data= serializer.data
            new_data['success']= f"student {student.last_name} updated successfully"
            return Response(new_data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST )

    def delete(self, request, pk):
        student=self.get_obj(pk)
        student.delete()
        data={
        "message": f"student {student.last_name} deleted successfully"
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)


### CBV GENERIC APIVIEW ###

class StudentListCreate(mixins.ListModelMixin, mixins.CreateModelMixin, GenericAPIView):
    queryset=Student.objects.all()
    serializer_class=StudentSerializer
    def get(self, request, *args, **kwargs):
        return self.list(request,*args, **kwargs )

    def post(self, request, *args, **kwargs):
        return self.create(request,*args, **kwargs )


class StudentURD(
    mixins.UpdateModelMixin, 
    mixins.RetrieveModelMixin, 
    mixins.DestroyModelMixin,
     GenericAPIView
    ):
    queryset=Student.objects.all()
    serializer_class=StudentSerializer
    def get(self, request, *args, **kwargs):
        return self.retrieve(request,*args, **kwargs )

    def put(self, request, *args, **kwargs):
        return self.update(request,*args, **kwargs )

    def delete(self, request, *args, **kwargs):
        return self.destroy(request,*args, **kwargs )


### CBV CONCRETE APIVIEW ###

class StudentLC(ListCreateAPIView):
    queryset=Student.objects.all()
    serializer_class=StudentSerializer

class StudentRUD(RetrieveUpdateDestroyAPIView):
    queryset=Student.objects.all()
    serializer_class=StudentSerializer




    

