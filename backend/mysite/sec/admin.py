from django.contrib import admin
from .models import extended_user, teacher_user, student_list

# Register your models here.
admin.site.register(extended_user)
admin.site.register(teacher_user)
admin.site.register(student_list)
