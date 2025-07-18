from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Marks, Subject, CustomUser
from .forms import CustomUserCreationForm

# Homepage
def home(request):
    return render(request, 'home.html')

# Login View
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        print(f"Trying to authenticate user: {username}")  # Debugging line

        user = authenticate(request, username=username, password=password)
        if user:
            print("✅ User authenticated")
            login(request, user)
            if user.role == 'student':
                return redirect('student_dashboard')
            elif user.role == 'teacher':
                return redirect('teacher_dashboard')
            else:
                print("⚠️ Unknown role:", user.role)
        else:
            print("❌ Invalid credentials for", username)
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')

# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')

# Student Dashboard
@login_required
def student_dashboard(request):
    if request.user.role != 'student':
        return redirect('login')

    student = request.user

    # ✅ Handle profile update
    if request.method == 'POST' and 'update_profile' in request.POST:
        student.email = request.POST.get('email')
        student.contact = request.POST.get('contact')
        student.course = request.POST.get('course')
        student.address = request.POST.get('address')
        student.save()

    # ✅ Fetch marks for attendance-style chart
    marks = Marks.objects.filter(student=student)

    # ✅ Build student info dict
    student_info = {
        'name': student.get_full_name() or student.username,
        'dob': student.dob.strftime('%d-%b-%Y') if student.dob else 'N/A',
        'course': student.course or 'Not Assigned',
        'contact': student.contact or 'Not Available',
        'email': student.email,
        'address': student.address or 'N/A',
    }

    # ✅ Attendance as per marks
    attendance_data = []
    for mark in marks:
        percent = mark.marks
        attendance_data.append({
            'subject': mark.subject.name,
            'attended': int(percent * 0.9),  # Simulated
            'total': 100,
            'percent': percent,
        })

    # ✅ Fake announcement feed (static for now)
    announcements = [
        {'title': 'Academics', 'desc': 'Summer internship details released', 'time': '2 minutes ago'},
        {'title': 'Co-Curricular', 'desc': 'Global internship opportunity available', 'time': '10 minutes ago'},
    ]

    # ✅ Static timetable (example only)
    timetable = [
        {'time': '10 - 11 AM', 'room': 'DBMS130', 'subject': 'Lecture'},
        {'time': '11 - 12 PM', 'room': 'CS200', 'subject': 'Lecture'},
        {'time': '1 - 2 PM', 'room': 'Lab302', 'subject': 'Practical'},
    ]

    return render(request, 'student_dashboard.html', {
        'student': student_info,
        'attendance': attendance_data,
        'announcements': announcements,
        'timetable': timetable,
    })

# Teacher Dashboard
@login_required
def teacher_dashboard(request):
    if request.user.role != 'teacher':
        return redirect('login')

    message = None

    if request.method == 'POST':
        if 'add_subject' in request.POST:
            subject_name = request.POST.get('subject_name')
            if subject_name:
                Subject.objects.create(name=subject_name)
                message = f"Subject '{subject_name}' added successfully."
        else:
            student_id = request.POST.get('student')
            subject_id = request.POST.get('subject')
            score = request.POST.get('score')

            student = CustomUser.objects.get(id=student_id)
            subject = Subject.objects.get(id=subject_id)

            Marks.objects.update_or_create(
                student=student,
                subject=subject,
                defaults={'marks': score, 'uploaded_by': request.user}
            )
            message = f"Marks uploaded for {student.username} in {subject.name}."

    students = CustomUser.objects.filter(role='student')
    subjects = Subject.objects.all()
    return render(request, 'teacher_dashboard.html', {
        'students': students,
        'subjects': subjects,
        'message': message
    })

# Register View
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})

# Admin - User List
def user_list(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_users')
        CustomUser.objects.filter(id__in=selected_ids).delete()
        return redirect('user_list')

    users = CustomUser.objects.all()
    return render(request, 'user_list.html', {'users': users})
