# Authentication Documentation

این بخش شامل تمام مستندات مربوط به احراز هویت (Authentication) است.

## فهرست مطالب

### 📚 مستندات اصلی

1. **[JWT Authentication Guide](./JWT_AUTHENTICATION.md)**
   - راهنمای کامل استفاده از JWT Token
   - نحوه Login و دریافت Token
   - Refresh Token و Verify Token
   - مثال‌های استفاده در Postman و JavaScript

2. **[API Authentication Documentation](./API_AUTH_DOCUMENTATION.md)**
   - مستندات کامل تمام Endpoint های احراز هویت
   - Register, Login, Logout
   - Profile Management
   - Password Change
   - مثال‌های Request/Response

3. **[Quick Reference](./AUTH_API_QUICK_REFERENCE.md)**
   - مرجع سریع دستورات
   - مثال‌های cURL
   - راهنمای سریع Postman

## Endpoint های احراز هویت

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/auth/register/` | POST | ثبت نام کاربر جدید |
| `/api/auth/login/` | POST | ورود و دریافت JWT Token |
| `/api/auth/logout/` | POST | خروج کاربر |
| `/api/auth/profile/` | GET | دریافت پروفایل کاربر |
| `/api/auth/profile/` | PUT | بروزرسانی پروفایل |
| `/api/auth/password/change/` | POST | تغییر رمز عبور |
| `/api/auth/token/refresh/` | POST | تازه‌سازی Access Token |
| `/api/auth/token/verify/` | POST | بررسی اعتبار Token |

## شروع سریع

### 1. ثبت نام
```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "securepass123",
    "password_confirm": "securepass123"
  }'
```

### 2. ورود و دریافت Token
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "securepass123"
  }'
```

### 3. استفاده از Token
```bash
curl -X GET http://127.0.0.1:8000/api/auth/profile/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## ویژگی‌ها

- ✅ JWT Token Authentication
- ✅ Session Authentication (برای سازگاری)
- ✅ Token Refresh
- ✅ Token Verification
- ✅ Password Validation
- ✅ User Profile Management

## امنیت

- Access Token: 1 ساعت اعتبار
- Refresh Token: 7 روز اعتبار
- Token Rotation: فعال
- Password Validation: Django validators

