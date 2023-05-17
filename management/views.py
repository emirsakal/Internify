from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.db.models import Q

from .models import Student, InternshipCoordinator, CareerCenterEmployee, Application, Document, Message, User
from .forms import StudentLoginForm, StaffLoginForm

def index(request):
    return render(request, "index.html")

def inbox(request):
    user = request.user
    if request.method == "POST":
        email = request.POST['email']
        title = request.POST['title']
        content = request.POST['content']
        
        user_arr = User.objects.filter(email=email)
        
        if len(user_arr) <= 0:
            messages.warning(request,"User not found!")
            return redirect(reverse('sendmessage'))
        
        user = user_arr[0]
        
        if user.email == request.user.email:
            messages.warning(request,"You can not send message to yourself.")
            return redirect(reverse('sendmessage'))
        message = Message.objects.create(title=title, content=content, receiver=user, sender=request.user, parent=None)
        message.save()
        
        messages.success(request,"message sent successfully!")
        return redirect(reverse('inbox'))
    
    emails = Message.objects.filter((Q(sender=request.user) | Q(receiver=request.user)) & Q(parent=None)).order_by('-date_created')
    
    context = {
        'emails': emails
    }
    return render(request, "inbox.html", context)

def sendmessage(request):
    return render(request, "sendmessage.html")

def message(request, id):
    parent = Message.objects.get(pk=id)
    
    if request.method == "POST":
        email = request.POST['email']
        title = request.POST['title']
        content = request.POST['content']
        
        receiver = User.objects.get(email=email)
        child = Message.objects.create(title=title, content=content, receiver=receiver, sender=request.user, parent=parent)
        child.save()
        
        return redirect(f'/inbox/message/{parent.id}/')

    children = Message.objects.filter(parent=parent)
    
    context = {
        'email': parent
    }
    
    if len(children) > 0:
        context['children'] = children

    return render(request, "message.html", context)

def profile(request):
    user = request.user
    if request.method == "POST":
        if 'photo' in request.FILES:
            user.photo = request.FILES['photo']
            user.save()
        return redirect(reverse('profile'))
    
    context = {}
    
    if user.groups.filter(name='Student').exists():
        student = Student.objects.get(user=user)
        
        if student:
            context['student'] = student
        return render(request, "profile.html", context)
    elif user.groups.filter(name='Coordinator').exists():
        coordinator = InternshipCoordinator.objects.get(user=user)

        if coordinator:
            context['coordinator'] = coordinator
        return render(request, "profile.html", context)

    return render(request, "profile.html")

# STUDENT

def internshipform(request):
    user = request.user
    student = Student.objects.get(user=user)
    
    if request.method == 'POST':
        if 'internship_form' in request.FILES:
            coordinator = InternshipCoordinator.objects.filter(department=student.department)
            staff = CareerCenterEmployee.objects.get(employee_id=1)
            if len(coordinator) > 0:
                application = Application.objects.create(coordinator=coordinator[0], student=student, employee=staff, status='W', type='I')
                application.save()
                
                document = Document.objects.create(document=request.FILES['internship_form'], application=application)
                document.save()
                return redirect(reverse('internshipform'))
    
    applications = Application.objects.filter(student=student, type='I').order_by('-date_created')
    
    context = {
        'applications': applications
    }
    
    return render(request, "student/internshipform.html", context)

def officialletter(request):
    user = request.user
    student = Student.objects.get(user=user)
    
    if request.method == 'POST':
        if 'transcript' in request.FILES:
            coordinator = InternshipCoordinator.objects.filter(department=student.department)
            staff = CareerCenterEmployee.objects.get(employee_id=1)
            if len(coordinator) > 0:
                application = Application.objects.create(coordinator=coordinator[0], student=student, employee=staff, status='W', type='L')
                application.save()
                
                document = Document.objects.create(document=request.FILES['transcript'], application=application)
                document.save()
                return redirect(reverse('officialletter'))
    
    applications = Application.objects.filter(student=student, type='L').order_by('-date_created')
    
    context = {
        'applications': applications
    }
    
    return render(request, "student/officialletter.html", context)

def internshipopp(request):
    return render(request, "student/internshipopp.html")

# CAREER CENTER

def sgkef(request):
    return render(request, "careercenter/sgkef.html")


# TEACHER

def applicationform(request):
    user = request.user
    
    coordinator = InternshipCoordinator.objects.filter(user=user)
    
    if len(coordinator) != 1:
        messages.warning('invalid user')
        return render(request, "teacher/applicationform.html")    
    
    applications =  Application.objects.filter(coordinator=coordinator[0], type='I')
    
    context = {
        "applications": applications
    }
    
    return render(request, "teacher/applicationform.html", context)

def offletters(request):
    user = request.user
    
    coordinator = InternshipCoordinator.objects.filter(user=user)
    
    if len(coordinator) != 1:
        messages.warning('invalid user')
        return render(request, "teacher/applicationform.html")    
    
    applications =  Application.objects.filter(coordinator=coordinator[0], type='L')
    
    context = {
        "applications": applications
    }
    
    return render(request, "teacher/offletters.html", context)

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