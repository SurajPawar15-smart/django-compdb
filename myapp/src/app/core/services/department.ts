import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment.development';
import { DepartmentModel } from '../models/class/department.model';
import { Constant } from '../Constants/Constant';

@Injectable({
  providedIn: 'root',
})
export class Department {
  constructor(private http: HttpClient) {}

  getAllDepartments() {
    return this.http.get(environment.API_URL + Constant.API_METHODS.DEPARTMENT.GET_ALL);
  }

  getDepartmentById(id: number) {
    return this.http.get(
      `${environment.API_URL}${Constant.API_METHODS.DEPARTMENT.GET_DEPARTMENT_BY_ID}${id}`,
    );
  }

  createNewDepartment(obj: DepartmentModel) {
    debugger;
    return this.http.post(
      environment.API_URL + Constant.API_METHODS.DEPARTMENT.NEW_DEPARTMENT,
      obj,
    );
  }

  deleteDepartment(id: number) {
    return this.http.delete(
      `${environment.API_URL}${Constant.API_METHODS.DEPARTMENT.GET_ALL}/${id}/`,
    );
  }
}
