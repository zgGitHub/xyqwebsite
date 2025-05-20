# utils/response_format.py
from rest_framework.response import Response
from typing import Dict, Any, Optional

class APIResponse(Response):
    """
    统一响应格式：
    {
        "code": 200,
        "message": "success",
        "data": {...}  # 原始数据
    }
    """
    def __init__(
        self,
        data: Any = None,
        code: int = 200,
        message: str = "success",
        status: Optional[int] = None,
        **kwargs
    ):
        formatted_data = {
            "code": code,
            "message": message,
            "data": data
        }
        if status is not None:
            super().__init__(data=formatted_data, status=status, **kwargs)
        else:
            super().__init__(data=formatted_data, **kwargs)



