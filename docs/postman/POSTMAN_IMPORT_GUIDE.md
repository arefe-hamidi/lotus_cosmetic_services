# راهنمای Import کردن در Postman

## فایل‌های آماده برای Import

دو فایل برای شما آماده شده است:

1. **`Lotus_Cosmetic_Services_API.postman_collection.json`** - Collection کامل API
2. **`Lotus_Local.postman_environment.json`** - Environment Variables

## مراحل Import

### مرحله 1: Import کردن Collection

1. Postman را باز کنید
2. روی دکمه **Import** در گوشه بالا سمت چپ کلیک کنید
3. روی **Upload Files** کلیک کنید
4. فایل **`Lotus_Cosmetic_Services_API.postman_collection.json`** را انتخاب کنید
5. روی **Import** کلیک کنید

### مرحله 2: Import کردن Environment

1. دوباره روی **Import** کلیک کنید
2. فایل **`Lotus_Local.postman_environment.json`** را انتخاب کنید
3. روی **Import** کلیک کنید
4. در گوشه بالا سمت راست، Environment را روی **"Lotus Local"** تنظیم کنید

### مرحله 3: استفاده از Collection

بعد از Import، شما یک Collection با نام **"Lotus Cosmetic Services API"** خواهید داشت که شامل:

#### 📁 Health & Test
- Health Check (GET)
- Protected Endpoint (GET)

#### 📁 Authentication
- Register (POST) - ثبت نام کاربر جدید
- Login (POST) - ورود کاربر
- Get Profile (GET) - دریافت پروفایل
- Update Profile (PUT) - بروزرسانی پروفایل
- Change Password (POST) - تغییر رمز عبور
- Logout (POST) - خروج

## نحوه استفاده

### 1. تست Health Check
- روی **Health Check** کلیک کنید
- روی **Send** کلیک کنید
- باید پاسخ موفقیت‌آمیز دریافت کنید

### 2. ثبت نام کاربر جدید
- روی **Register** کلیک کنید
- در قسمت Body می‌توانید اطلاعات را تغییر دهید
- روی **Send** کلیک کنید
- اگر موفق باشد، `user_id` و `username` به صورت خودکار در Environment ذخیره می‌شود

### 3. ورود (Login)
- روی **Login** کلیک کنید
- `username` از Environment استفاده می‌شود (می‌توانید تغییر دهید)
- روی **Send** کلیک کنید
- اگر موفق باشد، `session_id` به صورت خودکار ذخیره می‌شود

### 4. استفاده از Endpoint های محافظت شده
بعد از Login موفق، `session_id` به صورت خودکار در Cookie header قرار می‌گیرد و می‌توانید:
- Get Profile را تست کنید
- Update Profile را تست کنید
- Change Password را تست کنید
- Logout را تست کنید

## تنظیمات Environment Variables

در Environment **"Lotus Local"** این متغیرها وجود دارند:

- `base_url`: `http://127.0.0.1:8000`
- `session_id`: به صورت خودکار بعد از Login پر می‌شود
- `username`: نام کاربری پیش‌فرض
- `user_id`: به صورت خودکار بعد از Register/Login پر می‌شود
- `user_email`: به صورت خودکار بعد از Login پر می‌شود

## نکات مهم

1. **قبل از استفاده**: مطمئن شوید که Django server در حال اجرا است:
   ```bash
   ./venv/bin/python manage.py runserver
   ```

2. **ترتیب استفاده**:
   - ابتدا Register کنید (یا از کاربر موجود استفاده کنید)
   - سپس Login کنید
   - بعد از Login، می‌توانید از Endpoint های محافظت شده استفاده کنید

3. **Session Cookie**: بعد از Login موفق، `session_id` به صورت خودکار در Cookie header قرار می‌گیرد

4. **تغییر Environment**: اگر می‌خواهید URL را تغییر دهید، در Environment متغیر `base_url` را ویرایش کنید

## عیب‌یابی

### مشکل: Connection Refused
- مطمئن شوید Django server در حال اجرا است
- بررسی کنید که `base_url` درست تنظیم شده باشد

### مشکل: 401 Unauthorized در Endpoint های محافظت شده
- ابتدا Login کنید
- مطمئن شوید که `session_id` در Environment ذخیره شده است

### مشکل: 403 Forbidden
- بررسی کنید که کاربر فعال است
- دوباره Login کنید

## فایل‌های Import

- **Collection**: `Lotus_Cosmetic_Services_API.postman_collection.json`
- **Environment**: `Lotus_Local.postman_environment.json`

هر دو فایل در ریشه پروژه قرار دارند.

