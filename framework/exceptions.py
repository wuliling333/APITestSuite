"""
API测试框架异常定义
"""
from typing import Optional


class APITestException(Exception):
    """API测试框架基础异常"""
    
    def __init__(self, message: str, error_code: Optional[int] = None):
        """
        初始化异常
        
        Args:
            message: 错误消息
            error_code: 错误代码（可选）
        """
        super().__init__(message)
        self.message = message
        self.error_code = error_code
    
    def __str__(self):
        if self.error_code:
            return f"[{self.error_code}] {self.message}"
        return self.message


class ConnectionError(APITestException):
    """连接错误"""
    pass


class EncodingError(APITestException):
    """编码错误"""
    pass


class ConfigurationError(APITestException):
    """配置错误"""
    pass


class GitUpdateError(APITestException):
    """Git更新错误"""
    pass


class ProtobufParseError(APITestException):
    """Protobuf解析错误"""
    pass


class TestCaseError(APITestException):
    """测试用例错误"""
    pass


class ReportGenerationError(APITestException):
    """报告生成错误"""
    pass

