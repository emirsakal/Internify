from django.shortcuts import render, HttpResponse, redirect
from .forms import RegisterForm, StudentLoginForm, StaffLoginForm
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, authenticate, logout

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
            firstName = form.cleaned_data.get("firstName")
            lastName = form.cleaned_data.get("lastName")
            schoolID = form.cleaned_data.get("schoolID")
            profession = form.cleaned_data.get("profession")
            classes = form.cleaned_data.get("classes")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")

            newUser = User(first_name=firstName, last_name=lastName, username = schoolID , email=email)
            newUser.set_password(password)

            newUser.save()

            if profession == 'Student':
                group = Group.objects.get(name='Student')
                newUser.groups.add(group)
            elif profession == 'Teacher':
                group = Group.objects.get(name='Teacher')
                newUser.groups.add(group)
            elif profession == 'CareerCenter':
                group = Group.objects.get(name='CareerCenter')
                newUser.groups.add(group)

            if classes == 'Non-Student':
                group = Group.objects.get(name='Non-Student')
                newUser.groups.add(group)
            elif classes == '1.Class':
                group = Group.objects.get(name='1.Class')
                newUser.groups.add(group)
            elif classes == '2.Class':
                group = Group.objects.get(name='2.Class')
                newUser.groups.add(group)
            elif classes == '3.Class':
                group = Group.objects.get(name='3.Class')
                newUser.groups.add(group)
            elif classes == '4.Class':
                group = Group.objects.get(name='4.Class')
                newUser.groups.add(group)

            login(request, newUser)
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
    StudentForm = StudentLoginForm(request.POST or None)

    context = {
        "StudentForm" : StudentForm
    }
    
    if StudentForm.is_valid():
        StudentUsername = StudentForm.cleaned_data.get("username")
        StudentPassword = StudentForm.cleaned_data.get("password")
        StudentUser = authenticate(username = StudentUsername, password = StudentPassword)

        if StudentUser is None:
            messages.info(request,"Username or Password is wrong.")
            return render(request,"login.html",context)
        if StudentUser.groups.filter(name = 'Teacher').exists() or StudentUser.groups.filter(name = 'CareerCenter').exists():
            messages.info(request,"Please switch to the other login page.")
            return render(request,"login.html",context)
        if StudentUser.groups.filter(name = 'Student').exists():
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