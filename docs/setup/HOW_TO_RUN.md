# نحوه اجرای پروژه Django

## روش 1: استفاده از Virtual Environment (توصیه می‌شود)

```bash
cd /Users/arefeh_hamidi/Documents/Lotus/lotus_cosmetic_services
./venv/bin/python manage.py runserver
```

**⚠️ مهم**: در macOS دستور `python` وجود ندارد! باید از یکی از این روش‌ها استفاده کنید:

- ❌ **اشتباه**: `python manage.py runserver` (دستور python وجود ندارد)
- ❌ **اشتباه**: `manage.py runserver` (باید با Python اجرا شود)
- ✅ **درست**: `./venv/bin/python manage.py runserver` (توصیه می‌شود ⭐)
- ✅ **درست**: `python3 manage.py runserver` (اگر Django نصب باشد)

## روش 2: استفاده از Script آماده

```bash
cd /Users/arefeh_hamidi/Documents/Lotus/lotus_cosmetic_services
./run_server.sh
```

## روش 3: فعال کردن Virtual Environment و سپس اجرا

```bash
cd /Users/arefeh_hamidi/Documents/Lotus/lotus_cosmetic_services
source venv/bin/activate
python manage.py runserver
```

## دستورات مفید دیگر

### اجرای Migrations

```bash
./venv/bin/python manage.py migrate
```

### ایجاد Superuser

```bash
./venv/bin/python manage.py createsuperuser
```

### بررسی وضعیت پروژه

```bash
./venv/bin/python manage.py check
```

### اجرای Shell Django

```bash
./venv/bin/python manage.py shell
```

## نکات مهم

1. **همیشه از Virtual Environment استفاده کنید**: `./venv/bin/python` به جای `python` یا `py`
2. **سرور روی پورت 8000 اجرا می‌شود**: `http://127.0.0.1:8000`
3. **برای توقف سرور**: `Ctrl + C` را بزنید

## خطاهای رایج

### خطا: `command not found: py` یا `command not found: python`

- **علت**: دستورات `py` و `python` در macOS وجود ندارند (فقط `python3` وجود دارد)
- **راه حل**: از `./venv/bin/python` استفاده کنید (توصیه می‌شود) یا `python3`

### خطا: `ModuleNotFoundError: No module named 'django'`

- **علت**: Virtual Environment فعال نیست
- **راه حل**: از `./venv/bin/python` استفاده کنید یا Virtual Environment را فعال کنید

### خطا: `Port 8000 is already in use`

- **علت**: پورت 8000 قبلاً استفاده شده (احتمالاً یک سرور Django دیگر در حال اجرا است)
- **راه حل 1**: متوقف کردن سرور قبلی

  ```bash
  # پیدا کردن Process ID
  lsof -ti:8000

  # متوقف کردن Process (PID را جایگزین کنید)
  kill [PID]

  # یا متوقف کردن همه سرورهای Django
  pkill -f "manage.py runserver"
  ```

- **راه حل 2**: اجرا روی پورت دیگر
  ```bash
  ./venv/bin/python manage.py runserver 8001
  ```
