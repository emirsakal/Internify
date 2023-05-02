"""
URL configuration for Internify project.

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
from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from management import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.index, name="index"),
    path('home/', views.index, name="index"),
    path('inbox/', views.inbox, name = "inbox"),
    path('inbox/send-message', views.sendmessage, name = "sendmessage"),
    path('inbox/message', views.message, name = "message"), 
    path('profile/', views.profile, name = "profile"),
    #path('user/', include("user.urls")),

    # STUDENT URLS
    
    path('application-form/', views.internshipform, name = "internshipform"),
    path('official-letter/', views.officialletter, name = "officialletter"),
    path('internship-opportunities/', views.internshipopp, name = "internshipopp"),

    # CAREER CENTER URLS
    path('sgk-ef/', views.sgkef, name = "sgkef"),

    # TEACHER URLS
    path('teacher/internship-application-form', views.applicationform, name="applicationform"),
    path('official-letters/', views.offletters, name="offletters"),
    path('teacher/internship-application-form/detail', views.detail, name = "detail"),
    path('official-letters/detail', views.detail, name = "detail"),

    # USER URLS
    path('login/', views.loginUser, name="login"),
    path('login/staff', views.loginStaff, name="loginStaff"),
    path('logout/', views.logoutUser, name="logout"),
]
