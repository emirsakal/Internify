from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('home/', views.index, name="index"),
    path('inbox/', views.inbox, name = "inbox"),
    path('inbox/send-message', views.sendmessage, name = "sendmessage"),
    path('inbox/message/<int:id>/', views.message, name = "message"), 
    path('profile/', views.profile, name = "profile"),

    # STUDENT URLS
    
    path('application-form/', views.internshipform, name = "internshipform"),
    path('official-letter/', views.officialletter, name = "officialletter"),
    path('internship-opportunities/', views.internshipopp, name = "internshipopp"),

    # CAREER CENTER URLS
    path('sgk-ef/', views.sgkef, name = "sgkef"),
    path('add-internship/', views.addInternship, name = "addinternship"),

    # TEACHER URLS
    path('staff/application-form', views.applicationform, name="applicationform"),
    path('official-letters/', views.offletters, name="offletters"),
    path('staff/application-form/detail', views.detail, name = "detail"),
    path('official-letters/detail', views.detail, name = "detail"),

    # USER URLS
    path('login/', views.loginUser, name="login"),
    path('login/staff', views.loginStaff, name="loginStaff"),
    path('logout/', views.logoutUser, name="logout"),
]