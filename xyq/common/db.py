from django.db import models

class BaseModel(models.Model):
    """抽象的模型基类：定义一些公共的模型字段"""
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    is_deleted = models.BooleanField(default=False, verbose_name="删除标记")
    class Meta:
        # 声明这是一个抽象的模型，在执行迁移文件时，不会在数据库中生成表
        abstract = True
        verbose_name_plural = "公共字段表"
        db_table = "BaseTable"
