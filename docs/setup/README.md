# Setup & Installation Guide

این بخش شامل راهنمای نصب و راه‌اندازی پروژه است.

## فهرست مطالب

### 📚 مستندات

1. **[Quick Start Guide](./QUICK_START.md)**
   - راهنمای سریع شروع کار
   - نصب و راه‌اندازی اولیه
   - دستورات پایه

2. **[How to Run](./HOW_TO_RUN.md)**
   - راهنمای کامل اجرای پروژه
   - روش‌های مختلف اجرا
   - حل مشکلات رایج

3. **[Quick Commands](./QUICK_COMMANDS.md)**
   - دستورات سریع و مفید
   - خلاصه دستورات مهم

## نصب سریع

### 1. ایجاد Virtual Environment
```bash
python3 -m venv venv
```

### 2. نصب Dependencies
```bash
./venv/bin/pip install -r requirements.txt
```

### 3. تنظیم Environment Variables
```bash
cp .env.example .env
# ویرایش فایل .env
```

### 4. اجرای Migrations
```bash
./venv/bin/python manage.py migrate
```

### 5. ایجاد Superuser
```bash
./venv/bin/python manage.py createsuperuser
```

### 6. اجرای سرور
```bash
./venv/bin/python manage.py runserver
```

## دستورات مهم

### اجرای سرور
```bash
./venv/bin/python manage.py runserver
```

### اجرای Migrations
```bash
./venv/bin/python manage.py migrate
```

### ایجاد Superuser
```bash
./venv/bin/python manage.py createsuperuser
```

### بررسی وضعیت
```bash
./venv/bin/python manage.py check
```

### اجرای Shell Django
```bash
./venv/bin/python manage.py shell
```

## Scripts آماده

- `./run_server.sh` - اجرای سرور
- `./stop_server.sh` - متوقف کردن سرور

## نکات مهم

- در macOS از `./venv/bin/python` استفاده کنید (نه `python`)
- همیشه از Virtual Environment استفاده کنید
- سرور روی پورت 8000 اجرا می‌شود

