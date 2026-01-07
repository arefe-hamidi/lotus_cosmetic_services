# API App Structure

ساختار سازمان‌یافته و تمیز API app

## 📁 ساختار فایل‌ها

```
api/
├── __init__.py
├── apps.py
│
├── models/                # Models
│   ├── __init__.py
│   ├── role.py           # Role model
│   └── user_role.py      # UserRole model
│
├── admin/                 # Admin interfaces
│   ├── __init__.py
│   └── role_admin.py      # Role و UserRole admin
│
├── serializers/           # Serializers
│   ├── __init__.py
│   ├── auth.py           # Authentication serializers
│   ├── user.py           # User profile serializers
│   └── roles.py          # Role serializers
│
├── urls/                  # URL routing
│   ├── __init__.py       # Main URL config
│   ├── auth_urls.py      # Authentication endpoints
│   └── role_urls.py      # Role management endpoints
│
├── views/                 # View functions and classes
│   ├── __init__.py
│   ├── authentication.py # Authentication views
│   └── roles.py          # Role management views
│
└── migrations/            # Database migrations
```

## 📂 توضیحات بخش‌ها

### Models (`models/`)

- `role.py`: مدل `Role` برای نقش‌ها
- `user_role.py`: مدل `UserRole` برای ارتباط Many-to-Many بین User و Role

### Admin (`admin/`)

- `role_admin.py`: Admin interface برای Role و UserRole

### Serializers (`serializers/`)

- `auth.py`:
  - `UserRegistrationSerializer`
  - `UserLoginSerializer`
  - `PasswordChangeSerializer`
- `user.py`:
  - `UserProfileSerializer`
  - `UserUpdateSerializer`
- `roles.py`:
  - `RoleSerializer`
  - `UserRoleSerializer`

### Views (`views/`)

- `health.py`: Health check و protected endpoint
- `authentication.py`: Register, Login, Logout, Profile, Password Change
- `roles.py`: Role management views

### URLs (`urls/`)

- `health_urls.py`: `/api/health/`, `/api/protected/`
- `auth_urls.py`: `/api/auth/*`
- `role_urls.py`: `/api/roles/*`, `/api/users/*/roles/*`

## 🔗 Endpoint ها

### Health & Test

- `GET /api/health/` - Health check
- `GET /api/protected/` - Protected endpoint test

### Authentication

- `POST /api/auth/register/` - ثبت نام
- `POST /api/auth/login/` - ورود
- `POST /api/auth/logout/` - خروج
- `GET /api/auth/profile/` - دریافت پروفایل
- `PUT /api/auth/profile/` - بروزرسانی پروفایل
- `POST /api/auth/password/change/` - تغییر رمز عبور
- `POST /api/auth/token/refresh/` - تازه‌سازی Token
- `POST /api/auth/token/verify/` - بررسی Token

### Role Management (نیاز به نقش admin)

- `GET /api/roles/` - لیست نقش‌ها
- `POST /api/roles/` - ایجاد نقش
- `GET /api/roles/<id>/` - جزئیات نقش
- `PUT /api/roles/<id>/` - بروزرسانی نقش
- `DELETE /api/roles/<id>/` - حذف نقش
- `GET /api/users/<user_id>/roles/` - نقش‌های کاربر
- `POST /api/users/<user_id>/roles/` - اضافه کردن نقش
- `DELETE /api/users/<user_id>/roles/<role_id>/` - حذف نقش

## 📝 مزایای ساختار جدید

1. **سازمان‌دهی بهتر**: هر بخش در فایل خودش
2. **قابلیت نگهداری**: پیدا کردن و تغییر کد آسان‌تر
3. **مقیاس‌پذیری**: اضافه کردن feature های جدید راحت‌تر
4. **خوانایی بهتر**: فایل‌های کوچک‌تر و واضح‌تر
5. **جدا سازی Concerns**: هر فایل مسئولیت مشخص دارد

## 🔄 Import ها

تمام import ها از طریق `__init__.py` انجام می‌شود:

```python
# در views
from ..serializers import UserRegistrationSerializer

# در urls
from ..views import user_register
```

## 📚 مستندات بیشتر

- [Authentication Documentation](../docs/auth/)
- [Role Management Guide](../docs/postman/ROLE_MANAGEMENT_GUIDE.md)
- [CORS Setup](../docs/CORS_SETUP.md)
