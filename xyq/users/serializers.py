from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer, TokenObtainPairSerializer

from users.backends import MobileAuthBackend
from users.models import User
from rest_framework import exceptions


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        # 需要序列化的字段，"__all__"的意思是所有字段
        # fields = "__all__"
        fields = ['id','username', 'mobile', 'avatar','role','password']


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data.update({
            'username': self.user.username,
            'mobile': self.user.mobile,
            'id': self.user.id
        })
        return data

class MobileTokenObtainSerializer(TokenObtainPairSerializer):
    # 修改默认字段为mobile+password
    default_error_messages = {
        'no_active_account': '手机号或密码错误'
    }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[self.username_field] = self.fields.pop('username')
        self.fields['mobile'] = self.fields.pop(self.username_field)
        self.fields['password'].required = False  # 可选：手机号验证码登录场景
    def validate(self, attrs):
        mobile = attrs.get('mobile')
        password = attrs.get('password')
        # 手机号格式验证（示例）
        if not mobile or len(mobile) != 11:
            raise exceptions.ValidationError('请输入11位手机号')
        # 调用自定义认证后端
        user = MobileAuthBackend().authenticate(
            request=self.context.get('request'),
            mobile=mobile,
            password=password
        )
        if not user:
            raise exceptions.AuthenticationFailed(
                self.error_messages['no_active_account'],
                'no_active_account',
            )
        # 生成token
        refresh = self.get_token(user)
        data = {
            'mobile': mobile,
            'user_id': user.id,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return data
