"""
URL configuration for ollegro_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import yaml
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view
from rest_framework.schemas.openapi import SchemaGenerator
from django.http import HttpResponse
from django.conf import settings
from pathlib import Path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/user/', include('users.urls')),
    path('api/products/', include('products.urls')),
    path('api/payments/', include('ollegro_payments.urls')),
]


class TOSSchemaGenerator(SchemaGenerator):
    http_method_names = ['get']
    def get_schema(self, *args, **kwargs):
        with open(Path(settings.BASE_DIR, './openapi-schema.yml'), 'rb') as schema_file:
            yaml_data = yaml.safe_load(schema_file)
        schema = {
            'openapi': '3.0.2',
            'info': self.get_info(),
            'paths': yaml_data.get('paths', {}),
            'components': yaml_data.get('components', {}),
        }

        return schema


# urlpatterns += [
#     # path('api/openapi-v2', TOSSchemaGenerator.as_view(), name='openapi-schema-v2'),
#     path('api/openapi-v2', get_schema_view(
#         title="Your Project",
#         description="API for all things",
#         version="1.0.2",
#         generator_class=TOSSchemaGenerator,
#     ), name='openapi-schema-v2'),
#     path('api/swagger-ui/', TemplateView.as_view(
#         template_name='swagger-ui.html',
#         extra_context={'schema_url':'openapi-schema-v2'}
#     ), name='swagger-ui'),
#     path('api/redoc/', TemplateView.as_view(
#         template_name='redoc.html',
#         extra_context={'schema_url':'openapi-schema-v2'}
#     ), name='redoc'),
# ]

urlpatterns += [
    # YOUR PATTERNS
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]