from django.contrib import admin
from .models import User, Student, Attendance, Marks
# Register your models here.

admin.site.register(User)
admin.site.register(Student)
admin.site.register(Attendance)
admin.site.register(Marks)