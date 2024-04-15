from django.urls import path
from .views import businessView
from django.contrib.auth.decorators import login_required
from . import views


urlpatterns = [
    # Provider Views
    path('business/', views.business_list, name='business-list'),
    path('get_entreprenuer_businesses/<int:profile_id>', views.get_entreprenuer_businesses, name='business-list'),
    path('business/<str:id>/', views.business_detail, name='business-detail'),


    # Service Views
    path('services/<str:id>/', views.service_detail, name='service-detail'),
    path('services/<str:id>/', views.service_detail, name='service-detail'),
    path('services/', views.services, name='services'),
    path('entreprenuers/', views.entreprenuers, name='entreprenuers'),
    path('get_entreprenuers/', views.entreprenuers, name='entreprenuers'),
    path('entreprenuer/<int:profile_id>', views.entreprenuer, name='entreprenuer'),
    path('services/<str:phone>/services/', views.services_list, name='services-list'),
    path('services/<int:profile_id>/services/<int:service_id>/', views.service_detail, name='service-detail'),
    path('business_services/<int:business_id>', views.business_services, name='service-detail'),
    path('entreprenuer_services/<int:profile_id>', views.entreprenuer_services, name='service-detail'),
    # Service Image Views
    path('service_images/', views.service_images_list, name='service-images-list'),
    path('service_images/<str:id>/', views.service_image_detail, name='service-image-detail'),

    # Product Views  
    path('products/', views.products_list, name='products-list'),
    path('products/<str:id>/', views.product_detail, name='product-detail'),

    # Product Image Views
    path('product_images/', views.product_images_list, name='product-images-list'),
    path('product_images/<str:id>/', views.product_image_detail, name='product-image-detail'),
    path(
        "app/business/dashboard/",
        login_required(businessView.as_view(template_name="app_business_dashboard.html")),
        name="business-portal-dashboard",
    ),
    # products
    path(
        "app/business/producer/list/",
        login_required(businessView.as_view(template_name="app_business_producer_list.html")),
        name="business-portal-producer-list",
    ),
    path(
        "app/business/producer/add/",
        login_required(businessView.as_view(template_name="app_business_producer_add.html")),
        name="business-portal-producer-add",
    ),
    # products
    path(
        "app/business/product/list/",
        login_required(businessView.as_view(template_name="app_business_product_list.html")),
        name="business-portal-product-list",
    ),
    path(
        "app/business/product/add/",
        login_required(businessView.as_view(template_name="app_business_product_add.html")),
        name="business-portal-product-add",
    ),
    path(
        "app/business/product/category/",
        login_required(businessView.as_view(template_name="app_business_category_list.html")),
        name="business-portal-product-category-list",
    ),
    # services
    path(
        "app/business/service/list/",
        login_required(businessView.as_view(template_name="app_business_service_list.html")),
        name="business-portal-service-list",
    ),
    path(
        "app/business/service/add/",
        login_required(businessView.as_view(template_name="app_business_service_add.html")),
        name="business-portal-service-add",
    ),
    path(
        "app/business/service/category/",
        login_required(businessView.as_view(template_name="app_business_category_list.html")),
        name="business-portal-service-category-list",
    ),

    # orders
    path(
        "app/business/order/list/",
        login_required(businessView.as_view(template_name="app_business_order_list.html")),
        name="business-portal-order-list",
    ),
    path(
        "app/business/order/details/",
        login_required(businessView.as_view(template_name="app_business_order_details.html")),
        name="business-portal-order-details",
    ),
    path(
        "app/business/customer_all/",
        login_required(businessView.as_view(template_name="app_business_customer_all.html")),
        name="business-portal-customer-all",
    ),
    path(
        "app/business/customer/details/overview/",
        login_required(businessView.as_view(template_name="app_business_customer_details_overview.html" )),
        name="business-portal-customer-details-overview",
    ),
    path(
        "app/business/customer/details/security/",
        login_required(businessView.as_view(template_name="app_business_customer_details_security.html")),
        name="business-portal-customer-details-security",
    ),
    path(
        "app/business/customer/details/billing/",
        login_required(businessView.as_view(template_name="app_business_customer_details_billing.html")),
        name="business-portal-customer-details-billing",
    ),
    path(
        "app/business/customer/details/notifications/",
        login_required(businessView.as_view(template_name="app_business_customer_details_notifications.html" )),
        name="business-portal-customer-details-notifications",
    ),
    path(
        "app/business/manage_reviews/",
        login_required(businessView.as_view(template_name="app_business_manage_reviews.html")),
        name="business-portal-manage-reviews",
    ),
    path(
        "app/business/referrals/",
        login_required(businessView.as_view(template_name="app_business_referral.html")),
        name="business-portal-referrals",
    ),
    path(
        "app/business/settings/details/",
        login_required(businessView.as_view(template_name="app_business_settings_detail.html")),
        name="business-portal-settings-detail",
    ),
    path(
        "app/business/settings/payments/",
        login_required(businessView.as_view(template_name="app_business_settings_payments.html")),
        name="business-portal-settings-payments",
    ),

    path(
        "app/business/settings/shipping/",
        login_required(businessView.as_view(template_name="app_business_settings_shipping.html")),
        name="business-portal-settings-shipping",
    ),
    path(
        "app/business/settings/locations/",
        login_required(businessView.as_view(template_name="app_business_settings_locations.html")),
        name="business-portal-settings-locations",
    ),
    path(
        "app/business/settings/notifications/",
        login_required(businessView.as_view(template_name="app_business_settings_notifications.html")),
        name="business-portal-settings-notifications",
    ),
]
