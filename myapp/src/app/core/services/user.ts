import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environment.development';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root',
})
export class User {
  constructor(
    private http: HttpClient,
    private router: Router,
  ) {}

  onLogin(obj: any) {
    return this.http.post(environment.API_URL + 'login/', obj);
  }

  // Logout method
  onLogout() {
    // Clear localStorage
    localStorage.removeItem('access_token');
    localStorage.removeItem('LoginUser');

    // Navigate to login page
    this.router.navigateByUrl('/login');
  }

  // Check if user is authenticated
  isAuthenticated(): boolean {
    return !!localStorage.getItem('access_token');
  }

  // Get the stored access token
  getAccessToken(): string | null {
    return localStorage.getItem('access_token');
  }

  // Get the stored user data
  getLoggedInUser(): any {
    const userData = localStorage.getItem('LoginUser');
    return userData ? JSON.parse(userData) : null;
  }
}
