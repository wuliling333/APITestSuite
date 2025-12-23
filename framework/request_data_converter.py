"""
请求数据转换器 - 将YAML测试用例中的参数格式转换为实际请求数据
使用策略模式处理不同类型的转换
"""
from typing import Dict, Any, Optional, Callable


class RequestDataConverter:
    """请求数据转换器"""
    
    # 类型转换器映射（策略模式）
    _converters: Dict[str, Callable[[Any], Any]] = {
        'int32': lambda v: int(v) if v is not None else 0,
        'int64': lambda v: int(v) if v is not None else 0,
        'string': lambda v: str(v) if v is not None else '',
        'bool': lambda v: bool(v) if v is not None else False,
        'float': lambda v: float(v) if v is not None else 0.0,
        'double': lambda v: float(v) if v is not None else 0.0,
    }
    
    @classmethod
    def convert(cls, value: Any, field_type: str) -> Any:
        """根据类型转换值
        
        Args:
            value: 原始值
            field_type: 字段类型
            
        Returns:
            转换后的值
        """
        # 提取基础类型（去除 repeated、optional 等修饰符）
        base_type = field_type.lower()
        if 'repeated' in base_type:
            base_type = base_type.replace('repeated', '').strip()
        if 'optional' in base_type:
            base_type = base_type.replace('optional', '').strip()
        
        # 查找匹配的转换器
        for type_key, converter in cls._converters.items():
            if type_key in base_type:
                return converter(value)
        
        # 如果没有匹配的转换器，返回原值
        return value
    
    @staticmethod
    def convert_request_data(request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        将YAML测试用例中的参数格式转换为实际请求数据
        
        YAML格式: {"target_uid": {"value": 10000263, "type": "int64"}}
        转换为: {"target_uid": 10000263}
        
        Args:
            request_data: YAML中的请求数据（可能包含value/type格式）
            
        Returns:
            转换后的请求数据（直接值格式）
        """
        if not request_data:
            return {}
        
        converted = {}
        for key, value in request_data.items():
            # 检查是否是 {"value": ..., "type": ...} 格式
            if isinstance(value, dict) and 'value' in value:
                # 提取实际值
                actual_value = value['value']
                # 如果值是None，根据类型设置默认值
                if actual_value is None:
                    field_type = value.get('type', '')
                    if 'int' in field_type or 'int64' in field_type or 'int32' in field_type:
                        actual_value = 0
                    elif 'string' in field_type:
                        actual_value = ''
                    elif 'bool' in field_type:
                        actual_value = False
                    else:
                        actual_value = None
                converted[key] = actual_value
            else:
                # 直接使用原值
                converted[key] = value
        
        return converted
    
    @staticmethod
    def convert_nested_request_data(request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        递归转换嵌套的请求数据（处理嵌套对象）
        
        Args:
            request_data: YAML中的请求数据
            
        Returns:
            转换后的请求数据
        """
        if not request_data:
            return {}
        
        converted = {}
        for key, value in request_data.items():
            if isinstance(value, dict):
                # 检查是否是 {"value": ..., "type": ...} 格式
                if 'value' in value:
                    actual_value = value['value']
                    # 如果值是None，根据类型设置默认值
                    if actual_value is None:
                        field_type = value.get('type', '')
                        if 'int' in field_type or 'int64' in field_type or 'int32' in field_type:
                            actual_value = 0
                        elif 'string' in field_type:
                            actual_value = ''
                        elif 'bool' in field_type:
                            actual_value = False
                        else:
                            actual_value = None
                    # 如果实际值仍然是字典，递归转换
                    if isinstance(actual_value, dict):
                        actual_value = RequestDataConverter.convert_nested_request_data(actual_value)
                    converted[key] = actual_value
                else:
                    # 递归转换嵌套字典
                    converted[key] = RequestDataConverter.convert_nested_request_data(value)
            elif isinstance(value, list):
                # 处理列表
                converted[key] = [
                    RequestDataConverter.convert_nested_request_data(item) if isinstance(item, dict) else item
                    for item in value
                ]
            else:
                # 直接使用原值
                converted[key] = value
        
        return converted



