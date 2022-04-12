from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from core.admin import admin as base_admin

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description='TODO swagger API description',
        terms_of_service='https://www.google.com/policies/terms/',
        contact=openapi.Contact(email="admin@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    url=settings.SWAGGER_API_PATH,
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('admin/', base_admin.urls),
    path('users/', include('user.urls')),
    path('todos/', include('todo.urls')),
    path('auth/', include('user.auth_urls')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

]


# Static endpoints
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
