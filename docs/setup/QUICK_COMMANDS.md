# دستورات سریع برای اجرای پروژه

## 🚀 اجرای سرور (همیشه از این استفاده کنید)

```bash
./venv/bin/python manage.py runserver
```

## 📝 سایر دستورات مهم

```bash
# اجرای Migrations
./venv/bin/python manage.py migrate

# ایجاد Superuser
./venv/bin/python manage.py createsuperuser

# بررسی وضعیت
./venv/bin/python manage.py check

# اجرای Shell Django
./venv/bin/python manage.py shell
```

## ⚠️ نکته مهم

در macOS:
- ❌ `python` وجود ندارد
- ❌ `py` وجود ندارد  
- ✅ `python3` وجود دارد (اما Django در venv نصب شده)
- ✅ **همیشه از `./venv/bin/python` استفاده کنید**

## 🎯 خلاصه

**همیشه این دستور را استفاده کنید:**
```bash
./venv/bin/python manage.py [command]
```

مثال:
```bash
./venv/bin/python manage.py runserver
./venv/bin/python manage.py migrate
./venv/bin/python manage.py createsuperuser
```

