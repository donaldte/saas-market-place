
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html


from .models import *



@admin.register(User)
class UserAdminUI(UserAdmin):
    change_user_password_template = None

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),

        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    'is_client',
                    'is_seller',
                    'is_admin',
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
        "date_joined",
        "last_login"
    )
    list_filter = ("is_staff", "is_superuser", "is_active")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )


META_FIELDS = ["id", 'modified', 'activate_date',
               'deactivate_date', 'is_deleted', 'metadata']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display =  [
        'user',
        'phone_number',
        'country',
        'region',
        'city',
        'address',
        'zip_code'
    ]
    ordering = ("user",)





admin.site.site_title = _("ADMIN SAAS")
admin.site.site_header = _("ADMIN SAAS")
admin.site.index_title = _("ADMIN SAAS")

