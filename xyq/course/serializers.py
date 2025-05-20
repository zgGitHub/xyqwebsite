from django.template.context_processors import request
from rest_framework import serializers

from course.models import Course, Chapter, CourseCategory
from users.serializers import UserSerializer


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    动态字段序列化器基类
    """
    def __init__(self, *args, **kwargs):
        # 从context中获取要排除的字段
        exclude_fields = kwargs.pop('exclude_fields', None)
        super().__init__(*args, **kwargs)
        if exclude_fields:
            for field in exclude_fields:
                self.fields.pop(field)

class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    teacher = UserSerializer(read_only=True)
    category = CourseCategorySerializer(read_only=True)
    class Meta:
        model = Course
        fields = "__all__"

class ChapterSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Chapter
        fields = ['id', 'title', 'video_url','is_free','order']

    def validate(self, data):
        request = self.context.get('request')
        if request is None:
            raise serializers.ValidationError("Request context is missing")
        return data

    def to_representation(self, instance):
        """
        根据用户权限动态调整返回的字段
        """
        request = self.context.get('request')

        # 获取user的安全方式
        user = getattr(request, 'user', None) if request else None

        representation = super().to_representation(instance)

        # 安全地检查访问权限
        if not self._has_access(user, instance):
            representation.pop('video_url', None)  # 安全地移除字段

        return representation

    def _has_access(self, user, chapter):
        """检查用户是否有权访问该内容"""
        if chapter.is_free:
            return True
        if not user.is_authenticated:
            return False

        # 检查用户是否购买了关联课程
        return chapter.course.user_has_access(user)