# Django Built-in modules
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

# Local Apps
from utils.models import AbstractDateTimeModel

User = get_user_model()


class Role(AbstractDateTimeModel):
    """
    Role model for user roles.
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_('نام نقش'),
    )
    code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_('کد نقش'),
        help_text=_('کد یکتای نقش (مثلاً: admin, customer, staff)'),
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('توضیحات'),
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('فعال'),
    )

    class Meta:
        ordering = ('-created',)
        verbose_name = _('نقش')
        verbose_name_plural = _('نقش‌ها')

    def __str__(self):
        return self.name


class UserRole(AbstractDateTimeModel):
    """
    UserRole model to link users and roles (many-to-many relationship).
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_roles',
        verbose_name=_('کاربر'),
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name='user_roles',
        verbose_name=_('نقش'),
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('فعال'),
    )

    class Meta:
        ordering = ('-created',)
        verbose_name = _('نقش کاربر')
        verbose_name_plural = _('نقش‌های کاربران')
        unique_together = ('user', 'role')

    def __str__(self):
        return f'{self.user.username} - {self.role.name}'

