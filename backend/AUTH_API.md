# Authentication API

Session cookies with CSRF protection. No token is stored in `localStorage`.

| Method | URL | Body | Success |
|---|---|---|---|
| GET | `/api/auth/csrf/` | | 200 `{"csrfToken": "..."}` |
| POST | `/api/auth/register/` | `username`, `email`, `password`, `country` (optional) | 201 user, logged in |
| POST | `/api/auth/login/` | `username`, `password` | 200 user |
| POST | `/api/auth/logout/` | | 204 |
| GET | `/api/auth/me/` | | 200 user |

A user is `{"id", "username", "email", "country"}`.

Errors: 400 invalid data or credentials, 403 not logged in or bad CSRF token,
429 too many attempts (login: 10 per minute, register: 20 per hour).

New API views require a logged-in user by default. Public views must set
`permission_classes = [AllowAny]`.

## Frontend usage

- Use the same host name for both servers: `http://localhost:5173` with
  `http://localhost:8000`. Mixing `localhost` and `127.0.0.1` breaks cookies.
- Send every request with `credentials: "include"`.
- Before a POST, PUT, PATCH or DELETE, get a token and send it in the `X-CSRFToken` header.
  Get a new one after login, registration and logout.

```ts
const API = "http://localhost:8000/api";

async function apiPost(path: string, body?: unknown) {
  const csrf = await fetch(`${API}/auth/csrf/`, { credentials: "include" });
  const { csrfToken } = await csrf.json();
  return fetch(`${API}${path}`, {
    method: "POST",
    credentials: "include",
    headers: { "Content-Type": "application/json", "X-CSRFToken": csrfToken },
    body: body ? JSON.stringify(body) : undefined,
  });
}
```

On app start, call `/auth/me/` with `credentials: "include"` to check if the user is logged in.

## Not covered yet

Password reset, password change, account deletion and email verification.
The throttle uses Django's local memory cache, so it is only basic protection.
Production also needs HTTPS and secure cookie settings.

## Tests

The database user needs permission to create the test database
(`ALTER ROLE user1 CREATEDB;`, run as `postgres`). Then, from `backend/`:

```powershell
python manage.py test accounts
```
