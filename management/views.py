from django.shortcuts import render, redirect
from .forms import StudentLoginForm, StaffLoginForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import Group

from .models import User, Student, InternshipCoordinator, CareerCenterEmployee

def index(request):
    return render(request, "index.html")

def inbox(request):
    return render(request, "inbox.html")

def sendmessage(request):
    return render(request, "sendmessage.html")

def message(request):
    return render(request, "message.html")

def profile(request):
    user = request.user
    context = {}
    
    if user.groups.filter(name='Student').exists():
        student = Student.objects.get(user=user)
        
        if student:
            context['student'] = student
        return render(request, "profile.html", context)
    elif user.groups.filter(name='Coordinator').exists():
        print(user)
        coordinator = InternshipCoordinator.objects.get(user=user)
        print(coordinator)
        if coordinator:
            context['coordinator'] = coordinator
        return render(request, "profile.html", context)

    return render(request, "profile.html")

# STUDENT

def internshipform(request):
    return render(request, "student/internshipform.html")

def officialletter(request):
    return render(request, "student/officialletter.html")

def internshipopp(request):
    return render(request, "student/internshipopp.html")

# CAREER CENTER

def sgkef(request):
    return render(request, "careercenter/sgkef.html")


# TEACHER

def applicationform(request):
    return render(request, "teacher/applicationform.html")

def offletters(request):
    return render(request, "teacher/offletters.html")

def detail(request):
    return render(request, "detail.html")

# USER

def loginUser(request):
    form = StudentLoginForm(request.POST or None)

    context = {
        "StudentForm" : form
    }
    
    if form.is_valid():
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(username=email, password=password)
        
        print(user, email, password)
        
        if user is None:
            messages.info(request,"Email or password is wrong.")
            return render(request,"login.html",context)
        
        if user.groups.filter(name='Coordinator').exists() or user.groups.filter(name='Staff').exists():
            messages.info(request,"Please switch to the other login page.")
            return render(request,"login.html",context)
        
        if user.groups.filter(name = 'Student').exists():
            messages.success(request,"You successfully logged in.")
            login(request,user)
            return redirect("index")
    
    return render(request,"login.html", context)

def loginStaff(request):
    StaffForm = StaffLoginForm(request.POST or None)

    context = {
        "StaffForm" : StaffForm
    }

    if StaffForm.is_valid():
        email = StaffForm.cleaned_data.get("email")
        password = StaffForm.cleaned_data.get("password")
        
        user = authenticate(username=email, password=password)

        if user is None:
            messages.info(request,"Username or Password is wrong.")
            return render(request,"loginStaff.html",context)
        
        if user.groups.filter(name='Student').exists():
            messages.info(request,"Please switch to the other login page.")
            return render(request,"loginStaff.html",context)
        
        if user.groups.filter(name = 'Coordinator').exists() or user.groups.filter(name = 'Staff').exists():
            messages.success(request,"You successfully logged in.")
            login(request, user)
            return redirect("index")

    return render(request,"loginStaff.html", context)

def logoutUser(request):
    logout(request)
    messages.success(request,"You logged out succesfully.")
    
    return redirect("login")