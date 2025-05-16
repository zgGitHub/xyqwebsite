from django.contrib import admin

from course.models import Course, Chapter, CourseCategory


# Register your models here.
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price','sort_order')
    list_editable = ('sort_order',)  # 允许直接在列表页编辑排序
    list_filter = ('category',)
    search_fields = ('title',)

    # 按分类和排序的层次显示
    ordering = ('category', 'sort_order')

@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ('title','order')
    list_editable = ('order',)


admin.site.register(Chapter)