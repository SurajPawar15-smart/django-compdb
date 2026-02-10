import { Routes } from '@angular/router';
import { Login } from './pages/login/login';
import { Layout } from './pages/layout/layout';
import { EmployeesData } from './pages/employees-data/employees-data';
import { DepartmentsData } from './pages/departments-data/departments-data';
import { PageNotFound } from './pages/page-not-found/page-not-found';
import { AuthGuard } from './core/gurads/auth.guard';

export const routes: Routes = [
  { path: '', redirectTo: 'login', pathMatch: 'full' },
  { path: 'login', component: Login },
  {
    path: '',
    component: Layout,
    canActivate: [AuthGuard],

    children: [
      { path: 'employeesdata', component: EmployeesData },
      { path: 'departmentsdata', component: DepartmentsData },
    ],
  },
  // { path: '**', component: PageNotFound },
];
