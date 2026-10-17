# Security Before / After

## Password Storage

### Before

Passwords were stored directly in plaintext.

Example:

```text
demo1234

### After
Passwords are hashed using Argon2

Example:
$argon2id$....

Authentication

Before
Login returned only user information.
There was no session or token.

After
Successful login issues a time-limited JWT bearer token.

Authorization

Before
Any client could access the users endpoint.

After
The users endpoint requires:
1. Valid JWT authentication
2. Administrator privileges

Brute-Force Protection

Before
Unlimited login attempts.

After
Authentication attempts are rate limited.

Security Headers

Before
No explicit defensive HTTP headers.

After
The API sends:
- X-Content-Type-Options
- X-Frame-Options
- Referrer-Policy
- Permissions-Policy

Secrets Management

Before
No dedicated secrets configuration.

After
JWT secrets are stored in .env and excluded from Git.

Logging

Before
Authentication events were not logged.

After
The API logs:
- Successful authentication
- Failed authentication
- Unauthorized administrative access
Result
The project demonstrates the transformation of an intentionally insecure local REST API into a hardened API with modern defensive controls.
