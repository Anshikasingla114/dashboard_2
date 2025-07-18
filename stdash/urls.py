from django.contrib import admin
from django.urls import path
from core.views import (
    login_view,
    logout_view,
    register_view,
    student_dashboard,
    teacher_dashboard,
    home,
    user_list,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home, name='home'),
    
    # Auth
    path('', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),

    # Dashboards
    path('student/dashboard/', student_dashboard, name='student_dashboard'),
    path('teacher/dashboard/', teacher_dashboard, name='teacher_dashboard'),

    # Admin Panel
    path('users/', user_list, name='user_list'),
]
