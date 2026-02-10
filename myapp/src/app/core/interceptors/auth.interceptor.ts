import { Injectable } from '@angular/core';
import {
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpInterceptor,
  HttpErrorResponse,
} from '@angular/common/http';
import { Observable, throwError, BehaviorSubject, of } from 'rxjs';
import { catchError, filter, switchMap, take } from 'rxjs/operators';
import { AuthService } from '../services/auth.service';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  private isRefreshing = false;
  private refreshSubject: BehaviorSubject<string | null> = new BehaviorSubject<string | null>(null);

  constructor(private authService: AuthService) {}

  intercept(request: HttpRequest<unknown>, next: HttpHandler): Observable<HttpEvent<unknown>> {
    const token = this.authService.getAccessToken();

    let authReq = request;
    if (token) {
      authReq = this.addTokenHeader(request, token);
      console.log('[✓ Auth Interceptor] Bearer token added - Request:', request.url);
    } else {
      console.warn('[✗ Auth Interceptor] No token in localStorage - Request URL:', request.url);
    }

    return next.handle(authReq).pipe(
      catchError((error: HttpErrorResponse) => {
        if (error.status === 401) {
          // Attempt to refresh token
          return this.handle401Error(authReq, next);
        }

        if (error.status === 403) {
          // Forbidden
          this.authService.logout();
          return throwError(() => error);
        }

        return throwError(() => error);
      }),
    );
  }

  private addTokenHeader(request: HttpRequest<any>, token: string): HttpRequest<any> {
    return request.clone({ setHeaders: { Authorization: `Bearer ${token}` } });
  }

  private handle401Error(request: HttpRequest<any>, next: HttpHandler) {
    if (!this.isRefreshing) {
      this.isRefreshing = true;
      this.refreshSubject.next(null);

      return this.authService.refreshToken().pipe(
        switchMap((newToken: string) => {
          this.isRefreshing = false;
          if (newToken) {
            this.refreshSubject.next(newToken);
            return next.handle(this.addTokenHeader(request, newToken));
          }
          // Refresh failed
          this.authService.logout();
          return throwError(() => new Error('Refresh token failed'));
        }),
        catchError((err) => {
          this.isRefreshing = false;
          this.authService.logout();
          return throwError(() => err);
        }),
      );
    } else {
      return this.refreshSubject.pipe(
        filter((token) => token != null),
        take(1),
        switchMap((token) => next.handle(this.addTokenHeader(request, token!))),
      );
    }
  }
}
