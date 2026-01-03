# Django Built-in modules
from django.db import models
from django.utils.translation import gettext_lazy as _


class AbstractDateTimeModel(models.Model):
    """
    Abstract base model that provides created and updated datetime fields.
    All models should inherit from this class.
    """
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('تاریخ ایجاد'),
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name=_('تاریخ بروزرسانی'),
    )

    class Meta:
        abstract = True

