# JWT Authentication Guide

این راهنما نحوه استفاده از JWT Token برای احراز هویت در API را توضیح می‌دهد.

## نصب و تنظیمات

JWT Authentication با استفاده از `djangorestframework-simplejwt` پیاده‌سازی شده است.

### تنظیمات JWT

- **Access Token Lifetime**: 1 ساعت
- **Refresh Token Lifetime**: 7 روز
- **Token Rotation**: فعال (با هر refresh، token جدید تولید می‌شود)
- **Algorithm**: HS256

## Endpoint های JWT

### 1. Login (دریافت Token)

**Endpoint**: `POST /api/auth/login/`

**Request Body**:

```json
{
  "username": "testuser",
  "password": "testpass123"
}
```

**Response** (200 OK):

```json
{
  "status": "success",
  "message": "ورود با موفقیت انجام شد.",
  "tokens": {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  },
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "first_name": "Test",
    "last_name": "User"
  }
}
```

### 2. Refresh Token (تازه‌سازی Token)

**Endpoint**: `POST /api/auth/token/refresh/`

**Request Body**:

```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response** (200 OK):

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### 3. Verify Token (بررسی اعتبار Token)

**Endpoint**: `POST /api/auth/token/verify/`

**Request Body**:

```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response** (200 OK):

```json
{}
```

**Error Response** (401 Unauthorized):

```json
{
  "detail": "Token is invalid or expired"
}
```

## نحوه استفاده در Request ها

### استفاده در Postman

1. **Login کنید** و `access` token را کپی کنید
2. در Request های محافظت شده:
   - به تب **Authorization** بروید
   - Type را **Bearer Token** انتخاب کنید
   - Token را در فیلد Token وارد کنید

### استفاده در cURL

```bash
# Login و دریافت token
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'

# استفاده از token در Request
curl -X GET http://127.0.0.1:8000/api/auth/profile/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

### استفاده در JavaScript (Fetch API)

```javascript
// Login
const loginResponse = await fetch("http://127.0.0.1:8000/api/auth/login/", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    username: "testuser",
    password: "testpass123",
  }),
});

const loginData = await loginResponse.json();
const accessToken = loginData.tokens.access;

// استفاده از token در Request های بعدی
const profileResponse = await fetch("http://127.0.0.1:8000/api/auth/profile/", {
  method: "GET",
  headers: {
    Authorization: `Bearer ${accessToken}`,
  },
});
```

## مثال کامل در Postman

### Step 1: Login

- Method: `POST`
- URL: `{{base_url}}/api/auth/login/`
- Body (raw JSON):
  ```json
  {
    "username": "testuser",
    "password": "testpass123"
  }
  ```
- Tests Tab (برای ذخیره token):
  ```javascript
  if (pm.response.code === 200) {
    var jsonData = pm.response.json();
    pm.environment.set("access_token", jsonData.tokens.access);
    pm.environment.set("refresh_token", jsonData.tokens.refresh);
  }
  ```

### Step 2: استفاده از Token

- Method: `GET`
- URL: `{{base_url}}/api/auth/profile/`
- Authorization Tab:
  - Type: `Bearer Token`
  - Token: `{{access_token}}`

### Step 3: Refresh Token

- Method: `POST`
- URL: `{{base_url}}/api/auth/token/refresh/`
- Body (raw JSON):
  ```json
  {
    "refresh": "{{refresh_token}}"
  }
  ```
- Tests Tab:
  ```javascript
  if (pm.response.code === 200) {
    var jsonData = pm.response.json();
    pm.environment.set("access_token", jsonData.access);
  }
  ```

## نکات مهم

1. **Access Token**: برای دسترسی به API استفاده می‌شود (عمر: 1 ساعت)
2. **Refresh Token**: برای دریافت Access Token جدید استفاده می‌شود (عمر: 7 روز)
3. **Token Rotation**: با هر refresh، یک Refresh Token جدید نیز تولید می‌شود
4. **Header Format**: همیشه از `Authorization: Bearer <token>` استفاده کنید
5. **Token Expiry**: اگر Access Token منقضی شد، از Refresh Token برای دریافت token جدید استفاده کنید

## خطاهای رایج

### 401 Unauthorized - Token is invalid or expired

- **علت**: Token منقضی شده یا نامعتبر است
- **راه حل**: از Refresh Token برای دریافت Access Token جدید استفاده کنید

### 401 Unauthorized - Authentication credentials were not provided

- **علت**: Header Authorization ارسال نشده
- **راه حل**: Header `Authorization: Bearer <token>` را اضافه کنید

### 403 Forbidden

- **علت**: Token معتبر است اما کاربر دسترسی ندارد
- **راه حل**: بررسی کنید که کاربر دسترسی لازم را دارد

## مقایسه با Session Authentication

| ویژگی                 | JWT Token | Session Cookie |
| --------------------- | --------- | -------------- |
| Stateless             | ✅        | ❌             |
| مناسب برای Mobile App | ✅        | ❌             |
| مناسب برای SPA        | ✅        | ⚠️             |
| مناسب برای Web App    | ⚠️        | ✅             |
| نیاز به Storage       | ❌        | ✅             |

## امنیت

1. **HTTPS**: در Production همیشه از HTTPS استفاده کنید
2. **Token Storage**: Token ها را در localStorage یا secure cookie ذخیره کنید
3. **Token Expiry**: Token ها به صورت خودکار منقضی می‌شوند
4. **Token Rotation**: با هر refresh، token قبلی باطل می‌شود
