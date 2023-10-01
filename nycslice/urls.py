"""
URL configuration for nycslice project.

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
from django.contrib import admin
from django.urls import path
from slice import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register, name="register"),
    path('logout/', views.logoutUser, name="logout"),
    path('login/', views.loginUser, name="login"),
    path('profile/', views.profile, name="profile"),
    path('plan/', views.plan, name='plan'),
    path('plan/1', views.plansub1, name='plansub1'),
    path('plan/2', views.plansub2, name='plansub2'),
    path('plan/3', views.plansub3, name='plansub3'),
    path('', views.home, name="home"),
]

