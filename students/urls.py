from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # Dashboard
    path('', views.dashboard, name='dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('teacher-dashboard/', views.teacher_dashboard, name='teacher_dashboard'),

    # Students
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.add_student, name='add_student'),
    path('students/<int:pk>/edit/', views.edit_student, name='edit_student'),
    path('students/<int:pk>/delete/', views.delete_student, name='delete_student'),
    path('students/<int:pk>/', views.student_detail, name='student_detail'),

    # Marks
    path('marks/', views.marks_view, name='marks'),
    path('marks/<int:pk>/delete/', views.delete_marks, name='delete_marks'),

    # Attendance
    path('attendance/', views.attendance_view, name='attendance'),
    path('attendance/report/', views.attendance_report, name='attendance_report'),

    # Subjects
    path('subjects/', views.subject_list, name='subjects'),
    path('subjects/<int:pk>/delete/', views.delete_subject, name='delete_subject'),

    # Users (admin only)
    path('users/', views.user_list, name='users'),
    path('users/add/', views.add_user, name='add_user'),
  ]