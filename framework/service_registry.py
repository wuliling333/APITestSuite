"""
服务注册表
统一管理服务名和方法名的映射关系，便于扩展新服务
"""
from typing import Optional, Dict


class ServiceRegistry:
    """服务注册表"""
    
    _services: Dict[str, Dict[str, any]] = {
        'Hall': {
            'command': 2,
            'methods': {
                'FetchSelfFullUserInfo': 2,
                'FetchSimpleUserInfo': 3,
                'UpdateNickname': 4,
                'SellItem': 10,
                'BuyItem': 11,
                'StashToBackpack': 20,
                'BackpackToStash': 21,
                'ExchangeBackpackItem': 22,
                'DebugAddCash': 10000,
                'DebugAddItem': 10001,
            }
        },
        'Room': {
            'command': 4,
            'methods': {
                'GetUserState': 1,
                'CreateTeam': 2,
                'JoinTeam': 3,
                'LeaveTeam': 4,
                'GetTeamInfo': 5,
                'ChangeReadyState': 6,
                'StartGameFromTeam': 20,
                'Match': 21,
                'CancelMatch': 22,
                'GetGameInfo': 23,
            }
        },
        'Social': {
            'command': 3,
            'methods': {
                'SendMessage': 1,
                'PullMsgs': 2,
                'RevokeMsg': 3,
                'DeleteMsg': 4,
                'AddReaction': 10,
                'RemoveReaction': 11,
                'GetReactions': 12,
                'GetSingleChatConvList': 20,
                'MarkRead': 26,
                'GetFansList': 30,
                'GetFollowList': 31,
                'GetFriendList': 32,
                'Follow': 33,
                'Unfollow': 34,
            }
        }
    }
    
    @classmethod
    def get_command(cls, service: str) -> Optional[int]:
        """获取服务命令码
        
        Args:
            service: 服务名称（如 'Hall', 'Room', 'Social'）
            
        Returns:
            命令码，如果服务不存在返回 None
        """
        return cls._services.get(service, {}).get('command')
    
    @classmethod
    def get_op_type(cls, service: str, method: str) -> Optional[int]:
        """获取操作类型码
        
        Args:
            service: 服务名称
            method: 方法名称
            
        Returns:
            操作类型码，如果服务或方法不存在返回 None
        """
        return cls._services.get(service, {}).get('methods', {}).get(method)
    
    @classmethod
    def register_service(cls, service: str, command: int, methods: Dict[str, int]):
        """注册新服务
        
        Args:
            service: 服务名称
            command: 命令码
            methods: 方法名到操作类型码的映射
        """
        cls._services[service] = {
            'command': command,
            'methods': methods
        }
    
    @classmethod
    def register_method(cls, service: str, method: str, op_type: int):
        """注册新方法
        
        Args:
            service: 服务名称
            method: 方法名称
            op_type: 操作类型码
        """
        if service not in cls._services:
            cls._services[service] = {
                'command': 0,  # 默认命令码
                'methods': {}
            }
        cls._services[service]['methods'][method] = op_type
    
    @classmethod
    def get_all_services(cls) -> Dict[str, Dict[str, any]]:
        """获取所有服务信息"""
        return cls._services.copy()
    
    @classmethod
    def get_service_methods(cls, service: str) -> Dict[str, int]:
        """获取服务的所有方法"""
        return cls._services.get(service, {}).get('methods', {}).copy()

