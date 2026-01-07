# Django Built-in modules
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

# Local Apps
from utils.models import AbstractDateTimeModel
from .role import Role

User = get_user_model()


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

