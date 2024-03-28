from django.urls import path
from pereval_data.views import PerevalCreateViewset
from drf_yasg import openapi
from rest_framework import permissions
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
   openapi.Info(
      title="PerevalApi",
      default_version='v1',
      description="Test description",
      terms_of_service="https://pereval.online/",
      contact=openapi.Contact(email="denisevostyanov7@gmail.com"),
      license=openapi.License(name="D3n1s"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [

    path('submitData/', PerevalCreateViewset.as_view({'get': 'list'}), name='pereval'),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),



]




