from django.contrib import admin, messages
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from django.db.models import OuterRef, Sum
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django_celery_beat.models import (
    ClockedSchedule,
    CrontabSchedule,
    IntervalSchedule,
    PeriodicTask,
    SolarSchedule,
)
from guardian.admin import GuardedModelAdmin
from import_export.admin import ImportExportModelAdmin
from simple_history.admin import SimpleHistoryAdmin
from unfold.admin import ModelAdmin, StackedInline, TabularInline
from unfold.contrib.filters.admin import (
    RangeDateFilter,
    RangeNumericFilter,
    SingleNumericFilter,
)
from unfold.contrib.import_export.forms import ExportForm, ImportForm
from unfold.decorators import action, display

from unfold.widgets import UnfoldAdminColorInputWidget
# Register your models here.
from .sites import dashboards_admin_site

@admin.register(PeriodicTask, site=dashboards_admin_site)
class PeriodicTaskAdmin(ModelAdmin):
    pass


@admin.register(IntervalSchedule, site=dashboards_admin_site)
class IntervalScheduleAdmin(ModelAdmin):
    pass


@admin.register(CrontabSchedule, site=dashboards_admin_site)
class CrontabScheduleAdmin(ModelAdmin):
    pass


@admin.register(SolarSchedule, site=dashboards_admin_site)
class SolarScheduleAdmin(ModelAdmin):
    pass


@admin.register(ClockedSchedule, site=dashboards_admin_site)
class ClockedScheduleAdmin(ModelAdmin):
    pass




@admin.register(Group, site=dashboards_admin_site)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass

