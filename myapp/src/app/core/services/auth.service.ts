import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { Observable, of } from 'rxjs';
import { map, tap } from 'rxjs/operators';
import { environment } from '../../../environments/environment.development';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  constructor(
    private http: HttpClient,
    private router: Router,
  ) {}

  getAccessToken(): string | null {
    return localStorage.getItem('access_token');
  }

  getRefreshToken(): string | null {
    return localStorage.getItem('refresh_token') || localStorage.getItem('refresh');
  }

  setAccessToken(token: string) {
    localStorage.setItem('access_token', token);
  }

  setRefreshToken(token: string) {
    localStorage.setItem('refresh_token', token);
  }

  clearTokens() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('LoginUser');
  }

  logout() {
    this.clearTokens();
    this.router.navigateByUrl('/login');
  }

  // Call backend refresh endpoint and store new access token
  refreshToken(): Observable<string> {
    const refresh = this.getRefreshToken();
    if (!refresh) {
      return of('');
    }

    return this.http.post<any>(environment.API_URL + 'token/refresh/', { refresh }).pipe(
      map((res) => res.access || res.token || res.access_token),
      tap((newAccess) => {
        if (newAccess) this.setAccessToken(newAccess);
      }),
    );
  }
}
