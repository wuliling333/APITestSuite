"""
API客户端 - 处理与服务器的通信
"""
import requests
import json
import socket
import struct
import time
from typing import Dict, Any, Optional
from framework.config import Config
from framework.tcp_client import TCPClient
from framework.protobuf_helper import ProtobufHelper
from framework.exceptions import EncodingError, ConnectionError, APITestException
from framework.logger import logger
from framework.service_registry import ServiceRegistry
import sys
import os

# 添加generated_proto到路径
generated_proto_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'generated_proto')
sys.path.insert(0, generated_proto_path)
sys.path.insert(0, os.path.join(generated_proto_path, 'shared'))
sys.path.insert(0, os.path.join(generated_proto_path, 'client'))

try:
    from shared import head_pb2, gate_pb2
    from client import hall_reqrsp_pb2, room_reqrsp_pb2, social_reqrsp_pb2
    PROTOBUF_AVAILABLE = True
except ImportError as e:
    print(f"⚠ protobuf模块导入失败: {e}")
    PROTOBUF_AVAILABLE = False


class APIClient:
    """API客户端"""
    
    def __init__(self, config: Config):
        self.config = config
        self.gate_address = config.get_gate_address()
        self.login_url = config.get_login_url()
        self.uid = None
        self.token = None
        self.gate_socket = None
        self.tcp_client = None
        self.bound = False
    
    def login(self) -> bool:
        """登录获取token"""
        print("\n" + "=" * 80)
        print("登录服务器...")
        print("=" * 80)
        
        try:
            # 构造登录请求
            login_data = {
                'device_id': 'test_device_001',
                'data': '{}',
                'timestamp': int(time.time() * 1000)
            }
            
            # 发送登录请求
            response = requests.post(
                f"{self.login_url}/api/Login/LoginGuest",
                data=login_data,
                timeout=self.config.get_timeout()
            )
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    
                    # 服务器返回 code=200 表示成功（不是 code=0）
                    response_code = result.get('code') or result.get('Code', 0)
                    if response_code == 200:
                        data = result.get('data', {}) or result.get('Data', {})
                        user_info = data.get('UserInfo', {}) or data.get('userInfo', {})
                        self.uid = user_info.get('Uid') or user_info.get('uid')
                        # 服务器返回的是 Certificate，不是 Token
                        self.token = data.get('Certificate', '') or data.get('Token', '') or data.get('certificate', '') or data.get('token', '')
                        
                        if self.uid:
                            print(f"✓ 登录成功: UID={self.uid}")
                            return True
                        else:
                            print(f"✗ 登录失败: 无法获取UID，响应: {result}")
                            return False
                    else:
                        error_msg = result.get('msg') or result.get('Msg') or result.get('message') or '未知错误'
                        print(f"✗ 登录失败: {error_msg} (code={response_code})")
                        return False
                except Exception as e:
                    print(f"✗ 解析响应失败: {e}")
                    print(f"原始响应: {response.text[:500]}")
                    return False
            else:
                print(f"✗ 登录失败: HTTP {response.status_code}")
                print(f"响应内容: {response.text[:500]}")
                return False
        except Exception as e:
            print(f"✗ 登录失败: {e}")
            return False
    
    def connect_gate(self) -> bool:
        """连接Gate服务器"""
        print("\n" + "=" * 80)
        print("连接Gate服务器...")
        print("=" * 80)
        
        try:
            host, port = self.gate_address.split(':')
            port = int(port)
            
            # 使用TCP客户端
            self.tcp_client = TCPClient(self.config)
            if not self.tcp_client.connect(host, port):
                return False
            
            print(f"✓ Gate服务器连接成功: {host}:{port}")
            
            # 绑定到Gate服务器
            if not self._bind_to_gate():
                return False
            
            return True
        except Exception as e:
            print(f"✗ Gate服务器连接失败: {e}")
            return False
    
    def _bind_to_gate(self) -> bool:
        """绑定到Gate服务器"""
        if not self.uid or not self.token:
            print("✗ 绑定失败: 未登录")
            return False
        
        if not PROTOBUF_AVAILABLE:
            print("✗ 绑定失败: protobuf模块不可用")
            return False
        
        try:
            # 构造GateBindReq
            bind_req = gate_pb2.GateBindReq()
            bind_req.uid = self.uid
            bind_req.token = self.token
            bind_req.platform = "test"
            bind_req.lang = "zh"
            bind_req.appVersion = "1.0.0"
            
            # 构造GateBodyReq
            body_req = gate_pb2.GateBodyReq()
            body_req.bind.CopyFrom(bind_req)
            
            # 序列化body
            body_bytes = body_req.SerializeToString()
            
            # 发送绑定请求
            # CommandGate = 1, GateOpTypeBind = 2
            response = self.tcp_client.send_request(
                command=1,  # CommandGate
                op_type=2,  # GateOpTypeBind
                body_bytes=body_bytes
            )
            
            if response:
                # 解析响应头
                rsp_head = head_pb2.RspHead()
                rsp_head.ParseFromString(response.get('head_bytes', b''))
                
                if rsp_head.code == 200:
                    self.bound = True
                    print("✓ 绑定Gate服务器成功")
                    return True
                else:
                    print(f"✗ 绑定Gate服务器失败: code={rsp_head.code}, desc={rsp_head.desc}")
                    return False
            else:
                print("✗ 绑定Gate服务器失败: 无响应")
                return False
        
        except Exception as e:
            print(f"✗ 绑定Gate服务器失败: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def call_rpc(self, service: str, method: str, request_data: Dict) -> Dict[str, Any]:
        """
        调用RPC接口
        返回: {
            'success': bool,
            'response': dict,
            'error_code': int,
            'error_message': str
        }
        """
        print(f"\n📤 调用API: {service}.{method}")
        print(f"📥 请求参数: {json.dumps(request_data, indent=2, ensure_ascii=False)}")
        
        if not self.tcp_client or not self.bound:
            return {
                'success': False,
                'response': {},
                'error_code': 500,
                'error_message': '未连接到Gate服务器或未绑定'
            }
        
        try:
            # 获取command和op_type
            command, op_type = self._get_command_and_op_type(service, method)
            if command is None:
                return {
                    'success': False,
                    'response': {},
                    'error_code': 501,
                    'error_message': f'未知的服务或方法: {service}.{method}'
                }
            
            # 构造请求body
            try:
                body_bytes = self._encode_request_body(service, method, request_data)
            except EncodingError as e:
                logger.error(f"编码请求body失败: {e}")
                return {
                    'success': False,
                    'response': {},
                    'error_code': e.error_code or 500,
                    'error_message': str(e)
                }
            
            # 发送请求
            response = self.tcp_client.send_request(command, op_type, body_bytes)
            
            if response:
                # 解析响应
                error_code = self._extract_error_code(response.get('head_bytes', b''))
                error_message = self._extract_error_message(response.get('head_bytes', b''))
                body_data = self._parse_response_body(service, method, response.get('body_bytes', b''))
                
                success = error_code == 200
                
                result = {
                    'success': success,
                    'response': body_data,
                    'error_code': error_code,
                    'error_message': error_message
                }
                
                # 打印响应摘要
                try:
                    print(f"📥 响应: {json.dumps(result, indent=2, ensure_ascii=False, default=str)}")
                except:
                    print(f"✓ 调用成功: 响应码={error_code}" if success else f"✗ 调用失败: 响应码={error_code}, 错误={error_message}")
                
                return result
            else:
                return {
                    'success': False,
                    'response': {},
                    'error_code': 408,
                    'error_message': '请求超时'
                }
        
        except Exception as e:
            print(f"✗ RPC调用失败: {e}")
            return {
                'success': False,
                'response': {},
                'error_code': 500,
                'error_message': str(e)
            }
    
    def _get_command_and_op_type(self, service: str, method: str) -> tuple:
        """获取command和op_type"""
        # CommandType定义
        commands = {
            'Hall': 2,
            'Room': 4,
            'Social': 3
        }
        
        command = commands.get(service)
        if command is None:
            return None, None
        
        # 获取op_type（根据方法名映射）
        op_type_map = self._get_op_type_map(service)
        op_type = op_type_map.get(method, 0)
        
        if op_type == 0:
            print(f"⚠ 未找到方法 {method} 的op_type，使用默认值0")
        
        return command, op_type
    
    def _get_op_type_map(self, service: str) -> Dict[str, int]:
        """获取服务的方法到op_type的映射"""
        if service == 'Hall':
            return {
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
        elif service == 'Room':
            return {
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
        elif service == 'Social':
            return {
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
        return {}
    
    def _encode_request_body(self, service: str, method: str, request_data: Dict) -> bytes:
        """编码请求body"""
        if not PROTOBUF_AVAILABLE:
            print(f"⚠ 编码请求body失败: protobuf模块不可用")
            return b''
        
        # 统一服务名大小写（首字母大写）
        service_normalized = service.capitalize()
        
        try:
            if service_normalized == 'Hall':
                return self._encode_hall_body_req(method, request_data)
            elif service_normalized == 'Room':
                return self._encode_room_body_req(method, request_data)
            elif service_normalized == 'Social':
                return self._encode_social_body_req(method, request_data)
            else:
                error_msg = f"未知的服务 '{service}' (标准化后: '{service_normalized}')"
                logger.error(f"编码请求body失败: {error_msg}")
                logger.info(f"支持的服务: Hall, Room, Social")
                raise EncodingError(error_msg, 500)
        except EncodingError:
            raise
        except Exception as e:
            error_msg = f"编码请求body失败: {e}"
            logger.error(error_msg)
            logger.debug(f"服务: {service}, 方法: {method}, 请求数据: {request_data}")
            logger.exception("编码异常详情")
            raise EncodingError(str(e), 500) from e
    
    def _encode_hall_body_req(self, method: str, request_data: Dict) -> bytes:
        """编码HallBodyReq"""
        body_req = hall_reqrsp_pb2.HallBodyReq()
        
        # 根据方法名设置对应的字段
        method_map = {
            'FetchSelfFullUserInfo': ('fetch_self_full_user_info', hall_reqrsp_pb2.HallFetchSelfFullUserInfoReq()),
            'FetchSimpleUserInfo': ('fetch_simple_user_info', hall_reqrsp_pb2.HallFetchSimpleUserInfoReq()),
            'UpdateNickname': ('update_nickname', hall_reqrsp_pb2.HallUpdateNicknameReq()),
            'SellItem': ('sell_item', hall_reqrsp_pb2.HallSellItemReq()),
            'BuyItem': ('buy_item', hall_reqrsp_pb2.HallBuyItemReq()),
            'StashToBackpack': ('stash_to_backpack', hall_reqrsp_pb2.HallStashToBackpackReq()),
            'BackpackToStash': ('backpack_to_stash', hall_reqrsp_pb2.HallBackpackToStashReq()),
            'ExchangeBackpackItem': ('exchange_backpack_item', hall_reqrsp_pb2.HallExchangeBackpackItemReq()),
            'DebugAddCash': ('debug_add_cash', hall_reqrsp_pb2.HallDebugAddCashReq()),
            'DebugAddItem': ('debug_add_item', hall_reqrsp_pb2.HallDebugAddItemReq()),
        }
        
        if method in method_map:
            field_name, req_msg = method_map[method]
            # 填充请求数据
            for key, value in request_data.items():
                if hasattr(req_msg, key):
                    try:
                        setattr(req_msg, key, value)
                    except Exception as e:
                        logger.error(f"设置字段 {key} 失败: {e}, 值: {value}, 类型: {type(value)}")
                        raise EncodingError(f"设置字段 {key} 失败: {e}", 500) from e
                else:
                    logger.warning(f"请求消息中没有字段 '{key}'，跳过")
            
            # 设置到body_req
            getattr(body_req, field_name).CopyFrom(req_msg)
        else:
            error_msg = f"未知的方法 '{method}'"
            logger.error(f"编码Hall请求body失败: {error_msg}")
            logger.info(f"支持的方法: {list(method_map.keys())}")
            raise EncodingError(error_msg, 500)
        
        return body_req.SerializeToString()
    
    def _encode_room_body_req(self, method: str, request_data: Dict) -> bytes:
        """编码RoomBodyReq"""
        body_req = room_reqrsp_pb2.RoomBodyReq()
        
        method_map = {
            'GetUserState': ('get_user_state', room_reqrsp_pb2.RoomGetUserStateReq()),
            'CreateTeam': ('create_team', room_reqrsp_pb2.RoomCreateTeamReq()),
            'JoinTeam': ('join_team', room_reqrsp_pb2.RoomJoinTeamReq()),
            'LeaveTeam': ('leave_team', room_reqrsp_pb2.RoomLeaveTeamReq()),
            'GetTeamInfo': ('get_team_info', room_reqrsp_pb2.RoomGetTeamInfoReq()),
            'ChangeReadyState': ('change_ready_state', room_reqrsp_pb2.RoomChangeReadyStateReq()),
            'StartGameFromTeam': ('start_game_from_team', room_reqrsp_pb2.RoomStartGameFromTeamReq()),
            'Match': ('match', room_reqrsp_pb2.RoomMatchReq()),
            'CancelMatch': ('cancel_match', room_reqrsp_pb2.RoomCancelMatchReq()),
            'GetGameInfo': ('get_game_info', room_reqrsp_pb2.RoomGetGameInfoReq()),
        }
        
        if method in method_map:
            field_name, req_msg = method_map[method]
            for key, value in request_data.items():
                if hasattr(req_msg, key):
                    try:
                        setattr(req_msg, key, value)
                    except Exception as e:
                        logger.error(f"设置字段 {key} 失败: {e}, 值: {value}, 类型: {type(value)}")
                        raise EncodingError(f"设置字段 {key} 失败: {e}", 500) from e
                else:
                    logger.warning(f"请求消息中没有字段 '{key}'，跳过")
            getattr(body_req, field_name).CopyFrom(req_msg)
        else:
            error_msg = f"未知的方法 '{method}'"
            logger.error(f"编码Room请求body失败: {error_msg}")
            logger.info(f"支持的方法: {list(method_map.keys())}")
            raise EncodingError(error_msg, 500)
        
        return body_req.SerializeToString()
    
    def _encode_social_body_req(self, method: str, request_data: Dict) -> bytes:
        """编码SocialBodyReq"""
        body_req = social_reqrsp_pb2.SocialBodyReq()
        
        method_map = {
            'SendMessage': ('send_msg', social_reqrsp_pb2.SocialSendMsgReq()),
            'PullMsgs': ('pull_msgs', social_reqrsp_pb2.SocialPullMsgsReq()),
            'RevokeMsg': ('revoke_msg', social_reqrsp_pb2.SocialRevokeMsgReq()),
            'DeleteMsg': ('delete_msg', social_reqrsp_pb2.SocialDeleteMsgReq()),
            'AddReaction': ('add_reaction', social_reqrsp_pb2.SocialAddReactionReq()),
            'RemoveReaction': ('remove_reaction', social_reqrsp_pb2.SocialRemoveReactionReq()),
            'GetReactions': ('get_reactions', social_reqrsp_pb2.SocialGetReactionsReq()),
            'GetSingleChatConvList': ('get_single_chat_conv_list', social_reqrsp_pb2.SocialGetSingleChatConvListReq()),
            'MarkRead': ('mark_read', social_reqrsp_pb2.SocialMarkReadReq()),
            'GetFansList': ('get_fans_list', social_reqrsp_pb2.SocialGetFansListReq()),
            'GetFollowList': ('get_follow_list', social_reqrsp_pb2.SocialGetFollowListReq()),
            'GetFriendList': ('get_friend_list', social_reqrsp_pb2.SocialGetFriendListReq()),
            'Follow': ('follow', social_reqrsp_pb2.SocialFollowReq()),
            'Unfollow': ('unfollow', social_reqrsp_pb2.SocialUnfollowReq()),
        }
        
        if method in method_map:
            field_name, req_msg = method_map[method]
            for key, value in request_data.items():
                if hasattr(req_msg, key):
                    field_descriptor = req_msg.DESCRIPTOR.fields_by_name.get(key)
                    if field_descriptor:
                        # 特殊处理：content 字段需要构造嵌套的 protobuf 消息
                        if key == 'content':
                            from client import social_share_pb2
                            content_msg = social_share_pb2.ChatMsgContent()
                            
                            # 如果 value 是 None，创建一个默认的文本消息
                            if value is None:
                                # 默认创建一个文本消息
                                content_msg.msg_type = 1  # TextMsgType
                                text_msg = social_share_pb2.TextMsgContent()
                                text_msg.text = "test message"
                                content_msg.text.CopyFrom(text_msg)
                            elif isinstance(value, dict):
                                # 如果 value 是字典，解析其中的字段
                                if 'msg_type' in value:
                                    content_msg.msg_type = value['msg_type']
                                if 'text' in value and isinstance(value['text'], dict):
                                    text_msg = social_share_pb2.TextMsgContent()
                                    if 'text' in value['text']:
                                        text_msg.text = value['text']['text']
                                    content_msg.text.CopyFrom(text_msg)
                            getattr(req_msg, key).CopyFrom(content_msg)
                        # 特殊处理：repeated 字段（如 seqs）
                        elif field_descriptor.label == field_descriptor.LABEL_REPEATED:
                            field_list = getattr(req_msg, key)
                            if isinstance(value, list):
                                field_list.extend(value)
                            else:
                                field_list.append(value)
                        else:
                            try:
                                setattr(req_msg, key, value)
                            except Exception as e:
                                logger.error(f"设置字段 {key} 失败: {e}, 值: {value}, 类型: {type(value)}")
                                raise EncodingError(f"设置字段 {key} 失败: {e}", 500) from e
                    else:
                        logger.warning(f"请求消息中没有字段 '{key}'，跳过")
            getattr(body_req, field_name).CopyFrom(req_msg)
        else:
            error_msg = f"未知的方法 '{method}'"
            logger.error(f"编码Social请求body失败: {error_msg}")
            logger.info(f"支持的方法: {list(method_map.keys())}")
            raise EncodingError(error_msg, 500)
        
        return body_req.SerializeToString()
    
    def _extract_error_code(self, head_bytes: bytes) -> int:
        """从响应头提取错误码"""
        if not PROTOBUF_AVAILABLE:
            return 200
        
        try:
            rsp_head = head_pb2.RspHead()
            rsp_head.ParseFromString(head_bytes)
            return rsp_head.code
        except:
            return 200
    
    def _extract_error_message(self, head_bytes: bytes) -> str:
        """从响应头提取错误信息"""
        if not PROTOBUF_AVAILABLE:
            return ''
        
        try:
            rsp_head = head_pb2.RspHead()
            rsp_head.ParseFromString(head_bytes)
            return rsp_head.desc
        except:
            return ''
    
    def _parse_response_body(self, service: str, method: str, body_bytes: bytes) -> Dict:
        """解析响应body"""
        if not PROTOBUF_AVAILABLE or not body_bytes:
            if body_bytes:
                return {
                    'raw_bytes': body_bytes.hex(),
                    'size': len(body_bytes)
                }
            return {}
        
        try:
            if service == 'Hall':
                return self._parse_hall_body_rsp(method, body_bytes)
            elif service == 'Room':
                return self._parse_room_body_rsp(method, body_bytes)
            elif service == 'Social':
                return self._parse_social_body_rsp(method, body_bytes)
        except Exception as e:
            print(f"⚠ 解析响应body失败: {e}")
            # 返回原始数据
            return {
                'raw_bytes': body_bytes.hex(),
                'size': len(body_bytes),
                'parse_error': str(e)
            }
        
        return {}
    
    def _parse_hall_body_rsp(self, method: str, body_bytes: bytes) -> Dict:
        """解析HallBodyRsp"""
        if not body_bytes:
            return {}
        
        try:
            body_rsp = hall_reqrsp_pb2.HallBodyRsp()
            body_rsp.ParseFromString(body_bytes)
            
            # 转换为字典
            result = self._protobuf_to_dict(body_rsp)
            
            # 根据方法名提取对应的响应字段
            method_field_map = {
                'FetchSelfFullUserInfo': 'fetch_self_full_user_info',
                'FetchSimpleUserInfo': 'fetch_simple_user_info',
                'UpdateNickname': 'update_nickname',
                'SellItem': 'sell_item',
                'BuyItem': 'buy_item',
                'StashToBackpack': 'stash_to_backpack',
                'BackpackToStash': 'backpack_to_stash',
                'ExchangeBackpackItem': 'exchange_backpack_item',
                'DebugAddCash': 'debug_add_cash',
                'DebugAddItem': 'debug_add_item',
            }
            
            # 如果方法有对应的字段，提取它
            if method in method_field_map:
                field_name = method_field_map[method]
                if field_name in result:
                    return {method.lower(): result[field_name]}
            
            return result
        except Exception as e:
            print(f"⚠ 解析HallBodyRsp失败: {e}")
            return {'raw_bytes': body_bytes.hex(), 'parse_error': str(e)}
    
    def _parse_room_body_rsp(self, method: str, body_bytes: bytes) -> Dict:
        """解析RoomBodyRsp"""
        if not body_bytes:
            return {}
        
        try:
            body_rsp = room_reqrsp_pb2.RoomBodyRsp()
            body_rsp.ParseFromString(body_bytes)
            
            result = self._protobuf_to_dict(body_rsp)
            
            method_field_map = {
                'GetUserState': 'get_user_state',
                'CreateTeam': 'create_team',
                'JoinTeam': 'join_team',
                'LeaveTeam': 'leave_team',
                'GetTeamInfo': 'get_team_info',
                'ChangeReadyState': 'change_ready_state',
                'StartGameFromTeam': 'start_game_from_team',
                'Match': 'match',
                'CancelMatch': 'cancel_match',
                'GetGameInfo': 'get_game_info',
            }
            
            if method in method_field_map:
                field_name = method_field_map[method]
                if field_name in result:
                    return {method.lower(): result[field_name]}
            
            return result
        except Exception as e:
            print(f"⚠ 解析RoomBodyRsp失败: {e}")
            return {'raw_bytes': body_bytes.hex(), 'parse_error': str(e)}
    
    def _parse_social_body_rsp(self, method: str, body_bytes: bytes) -> Dict:
        """解析SocialBodyRsp"""
        if not body_bytes:
            return {}
        
        try:
            body_rsp = social_reqrsp_pb2.SocialBodyRsp()
            body_rsp.ParseFromString(body_bytes)
            
            result = self._protobuf_to_dict(body_rsp)
            
            method_field_map = {
                'SendMessage': 'send_msg',
                'PullMsgs': 'pull_msgs',
                'RevokeMsg': 'revoke_msg',
                'DeleteMsg': 'delete_msg',
                'AddReaction': 'add_reaction',
                'RemoveReaction': 'remove_reaction',
                'GetReactions': 'get_reactions',
                'GetSingleChatConvList': 'get_single_chat_conv_list',
                'MarkRead': 'mark_read',
                'GetFansList': 'get_fans_list',
                'GetFollowList': 'get_follow_list',
                'GetFriendList': 'get_friend_list',
                'Follow': 'follow',
                'Unfollow': 'unfollow',
            }
            
            if method in method_field_map:
                field_name = method_field_map[method]
                if field_name in result:
                    return {method.lower(): result[field_name]}
            
            return result
        except Exception as e:
            print(f"⚠ 解析SocialBodyRsp失败: {e}")
            return {'raw_bytes': body_bytes.hex(), 'parse_error': str(e)}
    
    def _protobuf_to_dict(self, msg) -> Dict:
        """将protobuf消息转换为字典"""
        try:
            # 使用MessageToDict，这是处理proto3的最佳方式
            from google.protobuf.json_format import MessageToDict
            return MessageToDict(msg, including_default_value_fields=True, preserving_proto_field_name=True)
        except Exception as e:
            # 回退到手动解析
            result = {}
            try:
                for field_descriptor in msg.DESCRIPTOR.fields:
                    field_name = field_descriptor.name
                    value = getattr(msg, field_name)
                    
                    # 对于proto3，检查值是否为默认值
                    if field_descriptor.label == field_descriptor.LABEL_REPEATED:
                        # 重复字段，需要递归转换每个元素
                        if field_descriptor.type == field_descriptor.TYPE_MESSAGE:
                            # 重复的消息类型
                            result[field_name] = [self._protobuf_to_dict(item) for item in value]
                        else:
                            # 重复的基本类型
                            result[field_name] = list(value)
                    elif field_descriptor.type == field_descriptor.TYPE_MESSAGE:
                        # 嵌套消息
                        if value:
                            result[field_name] = self._protobuf_to_dict(value)
                    elif field_descriptor.type == field_descriptor.TYPE_STRING:
                        # 字符串，空字符串也包含（使用 including_default_value_fields=True）
                        result[field_name] = value
                    elif field_descriptor.type == field_descriptor.TYPE_BYTES:
                        # bytes，空bytes也包含
                        result[field_name] = value.hex() if value else ''
                    elif field_descriptor.type == field_descriptor.TYPE_BOOL:
                        # bool，False也包含
                        result[field_name] = value
                    else:
                        # 数值类型，0也包含（使用 including_default_value_fields=True）
                        result[field_name] = value
            except Exception as e2:
                print(f"⚠ protobuf转字典失败: {e2}")
            
            return result
    
    def close(self):
        """关闭连接"""
        if self.tcp_client:
            self.tcp_client.close()
            self.tcp_client = None
        if self.gate_socket:
            self.gate_socket.close()
            self.gate_socket = None

