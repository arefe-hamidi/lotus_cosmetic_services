# Postman Setup Guide

This guide explains how to test the Lotus Cosmetic Services API using Postman.

## Prerequisites

1. Make sure the Django development server is running:
   ```bash
   ./venv/bin/python manage.py runserver
   ```
   The server will be available at: `http://127.0.0.1:8000`

## API Endpoints

### 1. Health Check (Public Endpoint)
- **URL**: `http://127.0.0.1:8000/api/health/`
- **Method**: `GET`
- **Authentication**: None required (public endpoint)
- **Permission**: `AllowAnyWithAPIKey`

### 2. Protected Endpoint
- **URL**: `http://127.0.0.1:8000/api/protected/`
- **Method**: `GET`
- **Authentication**: Required (Session or Token)
- **Permission**: `IsAuthenticatedWithAPIKey`

## Setting Up Postman

### Step 1: Create a New Collection

1. Open Postman
2. Click "New" → "Collection"
3. Name it "Lotus Cosmetic Services API"
4. Click "Create"

### Step 2: Add Health Check Request

1. Click "Add Request" in your collection
2. Name it "Health Check"
3. Set the method to `GET`
4. Enter the URL: `http://127.0.0.1:8000/api/health/`
5. Click "Send"
6. You should receive a response:
   ```json
   {
       "status": "success",
       "message": "API is running",
       "version": "1.0.0"
   }
   ```

### Step 3: Add Protected Endpoint Request

1. Click "Add Request" in your collection
2. Name it "Protected Endpoint"
3. Set the method to `GET`
4. Enter the URL: `http://127.0.0.1:8000/api/protected/`

#### Option A: Using Session Authentication (Recommended for Testing)

1. Go to the "Authorization" tab
2. Select "No Auth" for now (we'll set up authentication)
3. First, you need to log in via the Django admin or create a session

#### Option B: Using Basic Auth (For Testing)

1. Go to the "Authorization" tab
2. Select "Basic Auth"
3. Enter your Django superuser credentials
4. Click "Send"

### Step 4: Create a Superuser (If Not Already Created)

If you haven't created a superuser yet, run:

```bash
./venv/bin/python manage.py createsuperuser
```

Then use these credentials in Postman's Basic Auth.

### Step 5: Using Session Cookie Authentication

1. First, log in to Django admin: `http://127.0.0.1:8000/admin/`
2. Open browser DevTools (F12) → Application/Storage → Cookies
3. Copy the `sessionid` cookie value
4. In Postman, go to the "Headers" tab
5. Add a new header:
   - Key: `Cookie`
   - Value: `sessionid=YOUR_SESSION_ID_HERE`

## Postman Collection Variables

You can set up environment variables in Postman for easier management:

1. Click the eye icon (👁️) in the top right
2. Click "Add" to create a new environment
3. Add variables:
   - `base_url`: `http://127.0.0.1:8000`
   - `api_key`: (will be used when API key validation is implemented)

4. Update your requests to use: `{{base_url}}/api/health/`

## Testing the Endpoints

### Test Health Check:
```
GET {{base_url}}/api/health/
```

Expected Response (200 OK):
```json
{
    "status": "success",
    "message": "API is running",
    "version": "1.0.0"
}
```

### Test Protected Endpoint:
```
GET {{base_url}}/api/protected/
```

With Authentication - Expected Response (200 OK):
```json
{
    "status": "success",
    "message": "This is a protected endpoint",
    "user": "your_username"
}
```

Without Authentication - Expected Response (403 Forbidden):
```json
{
    "detail": "You do not have permission to perform this action."
}
```

## Troubleshooting

### Issue: Connection Refused
- **Solution**: Make sure the Django server is running on port 8000

### Issue: 404 Not Found
- **Solution**: Check that the URL path is correct: `/api/health/` or `/api/protected/`

### Issue: 403 Forbidden (Protected Endpoint)
- **Solution**: Make sure you're authenticated. Use Basic Auth or Session Cookie.

### Issue: CSRF Token Error
- **Solution**: For POST/PUT/DELETE requests, you may need to include CSRF token. For GET requests, this shouldn't be an issue.

## Next Steps

1. Implement API key validation in `utils/permissions.py`
2. Add more endpoints as you develop your application
3. Set up proper authentication tokens (JWT, etc.) if needed
4. Document your API endpoints using tools like drf-spectacular or drf-yasg

