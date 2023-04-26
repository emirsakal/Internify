from .models import Department, ClassRoom

def set_classroom(name, department):
	ClassRoom.objects.create(name=name, department=department, faculty=department.faculty)

def set_data():
	departments = Department.objects.all()
	
	for department in departments:
		set_classroom('Hazırlık', department)
		set_classroom('1. Sınıf', department)
		set_classroom('2. Sınıf', department)
		set_classroom('3. Sınıf', department)
		set_classroom('4. Sınıf', department)
