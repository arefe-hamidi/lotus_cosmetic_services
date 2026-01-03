# Authentication API Documentation

This document describes all authentication endpoints available in the Lotus Cosmetic Services API.

## Base URL

```
http://127.0.0.1:8000/api/auth/
```

## Endpoints

### 1. User Registration

Register a new user account.

**Endpoint**: `POST /api/auth/register/`

**Permission**: Public (AllowAnyWithAPIKey)

**Request Body**:

```json
{
  "username": "string (required)",
  "email": "string (required)",
  "first_name": "string (optional)",
  "last_name": "string (optional)",
  "password": "string (required, min 8 characters)",
  "password_confirm": "string (required, must match password)"
}
```

**Example Request**:

```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "password": "securepass123",
    "password_confirm": "securepass123"
  }'
```

**Success Response** (201 Created):

```json
{
  "status": "success",
  "message": "کاربر با موفقیت ثبت نام شد.",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com"
  }
}
```

**Error Response** (400 Bad Request):

```json
{
  "status": "error",
  "errors": {
    "username": ["A user with that username already exists."],
    "password_confirm": ["رمز عبور و تأیید رمز عبور باید یکسان باشند."]
  }
}
```

---

### 2. User Login

Authenticate a user and create a session.

**Endpoint**: `POST /api/auth/login/`

**Permission**: Public (AllowAnyWithAPIKey)

**Request Body**:

```json
{
  "username": "string (required)",
  "password": "string (required)"
}
```

**Example Request**:

```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "securepass123"
  }'
```

**Success Response** (200 OK):

```json
{
  "status": "success",
  "message": "ورود با موفقیت انجام شد.",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

**Error Response** (401 Unauthorized):

```json
{
  "status": "error",
  "message": "نام کاربری یا رمز عبور اشتباه است."
}
```

**Error Response** (403 Forbidden - Account Inactive):

```json
{
  "status": "error",
  "message": "حساب کاربری غیرفعال است."
}
```

---

### 3. User Logout

Log out the current authenticated user.

**Endpoint**: `POST /api/auth/logout/`

**Permission**: Authenticated (IsAuthenticatedWithAPIKey)

**Authentication**: Required (Session or Basic Auth)

**Example Request**:

```bash
curl -X POST http://127.0.0.1:8000/api/auth/logout/ \
  -H "Cookie: sessionid=your_session_id"
```

**Success Response** (200 OK):

```json
{
  "status": "success",
  "message": "خروج با موفقیت انجام شد."
}
```

---

### 4. User Profile

Get or update the current user's profile.

**Endpoint**:

- `GET /api/auth/profile/` - Get profile
- `PUT /api/auth/profile/` - Update profile

**Permission**: Authenticated (IsAuthenticatedWithAPIKey)

**Authentication**: Required (Session or Basic Auth)

#### GET Profile

**Example Request**:

```bash
curl -X GET http://127.0.0.1:8000/api/auth/profile/ \
  -H "Cookie: sessionid=your_session_id"
```

**Success Response** (200 OK):

```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "date_joined": "2024-01-01T12:00:00Z",
  "last_login": "2024-01-02T10:30:00Z"
}
```

#### PUT Profile

**Request Body**:

```json
{
  "email": "string (optional)",
  "first_name": "string (optional)",
  "last_name": "string (optional)"
}
```

**Example Request**:

```bash
curl -X PUT http://127.0.0.1:8000/api/auth/profile/ \
  -H "Content-Type: application/json" \
  -H "Cookie: sessionid=your_session_id" \
  -d '{
    "email": "newemail@example.com",
    "first_name": "Jane",
    "last_name": "Smith"
  }'
```

**Success Response** (200 OK):

```json
{
  "status": "success",
  "message": "پروفایل با موفقیت بروزرسانی شد.",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "newemail@example.com",
    "first_name": "Jane",
    "last_name": "Smith",
    "date_joined": "2024-01-01T12:00:00Z",
    "last_login": "2024-01-02T10:30:00Z"
  }
}
```

---

### 5. Password Change

Change the current user's password.

**Endpoint**: `POST /api/auth/password/change/`

**Permission**: Authenticated (IsAuthenticatedWithAPIKey)

**Authentication**: Required (Session or Basic Auth)

**Request Body**:

```json
{
  "old_password": "string (required)",
  "new_password": "string (required, min 8 characters)",
  "new_password_confirm": "string (required, must match new_password)"
}
```

**Example Request**:

```bash
curl -X POST http://127.0.0.1:8000/api/auth/password/change/ \
  -H "Content-Type: application/json" \
  -H "Cookie: sessionid=your_session_id" \
  -d '{
    "old_password": "oldpass123",
    "new_password": "newpass123",
    "new_password_confirm": "newpass123"
  }'
```

**Success Response** (200 OK):

```json
{
  "status": "success",
  "message": "رمز عبور با موفقیت تغییر کرد."
}
```

**Error Response** (400 Bad Request):

```json
{
  "status": "error",
  "errors": {
    "old_password": ["رمز عبور فعلی اشتباه است."],
    "new_password_confirm": ["رمز عبور جدید و تأیید رمز عبور باید یکسان باشند."]
  }
}
```

---

## Authentication Methods

### Method 1: Session Authentication (Recommended for Web)

1. Login using `/api/auth/login/` endpoint
2. The response will set a session cookie
3. Include the cookie in subsequent requests:
   ```
   Cookie: sessionid=your_session_id
   ```

### Method 2: Basic Authentication (For API Testing)

1. In Postman, go to Authorization tab
2. Select "Basic Auth"
3. Enter username and password
4. Postman will automatically add the Authorization header

### Method 3: Session Cookie from Browser

1. Log in to Django admin: `http://127.0.0.1:8000/admin/`
2. Open browser DevTools → Application → Cookies
3. Copy the `sessionid` value
4. Use it in API requests:
   ```
   Cookie: sessionid=your_session_id
   ```

## Postman Collection Setup

### Environment Variables

Create a Postman environment with:

- `base_url`: `http://127.0.0.1:8000`
- `session_id`: (will be set after login)

### Request Examples

1. **Register** → Save `user.id` to variable
2. **Login** → Save `sessionid` cookie to `session_id` variable
3. **Get Profile** → Use `{{session_id}}` in Cookie header
4. **Update Profile** → Use `{{session_id}}` in Cookie header
5. **Change Password** → Use `{{session_id}}` in Cookie header
6. **Logout** → Use `{{session_id}}` in Cookie header

## Error Codes

- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication failed
- `403 Forbidden`: Permission denied or account inactive
- `404 Not Found`: Endpoint not found

## Notes

- All password fields must meet Django's password validation requirements
- Session cookies expire based on Django's `SESSION_COOKIE_AGE` setting
- Username and email must be unique
- Email field is required for registration
