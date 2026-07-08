import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from students.models import Student, Subject, Attendance, Marks
import datetime

User = get_user_model()

print("Creating sample data...")

# 1. Create a Teacher
teacher, created = User.objects.get_or_create(
    username="teacher1",
    email="teacher1@example.com",
    defaults={"role": "teacher"}
)
if created:
    teacher.set_password("TeacherPass123!")
    teacher.save()
    print("Created teacher user: teacher1 / TeacherPass123!")
else:
    print("Teacher user teacher1 already exists.")

# 2. Create Subjects
math, _ = Subject.objects.get_or_create(name="Mathematics")
science, _ = Subject.objects.get_or_create(name="Science")
english, _ = Subject.objects.get_or_create(name="English")
print("Created subjects: Mathematics, Science, English")

# 3. Create Students
students_data = [
    {"name": "Alice Johnson", "roll_number": "S001", "student_class": "Class 10", "parent_phone": "9876543210"},
    {"name": "Bob Smith", "roll_number": "S002", "student_class": "Class 10", "parent_phone": "9876543211"},
    {"name": "Charlie Brown", "roll_number": "S003", "student_class": "Class 10", "parent_phone": "9876543212"},
    {"name": "Diana Prince", "roll_number": "S004", "student_class": "Class 10", "parent_phone": "9876543213"},
    {"name": "Evan Wright", "roll_number": "S005", "student_class": "Class 10", "parent_phone": "9876543214"},
]

students = []
for data in students_data:
    student, created = Student.objects.get_or_create(
        roll_number=data["roll_number"],
        defaults={
            "name": data["name"],
            "student_class": data["student_class"],
            "parent_phone": data["parent_phone"]
        }
    )
    students.append(student)
print(f"Created/verified {len(students)} students.")

# 4. Create Attendance
today = datetime.date.today()
for i, student in enumerate(students):
    status = (i % 2 == 0)  # Alternate present/absent
    Attendance.objects.get_or_create(
        student=student,
        date=today,
        defaults={"status": status, "recorded_by": teacher}
    )
print("Created sample attendance records for today.")

# 5. Create Marks
for student in students:
    Marks.objects.get_or_create(
        student=student,
        subject=math,
        defaults={"marks": 85, "max_marks": 100, "entered_by": teacher}
    )
    Marks.objects.get_or_create(
        student=student,
        subject=science,
        defaults={"marks": 90, "max_marks": 100, "entered_by": teacher}
    )
print("Created sample marks for students.")
print("Sample data populated successfully!")
