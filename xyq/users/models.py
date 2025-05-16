from django.db import models
from common.db import BaseModel
from django.contrib.auth.models import AbstractUser

class User(AbstractUser, BaseModel):
    ROLE_CHOICES = (
        ('student', '学生'),
        ('teacher', '教师'),
        ('admin', '管理员')
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student',verbose_name='角色')
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    avatar = models.ImageField(blank=True,upload_to='images/', verbose_name='头像')

    USERNAME_FIELD = 'mobile' # 设置为登录字段
    REQUIRED_FIELDS = ['username']
    class Meta:
        db_table = 'users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

class VerifCode(models.Model):
    """验证码模型"""
    mobile = models.CharField(verbose_name='手机号码',max_length=11)
    code = models.CharField(verbose_name='验证码',max_length=6)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    class Meta:
        db_table = 'verif_code'
        verbose_name = '验证码'

