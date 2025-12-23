"""
Base Page - 基础页面对象
"""
from typing import Dict, Any
from framework.client import APIClient


class BasePage:
    """基础页面对象类"""
    
    def __init__(self, client: APIClient, service_name: str):
        """
        初始化页面对象
        
        Args:
            client: API客户端实例
            service_name: 服务名称（Hall/Room/Social）
        """
        self.client = client
        self.service_name = service_name
    
    def call_api(self, method: str, request_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        调用API接口（通用方法）
        
        Args:
            method: 方法名
            request_data: 请求数据
            
        Returns:
            包含 success, response, error_code, error_message 的字典
        """
        if request_data is None:
            request_data = {}
        
        return self.client.call_rpc(
            service=self.service_name,
            method=method,
            request_data=request_data
        )
    
    def is_success(self, result: Dict[str, Any]) -> bool:
        """判断API调用是否成功"""
        return result.get('success', False)
    
    def get_error_code(self, result: Dict[str, Any]) -> int:
        """获取错误码"""
        return result.get('error_code', 0)
    
    def get_error_message(self, result: Dict[str, Any]) -> str:
        """获取错误信息"""
        return result.get('error_message', '')
    
    def get_response(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """获取响应数据"""
        return result.get('response', {})



