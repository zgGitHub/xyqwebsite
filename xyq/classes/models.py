from django.utils import timezone

from django.db import models
from users.models import User


class Class(models.Model):
    name = models.CharField(max_length=100,verbose_name='班级名称')
    head_teacher = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'role': 'teacher'},  # 限定班主任必须为教师角色
        verbose_name='班主任'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间',blank=True,null=True)
    members = models.ManyToManyField(
        User,
        through='ClassEnrollment',
        related_name='enrolled_class',
        limit_choices_to={'role': 'student'},
    )
    class Meta:
        verbose_name = '班级管理'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

# 中间模型（记录学生加入班级的详细信息）
class ClassEnrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='学生')
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE,verbose_name='加入班级')
    join_date = models.DateField(auto_now_add=True, verbose_name='加入时间')
    is_active = models.BooleanField(default=True, verbose_name='在籍状态')

    class Meta:
        unique_together = ('student', 'class_obj')  # 避免重复加入
        verbose_name = '记录管理'
        verbose_name_plural = verbose_name