import re
from functools import partial

from django.shortcuts import render
from rest_framework import status, serializers,mixins,permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.exceptions import InvalidToken,TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer,CustomTokenObtainPairSerializer
from users.models import User

'''
viewsets.ViewSet ： 最基本的视图集，不提供任何默认动作

viewsets.ModelViewSet : 完整实现了 CRUD操作的视图集
    list() - GET /books/
    create() - POST /books/
    retrieve() - GET /books/1/
    update() - PUT /books/1/
    partial_update() - PATCH /books/1/
    destroy() - DELETE /books/1/
    
viewsets.ReadOnlyModelViewSet :只提供读操作的视图集
list() - GET /authors/
retrieve() - GET /authors/1/

viewsets.GenericViewSet :结合了通用视图和视图集的混合类，可以自由组合各种mixin
mixins.CreateModelMixin,
mixins.ListModelMixin,
mixins.RetrieveModelMixin,
viewsets.GenericViewSet


'''


class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        # 1、接受用户参数
        username = request.data.get('username')
        password = request.data.get('password')
        password_confirmation = request.data.get('password_confirmation')
        mobile = request.data.get('mobile')
        email = request.data.get('email')

        #  2 、参数校验
        if not all([username, password, password_confirmation]):
            return Response({'error':'用户信息所有参数不能为空'},status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'error':'用户名已经存在'},status=status.HTTP_400_BAD_REQUEST)

        if password != password_confirmation:
            return Response({'error':'两次密码输入不一致'},status=status.HTTP_400_BAD_REQUEST)

        if len(password) < 6 or len(password) > 18:
            return Response({'error':'密码长度要在 6～18 位之间'},status=status.HTTP_400_BAD_REQUEST)

        # if not re.match(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]{2,}$', email):
        #     return Response({'error': "邮箱格式不正确"}, status=status.HTTP_400_BAD_REQUEST)
        # if User.objects.filter(email=email).exists():
        #     return Response({'error': "该邮箱已被使用"}, status=status.HTTP_400_BAD_REQUEST)

        # 3 、创建用户
        user = User.objects.create_user(username=username, password=password,mobile=mobile,email=email)
        refresh = RefreshToken.for_user(user)
        res = {
            'username': user.username,
            'id': user.id,
            'mobile': user.mobile,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return Response(res, status=status.HTTP_201_CREATED)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"code":200,
                         "data":{
                             "token": str(serializer.validated_data['access']),
                             "refresh": str(serializer.validated_data['refresh']),
                             "user_info":{
                                 "id": serializer.user.id,
                                 "username": serializer.user.username,
                                 "mobile": serializer.user.mobile,
                                 "role": serializer.user.role,
                             }
                         }}, status=status.HTTP_200_OK)
class UserViewSet(viewsets.GenericViewSet,mixins.RetrieveModelMixin):
    # queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        只返回当前 JWT Token 对应的用户数据
        """
        return User.objects.filter(id=self.request.user.id)


