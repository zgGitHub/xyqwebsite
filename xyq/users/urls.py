#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Date  : 2022/1/8
# @Name  : ZhouZongXin
"""
路由
"""
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import  TokenRefreshView, TokenVerifyView

from . import views  # 引用视图层
from django.views.decorators.csrf import csrf_exempt  # 解决跨域
from .views import UserViewSet, RegisterView, CustomTokenObtainPairView

# 路由list
urlpatterns = [
    # "login" 参数表示路径
    # csrf_exempt()用来解决前后端分离跨域问题，如果不添加这个那么无法进行跨域
    # views.apiLogin 是当前视图层views内的apiLogin方法
    # login/urls.py 中给路由起别名，name="路由别名"
    # path('<int:pk>/avatar/upload/',UserView.as_view({'post':'upload_avatar'}), name='user_avatar'),
    path("login/", CustomTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # 刷新 Token
    # path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),


    path("register/", RegisterView.as_view(), name='register'),
    # path("users/<int:pk>", csrf_exempt(UserView), name='users'),
    # path("users/<int:pk>", UserViewSet.as_view({"get":"retrieve"}), name='users'),
]

router = DefaultRouter()
router.register('users', UserViewSet,basename='users')
urlpatterns += router.urls


