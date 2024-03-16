from django.contrib import admin
from django.urls import path, include, re_path
from users import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('images/', include('images.urls')),
    re_path('account/login', views.login),
    re_path('account/signup', views.signup),
    re_path('account/test_token', views.test_token),
    re_path('account/verify-email', views.verify_email),
]
