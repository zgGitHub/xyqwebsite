# middleware/security_logging.py
import logging
from django.http import HttpRequest
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import AnonymousUser

logger = logging.getLogger('django.security')

class SecurityLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        response = self.get_response(request)
        return response

    def process_exception(self, request: HttpRequest, exception):
        if isinstance(exception, PermissionDenied):
            user = request.user if not isinstance(request.user, AnonymousUser) else 'Anonymous'
            ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
            path = request.get_full_path()

            logger.warning(
                '403 Forbidden: User=%s, IP=%s, Path=%s, Headers=%s',
                user,
                ip,
                path,
                dict(request.headers),  # 记录请求头用于分析
                extra={'request': request}  # 传递 request 对象用于日志格式化
            )
        return None