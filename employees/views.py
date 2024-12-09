from . import models
from . import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Employee
from django.contrib.auth.models import User
from .serializers import EmployeeSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics
from django.contrib.auth import authenticate
from . serializers import RegisterSerializer,LoginSerializer,UserSerializer

class EmployeePagination(PageNumberPagination):
    page_size = 10  # Limit results to 10 employees per page

class RegisterView(generics.CreateAPIView):
     queryset = User.objects.all()
    #  permission_classes = (AllowAny,) //optional
     serializer_class = RegisterSerializer



class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    # permission_classes = [AllowAny]  # Allow any user to access this view

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            user_serializer = UserSerializer(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': user_serializer.data
            })
        else:
            return Response({'detail': 'Invalid credentials'}, status=401)


class EmployeeViewSet(APIView):
    # authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated] 
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get(self, request, id=None):
        if id:
            try:
                item = models.Employee.objects.get(id=id)
                serializer = serializers.EmployeeSerializer(item)
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
            except models.Employee.DoesNotExist:
                return Response({"status": "error", "data": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

        # Filtering by query parameters 'department' and 'role'
        department = request.query_params.get('department')
        role = request.query_params.get('role')
        queryset = models.Employee.objects.all()

        # Validate department filter
        if department:
            if not queryset.filter(department=department).exists():
                return Response({"status": "error", "data": "Invalid department"}, status=status.HTTP_400_BAD_REQUEST)
            queryset = queryset.filter(department=department)

        # Validate role filter
        if role:
            if not queryset.filter(role=role).exists():
                return Response({"status": "error", "data": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)
            queryset = queryset.filter(role=role)

        paginator = EmployeePagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = serializers.EmployeeSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response({"status": "success", "data": serializer.data})

    def post(self, request):
        serializer = serializers.EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id=None):
        try:
            item = models.Employee.objects.get(id=id)
        except models.Employee.DoesNotExist:
            return Response({"status": "error", "data": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.EmployeeSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None):
        item = models.Employee.objects.filter(id=id)
        if not item.exists():
            return Response({"status": "error", "data": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
        
        item.delete()
        return Response({"status": "success", "data": "Item Deleted"}, status=status.HTTP_204_NO_CONTENT)
