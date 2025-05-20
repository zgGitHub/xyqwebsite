from django.shortcuts import render
from rest_framework import status, viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view
from course.models import Course, Chapter
from course.serializers import CourseSerializer, CourseCategorySerializer, ChapterSerializer
from xyq.utils.response_format import APIResponse
from .permissions import HasCourseAccess,IsAuthenticatedOrFreeCourse

@api_view(['GET',])
def course_list(request):
    data = Course.objects.all()
    m = []
    for course in data:
        cate_data = CourseCategorySerializer(course.category).data
        m.append({'id': course.id, 'title': course.title,'category':cate_data,'order':course.sort_order})
    return APIResponse(data=m)


@api_view(['GET',])
def course_detail(request, course_id):
    course = Course.objects.get(id=course_id)
    # data = {'id': course.id, 'title': course.title,'introduction': course.introduction,'teacher': {'username':course.teacher.username}}
    serializer = CourseSerializer(course)
    return APIResponse(data=serializer.data)

# @api_view(['GET',])
# def chapter_list(request, course_id):
#     # permission_classes = [IsAuthenticatedOrFreeCourse,HasCourseAccess]
#
#     data = Chapter.objects.get(id=course_id)
#     serializer = ChapterSerializer(data)
#     m = []
#
#     for chapter in serializer.data:
#         # if chapter.course_id == course_id:
#         m.append({'id': chapter.id, 'title': chapter.title,'video_url': chapter.video_url.url})
#     return Response(data={"code":status.HTTP_200_OK,"data":m,"msg":"操作成功"}, status=status.HTTP_200_OK)

class ChapterListDetailView(generics.RetrieveAPIView):
    serializer_class = ChapterSerializer
    permission_classes = [HasCourseAccess,IsAuthenticatedOrFreeCourse]

    def get_queryset(self):
        return Chapter.objects.filter(course_id=self.kwargs['pk'])

    def get_serializer_context(self):
        # 确保父类的上下文设置被执行
        context = super().get_serializer_context()
        print("Current context:", context)  # 调试时查看
        return context