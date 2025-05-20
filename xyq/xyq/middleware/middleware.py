
class ResponseFormatMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # 如果是 DRF 的 Response，统一格式化（需根据实际需求调整）
        if hasattr(response, 'data'):
            response.data = {
                "code": response.status_code,
                "message": "success" if response.status_code < 400 else "error",
                "data": response.data
            }
        return response