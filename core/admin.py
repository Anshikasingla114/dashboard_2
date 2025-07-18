from django.contrib import admin
from .models import CustomUser, Subject, Marks
from django.contrib.auth.admin import UserAdmin

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Subject)
admin.site.register(Marks)
