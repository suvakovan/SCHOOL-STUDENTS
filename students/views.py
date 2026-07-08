from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Count
from django.utils import timezone
from .models import Student, Attendance, Marks, Subject, User
from .forms import (
    LoginForm, StudentForm, MarksForm,
    AttendanceForm, SubjectForm, UserCreateForm
)
import datetime


# ─────────────────────────────────────────────
# AUTH VIEWS
# ─────────────────────────────────────────────

def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


# ─────────────────────────────────────────────
# DASHBOARD VIEWS
# ─────────────────────────────────────────────

@login_required
def dashboard(request):
    if request.user.role == 'admin':
        return redirect('admin_dashboard')
    return redirect('teacher_dashboard')


@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('teacher_dashboard')

    today = datetime.date.today()
    total_students = Student.objects.count()
    total_subjects = Subject.objects.count()
    total_teachers = User.objects.filter(role='teacher').count()
    today_attendance = Attendance.objects.filter(date=today)
    present_today = today_attendance.filter(status=True).count()
    absent_today = today_attendance.filter(status=False).count()

    # Chart data: attendance for last 7 days
    labels = []
    present_data = []
    absent_data = []
    for i in range(6, -1, -1):
        day = today - datetime.timedelta(days=i)
        labels.append(day.strftime('%d %b'))
        att = Attendance.objects.filter(date=day)
        present_data.append(att.filter(status=True).count())
        absent_data.append(att.filter(status=False).count())

    # Top performers
    top_students = (
        Marks.objects.values('student__name')
        .annotate(avg=Avg('marks'))
        .order_by('-avg')[:5]
    )

    return render(request, 'admin_dashboard.html', {
        'total_students': total_students,
        'total_subjects': total_subjects,
        'total_teachers': total_teachers,
        'present_today': present_today,
        'absent_today': absent_today,
        'chart_labels': labels,
        'present_data': present_data,
        'absent_data': absent_data,
        'top_students': top_students,
    })


@login_required
def teacher_dashboard(request):
    marks = Marks.objects.filter(entered_by=request.user)
    avg_marks = marks.aggregate(Avg('marks'))['marks__avg'] or 0
    today = datetime.date.today()
    today_attendance = Attendance.objects.filter(
        recorded_by=request.user, date=today
    )

    # Subject-wise average for this teacher
    subject_avgs = (
        marks.values('subject__name')
        .annotate(avg=Avg('marks'))
        .order_by('subject__name')
    )
    sub_labels = [s['subject__name'] for s in subject_avgs]
    sub_avgs = [round(s['avg'], 1) for s in subject_avgs]

    return render(request, 'teacher_dashboard.html', {
        'my_marks_count': marks.count(),
        'avg_marks': round(avg_marks, 2),
        'today_attendance_count': today_attendance.count(),
        'subject_labels': sub_labels,
        'subject_avgs': sub_avgs,
    })


# ─────────────────────────────────────────────
# STUDENT VIEWS
# ─────────────────────────────────────────────

@login_required
def student_list(request):
    q = request.GET.get('q', '').strip()
    students = Student.objects.all()
    if q:
        students = students.filter(name__icontains=q) | students.filter(roll_number__icontains=q)
    return render(request, 'list.html', {'students': students, 'q': q})


@login_required
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student added successfully!')
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'add_student.html', {'form': form, 'title': 'Add Student'})


@login_required
def edit_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student updated successfully!')
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'add_student.html', {'form': form, 'title': 'Edit Student', 'student': student})


@login_required
def delete_student(request, pk):
    if request.user.role != 'admin':
        messages.error(request, 'Only admins can delete students.')
        return redirect('student_list')
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student deleted.')
        return redirect('student_list')
    return render(request, 'confirm_delete.html', {'object': student, 'type': 'Student'})


@login_required
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    student_marks = Marks.objects.filter(student=student)
    
    # Full queryset for counting
    all_attendances = Attendance.objects.filter(student=student)
    total_days = all_attendances.count()
    present_days = all_attendances.filter(status=True).count()
    attendance_pct = round((present_days / total_days) * 100, 1) if total_days else 0
    
    # Sliced queryset only for display in template
    attendances = all_attendances.order_by('-date')[:30]
    
    return render(request, 'student_detail.html', {
        'student': student,
        'marks': student_marks,
        'attendances': attendances,
        'total_days': total_days,
        'present_days': present_days,
        'attendance_pct': attendance_pct,
    })

# ─────────────────────────────────────────────
# MARKS VIEWS
# ─────────────────────────────────────────────

@login_required
def marks_view(request):
    if request.method == 'POST':
        form = MarksForm(request.POST)
        if form.is_valid():
            mark = form.save(commit=False)
            mark.entered_by = request.user
            mark.save()
            messages.success(request, 'Marks saved successfully!')
            return redirect('marks')
    else:
        form = MarksForm()

    all_marks = Marks.objects.select_related('student', 'subject', 'entered_by').all()
    return render(request, 'marks.html', {'form': form, 'all_marks': all_marks})


@login_required
def delete_marks(request, pk):
    mark = get_object_or_404(Marks, pk=pk)
    if request.user.role != 'admin' and mark.entered_by != request.user:
        messages.error(request, 'Permission denied.')
        return redirect('marks')
    mark.delete()
    messages.success(request, 'Marks record deleted.')
    return redirect('marks')


# ─────────────────────────────────────────────
# ATTENDANCE VIEWS
# ─────────────────────────────────────────────

@login_required
def attendance_view(request):
    students = Student.objects.all()
    date_str = request.GET.get('date') or datetime.date.today().isoformat()
    try:
        selected_date = datetime.date.fromisoformat(date_str)
    except ValueError:
        selected_date = datetime.date.today()

    # Existing attendance for this date
    existing = {a.student_id: a.status for a in Attendance.objects.filter(date=selected_date)}

    if request.method == 'POST':
        date_val = request.POST.get('date')
        try:
            att_date = datetime.date.fromisoformat(date_val)
        except (ValueError, TypeError):
            att_date = datetime.date.today()

        for student in students:
            is_present = str(student.id) in request.POST
            Attendance.objects.update_or_create(
                student=student,
                date=att_date,
                defaults={'status': is_present, 'recorded_by': request.user}
            )
        messages.success(request, f'Attendance saved for {att_date}!')
        return redirect(f'/attendance/?date={att_date}')

    return render(request, 'attendance.html', {
        'students': students,
        'selected_date': selected_date,
        'existing': existing,
    })


@login_required
def attendance_report(request):
    students = Student.objects.all()
    report = []
    for student in students:
        total = Attendance.objects.filter(student=student).count()
        present = Attendance.objects.filter(student=student, status=True).count()
        pct = round((present / total) * 100, 1) if total else 0
        report.append({
            'student': student,
            'total': total,
            'present': present,
            'absent': total - present,
            'pct': pct,
        })
    return render(request, 'attendance_report.html', {'report': report})


# ─────────────────────────────────────────────
# SUBJECT VIEWS
# ─────────────────────────────────────────────
@login_required
def subject_list(request):
    if request.user.role != 'admin':
        messages.error(request, 'Only admins can manage subjects.')
        return redirect('dashboard')

    GRADE_SUBJECTS = {
        'primary': {  # Classes 1–10
            'grades': [str(i) for i in range(1, 11)],
            'subjects': ['Language 1', 'Language 2', 'Mathematics', 'Science', 'Social Science']
        },
        'higher': {  # Classes 11–12
            'grades': ['11', '12'],
            'subjects': [
                'Language 1', 'Language 2', 'Mathematics', 'Physics', 'Chemistry',
                'Biology', 'Zoology', 'Botany', 'Computer Science', 'Computer Application',
                'Business Maths', 'Commerce', 'Statistics', 'Economics',
                'History', 'Geography', 'Civics'
            ]
        }
    }

    subjects = Subject.objects.all()
    form = SubjectForm()

    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subject added!')
            return redirect('subjects')

    return render(request, 'subjects.html', {
        'subjects': subjects,
        'form': form,
        'grade_subjects': GRADE_SUBJECTS,
    })

# ─────────────────────────────────────────────
# USER MANAGEMENT (Admin only)
# ─────────────────────────────────────────────

@login_required
def user_list(request):
    if request.user.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    users = User.objects.all()
    return render(request, 'users.html', {'users': users})


@login_required
def add_user(request):
    if request.user.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User created successfully!')
            return redirect('users')
    else:
        form = UserCreateForm()
    return render(request, 'add_user.html', {'form': form})
# ─────────────────────────────────────────────
# delete
# ─────────────────────────────────────────────
@login_required
def delete_subject(request, pk):
    if request.user.role != 'admin':
        messages.error(request, 'Permission denied.')
        return redirect('subjects')
    subject = get_object_or_404(Subject, pk=pk)
    subject.delete()
    messages.success(request, 'Subject deleted.')
    return redirect('subjects')