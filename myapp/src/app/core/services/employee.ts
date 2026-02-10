import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { EmployeeModel } from '../models/class/employee.model';

@Injectable({
  providedIn: 'root',
})
export class Employee {
  private employees: EmployeeModel[] = [];
  private employeesSubject = new BehaviorSubject<EmployeeModel[]>([]);
  employees$ = this.employeesSubject.asObservable();
  private idCounter = 1;

  constructor() {
    // Initialize with some sample data
    this.employees = [];
    this.employeesSubject.next(this.employees);
  }

  // GET all employees
  getEmployees(): Observable<EmployeeModel[]> {
    return this.employees$;
  }

  // GET single employee by id
  getEmployeeById(id: number): EmployeeModel | undefined {
    return this.employees.find((emp) => emp.id === id);
  }

  // CREATE new employee
  createEmployee(employee: EmployeeModel): EmployeeModel {
    employee.id = this.idCounter++;
    this.employees.push(employee);
    this.employeesSubject.next([...this.employees]);
    return employee;
  }

  // UPDATE employee
  updateEmployee(id: number, updatedEmployee: EmployeeModel): boolean {
    const index = this.employees.findIndex((emp) => emp.id === id);
    if (index !== -1) {
      this.employees[index] = { ...updatedEmployee, id };
      this.employeesSubject.next([...this.employees]);
      return true;
    }
    return false;
  }

  // DELETE employee
  deleteEmployee(id: number): boolean {
    const index = this.employees.findIndex((emp) => emp.id === id);
    if (index !== -1) {
      this.employees.splice(index, 1);
      this.employeesSubject.next([...this.employees]);
      return true;
    }
    return false;
  }
}
