from django.contrib import admin
from .models import Department, Employee

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('department_id', 'department_name', 'created_at')
    search_fields = ('department_name',)
    ordering = ('department_name',)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        'employee_id',
        'employee_name',
        'email',
        'phone',
        'department',
        'designation',
        'date_of_joining',
        'is_active'
    )
    list_filter = ('department', 'is_active', 'date_of_joining')
    search_fields = ('employee_name', 'email', 'phone')
    ordering = ('employee_name',)
    list_per_page = 10
