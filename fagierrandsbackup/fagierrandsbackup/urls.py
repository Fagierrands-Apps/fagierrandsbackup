from django.contrib import admin
import os
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from django.views.generic import RedirectView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from django.views.static import serve
from drf_yasg import openapi
from orders.views import deployment_check_view, AppVersionsView

schema_view = get_schema_view(
    openapi.Info(
        title="Fagi Errands API",
        default_version='v1',
        description="API for Fagi Errands application",
        terms_of_service="https://www.fagierrands.com/terms/",
        contact=openapi.Contact(email="contact@fagierrands.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


def robots_txt(request):
    """Serve static robots.txt file"""
    return serve(request, "robots.txt", document_root=os.path.join(settings.BASE_DIR, "static"))


urlpatterns = [
    path('robots.txt', robots_txt),
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico', permanent=True)),
    path('', deployment_check_view, name='root'),  # Root URL for deployment check
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/locations/', include('locations.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('api/dashboard/', include('admin_dashboard.urls')),
    path('api/voice/', include('voice.urls')),
    path('api/marketplace/', include('marketplace.urls')),
    # App meta
    path('api/app/meta/versions/', AppVersionsView.as_view(), name='app-versions'),
    # Docs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui-docs'),
]

# Serve static files in production
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Serve media files in debug mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)