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

class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "User registered successfully"})

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        from django.contrib.auth import authenticate

        user = authenticate(
            username=request.data.get('username'),
            password=request.data.get('password')
        )

        if not user:
            return Response({"error": "Invalid credentials"}, status=401)

        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        })


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged out successfully"})
        except Exception:
            return Response({"error": "Invalid token"}, status=400)


# class DepartmentAPIView(APIView):
#     @swagger_auto_schema(
#         operation_description="Get all departments or a single department",
#         tags=["D1epartments"]
#     )
    
#     def get(self, request, id=None):
#         if id:
#             department = get_object_or_404(Department, pk=id)
#             serializer = DepartmentSerializer(department)
#             return Response(serializer.data)
#         search = request.query_params.get('search')
#         departments = Department.objects.all()

#         if search:
#             departments = departments.filter(
#                 department_name__icontains=search
#             )

#         paginator = PageNumberPagination()
#         paginator.page_size = 5
#         result_page = paginator.paginate_queryset(departments, request)

#         serializer = DepartmentSerializer(result_page, many=True)
#         return paginator.get_paginated_response(serializer.data)
   
#         departments = Department.objects.all()
#         serializer = DepartmentSerializer(departments, many=True)
#         return Response(serializer.data)
    
#     # POST (Create)
#     def post(self, request):
#         serializer = DepartmentSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(
#                 serializer.data,
#                 status=status.HTTP_201_CREATED
#             )
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def put(self, request, id):
#         department = get_object_or_404(Department, pk=id)
#         serializer = DepartmentSerializer(department, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     # DELETE
#     def delete(self, request, id):
#         department = get_object_or_404(Department, pk=id)
#         department.delete()
#         return Response(
#             {"message": "Department deleted successfully"},
#             status=status.HTTP_204_NO_CONTENT
#         )

# class EmployeeAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     @swagger_auto_schema(
#         operation_description="Get all employees or a single employee",
#         tags=["E1mployees"]
#     )
#     #parser_classes = (MultiPartParser, FormParser)

#     # GET (All / Single)
#     def get(self, request, id=None):
#         if id:
#             employee = get_object_or_404(Employee, pk=id)
#             serializer = EmployeeSerializer(employee)
#             return Response(serializer.data)
#         search = request.query_params.get('search')

#         employees = Employee.objects.all()

#         if search:
#             employees = employees.filter(
#                 Q(employee_name__icontains=search) |
#                 Q(email__icontains=search) |
#                 Q(designation__icontains=search)
#             )

#         paginator = PageNumberPagination()
#         paginator.page_size = 5
#         result_page = paginator.paginate_queryset(employees, request)

#         serializer = EmployeeSerializer(result_page, many=True)
#         return paginator.get_paginated_response(serializer.data)

#         employees = Employee.objects.all()
#         serializer = EmployeeSerializer(employees, many=True)
#         return Response({"message": "You are authenticated"})
#         return Response(serializer.data)

#     # POST (Create)
#     def post(self, request):
#         serializer = EmployeeSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(
#                 serializer.data,
#                 status=status.HTTP_201_CREATED
#             )
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     # PUT (Update)
#     def put(self, request, id):
#         employee = get_object_or_404(Employee, pk=id)
#         serializer = EmployeeSerializer(employee, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     # DELETE
#     def delete(self, request, id):
#         employee = get_object_or_404(Employee, pk=id)
#         employee.delete()
#         return Response(
#             {"message": "Employee deleted successfully"},
#             status=status.HTTP_204_NO_CONTENT
#         )


# class DepartmentAPIView(APIView):
#     @swagger_auto_schema(
#         operation_description="Get all departments or a single department",
#         tags=["Departments"]
#     )
#     def get(self, request, id=None):
#         if id:
#             department = get_object_or_404(Department, pk=id)
#             serializer = DepartmentSerializer(department)
#             return Response(serializer.data)

#         search = request.query_params.get('search')
#         departments = Department.objects.all()

#         if search:
#             departments = departments.filter(
#                 department_name__icontains=search
#             )

#         paginator = PageNumberPagination()
#         paginator.page_size = 5
#         result_page = paginator.paginate_queryset(departments, request)

#         serializer = DepartmentSerializer(result_page, many=True)
#         return paginator.get_paginated_response(serializer.data)

#     def post(self, request):
#         serializer = DepartmentSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def put(self, request, id):
#         department = get_object_or_404(Department, pk=id)
#         serializer = DepartmentSerializer(department, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, id):
#         department = get_object_or_404(Department, pk=id)
#         department.delete()
#         return Response(
#             {"message": "Department deleted successfully"},
#             status=status.HTTP_204_NO_CONTENT
#         )
# class EmployeeAPIView(APIView):
#     permission_classes = [IsAuthenticated]
#     # parser_classes = (MultiPartParser, FormParser)

#     @swagger_auto_schema(
#         operation_description="Get all employees or a single employee",
#         tags=["Employees"]
#     )
#     def get(self, request, id=None):
#         if id:
#             employee = get_object_or_404(Employee, pk=id)
#             serializer = EmployeeSerializer(employee)
#             return Response(serializer.data)

#         search = request.query_params.get('search')
#         employees = Employee.objects.all()

#         if search:
#             employees = employees.filter(
#                 Q(employee_name__icontains=search) |
#                 Q(email__icontains=search) |
#                 Q(designation__icontains=search)
#             )

#         paginator = PageNumberPagination()
#         paginator.page_size = 5
#         result_page = paginator.paginate_queryset(employees, request)

#         serializer = EmployeeSerializer(result_page, many=True)
#         return paginator.get_paginated_response(serializer.data)

#     def post(self, request):
#         serializer = EmployeeSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def put(self, request, id):
#         employee = get_object_or_404(Employee, pk=id)
#         serializer = EmployeeSerializer(employee, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, id):
#         employee = get_object_or_404(Employee, pk=id)
#         employee.delete()
#         return Response(
#             {"message": "Employee deleted successfully"},
#             status=status.HTTP_204_NO_CONTENT
#         )

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


# ---------------- Department API ----------------
class DepartmentAPIView(APIView):
    permission_classes = [AllowAny]  # Public access
    pagination_class = PageNumberPagination

    @swagger_auto_schema(
        operation_description="Get all departments or a single department",
        tags=["Departments"]
    )
    def get(self, request, id=None):
        if id:
            department = get_object_or_404(Department, pk=id)
            serializer = DepartmentSerializer(department)
            return Response(serializer.data)

        search = request.query_params.get('search', '')
        departments = Department.objects.all().order_by('id')  # ✅ ordering

        if search:
            departments = departments.filter(department_name__icontains=search)

        paginator = PageNumberPagination()
        paginator.page_size = 5
        result_page = paginator.paginate_queryset(departments, request)
        serializer = DepartmentSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new department",
        tags=["Departments"]
    )
    def post(self, request):
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DepartmentDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]  # JWT protected
    @swagger_auto_schema(
        operation_description="Get all departments or a single department",
        tags=["Departments"]
    )
    def get(self, request, id=None):
        if id:
            department = get_object_or_404(Department, pk=id)
            serializer = DepartmentSerializer(department)
            return Response(serializer.data)

        search = request.query_params.get('search', '')
        departments = Department.objects.all().order_by('id')  # ✅ ordering

        if search:
            departments = departments.filter(department_name__icontains=search)

        paginator = PageNumberPagination()
        paginator.page_size = 5
        result_page = paginator.paginate_queryset(departments, request)
        serializer = DepartmentSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update a department by ID",
        tags=["Departments"]
    )
    def put(self, request, id):
        department = get_object_or_404(Department, pk=id)
        serializer = DepartmentSerializer(department, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a department by ID",
        tags=["Departments"]
    )
    def delete(self, request, id):
        department = get_object_or_404(Department, pk=id)
        department.delete()
        return Response(
            {"message": "Department deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )


# ---------------- Employee API ----------------
class EmployeeAPIView(APIView):
    permission_classes = [IsAuthenticated]  # JWT protected
    parser_classes = (MultiPartParser, FormParser)  # For file uploads

    @swagger_auto_schema(
        operation_description="Get all employees or a single employee",
        tags=["Employees"]
    )
    def get(self, request, id=None):
        if id:
            employee = get_object_or_404(Employee, pk=id)
            serializer = EmployeeSerializer(employee)
            return Response(serializer.data)

        search = request.query_params.get('search', '')
        employees = Employee.objects.all().order_by('id')  # ✅ ordering

        if search:
            employees = employees.filter(
                Q(employee_name__icontains=search) |
                Q(email__icontains=search) |
                Q(designation__icontains=search)
            )

        paginator = PageNumberPagination()
        paginator.page_size = 5
        result_page = paginator.paginate_queryset(employees, request)
        serializer = EmployeeSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
        return paginator.get_paginated_response(response_data)

    @swagger_auto_schema(
        operation_description="Create a new employee",
        tags=["Employees"]
    )
    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmployeeDetailAPIView(APIView):   
    permission_classes = [IsAuthenticated]  # JWT protected
    
    @swagger_auto_schema(
        operation_description="Get all employees or a single employee",
        tags=["Employees"]
    )
    def get(self, request, id=None):
        if id:
            employee = get_object_or_404(Employee, pk=id)
            serializer = EmployeeSerializer(employee)
            return Response(serializer.data)

        search = request.query_params.get('search', '')
        employees = Employee.objects.all().order_by('id')  # ✅ ordering

        if search:
            employees = employees.filter(
                Q(employee_name__icontains=search) |
                Q(email__icontains=search) |
                Q(designation__icontains=search)
            )

        paginator = PageNumberPagination()
        paginator.page_size = 5
        result_page = paginator.paginate_queryset(employees, request)
        serializer = EmployeeSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update an employee by ID",
        tags=["Employees"]
    )
    def put(self, request, id):
        employee = get_object_or_404(Employee, pk=id)
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete an employee by ID",
        tags=["Employees"]
    )
    def delete(self, request, id):
        employee = get_object_or_404(Employee, pk=id)
        employee.delete()
        return Response(
            {"message": "Employee deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )
