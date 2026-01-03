# Lotus Cosmetic Services

A Django REST Framework project for managing cosmetic services.

## Features

- Django 4.2+
- Django REST Framework
- Unfold Admin Interface
- PostgreSQL Database
- Custom Permission Classes with API Key support
- Abstract DateTime Model for all models
- Persian language support

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Copy environment variables:
```bash
cp .env.example .env
```

4. Update `.env` file with your database credentials and secret key.

5. Run migrations:
```bash
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

## Project Structure

```
lotus_cosmetic_services/
├── config/           # Project settings and configuration
├── utils/            # Utility classes and helpers
│   ├── models.py     # AbstractDateTimeModel
│   ├── admin.py      # DateTimeAdminMixin
│   └── permissions.py # Custom permission classes
├── api/              # API endpoints
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

