import re
from functools import partial

from django.shortcuts import render
from rest_framework import status, serializers,mixins,permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.exceptions import InvalidToken,TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from tutorial.quickstart.serializers import UserSerializer
from .serializers import CustomTokenObtainPairSerializer
from users.models import User

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
    # serializer_class = CustomTokenObtainPairSerializer
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
class UserView(GenericViewSet,mixins.RetrieveModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def upload_avatar(self, request, *args, **kwargs):
        # 上传用户头像
        avatar = request.data.get('avatar')
        # 校验是否有上传文件
        if not avatar:
            return Response({'error':'上传失败，文件不能为空'},status=status.HTTP_400_BAD_REQUEST)
        # 校验文件大小不能超过 300kb
        if avatar.size > 1024*300:
            return Response({'error':'文件大小不能超过 300kb'},status=status.HTTP_400_BAD_REQUEST)

        # 保存文件
        user = self.get_object()
        ser = self.get_serializer(user, data={'avatar': avatar},partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response({'avatar':ser.data['avatar']}, status=status.HTTP_200_OK)