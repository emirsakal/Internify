from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.db.models import Q
from django.views.decorators.clickjacking import xframe_options_sameorigin

from .create_doc import create_letter

from .models import (
    	Student,
		InternshipCoordinator,
		CareerCenterEmployee,
		Application,
		Document,
		Message,
		User,
		Internship,
		Announcement,
		Province,
		Faculty,
		Department
	)
from .forms import StudentLoginForm, StaffLoginForm

def index(request):
	announcements = Announcement.objects.all().order_by('-date_created')[:3]
	context = {
		'announcements': announcements
	}
	return render(request, "index.html", context)

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
	
	emails = Message.objects.filter((Q(sender=request.user) | Q(receiver=request.user)) & Q(parent=None)).order_by('-date_updated')
	
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
				
				document = Document.objects.create(document=request.FILES['transcript'], application=application, type='S')
				document.save()
				return redirect(reverse('officialletter'))
	
	applications = Application.objects.filter(student=student, type='L').order_by('-date_created')
	documents = Document.objects.filter(application__in=applications)
	context = {
		'applications': applications,
		'documents': documents
	}
	
	return render(request, "student/officialletter.html", context)

def internshipopp(request):
	user = request.user

	if request.method == 'POST':
		company = request.POST['company']
		job = request.POST['job']
		start_date = request.POST['startdate']
		end_date = request.POST['enddate']
		url = request.POST['url']
		internship = Internship.objects.create(company=company, job=job, start_date=start_date, end_date=end_date, url=url)
		if 'province' in request.POST:
			province = Province.objects.get(name=request.POST['province'])
			internship.province = province
		
		if 'faculty' in request.POST:
			faculty = Faculty.objects.get(name=request.POST['faculty'])
			internship.faculty = faculty
		
		if 'department' in request.POST:
			department = Department.objects.get(name=request.POST['department'])
			internship.department = department
		
		if 'logo' in request.FILES:
			logo = request.FILES['logo']
			internship.logo = logo

		internship.save()
		return redirect(reverse('internshipopp'))

	if user.groups.all()[0].name == 'Student':
		student = Student.objects.get(user=user)
		internships = Internship.objects.filter(faculty=student.faculty).order_by('-date_created')[:20]
		return render(request, "student/internshipopp.html", {'internships':internships})
	
	
	provinces = Province.objects.all().order_by('name')
	internships = Internship.objects.all().order_by('-date_created')[:20]
	faculties = Faculty.objects.all()
	departments = Department.objects.all()

	context = {
		'provinces': provinces,
		'internships': internships,
		'faculties': faculties,
		'departments': departments,
	}
	return render(request, "student/internshipopp.html", context)

# CAREER CENTER

def sgkef(request):
	user = request.user
	employee = CareerCenterEmployee.objects.get(user=user)

	if request.method == 'POST':
		id = request.POST['application']
		status = request.POST['status']

		application = Application.objects.get(pk=id)
		title = request.POST['title']
		if status == 'archived':
			application.status = 'Z'

			file = request.FILES['insurance']
			document = Document.objects.create(document=file, application=application)
			document.save()

			url = request.build_absolute_uri(document.document.url)
			
			message = Message.objects.create(sender=user, 
				    receiver=application.student.user, 
					title=title,
					content=f'Your application has been approved by University. You can download your insurance from link below\n{url}',
					parent=None,
					)
			message.save()
	
		elif status == 'rejected':
			content = request.POST['content']
			message = Message.objects.create(sender=user, 
				    receiver=application.student.user, 
					title=title,
					content=content,
					parent=None,
					)
			message.save()
			application.status = 'R'
		application.save()

		return redirect(reverse('sgkef'))

	applications = Application.objects.filter(type='I', employee=employee, status='A').order_by('-date_created')
	documents = Document.objects.filter(application__employee=employee, application__type='I', application__status='A')
	
	context = {
		'applications': applications,
		'documents': documents,
	}
	return render(request, "careercenter/sgkef.html", context)


# TEACHER
@xframe_options_sameorigin
def applicationform(request):
	user = request.user
	
	if request.method == 'POST':
		id = request.POST['application']
		status = request.POST['status']

		application = Application.objects.get(pk=id)
		if status == 'approved':
			application.status = 'A'
		elif status == 'rejected' and 'receiver' in request.POST and 'title' in request.POST and 'content' in request.POST:
			application.status = 'R'

			receiver = request.POST['receiver']
			title = request.POST['title']
			content = request.POST['content']
			message = Message.objects.create(title=title, content=content, receiver=User.objects.get(email=receiver), sender=user, parent=None)
			message.save()

		application.save()
		return redirect(reverse('applicationform'))

	coordinator = InternshipCoordinator.objects.filter(user=user)
	
	if len(coordinator) != 1:
		messages.warning('invalid user')
		return render(request, "teacher/applicationform.html")    
	
	applications =  Application.objects.filter(coordinator=coordinator[0], type='I', status='W').order_by('-date_created')    
	documents = Document.objects.filter(application__coordinator=coordinator[0], application__type='I')
	
	context = {
		"applications": applications,
		"documents": documents
	}
	
	return render(request, "teacher/applicationform.html", context)

@xframe_options_sameorigin
def offletters(request):
	user = request.user
	
	if request.method == 'POST':
		id = request.POST['application']
		status = request.POST['status']

		application = Application.objects.get(pk=id)
		if status == 'approved':
			application.status = 'A'
			internship = request.POST['internship']
			student = application.student
			
			ch = ''
			if internship == '1':
				ch = 's'
				internship = '2'
			elif internship == '2':
				internship = '1'

			data = {
				'student': student.user.get_full_name(),
				'faculty': student.faculty.name,
				'department': student.department.name,
				'date':	application.date_created.strftime('%d.%m.%Y'),
				'staff': user.get_full_name(),
				'internship': internship,
				'count': ch,
			}
			
			file = create_letter(data, student.student_id)

			document = Document.objects.create(document='\\files\\'+ file, application=application, type='G')
			document.save()

			message = Message.objects.create(sender=user, 
				    receiver=student.user, 
					title=request.POST['title'], 
					content='Your application for internship letter has been approved. You can download your letter official letters page\n',
					parent=None)
			message.save()

		elif status == 'rejected':
			application.status = 'R'

			receiver = request.POST['receiver']
			title = request.POST['title']
			content = request.POST['content']
			message = Message.objects.create(title=title, content=content, receiver=User.objects.get(email=receiver), sender=user, parent=None)
			message.save()

		application.save()
		return redirect(reverse('offletters'))

	coordinator = InternshipCoordinator.objects.filter(user=user)
	
	if len(coordinator) != 1:
		messages.warning('invalid user')
		return render(request, "teacher/applicationform.html")    
	
	applications =  Application.objects.filter(coordinator=coordinator[0], type='L', status='W').order_by('-date_created')
	documents = Document.objects.filter(application__coordinator=coordinator[0], application__type='L')
	
	context = {
		"applications": applications,
		"documents": documents
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