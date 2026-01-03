# Django Built-in modules
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class DateTimeAdminMixin:
    """
    Mixin for admin classes to add created and updated fields to fieldsets.
    """
    fieldsets = (
        (_('اطلاعات زمانی'), {
            'fields': ('created', 'updated',),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('created', 'updated',)

