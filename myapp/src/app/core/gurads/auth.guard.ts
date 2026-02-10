import { Injectable } from '@angular/core';
import { Router, CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';

@Injectable({
  providedIn: 'root',
})
export class AuthGuard implements CanActivate {
  constructor(private router: Router) {}

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): boolean {
    const token = localStorage.getItem('access_token');

    if (token) {
      // Token exists, allow access
      return true;
    } else {
      // No token, redirect to login
      this.router.navigateByUrl('/login');
      return false;
    }
  }
}
