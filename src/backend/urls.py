from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from dashboards.sites import dashboards_admin_site
from dashboards.views import HomeView
from .api import UserViewSet
from django.urls import include, path, re_path
from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from search import views as search_views
from .api import api_router
schema_view = get_schema_view(
   openapi.Info(
      title=" Platform API",
      default_version='v1',
      description="comprehensive tools",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@simplyledgers.systems"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

router = routers.DefaultRouter()
router.register("users", UserViewSet, basename="api-users")

urlpatterns = [
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
    ),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/", include(router.urls)),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("admin/", dashboards_admin_site.urls),
    # path("admin/", admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', include('friends.urls')),
    path('', include('chat.urls')),
        # User urls
    # path("", include("akyc.urls")), //uncomment change here
    # marketplace urls
    path("", include("business.urls")),
    # auth urls
    
    path("", include("auth.urls")),
    path("", include("publishing.urls")),
        # Dashboard urls
    path("dashboards/", include("dashboards.urls")),
    # Other URL patterns for the project
    path('api-doc/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/v2/', api_router.urls),
    path("website/", HomeView.as_view(), name="website"),
    path("cms/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),
    re_path(r'^', include(wagtail_urls)),
    path("__debug__/", include("debug_toolbar.urls")),
] 

# if settings.DEBUG:
#     urlpatterns += staticfiles_urlpatterns()
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
urlpatterns = urlpatterns + [
    path("", include(wagtail_urls)),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)