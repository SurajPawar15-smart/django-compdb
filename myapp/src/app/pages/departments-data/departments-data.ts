import { CommonModule, NgFor, NgIf } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { DepartmentModel } from '../../core/models/class/department.model';
import { Department } from '../../core/services/department';

@Component({
  selector: 'app-departments-data',
  imports: [ReactiveFormsModule, NgIf, NgFor, CommonModule],
  templateUrl: './departments-data.html',
  styleUrl: './departments-data.css',
})
export class DepartmentsData implements OnInit {
  departmentForm!: FormGroup;
  departmentList: DepartmentModel[] = [];
  isEditMode = false;
  selectedDepartmentId: number | null = null;
  isLoading = false;
  successMessage = '';
  errorMessage = '';

  constructor(
    private fb: FormBuilder,
    private departmentService: Department,
  ) {}

  ngOnInit(): void {
    this.createForm();
    this.loadDepartments();
  }

  createForm() {
    this.departmentForm = this.fb.group({
      department_name: ['', Validators.required],
      description: ['', Validators.required],
    });
  }

  // Enable/disable form controls based on loading state
  setFormControlsDisabled(disabled: boolean) {
    Object.keys(this.departmentForm.controls).forEach((key) => {
      const control = this.departmentForm.get(key);
      if (disabled) {
        control?.disable({ emitEvent: false });
      } else {
        control?.enable({ emitEvent: false });
      }
    });
  }

  // 🔹 GET ALL
  loadDepartments() {
    this.isLoading = true;
    this.departmentService.getAllDepartments().subscribe({
      next: (res: any) => {
        this.departmentList = res.data || res;
        this.isLoading = false;
      },
      error: (err) => {
        console.error('Failed to load departments:', err);
        this.errorMessage = 'Failed to load departments. Please try again.';
        this.isLoading = false;
        this.clearMessages();
      },
    });
  }

  // 🔹 CREATE / UPDATE
  onSubmit() {
    if (this.departmentForm.invalid) {
      return;
    }

    this.isLoading = true;
    this.setFormControlsDisabled(true);
    const payload: DepartmentModel = this.departmentForm.value;

    if (this.isEditMode && this.selectedDepartmentId) {
      // UPDATE
      this.departmentService
        .createNewDepartment({
          ...payload,
          department_id: this.selectedDepartmentId,
        })
        .subscribe({
          next: () => {
            this.successMessage = 'Department updated successfully!';
            this.resetForm();
            this.setFormControlsDisabled(false);
            this.loadDepartments();
            this.clearMessages();
          },
          error: (err) => {
            console.error('Failed to update department:', err);
            this.errorMessage = 'Failed to update department. Please try again.';
            this.isLoading = false;
            this.setFormControlsDisabled(false);
            this.clearMessages();
          },
        });
    } else {
      // CREATE
      this.departmentService.createNewDepartment(payload).subscribe({
        next: () => {
          this.successMessage = 'Department created successfully!';
          this.resetForm();
          this.setFormControlsDisabled(false);
          this.loadDepartments();
          this.clearMessages();
        },
        error: (err) => {
          console.error('Failed to create department:', err);
          this.errorMessage = 'Failed to create department. Please try again.';
          this.isLoading = false;
          this.setFormControlsDisabled(false);
          this.clearMessages();
        },
      });
    }
  }

  // 🔹 EDIT
  onEdit(dept: DepartmentModel) {
    this.isEditMode = true;
    this.selectedDepartmentId = dept.department_id!;

    this.departmentForm.patchValue({
      department_name: dept.department_name,
      description: dept.description,
    });
  }

  // 🔹 DELETE
  onDelete(id: number) {
    if (confirm('Are you sure you want to delete this department?')) {
      this.isLoading = true;
      this.setFormControlsDisabled(true);
      this.departmentService.deleteDepartment(id).subscribe({
        next: () => {
          this.successMessage = 'Department deleted successfully!';
          this.setFormControlsDisabled(false);
          this.loadDepartments();
          this.clearMessages();
        },
        error: (err) => {
          console.error('Failed to delete department:', err);
          this.errorMessage = 'Failed to delete department. Please try again.';
          this.isLoading = false;
          this.setFormControlsDisabled(false);
          this.clearMessages();
        },
      });
    }
  }

  resetForm() {
    this.departmentForm.reset();
    this.isEditMode = false;
    this.selectedDepartmentId = null;
  }

  clearMessages() {
    setTimeout(() => {
      this.successMessage = '';
      this.errorMessage = '';
    }, 3000);
  }
}
