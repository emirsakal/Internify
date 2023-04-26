from django.shortcuts import render, HttpResponse, redirect
from .forms import RegisterForm, StudentLoginForm, StaffLoginForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import Group

from .models import User

def index(request):
    return render(request, "index.html")

def inbox(request):
    return render(request, "inbox.html")

def sendmessage(request):
    return render(request, "sendmessage.html")

def message(request):
    return render(request, "message.html")

def profile(request):
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

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            gender = form.cleaned_data.get("gender")
            type = form.cleaned_data.get("type")
            
            new_user = User(first_name=first_name, last_name=last_name, email=email, password=password, gender=gender)
            new_user.set_password(password)

            new_user.save()
            
            if type == 'Student':
                group = Group.objects.get(name='Student')
                new_user.groups.add(group)
            elif type == 'Coordinator':
                group = Group.objects.get(name='Coordinator')
                new_user.groups.add(group)
            else:
                group = Group.objects.get(name='Staff')
                new_user.groups.add(group)
            
            login(request, new_user)
            messages.success(request,"You have succesfully registered.")

            return redirect("index")
        
        context = {
                "form" : form
            }
        return render(request,"register.html",context)
    else:
        form = RegisterForm()
        context = {
        "form" : form
        }
        return render(request, "register.html", context)

def loginUser(request):
    form = StudentLoginForm(request.POST or None)

    context = {
        "StudentForm" : form
    }
    
    if form.is_valid():
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(email=email, password=password)

        if user is None:
            messages.info(request,"Email or password is wrong.")
            return render(request,"login.html",context)
        
        if user.groups.filter(name = 'Teacher').exists() or StudentUser.groups.filter(name = 'CareerCenter').exists():
            messages.info(request,"Please switch to the other login page.")
            return render(request,"login.html",context)
        if user.groups.filter(name = 'Student').exists():
            messages.success(request,"You successfully logged in.")
            login(request,StudentUser)
            return redirect("index")
    
    return render(request,"login.html", context)

def loginStaff(request):
    StaffForm = StaffLoginForm(request.POST or None)

    context = {
        "StaffForm" : StaffForm
    }

    if StaffForm.is_valid():
        StaffUsername = StaffForm.cleaned_data.get("username")
        StaffPassword = StaffForm.cleaned_data.get("password")
        StaffUser = authenticate(username = StaffUsername, password = StaffPassword)

        if StaffUser is None:
            messages.info(request,"Username or Password is wrong.")
            return render(request,"loginStaff.html",context)
        
        if StaffUser.groups.filter(name = 'Student').exists():
            messages.info(request,"Please switch to the other login page.")
            return render(request,"loginStaff.html",context)
        
        if StaffUser.groups.filter(name = 'Teacher').exists() or StaffUser.groups.filter(name = 'CareerCenter').exists():
            messages.success(request,"You successfully logged in.")
            login(request,StaffUser)
            return redirect("index")

    return render(request,"loginStaff.html", context)

def logoutUser(request):
    logout(request)
    messages.success(request,"You logged out succesfully.")
    return redirect("login")