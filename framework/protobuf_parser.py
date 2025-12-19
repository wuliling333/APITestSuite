"""
Protobuf解析器 - 从proto文件解析API接口定义
"""
import os
import re
from typing import Dict, List, Set
from framework.config import Config


class ProtobufParser:
    """Protobuf解析器"""
    
    def __init__(self, config: Config):
        self.config = config
    
    def discover_interfaces(self) -> Dict[str, List[Dict]]:
        """
        发现所有服务的接口
        返回: {service_name: [interface_info, ...]}
        """
        interfaces = {}
        
        for service_name in ['hall', 'room', 'social']:
            service_interfaces = self._parse_service_interfaces(service_name)
            if service_interfaces:
                interfaces[service_name] = service_interfaces
        
        return interfaces
    
    def _parse_service_interfaces(self, service_name: str) -> List[Dict]:
        """解析单个服务的接口"""
        proto_path = self.config.get_service_proto_path(service_name)
        proto_file = os.path.join(proto_path, f"{service_name}_reqrsp.proto")
        
        if not os.path.exists(proto_file):
            # 尝试其他可能的路径
            proto_file = os.path.join(proto_path, f"{service_name}.proto")
            if not os.path.exists(proto_file):
                print(f"⚠ 未找到 {service_name} 的proto文件: {proto_path}")
                return []
        
        return self._parse_proto_file(proto_file, service_name)
    
    def _parse_proto_file(self, proto_file: str, service_name: str) -> List[Dict]:
        """解析proto文件"""
        interfaces = []
        
        try:
            with open(proto_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 解析消息定义
            # 匹配: message ServiceMethodReq { ... }
            service_cap = service_name.capitalize()
            pattern = rf'message\s+{service_cap}(\w+)Req\s*{{'
            
            matches = re.finditer(pattern, content)
            
            for match in matches:
                method_name = match.group(1)
                
                # 跳过BodyReq和BodyRsp（这些是包装消息）
                if method_name == 'Body':
                    continue
                
                # 转换为标准格式（如 SendMsg -> SendMessage）
                method_name = self._normalize_method_name(method_name)
                
                if method_name:
                    interfaces.append({
                        'name': method_name,
                        'req_message': f"{service_cap}{match.group(1)}Req",
                        'rsp_message': f"{service_cap}{match.group(1)}Rsp",
                        'service': service_name
                    })
        
        except Exception as e:
            print(f"⚠ 解析proto文件失败 {proto_file}: {e}")
        
        return interfaces
    
    def _normalize_method_name(self, name: str) -> str:
        """标准化方法名"""
        # 简单的标准化规则
        if not name:
            return None
        
        # 如果已经是标准格式，直接返回
        if name.endswith('Message'):
            return name.replace('Message', 'Message')
        
        # 常见转换
        name_map = {
            'SendMsg': 'SendMessage',
            'PullMsg': 'PullMsgs',
            'GetConvList': 'GetSingleChatConvList',
            'FetchFullUserInfo': 'FetchFullUserInfo',
        }
        
        return name_map.get(name, name)

