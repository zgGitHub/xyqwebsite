from rest_framework import permissions

from course.models import Order, Course, Chapter


# class HasCourseAccess(permissions.BasePermission):
#     message= '您需要先购买该课程才能访问内容'
#
#     def has_permission(self, request, view):
#         course_id = view.kwargs.get('course_id')
#         try:
#             course = Course.objects.get(id=course_id)
#
#             # 课程是免费的，允许访问
#             if course.is_free():
#                 return True
#
#             return Order.objects.filter(
#                 user=request.user,
#                 course=course,
#                 payment_status=True
#             ).exists()
#         except Course.DoesNotExist:
#             return False
#
#
# # 或者创建更灵活的权限组合
# class IsAuthenticatedOrFreeCourse(permissions.BasePermission):
#     """
#     组合权限：允许认证用户或免费课程
#     """
#
#     def has_permission(self, request, view):
#         course_id = view.kwargs.get('course_id')
#         course = Course.objects.get(id=course_id)
#
#         # 如果课程免费，无需认证
#         if course.is_free():
#             return True
#
#         # 否则需要认证用户
#         return request.user and request.user.is_authenticated
#
#
# class HasCourseContentAccess(permissions.BasePermission):
#     """
#     根据内容类型检查权限
#     """
#
#     def has_permission(self, request, view):
#         course_id = view.kwargs.get('course_id')
#         chapter = Chapter().objects.get(id=course_id)
#
#         # 内容本身就是免费的
#         if chapter.is_free:
#             return True
#
#         # 否则检查课程访问权限
#         return HasCourseAccess().has_permission(request, view)