import { Component, OnInit } from '@angular/core';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { Employee } from '../../core/services/employee';
import { EmployeeModel } from '../../core/models/class/employee.model';

@Component({
  selector: 'app-employees-data',
  imports: [ReactiveFormsModule, CommonModule],
  templateUrl: './employees-data.html',
  styleUrl: './employees-data.css',
})
export class EmployeesData implements OnInit {
  employeeForm!: FormGroup;
  employees: EmployeeModel[] = [];
  editingId: number | null = null;
  showForm = false;

  constructor(
    private fb: FormBuilder,
    private employeeService: Employee,
  ) {
    this.initializeForm();
  }

  ngOnInit(): void {
    this.loadEmployees();
  }

  initializeForm(): void {
    this.employeeForm = this.fb.group({
      employee_name: ['', [Validators.required, Validators.minLength(3)]],
      email: ['', [Validators.required, Validators.email]],
      phone: ['', [Validators.required, Validators.pattern(/^\d{10}$/)]],
      date_of_joining: ['', Validators.required],
      salary: ['', [Validators.required, Validators.pattern(/^\d+(\.\d{1,2})?$/)]],
      designation: ['', Validators.required],
      is_active: [true],
      department: [0, Validators.required],
    });
  }

  loadEmployees(): void {
    this.employeeService.employees$.subscribe((employees) => {
      this.employees = employees;
    });
  }

  onSubmit(): void {
    if (this.employeeForm.valid) {
      if (this.editingId !== null) {
        // Update existing employee
        const success = this.employeeService.updateEmployee(
          this.editingId,
          this.employeeForm.value,
        );
        if (success) {
          alert('Employee updated successfully!');
          this.resetForm();
        }
      } else {
        // Create new employee
        this.employeeService.createEmployee(this.employeeForm.value);
        alert('Employee created successfully!');
        this.resetForm();
      }
    }
  }

  editEmployee(employee: EmployeeModel): void {
    this.editingId = employee.id || null;
    this.employeeForm.patchValue(employee);
    this.showForm = true;
    window.scrollTo(0, 0);
  }

  deleteEmployee(id: number | undefined): void {
    if (id && confirm('Are you sure you want to delete this employee?')) {
      const success = this.employeeService.deleteEmployee(id);
      if (success) {
        alert('Employee deleted successfully!');
      }
    }
  }

  resetForm(): void {
    this.employeeForm.reset({
      is_active: true,
      department: 0,
    });
    this.editingId = null;
    this.showForm = false;
  }

  toggleForm(): void {
    this.showForm = !this.showForm;
    if (!this.showForm) {
      this.resetForm();
    }
  }

  get employee_name() {
    return this.employeeForm.get('employee_name');
  }

  get email() {
    return this.employeeForm.get('email');
  }

  get phone() {
    return this.employeeForm.get('phone');
  }

  get date_of_joining() {
    return this.employeeForm.get('date_of_joining');
  }

  get salary() {
    return this.employeeForm.get('salary');
  }

  get designation() {
    return this.employeeForm.get('designation');
  }

  get department() {
    return this.employeeForm.get('department');
  }
}
