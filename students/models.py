from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# CUSTOM USER
class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='teacher')

    def __str__(self):
        return f"{self.username} ({self.role})"

    def is_admin_user(self):
        return self.role == 'admin'

    def is_teacher_user(self):
        return self.role == 'teacher'


# STUDENT
class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20, unique=True)
    student_class = models.CharField(max_length=20)
    parent_phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.roll_number})"


# SUBJECT
class Subject(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


# ATTENDANCE
class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    status = models.BooleanField(default=False, help_text="True = Present, False = Absent")
    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='recorded_attendances'
    )

    class Meta:
        unique_together = ('student', 'date')
        ordering = ['-date']

    def __str__(self):
        status_str = "Present" if self.status else "Absent"
        return f"{self.student.name} - {self.date} - {status_str}"


# MARKS
class Marks(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='marks')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='marks')
    marks = models.PositiveIntegerField()
    max_marks = models.PositiveIntegerField(default=100)
    entered_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='entered_marks'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'subject')
        ordering = ['-created_at']

    @property
    def grade(self):
        if self.max_marks == 0:
            return 'N/A'
        percentage = (self.marks / self.max_marks) * 100
        if percentage >= 90:
            return 'A+'
        elif percentage >= 75:
            return 'A'
        elif percentage >= 60:
            return 'B'
        elif percentage >= 50:
            return 'C'
        elif percentage >= 35:
            return 'D'
        else:
            return 'F'

