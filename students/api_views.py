# from rest_framework import generics
# from .models import User, Student, Subject, Attendance, Marks
# from .serializers import (
#     UserSerializer, StudentSerializer, SubjectSerializer,
#     AttendanceSerializer, MarksSerializer
# )


# # --- USER endpoints ---
# class UserListCreateView(generics.ListCreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


# class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


# # --- STUDENT endpoints ---
# class StudentListCreateView(generics.ListCreateAPIView):
#     queryset = Student.objects.all()
#     serializer_class = StudentSerializer


# class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Student.objects.all()
#     serializer_class = StudentSerializer


# # --- SUBJECT endpoints ---
# class SubjectListCreateView(generics.ListCreateAPIView):
#     queryset = Subject.objects.all()
#     serializer_class = SubjectSerializer


# class SubjectDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Subject.objects.all()
#     serializer_class = SubjectSerializer


# # --- ATTENDANCE endpoints ---
# class AttendanceListCreateView(generics.ListCreateAPIView):
#     queryset = Attendance.objects.all()
#     serializer_class = AttendanceSerializer

#     def get_queryset(self):
#         queryset = Attendance.objects.all()
#         student_id = self.request.query_params.get('student')
#         date = self.request.query_params.get('date')
#         if student_id:
#             queryset = queryset.filter(student_id=student_id)
#         if date:
#             queryset = queryset.filter(date=date)
#         return queryset


# class AttendanceDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Attendance.objects.all()
#     serializer_class = AttendanceSerializer


# # --- MARKS endpoints ---
# class MarksListCreateView(generics.ListCreateAPIView):
#     queryset = Marks.objects.all()
#     serializer_class = MarksSerializer

#     def get_queryset(self):
#         queryset = Marks.objects.all()
#         student_id = self.request.query_params.get('student')
#         subject_id = self.request.query_params.get('subject')
#         if student_id:
#             queryset = queryset.filter(student_id=student_id)
#         if subject_id:
#             queryset = queryset.filter(subject_id=subject_id)
#         return queryset


# class MarksDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Marks.objects.all()
#     serializer_class = MarksSerializer