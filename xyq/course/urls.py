#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Date  : 2022/1/8
# @Name  : ZhouZongXin
"""
路由
"""
from django.urls import path
from django.views.decorators.csrf import csrf_exempt  # 解决跨域

from .views import ChapterViewSet,course_list,course_detail

# 路由list
urlpatterns = [
    # "login" 参数表示路径
    # csrf_exempt()用来解决前后端分离跨域问题，如果不添加这个那么无法进行跨域
    # views.apiLogin 是当前视图层views内的apiLogin方法
    # login/urls.py 中给路由起别名，name="路由别名"
    path("list", csrf_exempt(course_list), name='course_list'),  # 第一个参数表示路径
    path("detail/<int:course_id>", csrf_exempt(course_detail), name='course_detail'),
    path("chapter/<int:course_id>", ChapterViewSet.as_view({'get':'list'}), name='chapter_list'),
]

