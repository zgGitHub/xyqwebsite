from django.db import models
from users.models import User


class CourseCategory(models.Model):
    title = models.CharField(max_length=100, verbose_name="分类名称")
    order = models.PositiveIntegerField(default=0, verbose_name="排序")

    class Meta:
        verbose_name = "课程分类"
        verbose_name_plural = verbose_name
        ordering = ['order', 'id']  # 先按order排序，再按id

    def __str__(self):
        return self.title


class Course(models.Model):
    title = models.CharField(max_length=100,verbose_name='课程名称')
    description = models.TextField(verbose_name='简介')
    teacher = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='courses',verbose_name='讲师',limit_choices_to={'role':'teacher'})
    price = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    is_free_for_all = models.BooleanField(default=False)
    def is_free(self):
        '''检查课程是否免费'''
        return self.is_free_for_all or self.price == 0

    def user_has_access(self, user):
        """
        检查指定用户是否有权访问该课程
        可用于模板或其他需要检查权限的地方
        """
        return self.orders.filter(user=user, payment_status=True).exists()

    category = models.ForeignKey(
        CourseCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="课程分类"
    )

    sort_order = models.PositiveIntegerField(default=0, verbose_name="排序")

    def __str__(self):
        return self.title
    class Meta:
        verbose_name = '课程管理'
        verbose_name_plural = verbose_name
        ordering = ['sort_order',]


class Chapter(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='chapters', verbose_name='所属课程')
    title = models.CharField(max_length=100,verbose_name='章节名称')
    video_url = models.FileField(upload_to='videos/',blank=True,verbose_name='章节视频地址')
    is_free = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)  # 内容排序
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = '章节管理'
        verbose_name_plural = verbose_name


class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    course = models.ForeignKey(Course,on_delete=models.CASCADE,null=True,blank=True, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.BooleanField(default=False)
    amount_paid = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '订单管理'
        verbose_name_plural = verbose_name
        unique_together = ('user', 'course')