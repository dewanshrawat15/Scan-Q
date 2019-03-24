from django.contrib import admin
from .models import extended_user
from .models import teacher_user

# Register your models here.
admin.site.register(extended_user)
admin.site.register(teacher_user)
