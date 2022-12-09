"""lfjennings URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings 
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib import admin


admin.site.site_header = 'L.F. Jennings Admin Panel'
admin.site.site_title = 'L.F. Jennings'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('auth/', include('login_app.urls')),
    path('app/', include('app.urls')),
    
    path('password_reset', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_sent', auth_views.PasswordResetDoneView.as_view(), name='password_reset_sent'),
    path('password/<uidb64>/<token>/ ', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]