# Postman Documentation

این بخش شامل تمام فایل‌ها و راهنماهای مربوط به Postman است.

## فهرست مطالب

### 📚 مستندات

1. **[Postman Setup Guide](./POSTMAN_SETUP.md)**
   - راهنمای کامل تنظیم Postman
   - نحوه استفاده از Collection
   - تنظیم Environment Variables

2. **[Import Guide](./POSTMAN_IMPORT_GUIDE.md)**
   - راهنمای Import کردن Collection
   - راهنمای Import کردن Environment
   - نحوه استفاده

### 📦 فایل‌های Postman

1. **Collection**: `Lotus_Cosmetic_Services_API.postman_collection.json`
   - شامل تمام Endpoint های API
   - شامل Health Check و Authentication
   - تست‌های خودکار برای ذخیره Token

2. **Environment**: `Lotus_Local.postman_environment.json`
   - متغیرهای محیطی پیش‌فرض
   - base_url, session_id, tokens, etc.

## Import کردن در Postman

### Step 1: Import Collection
1. Postman را باز کنید
2. روی **Import** کلیک کنید
3. فایل `Lotus_Cosmetic_Services_API.postman_collection.json` را انتخاب کنید
4. روی **Import** کلیک کنید

### Step 2: Import Environment
1. دوباره روی **Import** کلیک کنید
2. فایل `Lotus_Local.postman_environment.json` را انتخاب کنید
3. روی **Import** کلیک کنید
4. Environment را روی **"Lotus Local"** تنظیم کنید

## استفاده از Collection

### 1. Health Check
- تست کنید که سرور در حال اجرا است

### 2. Register
- یک کاربر جدید ثبت نام کنید
- `user_id` و `username` به صورت خودکار ذخیره می‌شود

### 3. Login
- وارد شوید
- `access_token` و `refresh_token` به صورت خودکار ذخیره می‌شود
- `session_id` نیز ذخیره می‌شود (برای Session Auth)

### 4. استفاده از Endpoint های محافظت شده
- بعد از Login، Token به صورت خودکار در Header قرار می‌گیرد
- می‌توانید Profile, Update Profile, Change Password را تست کنید

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `base_url` | آدرس پایه API | `http://127.0.0.1:8000` |
| `access_token` | JWT Access Token | (به صورت خودکار پر می‌شود) |
| `refresh_token` | JWT Refresh Token | (به صورت خودکار پر می‌شود) |
| `session_id` | Session Cookie | (به صورت خودکار پر می‌شود) |
| `username` | نام کاربری | `testuser` |
| `user_id` | شناسه کاربر | (به صورت خودکار پر می‌شود) |

## نکات

- بعد از Login موفق، Token ها به صورت خودکار ذخیره می‌شوند
- برای استفاده از JWT، در Authorization Tab نوع **Bearer Token** را انتخاب کنید
- برای Session Auth، Cookie به صورت خودکار ارسال می‌شود

