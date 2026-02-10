import { Component, inject } from '@angular/core';
import { UserLogin } from '../../core/models/class/user.model';
import { User } from '../../core/services/user';
import { Router, RouterLink, RouterOutlet } from '@angular/router';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-login',
  imports: [RouterOutlet, RouterLink, FormsModule],
  templateUrl: './login.html',
  styleUrl: './login.css',
})
export class Login {
  // loginObj: UserLogin = new UserLogin();

  loginObj: UserLogin = {
    password: '',
    username: '',
  };
  userService = inject(User);
  router = inject(Router);

  onLogin() {
    debugger;
    this.userService.onLogin(this.loginObj).subscribe({
      next: (response: any) => {
        // Store user data
        localStorage.setItem('LoginUser', JSON.stringify(response));

        // Store access token from response (handle multiple field names)
        const token =
          response.access || response.access_token || response.token || response.accessToken;
        if (token) {
          localStorage.setItem('access_token', token);
          console.log('Token stored:', token.substring(0, 20) + '...');
        } else {
          console.warn('No token found in login response:', response);
        }

        // Store refresh token if present
        const refresh = response.refresh || response.refresh_token || response.refreshToken;
        if (refresh) {
          localStorage.setItem('refresh_token', refresh);
        }

        // Navigate to departments data page
        this.router.navigateByUrl('/departmentsdata');
      },
      error: (err: any) => {
        alert('Wrong user and password');
      },
    });
  }
}
