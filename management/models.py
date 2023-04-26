from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models import CASCADE

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
    photo = models.ImageField(upload_to='users', null=True)

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

class Message(BaseAbstractModel):
    title = models.CharField(max_length=255)
    content = models.TextField()    
    sender = models.ForeignKey(User, on_delete=CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=CASCADE, related_name='receiver')
    
    def __str__(self):
        return f'{self.title} | {self.sender.email}'

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
    student = models.ForeignKey(Student, on_delete=CASCADE)
    coordinator = models.ForeignKey(InternshipCoordinator, on_delete=CASCADE)
    employee = models.ForeignKey(CareerCenterEmployee, on_delete=CASCADE)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    
    def __str__(self):
        return f'{self.id} | {self.status}'

class Document(BaseAbstractModel):
    document = models.FileField(upload_to='files')
    application = models.ForeignKey(Application, on_delete=CASCADE)
    
    def __str__(self):
        return f'{self.application.id} | {self.application.status}'