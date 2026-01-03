# Authentication API Quick Reference

## Available Endpoints

| Endpoint | Method | Auth Required | Description |
|----------|--------|---------------|-------------|
| `/api/auth/register/` | POST | No | Register a new user |
| `/api/auth/login/` | POST | No | Login and create session |
| `/api/auth/logout/` | POST | Yes | Logout current user |
| `/api/auth/profile/` | GET | Yes | Get user profile |
| `/api/auth/profile/` | PUT | Yes | Update user profile |
| `/api/auth/password/change/` | POST | Yes | Change password |

## Quick Test Commands

### 1. Register a User
```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "email": "user@example.com",
    "password": "securepass123",
    "password_confirm": "securepass123"
  }'
```

### 2. Login
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{
    "username": "newuser",
    "password": "securepass123"
  }'
```

### 3. Get Profile (after login)
```bash
curl -X GET http://127.0.0.1:8000/api/auth/profile/ \
  -b cookies.txt
```

### 4. Update Profile
```bash
curl -X PUT http://127.0.0.1:8000/api/auth/profile/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "email": "newemail@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

### 5. Change Password
```bash
curl -X POST http://127.0.0.1:8000/api/auth/password/change/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "old_password": "securepass123",
    "new_password": "newpass123",
    "new_password_confirm": "newpass123"
  }'
```

### 6. Logout
```bash
curl -X POST http://127.0.0.1:8000/api/auth/logout/ \
  -b cookies.txt
```

## Postman Setup

1. **Create Environment**: 
   - Variable: `base_url` = `http://127.0.0.1:8000`

2. **Register Request**:
   - Method: POST
   - URL: `{{base_url}}/api/auth/register/`
   - Body (raw JSON):
     ```json
     {
       "username": "testuser",
       "email": "test@example.com",
       "password": "testpass123",
       "password_confirm": "testpass123"
     }
     ```

3. **Login Request**:
   - Method: POST
   - URL: `{{base_url}}/api/auth/login/`
   - Body (raw JSON):
     ```json
     {
       "username": "testuser",
       "password": "testpass123"
     }
     ```
   - Tests Tab (to save session):
     ```javascript
     pm.environment.set("session_id", pm.cookies.get("sessionid"));
     ```

4. **Profile Requests** (GET/PUT):
   - Method: GET or PUT
   - URL: `{{base_url}}/api/auth/profile/`
   - Headers:
     - Cookie: `sessionid={{session_id}}`
   - Or use Basic Auth with username/password

## Response Format

All endpoints return JSON with this structure:

**Success**:
```json
{
  "status": "success",
  "message": "Persian message",
  "user": { ... }  // if applicable
}
```

**Error**:
```json
{
  "status": "error",
  "message": "Error message",  // or
  "errors": { ... }  // field-specific errors
}
```

## Notes

- All messages are in Persian (Farsi)
- Session authentication is used by default
- Passwords must meet Django's validation requirements
- Email is required for registration
- Username must be unique

