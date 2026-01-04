# Lotus Cosmetic Services

A Django REST Framework project for managing cosmetic services.

## ✨ Features

- Django 4.2+
- Django REST Framework
- JWT Authentication
- Unfold Admin Interface
- PostgreSQL Database Support
- Custom Permission Classes with API Key support
- Abstract DateTime Model for all models
- Persian language support

## 🚀 Quick Start

### Installation

1. Create a virtual environment:

```bash
python3 -m venv venv
```

2. Install dependencies:

```bash
./venv/bin/pip install -r requirements.txt
```

3. Run migrations:

```bash
./venv/bin/python manage.py migrate
```

4. Create a superuser:

```bash
./venv/bin/python manage.py createsuperuser
```

5. Run the development server:

```bash
./venv/bin/python manage.py runserver
```

Server will be available at: `http://127.0.0.1:8000`

## 📚 Documentation

تمام مستندات در پوشه `docs/` قرار دارند:

- **[📖 Documentation Index](./docs/README.md)** - فهرست کامل مستندات
- **[🔐 Authentication](./docs/auth/)** - راهنمای احراز هویت و JWT
- **[🚀 Setup Guide](./docs/setup/)** - راهنمای نصب و راه‌اندازی
- **[📮 Postman](./docs/postman/)** - راهنمای استفاده از Postman

### Quick Links

- [Quick Start Guide](./docs/setup/QUICK_START.md)
- [How to Run](./docs/setup/HOW_TO_RUN.md)
- [JWT Authentication](./docs/auth/JWT_AUTHENTICATION.md)
- [Postman Import Guide](./docs/postman/POSTMAN_IMPORT_GUIDE.md)

## 📁 Project Structure

```
lotus_cosmetic_services/
├── api/              # API endpoints
│   ├── views.py      # API views
│   ├── serializers.py # Serializers
│   └── urls.py       # URL routing
├── config/           # Project settings
│   ├── settings.py   # Django settings
│   └── urls.py       # Main URL config
├── utils/            # Utility classes
│   ├── models.py     # AbstractDateTimeModel
│   ├── admin.py      # DateTimeAdminMixin
│   └── permissions.py # Custom permissions
├── docs/             # Documentation
│   ├── auth/         # Authentication docs
│   ├── setup/        # Setup guides
│   └── postman/      # Postman guides
├── manage.py
└── requirements.txt
```

## Development Guidelines

### Models

- All models must inherit from `AbstractDateTimeModel`
- All field verbose names must be in Persian using `gettext_lazy`
- Models must have `verbose_name` and `verbose_name_plural` in Persian

### Admin

- All admin classes must inherit from `unfold_admin.admin.ModelAdmin`
- Use `DateTimeAdminMixin` for created/updated fields
- Organize fields using fieldsets

### Views

- Use generic views when possible
- All views must have serializers (except specific cases)
- Define `permission_classes` in views
- Use `AllowAnyWithAPIKey` for public endpoints
- Use `IsAuthenticatedWithAPIKey` for protected endpoints

### URLs

- URL names should be meaningful
- Follow the pattern: `app_name/action/` or `app_name/action/<id>/`

## License

This project is proprietary software.
