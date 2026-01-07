# Django Built-in modules
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.text import Truncator

# Third Party Packages
from unfold.admin import ModelAdmin

# Local Apps
from utils.admin import DateTimeAdminMixin
from ..models import Role, UserRole


@admin.register(Role)
class RoleAdmin(ModelAdmin):
    list_display = ('name', 'code', 'display_truncate_description', 'is_active', 'jcreated',)
    fieldsets = (
        (_('اطلاعات نقش'), {'fields': ('name', 'code', 'description', 'is_active',)}),
        *DateTimeAdminMixin.fieldsets,
    )
    list_filter = ('is_active',)
    list_editable = ('is_active',)
    search_fields = ('name', 'code', 'description',)
    readonly_fields = (*DateTimeAdminMixin.readonly_fields,)
    save_on_top = False

    @admin.display(description=_('توضیحات'), empty_value='-')
    def display_truncate_description(self, obj):
        if obj.description:
            return Truncator(obj.description).chars(50)
        return '-'

    @admin.display(description=_('تاریخ ایجاد'), ordering='created')
    def jcreated(self, obj):
        return obj.created.strftime('%Y/%m/%d %H:%M') if obj.created else '-'


@admin.register(UserRole)
class UserRoleAdmin(ModelAdmin):
    list_display = ('user', 'role', 'is_active', 'jcreated',)
    fieldsets = (
        (_('اطلاعات نقش کاربر'), {'fields': ('user', 'role', 'is_active',)}),
        *DateTimeAdminMixin.fieldsets,
    )
    list_filter = ('is_active', 'role',)
    list_editable = ('is_active',)
    search_fields = ('user__username', 'user__email', 'role__name', 'role__code',)
    readonly_fields = (*DateTimeAdminMixin.readonly_fields,)
    save_on_top = False

    @admin.display(description=_('تاریخ ایجاد'), ordering='created')
    def jcreated(self, obj):
        return obj.created.strftime('%Y/%m/%d %H:%M') if obj.created else '-'

