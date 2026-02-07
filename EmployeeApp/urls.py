from django.urls import path
# from .views import (
#     DepartmentAPIView,
#     DepartmentDetailAPIView,
#     EmployeeAPIView,
#     EmployeeDetailAPIView
# )
from .views import (
    DepartmentListCreateAPIView,
    DepartmentDetailAPIView,
    EmployeeListCreateAPIView,
    EmployeeDetailAPIView,
)
from .views import RegisterAPIView, LoginAPIView, LogoutAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('logout/', LogoutAPIView.as_view()),

#    # Departments
#     path('departments/', DepartmentAPIView.as_view()),
#     path('departments/<int:id>/', DepartmentDetailAPIView.as_view()),

#     # Employees
#     path('employees/', EmployeeAPIView.as_view()),
#     path('employees/<int:id>/', EmployeeDetailAPIView.as_view()),

     # Department
    path('departments/', DepartmentListCreateAPIView.as_view(), name='department-list-create'),
    path('departments/<int:pk>/', DepartmentDetailAPIView.as_view(), name='department-detail'),

    # Employee
    path('employees/', EmployeeListCreateAPIView.as_view(), name='employee-list-create'),
    path('employees/<int:pk>/', EmployeeDetailAPIView.as_view(), name='employee-detail'),
]


