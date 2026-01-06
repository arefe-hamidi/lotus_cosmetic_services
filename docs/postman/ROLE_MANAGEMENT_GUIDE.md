# Role Management in Postman

راهنمای استفاده از Role Management endpoints در Postman

## پیش‌نیازها

1. **Import Collection**: فایل `Lotus_Cosmetic_Services_API.postman_collection.json` را Import کنید
2. **Import Environment**: فایل `Lotus_Local.postman_environment.json` را Import کنید
3. **Login**: ابتدا با یک کاربر که نقش admin دارد Login کنید

## مراحل استفاده

### Step 1: Login و دریافت Token

1. Request **"Login"** را اجرا کنید
2. بعد از Login موفق، `access_token` و `refresh_token` به صورت خودکار در Environment ذخیره می‌شوند

### Step 2: ایجاد نقش Admin (اولین بار)

**⚠️ مهم**: برای اولین بار، باید نقش admin را از Django Admin ایجاد کنید:

1. به `http://127.0.0.1:8000/admin/` بروید
2. وارد شوید
3. به بخش **Roles** بروید
4. یک Role جدید با:
   - Name: `مدیر سیستم`
   - Code: `admin`
   - Description: `دسترسی کامل به سیستم`
   - Is Active: ✅
5. Save کنید

### Step 3: اختصاص نقش Admin به کاربر

1. به بخش **User Roles** در Django Admin بروید
2. یک UserRole جدید ایجاد کنید:
   - User: کاربر مورد نظر
   - Role: admin
   - Is Active: ✅

### Step 4: استفاده از Role Endpoints در Postman

بعد از Login با کاربر admin، می‌توانید از این Endpoint ها استفاده کنید:

#### 📋 List Roles

- **Request**: "List Roles"
- **Method**: GET
- **URL**: `{{base_url}}/api/roles/`
- **Auth**: Bearer Token (به صورت خودکار)

#### ➕ Create Role

- **Request**: "Create Role"
- **Method**: POST
- **URL**: `{{base_url}}/api/roles/`
- **Body**:
  ```json
  {
    "name": "کارمند",
    "code": "staff",
    "description": "دسترسی کارمند"
  }
  ```

#### 👁️ Get Role Detail

- **Request**: "Get Role Detail"
- **Method**: GET
- **URL**: `{{base_url}}/api/roles/{{role_id}}/`
- **Note**: `role_id` را از Response ایجاد نقش کپی کنید

#### ✏️ Update Role

- **Request**: "Update Role"
- **Method**: PUT
- **URL**: `{{base_url}}/api/roles/{{role_id}}/`
- **Body**: فیلدهای مورد نظر برای بروزرسانی

#### 🗑️ Delete Role

- **Request**: "Delete Role"
- **Method**: DELETE
- **URL**: `{{base_url}}/api/roles/{{role_id}}/`
- **Note**: Soft delete (is_active = False)

#### 👤 Get User Roles

- **Request**: "Get User Roles"
- **Method**: GET
- **URL**: `{{base_url}}/api/users/{{user_id}}/roles/`
- **Note**: `user_id` از Environment استفاده می‌شود

#### ➕ Add Role to User

- **Request**: "Add Role to User"
- **Method**: POST
- **URL**: `{{base_url}}/api/users/{{user_id}}/roles/`
- **Body**:
  ```json
  {
    "role_id": 1
  }
  ```

#### ➖ Remove Role from User

- **Request**: "Remove Role from User"
- **Method**: DELETE
- **URL**: `{{base_url}}/api/users/{{user_id}}/roles/{{role_id}}/`

## Environment Variables

متغیرهای موجود در Environment:

| Variable        | Description       | Auto-filled     |
| --------------- | ----------------- | --------------- |
| `base_url`      | آدرس API          | ❌              |
| `access_token`  | JWT Access Token  | ✅ بعد از Login |
| `refresh_token` | JWT Refresh Token | ✅ بعد از Login |
| `user_id`       | شناسه کاربر       | ✅ بعد از Login |
| `username`      | نام کاربری        | ✅ بعد از Login |
| `role_id`       | شناسه نقش         | ❌ (دستی)       |

## نکات مهم

1. **همه Role Endpoints نیاز به نقش admin دارند**
2. **بعد از Login، Token به صورت خودکار در Header قرار می‌گیرد**
3. **برای استفاده از `{{role_id}}`، باید آن را از Response ایجاد نقش کپی کنید**
4. **Profile endpoint اکنون نقش‌های کاربر را نمایش می‌دهد**

## مثال کامل

### 1. Login

```
POST /api/auth/login/
Body: {"username": "admin_user", "password": "password"}
→ access_token ذخیره می‌شود
```

### 2. Create Role

```
POST /api/roles/
Authorization: Bearer {{access_token}}
Body: {"name": "کارمند", "code": "staff"}
→ role_id را کپی کنید
```

### 3. Add Role to User

```
POST /api/users/{{user_id}}/roles/
Authorization: Bearer {{access_token}}
Body: {"role_id": 1}
```

### 4. Get User Profile (با نقش‌ها)

```
GET /api/auth/profile/
Authorization: Bearer {{access_token}}
→ Response شامل roles می‌شود
```

## عیب‌یابی

### خطا: 403 Forbidden

- **علت**: کاربر نقش admin ندارد
- **راه حل**: از Django Admin نقش admin را به کاربر اختصاص دهید

### خطا: 401 Unauthorized

- **علت**: Token منقضی شده
- **راه حل**: دوباره Login کنید یا از Refresh Token استفاده کنید

### خطا: Role not found

- **علت**: `role_id` اشتباه است
- **راه حل**: از "List Roles" لیست نقش‌ها را ببینید
