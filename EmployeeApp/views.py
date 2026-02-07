from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.filters import SearchFilter
from django.db.models import Q
from .models import Department, Employee
from .serializers import DepartmentSerializer, EmployeeSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .serializers import RegisterSerializer

# class RegisterAPIView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         serializer = RegisterSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({"message": "User registered successfully"})

# class LoginAPIView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         from django.contrib.auth import authenticate

#         user = authenticate(
#             username=request.data.get('username'),
#             password=request.data.get('password')
#         )

#         if not user:
#             return Response({"error": "Invalid credentials"}, status=401)

#         refresh = RefreshToken.for_user(user)

#         return Response({
#             "access": str(refresh.access_token),
#             "refresh": str(refresh),
#         })


# class LogoutAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         try:
#             refresh_token = request.data["refresh"]
#             token = RefreshToken(refresh_token)
#             token.blacklist()
#             return Response({"message": "Logged out successfully"})
#         except Exception:
#             return Response({"error": "Invalid token"}, status=400)


# ================== REGISTER ==================
class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=RegisterSerializer,
        responses={
            201: openapi.Response(description="User registered successfully"),
            400: "Validation Error"
        },
        operation_description="Register a new user"
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)


# ================== LOGIN ==================
class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username of the user'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password of the user'),
            },
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'access': openapi.Schema(type=openapi.TYPE_STRING, description='Access token'),
                    'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token'),
                },
            ),
            401: "Invalid credentials"
        },
        operation_description="Login a user and return JWT tokens"
    )
    def post(self, request):
        from django.contrib.auth import authenticate

        user = authenticate(
            username=request.data.get('username'),
            password=request.data.get('password')
        )

        if not user:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        })


# ================== LOGOUT ==================
class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['refresh'],
            properties={
                'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token to blacklist'),
            },
        ),
        responses={
            200: "Logged out successfully",
            400: "Invalid token"
        },
        operation_description="Logout a user by blacklisting refresh token"
    )
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
            
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema

from .models import Department, Employee
from .serializers import DepartmentSerializer, EmployeeSerializer

# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Department, Employee
from .serializers import DepartmentSerializer, EmployeeSerializer

# ================== PAGINATION ==================
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5          # default items per page
    page_size_query_param = 'page_size'
    max_page_size = 50

# ================== DEPARTMENT ==================
class DepartmentListCreateAPIView(APIView):
    pagination_class = StandardResultsSetPagination

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('search', openapi.IN_QUERY, description="Search by name or description", type=openapi.TYPE_STRING),
            openapi.Parameter('ordering', openapi.IN_QUERY, description="Order by fields: department_name or created_at (prefix with '-' for descending)", type=openapi.TYPE_STRING),
            openapi.Parameter('page', openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER),
            openapi.Parameter('page_size', openapi.IN_QUERY, description="Page size", type=openapi.TYPE_INTEGER),
        ],
        responses={200: DepartmentSerializer(many=True)}
    )
    def get(self, request):
        queryset = Department.objects.all()
        search = request.GET.get('search')
        if search:
            queryset = queryset.filter(Q(department_name__icontains=search) | Q(description__icontains=search))
        ordering = request.GET.get('ordering')
        if ordering:
            queryset = queryset.order_by(ordering)
        paginator = StandardResultsSetPagination()
        paginated_qs = paginator.paginate_queryset(queryset, request)
        serializer = DepartmentSerializer(paginated_qs, many=True)
        return paginator.get_paginated_response(serializer.data)

    @swagger_auto_schema(request_body=DepartmentSerializer)
    def post(self, request):
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # ================== DEPARTMENT ==================
class DepartmentDetailAPIView(APIView):
    @swagger_auto_schema(responses={200: DepartmentSerializer})
    def get_object(self, pk):
        try:
            return Department.objects.get(pk=pk)
        except Department.DoesNotExist:
            return None

    @swagger_auto_schema(responses={200: DepartmentSerializer})
    def get(self, request, pk):
        department = self.get_object(pk)
        if not department:
            return Response({"error": "Department not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = DepartmentSerializer(department)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=DepartmentSerializer)
    def put(self, request, pk):
        department = self.get_object(pk)
        if not department:
            return Response({"error": "Department not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = DepartmentSerializer(department, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        department = self.get_object(pk)
        if not department:
            return Response({"error": "Department not found"}, status=status.HTTP_404_NOT_FOUND)
        department.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# ================== EMPLOYEE ==================
class EmployeeListCreateAPIView(APIView):
    pagination_class = StandardResultsSetPagination

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('search', openapi.IN_QUERY, description="Search by name, email, phone, designation, or department", type=openapi.TYPE_STRING),
            openapi.Parameter('department', openapi.IN_QUERY, description="Filter by department_id", type=openapi.TYPE_INTEGER),
            openapi.Parameter('ordering', openapi.IN_QUERY, description="Order by fields: employee_name, date_of_joining, salary (prefix '-' for descending)", type=openapi.TYPE_STRING),
            openapi.Parameter('page', openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER),
            openapi.Parameter('page_size', openapi.IN_QUERY, description="Page size", type=openapi.TYPE_INTEGER),
        ],
        responses={200: EmployeeSerializer(many=True)}
    )
    def get(self, request):
        queryset = Employee.objects.all()

        # ===== SEARCH =====
        search = request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(employee_name__icontains=search) |
                Q(email__icontains=search) |
                Q(phone__icontains=search) |
                Q(designation__icontains=search) |
                Q(department__department_name__icontains=search)
            )

        # ===== FILTER BY DEPARTMENT =====
        department_id = request.GET.get('department')
        if department_id:
            queryset = queryset.filter(department_id=department_id)

        # ===== ORDERING =====
        ordering = request.GET.get('ordering')
        if ordering:
            queryset = queryset.order_by(ordering)

        # ===== PAGINATION =====
        paginator = StandardResultsSetPagination()
        paginated_qs = paginator.paginate_queryset(queryset, request)
        serializer = EmployeeSerializer(paginated_qs, many=True)
        return paginator.get_paginated_response(serializer.data)

    @swagger_auto_schema(request_body=EmployeeSerializer)
    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ================== EMPLOYEE ==================
class EmployeeDetailAPIView(APIView):
    @swagger_auto_schema(responses={200: EmployeeSerializer})
    def get_object(self, pk):
        try:
            return Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            return None

    @swagger_auto_schema(responses={200: EmployeeSerializer})
    def get(self, request, pk):
        employee = self.get_object(pk)
        if not employee:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=EmployeeSerializer)
    def put(self, request, pk):
        employee = self.get_object(pk)
        if not employee:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        employee = self.get_object(pk)
        if not employee:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

