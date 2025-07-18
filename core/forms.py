from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )
    username = forms.CharField(
        max_length=20,  # 🔧 Set max length
        min_length=4,   # 🔧 Optional: set min length
        required=True,
        label = 'username',
        widget=forms.TextInput(attrs={'placeholder': 'Username'})
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'role', 'password1', 'password2']
