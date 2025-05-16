from django.contrib import admin
from .models import Class,ClassEnrollment

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'head_teacher')
    raw_id_fields = ('head_teacher',)  # 优化教师选择界面

@admin.register(ClassEnrollment)
class ClassEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'class_obj', 'join_date', 'is_active')
