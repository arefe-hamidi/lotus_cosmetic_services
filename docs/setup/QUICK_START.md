# Quick Start Guide

## Running the Project

### 1. Start the Development Server

```bash
cd /Users/arefeh_hamidi/Documents/Lotus/lotus_cosmetic_services
./venv/bin/python manage.py runserver
```

The server will start at: **http://127.0.0.1:8000**

### 2. Access Points

- **Admin Panel**: http://127.0.0.1:8000/admin/
- **API Health Check**: http://127.0.0.1:8000/api/health/
- **API Protected**: http://127.0.0.1:8000/api/protected/

## Postman Quick Setup

### Method 1: Import Collection (Recommended)

1. Open Postman
2. Create a new Collection: "Lotus Cosmetic Services"
3. Add these requests:

#### Request 1: Health Check
- **Method**: `GET`
- **URL**: `http://127.0.0.1:8000/api/health/`
- **Auth**: No Auth
- **Expected**: 200 OK with JSON response

#### Request 2: Protected Endpoint
- **Method**: `GET`
- **URL**: `http://127.0.0.1:8000/api/protected/`
- **Auth**: Basic Auth (use your Django superuser credentials)
- **Expected**: 200 OK if authenticated, 403 if not

### Method 2: Using Postman Environment

1. Create Environment: "Lotus Local"
2. Add variable: `base_url` = `http://127.0.0.1:8000`
3. Use in requests: `{{base_url}}/api/health/`

## Testing in Browser

You can also test the public endpoint directly in your browser:
- http://127.0.0.1:8000/api/health/

## Creating a Superuser (If Needed)

```bash
./venv/bin/python manage.py createsuperuser
```

Then use these credentials in Postman's Basic Auth for protected endpoints.

## Stop the Server

Press `Ctrl+C` in the terminal where the server is running, or find and kill the process.

