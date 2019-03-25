"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path, include, re_path
from sec import views as sec_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', sec_view.register, name='register'),
	path('api/login/', sec_view.login_api, name='login_api'),
	path('faq/', sec_view.faq, name='faq'),
	path('teacher/', sec_view.teacher, name='teacher'),
	path('qr/<str:key>/display/', sec_view.qr, name='qr'),
	path('capture/<str:key>/attend', sec_view.capture, name='capture'),
	path('profile/edit/', sec_view.edit, name='edit'),
	path('login/', auth_views.LoginView.as_view(template_name='sec/login.html'), name='login'),
	path('logout/', auth_views.LogoutView.as_view(template_name='sec/logout.html'), name='logout'),
	path('profile/', sec_view.profile, name='profile'),
	path('profile/password/', sec_view.change_password, name='change_password'),
	path('', sec_view.home, name='home'),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
