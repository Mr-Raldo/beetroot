from django.contrib import admin
from .models import Business,ProductImage,Product, Service,ServiceImage
from djangoql.admin import DjangoQLSearchMixin
from django.contrib.admin import SimpleListFilter
from import_export.admin import ImportExportActionModelAdmin
from dashboards.sites import dashboards_admin_site
from unfold.admin import ModelAdmin

@admin.action(description="Activate services trending")
def activate_services(modeladmin, request, queryset):
    queryset.update(is_trending=True)


@admin.action(description="Deactivate services trending")
def deactivate_services(modeladmin, request, queryset):
    queryset.update(is_trending=False)

class SoldOutFilter(SimpleListFilter):
    title = "Most Active"
    parameter_name = "most_active"

    def lookups(self, request, model_admin):
        return [
            ("yes", "Yes"),
            ("no", "No"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.filter(price=20)
        else:
            return queryset.exclude(price=0)

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

@admin.register(Business, site=dashboards_admin_site)
class BusinessAdmin(ModelAdmin):
    date_hierarchy = "created_date"
    empty_value_display = "-not-set-"
    list_display_links = [ "trade_sector"]
    list_select_related = ["entreprenuer"]
    search_fields = ["specialization", "service_type", "trade_sector", "trading_name", "business_description", "service_type"]
    inlines = [ServiceInline]

    list_display = [
                # "created_at",
        # "upper_case_name",
        "specialization",
        "trade_sector",
        "service_type",
        "account_type",
    ]


    fieldsets = [
        (
            "User Profile Detail",
            {  "classes": ["wide", "extrapretty"],
                "fields": [("service_type","specialization"),("phone","email"), ("account_type","trade_sector"),("is_subscribed","is_premium_subscribed"),"business_description"],
            },
        ),
        # (
        #     "Entreprenurial Profile",
        #     {
        #         "classes":["wide", "extrapretty"],
        #         "fields": ["entreprenuer__trading_as", "entreprenuer__specialization", "entreprenuer__special_skills","entreprenuer__expected_experience"],
        #     },
        # ),
        (
            "Business Goals",
            {
                "classes":["wide", "extrapretty"],
                "fields": ["short_term_goals", "long_term_goals","business_stage"],
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
    @admin.display(description="Name")
    def upper_case_name(self,obj):
        return f"{obj.trading_name}".upper()

class ServiceImageInline(admin.TabularInline):
    model = ServiceImage

@admin.register(Service, site=dashboards_admin_site)
class ServiceAdmin(DjangoQLSearchMixin, ImportExportActionModelAdmin):
    inlines = [ServiceImageInline]
    date_hierarchy = "created_date"
    empty_value_display = "-not-set-"
    list_display_links = ["upper_case_name", "category"]
    list_select_related = ["business", "entreprenuer"]
    search_fields = ["name", "category", "description"]
    actions = [activate_services, deactivate_services]
    list_filter = ["category", "entreprenuer","business","trade_status",
        "is_trending",]
    readonly_fields = ('display_service_images',)  # Make sure to include this field in readonly_fields

    list_display = [
                # "created_at",
        "upper_case_name",
        "name",
        "category",
        "price",
        "business",
        "entreprenuer",
        "trade_status",
        "is_trending",
    ]


    fieldsets = [
        (
            "Service Profile Detail",
            {  "classes": ["wide", "extrapretty"],
                "fields": [("name"), ("trade_status","is_trending"),"description"],
            },
        ),
        # (
        #     "Entreprenuer Profile",
        #     {
        #         "classes":["wide", "extrapretty"],
        #         "fields": ["entreprenuer__first_name", "entreprenuer__specialization", "entreprenuer__special_skills","entreprenuer__expected_experience"],
        #     },
        # ),
        # (
        #     "Images",
        #     {
        #         "classes":["wide", "extrapretty"],
        #         "fields": ["ideals", "immeditiate_needs","platform_joining_goals"],
        #     },
        # ),

    ]
    @admin.display(description="Name")
    def upper_case_name(self,obj):
        return f"{obj.name}".upper()

    def display_service_images(self, obj):
        # This assumes the Service model has a related_name='images' for the ServiceImage foreign key
        images = obj.images.all()
        if images:
            return ', '.join([f'<img src="{image.image.url}" height="50" width="50" />' for image in images])
        return "No images available"

    display_service_images.allow_tags = True
    display_service_images.short_description = "Service Images"

@admin.register(Product, site=dashboards_admin_site)
class ProductAdmin(DjangoQLSearchMixin, ImportExportActionModelAdmin):
    date_hierarchy = "created_date"
    empty_value_display = "-not-set-"
    list_display_links = ["upper_case_name", "category"]
    list_select_related = ["business", "entreprenuer"]
    search_fields = ["name", "category", "description"]
    actions = [activate_services, deactivate_services]
    list_filter = ["category", "entreprenuer","business","trade_status",
        "is_trending",]

    list_display = [
                # "created_at",
        "upper_case_name",
        "name",
        "category",
        "quantity",
        "weight",
        "price",
        "business",
        "entreprenuer",
        "trade_status",
        "is_trending",
    ]


    fieldsets = [
        (
            "Service Profile Detail",
            {  "classes": ["wide", "extrapretty"],
                "fields": [("name"), ("trade_status","is_trending"),"description"],
            },
        ),
        # (
        #     "Entreprenuer Profile",
        #     {
        #         "classes":["wide", "extrapretty"],
        #         "fields": ["entreprenuer__first_name", "entreprenuer__specialization", "entreprenuer__special_skills","entreprenuer__expected_experience"],
        #     },
        # ),
        # (
        #     "Images",
        #     {
        #         "classes":["wide", "extrapretty"],
        #         "fields": ["ideals", "immeditiate_needs","platform_joining_goals"],
        #     },
        # ),

    ]
    @admin.display(description="Name")
    def upper_case_name(self,obj):
        return f"{obj.name}".upper()

admin.site.register(ServiceImage, site=dashboards_admin_site)

admin.site.register(ProductImage, site=dashboards_admin_site)
