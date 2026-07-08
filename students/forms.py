from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Student, Subject, Attendance, Marks, User
import datetime


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-input'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-input'})
    )


class StudentForm(forms.ModelForm):
    CLASS_CHOICES = [
        ('', '-- Select Class --'),
        ('1', 'Class 1'), ('2', 'Class 2'), ('3', 'Class 3'),
        ('4', 'Class 4'), ('5', 'Class 5'), ('6', 'Class 6'),
        ('7', 'Class 7'), ('8', 'Class 8'), ('9', 'Class 9'),
        ('10', 'Class 10'), ('11', 'Class 11'), ('12', 'Class 12'),
    ]

    student_class = forms.ChoiceField(
        choices=CLASS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-input'})
    )

    class Meta:
        model = Student
        fields = ['name', 'roll_number', 'student_class', 'parent_phone']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Full Name', 'class': 'form-input'}),
            'roll_number': forms.TextInput(attrs={'placeholder': 'Roll Number', 'class': 'form-input'}),
            'parent_phone': forms.TextInput(attrs={'placeholder': 'Parent Phone', 'class': 'form-input'}),
        }


class SubjectForm(forms.ModelForm):
    SUBJECT_CHOICES = [
        ('', '-- Select Subject --'),
        ('Language 1', 'Language 1'),
        ('Language 2', 'Language 2'),
        ('Mathematics', 'Mathematics'),
        ('Science', 'Science'),
        ('Social Science', 'Social Science'),
        ('Physics', 'Physics'),
        ('Chemistry', 'Chemistry'),
        ('Biology', 'Biology'),
        ('Zoology', 'Zoology'),
        ('Botany', 'Botany'),
        ('Computer Science', 'Computer Science'),
        ('Computer Application', 'Computer Application'),
        ('Business Maths', 'Business Maths'),
        ('Commerce', 'Commerce'),
        ('Statistics', 'Statistics'),
        ('Economics', 'Economics'),
        ('History', 'History'),
        ('Geography', 'Geography'),
        ('Civics', 'Civics'),
    ]

    name = forms.ChoiceField(
        choices=SUBJECT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-input'})
    )

    class Meta:
        model = Subject
        fields = ['name']


class MarksForm(forms.ModelForm):
    PRIMARY_SUBJECTS = ['Language 1', 'Language 2', 'Mathematics', 'Science', 'Social Science']
    HIGHER_SUBJECTS = [
        'Language 1', 'Language 2', 'Mathematics', 'Physics', 'Chemistry',
        'Biology', 'Zoology', 'Botany', 'Computer Science', 'Computer Application',
        'Business Maths', 'Commerce', 'Statistics', 'Economics',
        'History', 'Geography', 'Civics'
    ]

    class Meta:
        model = Marks
        fields = ['student', 'subject', 'marks', 'max_marks']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-input', 'id': 'id_student'}),
            'subject': forms.Select(attrs={'class': 'form-input', 'id': 'id_subject'}),
            'marks': forms.NumberInput(attrs={'placeholder': 'Marks Obtained', 'class': 'form-input', 'min': 0}),
            'max_marks': forms.NumberInput(attrs={'placeholder': 'Maximum Marks', 'class': 'form-input', 'min': 1}),
        }

    def clean(self):
        cleaned_data = super().clean()
        marks = cleaned_data.get('marks')
        max_marks = cleaned_data.get('max_marks')
        if marks is not None and max_marks is not None:
            if marks > max_marks:
                raise forms.ValidationError("Marks obtained cannot exceed maximum marks.")
        return cleaned_data


class AttendanceForm(forms.Form):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
        initial=datetime.date.today
    )


class UserCreateForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Password'})
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Confirm Password'})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'role']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email'}),
            'role': forms.Select(attrs={'class': 'form-input'}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user