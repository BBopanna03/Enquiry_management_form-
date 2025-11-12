"""
URL configuration for student_enquiry project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from users import views

schema_view = get_schema_view(
   openapi.Info(
      title="Student Enquiry Management API", 
      default_version='v1',                    
      description="API documentation for managing student enquiries, courses, and batches with role-based access.",
      terms_of_service="https://yourdomain.com/terms/",  
      contact=openapi.Contact(email="admin@yourdomain.com"),  
      license=openapi.License(name="MIT License"),  
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),  
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include("users.urls")),
    path('token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Note: TokenRefresh and TokenVerify views don't exist in current views.py
    # Using Django REST framework's built-in views instead
    # path('token/refresh/', views.TokenRefresh.as_view(), name='token_refresh'),
    # path('token/verify/', views.TokenVerify.as_view(), name='token_verify'),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]