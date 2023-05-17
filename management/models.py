from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models import CASCADE, SET_NULL
from django.urls import reverse

class BaseAbstractModel(models.Model):
    is_visible = models.BooleanField(default=True, verbose_name='Visibility')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Faculty(BaseAbstractModel):
    name = models.CharField(max_length=150)
    
    def __str__(self):
        return self.name

class Department(BaseAbstractModel):
    name = models.CharField(max_length=200)
    faculty = models.ForeignKey(Faculty, on_delete=CASCADE)
    
    def __str__(self):
        return f'{self.name} | {self.faculty.name}'

class ClassRoom(BaseAbstractModel):
    name = models.CharField(max_length=250)  
    department = models.ForeignKey(Department, on_delete=CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=CASCADE)

    def __str__(self):
        return f'{self.name} | {self.department.name}'

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    photo = models.ImageField(upload_to='users', null=True, blank=True)

    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'gender',  'password']

    def __str__(self):
        return f'{self.first_name} | {self.email}'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

class Message(BaseAbstractModel):
    title = models.CharField(max_length=255)
    content = models.TextField()    
    sender = models.ForeignKey(User, on_delete=CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=CASCADE, related_name='receiver')
    parent = models.ForeignKey('self', on_delete=SET_NULL, null=True, related_name='parentnode')
    def __str__(self):
        return f'{self.title} | {self.sender.email}'
    
    def get_absolute_url(self):
        return reverse('message', args=[str(self.id)])

class Student(BaseAbstractModel):
    student_id = models.CharField(max_length=20, primary_key=True, unique=True)
    department = models.ForeignKey(Department, on_delete=CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=CASCADE)
    class_room = models.ForeignKey(ClassRoom, on_delete=CASCADE)
    user = models.ForeignKey(User, on_delete=CASCADE)
    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} | {self.student_id}'

class InternshipCoordinator(BaseAbstractModel):
    coordinator_id = models.CharField(max_length=20, primary_key=True, unique=True)
    department = models.ForeignKey(Department, on_delete=CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=CASCADE)
    user = models.ForeignKey(User, on_delete=CASCADE)
    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} | {self.coordinator_id}'

class CareerCenterEmployee(BaseAbstractModel):
    employee_id = models.CharField(max_length=20, primary_key=True, unique=True)
    user = models.ForeignKey(User, on_delete=CASCADE)
    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} | {self.employee_id}'

class Application(BaseAbstractModel):
    STATUS_CHOICES = (
        ('W', 'Waiting'),
        ('R', 'Rejected'),
        ('A', 'Approved'),
    )
    TYPE_CHOICES = (
        ('L', 'Letter'),
        ('I', 'Internship'),
    )
    student = models.ForeignKey(Student, on_delete=CASCADE)
    coordinator = models.ForeignKey(InternshipCoordinator, on_delete=CASCADE)
    employee = models.ForeignKey(CareerCenterEmployee, on_delete=CASCADE)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    type = models.CharField(max_length=1, choices=TYPE_CHOICES, default='I')
    def __str__(self):
        return f'{self.id} | {self.status}'

class Document(BaseAbstractModel):
    document = models.FileField(upload_to='files')
    application = models.ForeignKey(Application, on_delete=CASCADE)
    
    def __str__(self):
        return f'{self.application.id} | {self.application.status}'