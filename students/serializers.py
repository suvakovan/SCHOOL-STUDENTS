# from rest_framework import serializers
# from .models import User, Student, Subject, Attendance, Marks


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email', 'role', 'is_active']


# class StudentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Student
#         fields = '__all__'


# class SubjectSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Subject
#         fields = '__all__'


# class AttendanceSerializer(serializers.ModelSerializer):
#     student_name = serializers.CharField(source='student.name', read_only=True)
#     recorded_by_username = serializers.CharField(source='recorded_by.username', read_only=True)

#     class Meta:
#         model = Attendance
#         fields = ['id', 'student', 'student_name', 'date', 'status', 'recorded_by', 'recorded_by_username']


# class MarksSerializer(serializers.ModelSerializer):
#     student_name = serializers.CharField(source='student.name', read_only=True)
#     subject_name = serializers.CharField(source='subject.name', read_only=True)
#     entered_by_username = serializers.CharField(source='entered_by.username', read_only=True)

#     class Meta:
#         model = Marks
#         fields = ['id', 'student', 'student_name', 'subject', 'subject_name', 'marks', 'entered_by', 'entered_by_username']