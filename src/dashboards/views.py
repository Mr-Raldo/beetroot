from django.views.generic import TemplateView
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.views.generic import RedirectView
from web_project import TemplateLayout
import json
import random
from akyc.models import Profile
from akyc.serializers import ProfileSerializer
from business.models import Service, Business
from django.utils import timezone

"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to dashboards/urls.py file for more pages.
"""


class DashboardsView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        return context


class HomeView(RedirectView):
    pattern_name = "admin:index"

# Function to calculate the increase or decrease of profiles for the last 1 week
def calculate_profile_change():
    current_week_start = timezone.now().date() - timezone.timedelta(days=timezone.now().weekday())
    last_week_start = current_week_start - timezone.timedelta(weeks=1)

    profiles_current_week = Profile.objects.filter(created_at__gte=current_week_start)
    profiles_last_week = Profile.objects.filter(created_at__range=(last_week_start, current_week_start - timezone.timedelta(days=1)))

    increase = profiles_current_week.count() - profiles_last_week.count()

    return increase

def dashboard_callback(request, context):
    WEEKDAYS = [
        "Mon",
        "Tue",
        "Wed",
        "Thu",
        "Fri",
        "Sat",
        "Sun",
    ]

    positive = [[1, random.randrange(8, 28)] for i in range(1, 28)]
    negative = [[-1, -random.randrange(8, 28)] for i in range(1, 28)]
    average = [r[1] - random.randint(3, 5) for r in positive]
    performance_positive = [[1, random.randrange(8, 28)] for i in range(1, 28)]
    performance_negative = [[-1, -random.randrange(8, 28)] for i in range(1, 28)]
    stylists = Profile.objects.filter(account_type='provider').count()
    clients = Business.objects.count()
    trending_styles = Service.objects.filter(is_trending=True).count()
    profile_change = calculate_profile_change()
    print(f"Profile Change in the Last Week: {profile_change}")

    print('stylist.data', stylists )
    context.update(
        {
            "navigation": [
                {"title": _("Dashboard"), "link": "", "active": True},
                {"title": _("CMS"), "link": "/cms"},
                {"title": _("Website"), "link": "/"},
            ],
            "filters": [
                {"title": _("All"), "link": "#", "active": True},
                {
                    "title": _("New"),
                    "link": "#",
                },
            ],
            "kpi": [
                {
                    "title": "Entreprenuers Accounts",
                    "metric": stylists,
                    "footer": mark_safe(
                        f'<strong class="text-green-600 font-medium">+{profile_change}%</strong>&nbsp;progress from last week'
                    ),
                    "chart": json.dumps(
                        {
                            "labels": [WEEKDAYS[day % 7] for day in range(1, 28)],
                            "datasets": [{"data": average, "borderColor": "#9333ea"}],
                        }
                    ),
                },
                {
                    "title": "Businesses Account",
                    "metric": clients,
                    "footer": mark_safe(
                        f'<strong class="text-green-600 font-medium">+{profile_change}%</strong>&nbsp;progress from last week'
                    ),
                },
                {
                    "title": "Total Exhibits Services",
                    "metric": trending_styles,
                    "footer": mark_safe(
                        f'<strong class="text-green-600 font-medium">+{profile_change}%</strong>&nbsp;progress from last week'
                    ),
                },
            ],
            "progress": [
                {
                    "title": "Social marketing e-book",
                    "description": " $1,234.56",
                    "value": random.randint(10, 90),
                },
                {
                    "title": "Freelancing tasks",
                    "description": " $1,234.56",
                    "value": random.randint(10, 90),
                },
                {
                    "title": "Development coaching",
                    "description": " $1,234.56",
                    "value": random.randint(10, 90),
                },
                {
                    "title": "Product consulting",
                    "description": " $1,234.56",
                    "value": random.randint(10, 90),
                },
                {
                    "title": "Other income",
                    "description": " $1,234.56",
                    "value": random.randint(10, 90),
                },
            ],
            "chart": json.dumps(
                {
                    "labels": [WEEKDAYS[day % 7] for day in range(1, 28)],
                    "datasets": [
                        {
                            "label": "App Downloads",
                            "type": "line",
                            "data": average,
                            "backgroundColor": "#f0abfc",
                            "borderColor": "#f0abfc",
                        },
                        {
                            "label": "New Accounts",
                            "data": positive,
                            "backgroundColor": "#9333ea",
                        },
                        {
                            "label": "Taggings",
                            "data": negative,
                            "backgroundColor": "#f43f5e",
                        },
                    ],
                }
            ),
            "performance": [
                {
                    "title": _("Last week revenue"),
                    "metric": "$1,234.56",
                    "footer": mark_safe(
                        '<strong class="text-green-600 font-medium">+3.14%</strong>&nbsp;progress from last week'
                    ),
                    "chart": json.dumps(
                        {
                            "labels": [WEEKDAYS[day % 7] for day in range(1, 28)],
                            "datasets": [
                                {"data": performance_positive, "border Color": "#9333ea"}
                            ],
                        }
                    ),
                },
                {
                    "title": _("Last week expenses"),
                    "metric": "$1,234.56",
                    "footer": mark_safe(
                        '<strong class="text-green-600 font-medium">+3.14%</strong>&nbsp;progress from last week'
                    ),
                    "chart": json.dumps(
                        {
                            "labels": [WEEKDAYS[day % 7] for day in range(1, 28)],
                            "datasets": [
                                {"data": performance_negative, "borderColor": "#f43f5e"}
                            ],
                        }
                    ),
                },
            ],
        },
    )

    return context
