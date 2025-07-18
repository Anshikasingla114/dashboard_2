from django.contrib.auth.models import AbstractUser
from django.db import models

# models.py
class CustomUser(AbstractUser):
    role = models.CharField(max_length=10, choices=[('student', 'Student'), ('teacher', 'Teacher')])
    dob = models.DateField(null=True, blank=True)
    contact = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    course = models.CharField(max_length=100, blank=True)




class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Marks(models.Model):
    student = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE, 
        limit_choices_to={'role': 'student'},
        related_name='student_marks'
    )
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks = models.FloatField()
    uploaded_by = models.ForeignKey(
        CustomUser, 
        on_delete=models.SET_NULL, 
        null=True, 
        limit_choices_to={'role': 'teacher'},
        related_name='teacher_uploaded_marks'
    )
    uploaded_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.subject.name}: {self.marks}"

