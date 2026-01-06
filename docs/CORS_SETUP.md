# CORS Configuration Guide

راهنمای تنظیم CORS برای ارتباط Frontend (پورت 3000) با Backend (پورت 8000)

## مشکل

وقتی از Frontend (مثلاً React/Next.js روی پورت 3000) به Backend Django (پورت 8000) درخواست می‌دهید، خطای CORS دریافت می‌کنید:

```
Access to fetch at 'http://127.0.0.1:8000/api/auth/login/' from origin 'http://localhost:3000'
has been blocked by CORS policy: The request client is not a secure context and the resource
is on a more-private address space.
```

## راه‌حل

CORS برای پروژه تنظیم شده است و درخواست‌ها از پورت 3000 مجاز هستند.

## تنظیمات انجام شده

### 1. نصب django-cors-headers

```bash
pip install django-cors-headers
```

### 2. اضافه شدن به INSTALLED_APPS

```python
INSTALLED_APPS = [
    ...
    'corsheaders',
    ...
]
```

### 3. اضافه شدن Middleware

```python
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # باید در ابتدا باشد
    ...
]
```

### 4. تنظیمات CORS

```python
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]
```

## استفاده در Frontend

### JavaScript/React Example

```javascript
// Login example
const login = async (username, password) => {
  const response = await fetch("http://127.0.0.1:8000/api/auth/login/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "include", // برای Cookie ها
    body: JSON.stringify({
      username: username,
      password: password,
    }),
  });

  const data = await response.json();

  if (data.tokens) {
    // ذخیره Token
    localStorage.setItem("access_token", data.tokens.access);
    localStorage.setItem("refresh_token", data.tokens.refresh);
  }

  return data;
};

// استفاده از Token در Request های بعدی
const getProfile = async () => {
  const token = localStorage.getItem("access_token");

  const response = await fetch("http://127.0.0.1:8000/api/auth/profile/", {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    credentials: "include",
  });

  return await response.json();
};
```

### Axios Example

```javascript
import axios from "axios";

// تنظیم Base URL
const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api",
  withCredentials: true, // برای Cookie ها
});

// اضافه کردن Token به Header
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Login
const login = async (username, password) => {
  const response = await api.post("/auth/login/", {
    username,
    password,
  });

  if (response.data.tokens) {
    localStorage.setItem("access_token", response.data.tokens.access);
    localStorage.setItem("refresh_token", response.data.tokens.refresh);
  }

  return response.data;
};

// Get Profile
const getProfile = async () => {
  const response = await api.get("/auth/profile/");
  return response.data;
};
```

## افزودن Origin های جدید

اگر می‌خواهید Origin های دیگری را اضافه کنید:

### روش 1: از Environment Variable

```bash
# در .env
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001,https://yourdomain.com
```

### روش 2: مستقیماً در settings.py

```python
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'http://localhost:3001',
    'https://yourdomain.com',
]
```

## برای Development (توسعه)

اگر می‌خواهید همه Origin ها را مجاز کنید (فقط برای Development):

```python
# ⚠️ فقط برای Development!
CORS_ALLOW_ALL_ORIGINS = True
```

**⚠️ هشدار**: هرگز این تنظیم را در Production استفاده نکنید!

## تست CORS

### با cURL

```bash
# تست Preflight Request
curl -X OPTIONS http://127.0.0.1:8000/api/health/ \
  -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: GET" \
  -v

# باید Header های CORS را در Response ببینید
```

### با Browser Console

```javascript
fetch("http://127.0.0.1:8000/api/health/", {
  method: "GET",
  headers: {
    "Content-Type": "application/json",
  },
})
  .then((response) => response.json())
  .then((data) => console.log(data))
  .catch((error) => console.error("Error:", error));
```

## عیب‌یابی

### مشکل: هنوز CORS error می‌گیرم

1. مطمئن شوید سرور Django را restart کرده‌اید
2. بررسی کنید که `corsheaders.middleware.CorsMiddleware` در ابتدای MIDDLEWARE است
3. بررسی کنید که Origin در `CORS_ALLOWED_ORIGINS` وجود دارد

### مشکل: Cookie ها ارسال نمی‌شوند

- مطمئن شوید `CORS_ALLOW_CREDENTIALS = True` است
- در Frontend از `credentials: 'include'` استفاده کنید

### مشکل: Authorization Header ارسال نمی‌شود

- بررسی کنید که `authorization` در `CORS_ALLOW_HEADERS` وجود دارد
- در Frontend Header را به درستی تنظیم کنید

## Production Settings

برای Production، تنظیمات امن‌تری استفاده کنید:

```python
# Production CORS Settings
CORS_ALLOWED_ORIGINS = [
    'https://yourdomain.com',
    'https://www.yourdomain.com',
]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = False  # همیشه False در Production
```

## نکات امنیتی

1. **هرگز `CORS_ALLOW_ALL_ORIGINS = True` را در Production استفاده نکنید**
2. **فقط Origin های مورد اعتماد را در `CORS_ALLOWED_ORIGINS` اضافه کنید**
3. **در Production از HTTPS استفاده کنید**
4. **Token ها را در localStorage یا secure cookie ذخیره کنید**
