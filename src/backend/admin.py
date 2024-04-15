from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from dashboards.sites import dashboards_admin_site
from .models import User
from unfold.contrib.forms.widgets import WysiwygWidget
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from django.db.models import TextChoices

from django.db import models
from unfold.decorators import action, display
from django.utils.translation import gettext_lazy as _
from akyc.models import (
    Profile,
)

from business.models import Service
from django.utils.safestring import mark_safe

from unfold.contrib.filters.admin import (
    RangeDateFilter,
    RangeDateTimeFilter,
    RangeNumericListFilter,
    RangeNumericFilter,
    SingleNumericFilter,
    SliderNumericFilter,
)

admin.site.unregister(Group)

# admin.site.unregister(Profile)
class UserStatus(TextChoices):
    ACTIVE = "ACTIVE", _("Active")
    PENDING = "PENDING", _("Pending")
    INACTIVE = "INACTIVE", _("Inactive")
    CANCELLED = "CANCELLED", _("Cancelled")

class CustomSliderNumericFilter(SliderNumericFilter):
    MAX_DECIMALS = 2
    STEP = 10


class CustomRangeNumericListFilter(RangeNumericListFilter):
    parameter_name = "items_count"
    title = "items"




class ServiceInline(admin.TabularInline):
    model = Service
    fields = ["name",
        "category",
        "price",
        "business",
        "entreprenuer",
        "trade_status",
        "is_trending"]

    # optional: make the inline read-only
    readonly_fields = ["name",
        "category",
        "price",
        "business",
        "entreprenuer",
        "trade_status",
        "is_trending"]
    can_delete = False
    max_num = 0
    extra = 0
    show_change_link = True
# Register your models here.


@admin.register(Profile, site=dashboards_admin_site)
class MemberAdmin(ModelAdmin):
    date_hierarchy = "created_at"
    empty_value_display = "-not-set-"
    list_display_links = ["upper_case_name", "phone"]
    list_select_related = ["user", "wallet"]
    search_fields = ["user__username", "first_name", "specialization", "neighbourhood", "city", "gender"]
    inlines = [ServiceInline]
    list_filter_submit = True  # Submit button at the bottom of the filter
    list_filter = (
        ("created_at", RangeDateFilter),  # Date filter
        ("created_at", RangeDateTimeFilter),  # Datetime filter
        # ("field_A", SingleNumericFilter),  # Numeric single field search, __gte lookup
        # ("field_B", RangeNumericFilter),  # Numeric range search, __gte and __lte lookup
        # ("field_C", SliderNumericFilter),  # Numeric range filter but with slider
        # ("field_D", CustomSliderNumericFilter),  # Numeric filter with custom attributes
        CustomRangeNumericListFilter,  # Numeric range search not restricted to a model field
    )

    list_display = [
                # "created_at",
        "display_profile_image",
        "display_as_two_line_heading",
        "show_status_with_custom_label",
        "upper_case_name",
        "phone",
        "account_type",
        "is_subscribed",
        "is_premium_subscribed",
        "gender",
        "specialization",
        "neighbourhood",
        "city",
        "is_verified",
        "status",

    ]


    fieldsets = [
        (
            "User Profile Detail",
            {  "classes": ["wide", "extrapretty"],
                "fields": [("user","gender"), ("first_name","last_name"),("phone","email"), ("account_type","is_verified"),("is_subscribed","is_premium_subscribed"),"self_description","profile_image"],
            },
        ),
        (
            "Entreprenurial Profile",
            {
                "classes":["wide", "extrapretty"],
                "fields": ["trading_as", "specialization", "special_skills","expected_experience"],
            },
        ),
        (
            "Interest",
            {
                "classes":["wide", "extrapretty"],
                "fields": ["ideals", "immeditiate_needs","platform_joining_goals"],
            },
        ),
        (
            "Location",
            {
                "classes":["wide", "extrapretty"],
                "fields": [("street_address", "neighbourhood"),("city", "country")],
            },
        ),
        (
            "Advanced options",
            {
                "classes": ["collapse"],
                "fields": ["online_status", "wallet_address"],
            },
        ),
    ]
    @admin.display(description="Profile Image")
    @mark_safe
    def display_profile_image(self, obj):
        if obj.profile_image and obj.profile_image.file:
            return f'<img src="{obj.profile_image.url}" height="{obj.profile_image.height}" width="{obj.profile_image.width}" />'
        else:
            return "No profile"
    @display(
        description=_("Status"),
        ordering="status",
        label=True
    )
    def show_status_default_color(self, obj):
        return obj.status

    @display(
        description=_("Status"),
        ordering="status",
        label={
            UserStatus.ACTIVE: "success",  # green
            UserStatus.PENDING: "info",  # blue
            UserStatus.INACTIVE: "warning",  # orange
            UserStatus.CANCELLED: "danger",  # red
        },
    )
    def show_status_customized_color(self, obj):
        return obj.status

    @display(description=_("Status with label"), ordering="status", label=True)
    def show_status_with_custom_label(self, obj):
        return obj.status, obj.get_status_display()

    @display(header=True)
    def display_as_two_line_heading(self, obj):
        """
        Third argument is short text which will appear as prefix in circle
        """
        return f"{obj.first_name} {obj.last_name}", f"{obj.specialization}, {obj.trading_as}"

    @admin.display(description="Name")
    def upper_case_name(self,obj):
        return f"{obj.first_name} {obj.last_name}".upper()


@admin.register(User, site=dashboards_admin_site)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = [
        "display_header",
        "is_active",
        "display_staff",
        "display_superuser",
        "display_created",
    ]
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"),
            {"fields": (("first_name", "last_name"), "email", "biography")},
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        }
    }
    readonly_fields = ["last_login", "date_joined"]

    @display(description=_("User"), header=True)
    def display_header(self, instance: User):
        return instance.full_name, instance.email

    @display(description=_("Staff"), boolean=True)
    def display_staff(self, instance: User):
        return instance.is_staff

    @display(description=_("Superuser"), boolean=True)
    def display_superuser(self, instance: User):
        return instance.is_superuser

    @display(description=_("Created"))
    def display_created(self, instance: User):
        return instance.created_at


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass
