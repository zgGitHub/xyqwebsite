from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view
from course.models import Course, Chapter
from course.serializers import CourseSerializer, CourseCategorySerializer, ChapterSerializer
# from .permissions import HasCourseAccess,IsAuthenticatedOrFreeCourse

@api_view(['GET',])
def course_list(request):
    data = Course.objects.all()
    m = []
    for course in data:
        cate_data = CourseCategorySerializer(course.category).data
        m.append({'id': course.id, 'title': course.title,'category':cate_data,'order':course.sort_order})
    return Response(data={"code":status.HTTP_200_OK,"data":m,"msg":"操作成功"}, status=status.HTTP_200_OK)


@api_view(['GET',])
def course_detail(request, course_id):
    course = Course.objects.get(id=course_id)
    # data = {'id': course.id, 'title': course.title,'introduction': course.introduction,'teacher': {'username':course.teacher.username}}
    serializer = CourseSerializer(course)
    return Response(data={"code":status.HTTP_200_OK,"data":serializer.data,"msg":"操作成功"}, status=status.HTTP_200_OK)

# @api_view(['GET',])
# def chapter_list(request, course_id):
#     permission_classes = [IsAuthenticatedOrFreeCourse,HasCourseAccess]
#
#     data = Chapter.objects.all()
#     m = []
#     video_url = '需购买后查看'
#
#     for chapter in data:
#         if chapter.course_id == course_id:
#             m.append({'id': chapter.id, 'title': chapter.title,'video_url': chapter.video_url.url})
#     return Response(data={"code":status.HTTP_200_OK,"data":m,"msg":"操作成功"}, status=status.HTTP_200_OK)

class ChapterViewSet(viewsets.ModelViewSet):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
    # permission_classes = [IsAuthenticatedOrFreeCourse,HasCourseAccess]
