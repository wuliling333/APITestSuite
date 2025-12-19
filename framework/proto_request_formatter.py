"""
从proto定义中提取请求参数结构
"""
import sys
import os
from typing import Dict, Any, Optional

# 添加generated_proto到路径
generated_proto_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'generated_proto')
sys.path.insert(0, generated_proto_path)
sys.path.insert(0, os.path.join(generated_proto_path, 'shared'))
sys.path.insert(0, os.path.join(generated_proto_path, 'client'))

try:
    from client import hall_reqrsp_pb2, room_reqrsp_pb2, social_reqrsp_pb2
    PROTOBUF_AVAILABLE = True
except ImportError:
    PROTOBUF_AVAILABLE = False


class ProtoRequestFormatter:
    """从proto定义格式化请求参数结构"""
    
    @staticmethod
    def get_request_structure(service: str, method: str) -> Optional[Dict[str, Any]]:
        """获取请求参数结构（从proto定义）"""
        if not PROTOBUF_AVAILABLE:
            return None
        
        try:
            if service == 'Hall':
                return ProtoRequestFormatter._get_hall_request_structure(method)
            elif service == 'Room':
                return ProtoRequestFormatter._get_room_request_structure(method)
            elif service == 'Social':
                return ProtoRequestFormatter._get_social_request_structure(method)
        except Exception as e:
            print(f"⚠ 获取请求结构失败 {service}.{method}: {e}")
        
        return None
    
    @staticmethod
    def _get_hall_request_structure(method: str) -> Optional[Dict[str, Any]]:
        """获取Hall服务请求结构"""
        method_map = {
            'FetchSelfFullUserInfo': hall_reqrsp_pb2.HallFetchSelfFullUserInfoReq,
            'FetchSimpleUserInfo': hall_reqrsp_pb2.HallFetchSimpleUserInfoReq,
            'UpdateNickname': hall_reqrsp_pb2.HallUpdateNicknameReq,
            'SellItem': hall_reqrsp_pb2.HallSellItemReq,
            'BuyItem': hall_reqrsp_pb2.HallBuyItemReq,
            'StashToBackpack': hall_reqrsp_pb2.HallStashToBackpackReq,
            'BackpackToStash': hall_reqrsp_pb2.HallBackpackToStashReq,
            'ExchangeBackpackItem': hall_reqrsp_pb2.HallExchangeBackpackItemReq,
            'DebugAddCash': hall_reqrsp_pb2.HallDebugAddCashReq,
            'DebugAddItem': hall_reqrsp_pb2.HallDebugAddItemReq,
        }
        
        req_class = method_map.get(method)
        if not req_class:
            return None
        
        return ProtoRequestFormatter._extract_fields_from_descriptor(req_class())
    
    @staticmethod
    def _get_room_request_structure(method: str) -> Optional[Dict[str, Any]]:
        """获取Room服务请求结构"""
        method_map = {
            'GetUserState': room_reqrsp_pb2.RoomGetUserStateReq,
            'CreateTeam': room_reqrsp_pb2.RoomCreateTeamReq,
            'JoinTeam': room_reqrsp_pb2.RoomJoinTeamReq,
            'LeaveTeam': room_reqrsp_pb2.RoomLeaveTeamReq,
            'GetTeamInfo': room_reqrsp_pb2.RoomGetTeamInfoReq,
            'ChangeReadyState': room_reqrsp_pb2.RoomChangeReadyStateReq,
            'StartGameFromTeam': room_reqrsp_pb2.RoomStartGameFromTeamReq,
            'Match': room_reqrsp_pb2.RoomMatchReq,
            'CancelMatch': room_reqrsp_pb2.RoomCancelMatchReq,
            'GetGameInfo': room_reqrsp_pb2.RoomGetGameInfoReq,
        }
        
        req_class = method_map.get(method)
        if not req_class:
            return None
        
        return ProtoRequestFormatter._extract_fields_from_descriptor(req_class())
    
    @staticmethod
    def _get_social_request_structure(method: str) -> Optional[Dict[str, Any]]:
        """获取Social服务请求结构"""
        method_map = {
            'SendMessage': social_reqrsp_pb2.SocialSendMsgReq,
            'PullMsgs': social_reqrsp_pb2.SocialPullMsgsReq,
            'RevokeMsg': social_reqrsp_pb2.SocialRevokeMsgReq,
            'DeleteMsg': social_reqrsp_pb2.SocialDeleteMsgReq,
            'AddReaction': social_reqrsp_pb2.SocialAddReactionReq,
            'RemoveReaction': social_reqrsp_pb2.SocialRemoveReactionReq,
            'GetReactions': social_reqrsp_pb2.SocialGetReactionsReq,
            'GetSingleChatConvList': social_reqrsp_pb2.SocialGetSingleChatConvListReq,
            'MarkRead': social_reqrsp_pb2.SocialMarkReadReq,
            'GetFansList': social_reqrsp_pb2.SocialGetFansListReq,
            'GetFollowList': social_reqrsp_pb2.SocialGetFollowListReq,
            'GetFriendList': social_reqrsp_pb2.SocialGetFriendListReq,
            'Follow': social_reqrsp_pb2.SocialFollowReq,
            'Unfollow': social_reqrsp_pb2.SocialUnfollowReq,
        }
        
        req_class = method_map.get(method)
        if not req_class:
            return None
        
        return ProtoRequestFormatter._extract_fields_from_descriptor(req_class())
    
    @staticmethod
    def _extract_fields_from_descriptor(message_instance) -> Dict[str, Any]:
        """从protobuf消息描述符提取字段信息"""
        structure = {}
        
        for field_descriptor in message_instance.DESCRIPTOR.fields:
            field_name = field_descriptor.name
            field_type = ProtoRequestFormatter._get_field_type_name(field_descriptor)
            
            if field_descriptor.label == field_descriptor.LABEL_REPEATED:
                structure[field_name] = f"repeated {field_type}"
            else:
                structure[field_name] = field_type
        
        return structure
    
    @staticmethod
    def _get_field_type_name(field_descriptor) -> str:
        """获取字段类型名称"""
        type_map = {
            1: 'double',
            2: 'float',
            3: 'int64',
            4: 'uint64',
            5: 'int32',
            6: 'fixed64',
            7: 'fixed32',
            8: 'bool',
            9: 'string',
            10: 'group',
            11: 'message',
            12: 'bytes',
            13: 'uint32',
            14: 'enum',
            15: 'sfixed32',
            16: 'sfixed64',
            17: 'sint32',
            18: 'sint64',
        }
        
        if field_descriptor.type == field_descriptor.TYPE_MESSAGE:
            # 嵌套消息，返回消息类型名
            return field_descriptor.message_type.name
        elif field_descriptor.type == field_descriptor.TYPE_ENUM:
            # 枚举类型
            return field_descriptor.enum_type.name
        else:
            # 基本类型
            return type_map.get(field_descriptor.type, 'unknown')

