"""
自动生成的Social服务测试代码
"""
import unittest
import sys
import os
import json

# 添加框架路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from framework.client import APIClient
from framework.config import Config


def safe_json_dumps(obj, indent=2, ensure_ascii=False):
    """安全地将对象转换为JSON字符串，处理protobuf对象"""
    def convert_to_dict(val):
        # 检查是否是 protobuf 消息对象
        if hasattr(val, 'DESCRIPTOR') and hasattr(val, 'SerializeToString'):
            try:
                from google.protobuf.json_format import MessageToDict
                return MessageToDict(val, including_default_value_fields=True, preserving_proto_field_name=True)
            except:
                # 如果 MessageToDict 失败，尝试手动转换
                result = {}
                try:
                    for field_descriptor in val.DESCRIPTOR.fields:
                        field_name = field_descriptor.name
                        field_value = getattr(val, field_name)
                        if field_descriptor.label == field_descriptor.LABEL_REPEATED:
                            result[field_name] = [convert_to_dict(item) for item in field_value]
                        elif field_descriptor.type == field_descriptor.TYPE_MESSAGE:
                            if field_value:
                                result[field_name] = convert_to_dict(field_value)
                        else:
                            result[field_name] = field_value
                except:
                    pass
                return result
        elif isinstance(val, dict):
            return {k: convert_to_dict(v) for k, v in val.items()}
        elif isinstance(val, list):
            return [convert_to_dict(item) for item in val]
        else:
            return val
    
    try:
        converted = convert_to_dict(obj)
        return json.dumps(converted, indent=indent, ensure_ascii=ensure_ascii, default=str)
    except Exception as e:
        # 如果转换失败，返回字符串表示
        return str(obj)


class TestSocial(unittest.TestCase):
    """Social服务测试"""
    
    @classmethod
    def setUpClass(cls):
        """测试类初始化"""
        cls.config = Config()
        cls.client = APIClient(cls.config)
        
        # 登录
        if not cls.client.login():
            raise Exception("登录失败")
        
        # 连接Gate
        if not cls.client.connect_gate():
            raise Exception("Gate连接失败")
        
        # 获取当前用户的UID（用于需要target_uid的接口）
        try:
            result = cls.client.call_rpc('Hall', 'FetchSelfFullUserInfo', {})
            if result.get('success'):
                response = result.get('response', {})
                # 提取UID
                if 'fetchselffulluserinfo' in response:
                    full_info = response['fetchselffulluserinfo']
                    if 'full_user_info' in full_info:
                        cls.current_uid = full_info['full_user_info'].get('uid', cls.client.uid)
                    else:
                        cls.current_uid = cls.client.uid
                else:
                    cls.current_uid = cls.client.uid
            else:
                cls.current_uid = cls.client.uid
        except:
            cls.current_uid = cls.client.uid
    
    @classmethod
    def tearDownClass(cls):
        """测试类清理"""
        if cls.client:
            cls.client.close()
    

    def test_sendmessage(self):
        """测试 SendMessage 接口（使用世界聊天场景）"""
        # 使用世界聊天场景（scene=4），不需要 room_id 或 to_uid，避免私聊需要先关注的问题
        request_data = {'to_uid': 0, 'conv_id': '', 'scene': 4, 'scene_id': 0, 'content': {'msg_type': 1, 'text': {'text': 'test message'}}}
        
        result = self.client.call_rpc(
            service='Social',
            method='SendMessage',
            request_data=request_data
        )
        
        # 保存测试结果用于报告
        self.test_result = {
            'name': 'SendMessage',
            'method': 'SendMessage',
            'request': request_data,
            'response': result,  # 保存完整的result，包括success、response、error_code、error_message
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': []
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n============================================================")
        print(f"测试接口: SendMessage")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"============================================================")
        
        # 断言
        if not result.get('success', False):
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ SendMessage 测试失败: {error_msg}")
            self.assertTrue(False, f"API调用失败: {error_msg}")
        else:
            print(f"\n✓ SendMessage 测试通过")

    def test_pullmsgs(self):
        """测试 PullMsgs 接口（前置条件：先发送消息获取conv_id）"""
        # 前置条件：先发送消息获取 conv_id（使用世界聊天场景，避免私聊需要先关注）
        send_result = self.client.call_rpc(
            service='Social',
            method='SendMessage',
            request_data={'to_uid': 0, 'scene': 4, 'scene_id': 0, 'content': {'msg_type': 1, 'text': {'text': 'test message'}}}
        )
        
        if not send_result.get('success'):
            self.skipTest(f"前置条件失败：无法发送消息 - {send_result.get('error_message', '未知错误')}")
        
        # 从发送消息的响应中获取 conv_id 和 seq
        send_response = send_result.get('response', {})
        conv_id = ''
        seq = 0
        if 'sendmessage' in send_response:
            send_msg = send_response['sendmessage']
            conv_id = send_msg.get('conv_id', '')
            seq = send_msg.get('seq', 0)
        
        if not conv_id:
            self.skipTest("前置条件失败：无法获取有效的 conv_id")
        
        # 使用获取到的 conv_id 调用接口
        # PullMsgs 需要 scene 参数，使用世界聊天场景（scene=4）
        request_data = {'conv_id': conv_id, 'scene': 4, 'scene_id': 0, 'start_seq': 0, 'count': 20, 'reverse': False}
        
        result = self.client.call_rpc(
            service='Social',
            method='PullMsgs',
            request_data=request_data
        )
        
        # 保存测试结果用于报告
        self.test_result = {
            'name': 'PullMsgs',
            'method': 'PullMsgs',
            'request': request_data,
            'response': result,  # 保存完整的result，包括success、response、error_code、error_message
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': []
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n============================================================")
        print(f"测试接口: PullMsgs")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"============================================================")
        
        # 断言
        if not result.get('success', False):
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ PullMsgs 测试失败: {error_msg}")
            self.assertTrue(False, f"API调用失败: {error_msg}")
        else:
            print(f"\n✓ PullMsgs 测试通过")

    def test_revokemsg(self):
        """测试 RevokeMsg 接口（前置条件：先发送消息获取conv_id和seq）"""
        # 前置条件：先发送消息获取 conv_id 和 seq（使用世界聊天场景，避免私聊需要先关注）
        send_result = self.client.call_rpc(
            service='Social',
            method='SendMessage',
            request_data={'to_uid': 0, 'scene': 4, 'scene_id': 0, 'content': {'msg_type': 1, 'text': {'text': 'test message'}}}
        )
        
        if not send_result.get('success'):
            self.skipTest(f"前置条件失败：无法发送消息 - {send_result.get('error_message', '未知错误')}")
        
        # 从发送消息的响应中获取 conv_id 和 seq
        send_response = send_result.get('response', {})
        conv_id = ''
        seq = 0
        if 'sendmessage' in send_response:
            send_msg = send_response['sendmessage']
            conv_id = send_msg.get('conv_id', '')
            seq = send_msg.get('seq', 0)
        
        if not conv_id or seq == 0:
            self.skipTest("前置条件失败：无法获取有效的 conv_id 和 seq")
        
        # 使用获取到的 conv_id 和 seq 调用接口
        if 'RevokeMsg' == 'DeleteMsg':
            request_data = {'conv_id': conv_id, 'seqs': [seq]}
        else:
            request_data = {'conv_id': conv_id, 'seq': seq}
        
        result = self.client.call_rpc(
            service='Social',
            method='RevokeMsg',
            request_data=request_data
        )
        
        # 保存测试结果用于报告
        self.test_result = {
            'name': 'RevokeMsg',
            'method': 'RevokeMsg',
            'request': request_data,
            'response': result,  # 保存完整的result，包括success、response、error_code、error_message
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': ['发送消息 (SendMessage)', '获取 conv_id']
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n============================================================")
        print(f"测试接口: RevokeMsg")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"============================================================")
        
        # 断言
        if not result.get('success', False):
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ RevokeMsg 测试失败: {error_msg}")
            self.assertTrue(False, f"API调用失败: {error_msg}")
        else:
            print(f"\n✓ RevokeMsg 测试通过")

    def test_deletemsg(self):
        """测试 DeleteMsg 接口（前置条件：先发送消息获取conv_id和seq）"""
        # 前置条件：先发送消息获取 conv_id 和 seq（使用世界聊天场景，避免私聊需要先关注）
        send_result = self.client.call_rpc(
            service='Social',
            method='SendMessage',
            request_data={'to_uid': 0, 'scene': 4, 'scene_id': 0, 'content': {'msg_type': 1, 'text': {'text': 'test message'}}}
        )
        
        if not send_result.get('success'):
            self.skipTest(f"前置条件失败：无法发送消息 - {send_result.get('error_message', '未知错误')}")
        
        # 从发送消息的响应中获取 conv_id 和 seq
        send_response = send_result.get('response', {})
        conv_id = ''
        seq = 0
        if 'sendmessage' in send_response:
            send_msg = send_response['sendmessage']
            conv_id = send_msg.get('conv_id', '')
            seq = send_msg.get('seq', 0)
        
        if not conv_id or seq == 0:
            self.skipTest("前置条件失败：无法获取有效的 conv_id 和 seq")
        
        # 使用获取到的 conv_id 和 seq 调用接口
        if 'DeleteMsg' == 'DeleteMsg':
            request_data = {'conv_id': conv_id, 'seqs': [seq]}
        else:
            request_data = {'conv_id': conv_id, 'seq': seq}
        
        result = self.client.call_rpc(
            service='Social',
            method='DeleteMsg',
            request_data=request_data
        )
        
        # 保存测试结果用于报告
        self.test_result = {
            'name': 'DeleteMsg',
            'method': 'DeleteMsg',
            'request': request_data,
            'response': result,  # 保存完整的result，包括success、response、error_code、error_message
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': ['发送消息 (SendMessage)', '获取 conv_id']
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n============================================================")
        print(f"测试接口: DeleteMsg")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"============================================================")
        
        # 断言
        if not result.get('success', False):
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ DeleteMsg 测试失败: {error_msg}")
            self.assertTrue(False, f"API调用失败: {error_msg}")
        else:
            print(f"\n✓ DeleteMsg 测试通过")

    def test_addreaction(self):
        """测试 AddReaction 接口（前置条件：先发送消息获取conv_id和seq）"""
        # 前置条件：先发送消息获取 conv_id 和 seq（使用世界聊天场景，避免私聊需要先关注）
        send_result = self.client.call_rpc(
            service='Social',
            method='SendMessage',
            request_data={'to_uid': 0, 'scene': 4, 'scene_id': 0, 'content': {'msg_type': 1, 'text': {'text': 'test message'}}}
        )
        
        if not send_result.get('success'):
            self.skipTest(f"前置条件失败：无法发送消息 - {send_result.get('error_message', '未知错误')}")
        
        # 从发送消息的响应中获取 conv_id 和 seq
        send_response = send_result.get('response', {})
        conv_id = ''
        seq = 0
        if 'sendmessage' in send_response:
            send_msg = send_response['sendmessage']
            conv_id = send_msg.get('conv_id', '')
            seq = send_msg.get('seq', 0)
        
        if not conv_id or seq == 0:
            self.skipTest("前置条件失败：无法获取有效的 conv_id 和 seq")
        
        # 使用获取到的 conv_id 和 seq 调用接口
        if 'AddReaction' == 'DeleteMsg':
            request_data = {'conv_id': conv_id, 'seqs': [seq]}
        else:
            request_data = {'conv_id': conv_id, 'seq': seq}
        
        result = self.client.call_rpc(
            service='Social',
            method='AddReaction',
            request_data=request_data
        )
        
        # 保存测试结果用于报告
        self.test_result = {
            'name': 'AddReaction',
            'method': 'AddReaction',
            'request': request_data,
            'response': result,  # 保存完整的result，包括success、response、error_code、error_message
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': ['发送消息 (SendMessage)', '获取 conv_id']
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n============================================================")
        print(f"测试接口: AddReaction")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"============================================================")
        
        # 断言
        if not result.get('success', False):
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ AddReaction 测试失败: {error_msg}")
            self.assertTrue(False, f"API调用失败: {error_msg}")
        else:
            print(f"\n✓ AddReaction 测试通过")

    def test_removereaction(self):
        """测试 RemoveReaction 接口（前置条件：先发送消息获取conv_id和seq）"""
        # 前置条件：先发送消息获取 conv_id 和 seq（使用世界聊天场景，避免私聊需要先关注）
        send_result = self.client.call_rpc(
            service='Social',
            method='SendMessage',
            request_data={'to_uid': 0, 'scene': 4, 'scene_id': 0, 'content': {'msg_type': 1, 'text': {'text': 'test message'}}}
        )
        
        if not send_result.get('success'):
            self.skipTest(f"前置条件失败：无法发送消息 - {send_result.get('error_message', '未知错误')}")
        
        # 从发送消息的响应中获取 conv_id 和 seq
        send_response = send_result.get('response', {})
        conv_id = ''
        seq = 0
        if 'sendmessage' in send_response:
            send_msg = send_response['sendmessage']
            conv_id = send_msg.get('conv_id', '')
            seq = send_msg.get('seq', 0)
        
        if not conv_id or seq == 0:
            self.skipTest("前置条件失败：无法获取有效的 conv_id 和 seq")
        
        # 使用获取到的 conv_id 和 seq 调用接口
        if 'RemoveReaction' == 'DeleteMsg':
            request_data = {'conv_id': conv_id, 'seqs': [seq]}
        else:
            request_data = {'conv_id': conv_id, 'seq': seq}
        
        result = self.client.call_rpc(
            service='Social',
            method='RemoveReaction',
            request_data=request_data
        )
        
        # 保存测试结果用于报告
        self.test_result = {
            'name': 'RemoveReaction',
            'method': 'RemoveReaction',
            'request': request_data,
            'response': result,  # 保存完整的result，包括success、response、error_code、error_message
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': ['发送消息 (SendMessage)', '获取 conv_id']
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n============================================================")
        print(f"测试接口: RemoveReaction")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"============================================================")
        
        # 断言
        if not result.get('success', False):
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ RemoveReaction 测试失败: {error_msg}")
            self.assertTrue(False, f"API调用失败: {error_msg}")
        else:
            print(f"\n✓ RemoveReaction 测试通过")

    def test_getreactions(self):
        """测试 GetReactions 接口（前置条件：先发送消息获取conv_id和seq）"""
        # 前置条件：先发送消息获取 conv_id 和 seq（使用世界聊天场景，避免私聊需要先关注）
        send_result = self.client.call_rpc(
            service='Social',
            method='SendMessage',
            request_data={'to_uid': 0, 'scene': 4, 'scene_id': 0, 'content': {'msg_type': 1, 'text': {'text': 'test message'}}}
        )
        
        if not send_result.get('success'):
            self.skipTest(f"前置条件失败：无法发送消息 - {send_result.get('error_message', '未知错误')}")
        
        # 从发送消息的响应中获取 conv_id 和 seq
        send_response = send_result.get('response', {})
        conv_id = ''
        seq = 0
        if 'sendmessage' in send_response:
            send_msg = send_response['sendmessage']
            conv_id = send_msg.get('conv_id', '')
            seq = send_msg.get('seq', 0)
        
        if not conv_id or seq == 0:
            self.skipTest("前置条件失败：无法获取有效的 conv_id 和 seq")
        
        # 使用获取到的 conv_id 和 seq 调用接口
        if 'GetReactions' == 'DeleteMsg':
            request_data = {'conv_id': conv_id, 'seqs': [seq]}
        else:
            request_data = {'conv_id': conv_id, 'seq': seq}
        
        result = self.client.call_rpc(
            service='Social',
            method='GetReactions',
            request_data=request_data
        )
        
        # 保存测试结果用于报告
        self.test_result = {
            'name': 'GetReactions',
            'method': 'GetReactions',
            'request': request_data,
            'response': result,  # 保存完整的result，包括success、response、error_code、error_message
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': ['发送消息 (SendMessage)', '获取 conv_id']
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n============================================================")
        print(f"测试接口: GetReactions")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"============================================================")
        
        # 断言
        if not result.get('success', False):
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetReactions 测试失败: {error_msg}")
            self.assertTrue(False, f"API调用失败: {error_msg}")
        else:
            print(f"\n✓ GetReactions 测试通过")

    def test_getsinglechatconvlist(self):
        """测试 GetSingleChatConvList 接口"""
        request_data = {}
        
        result = self.client.call_rpc(
            service='Social',
            method='GetSingleChatConvList',
            request_data=request_data
        )
        
        # 保存测试结果用于报告
        self.test_result = {
            'name': 'GetSingleChatConvList',
            'method': 'GetSingleChatConvList',
            'request': request_data,
            'response': result,  # 保存完整的result，包括success、response、error_code、error_message
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': []
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n============================================================")
        print(f"测试接口: GetSingleChatConvList")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"============================================================")
        
        # 断言
        if not result.get('success', False):
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetSingleChatConvList 测试失败: {error_msg}")
            self.assertTrue(False, f"API调用失败: {error_msg}")
        else:
            print(f"\n✓ GetSingleChatConvList 测试通过")

    def test_markread(self):
        """测试 MarkRead 接口（服务器端未实现）"""
        # MarkRead 接口在服务器端未实现，跳过测试
        self.skipTest("MarkRead 接口在服务器端未实现")

    def test_getfanslist(self):
        """测试 GetFansList 接口"""
        request_data = {}
        
        result = self.client.call_rpc(
            service='Social',
            method='GetFansList',
            request_data=request_data
        )
        
        # 保存测试结果用于报告
        self.test_result = {
            'name': 'GetFansList',
            'method': 'GetFansList',
            'request': request_data,
            'response': result,  # 保存完整的result，包括success、response、error_code、error_message
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': []
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n============================================================")
        print(f"测试接口: GetFansList")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"============================================================")
        
        # 断言
        if not result.get('success', False):
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetFansList 测试失败: {error_msg}")
            self.assertTrue(False, f"API调用失败: {error_msg}")
        else:
            print(f"\n✓ GetFansList 测试通过")

    def test_getfollowlist(self):
        """测试 GetFollowList 接口"""
        request_data = {}
        
        result = self.client.call_rpc(
            service='Social',
            method='GetFollowList',
            request_data=request_data
        )
        
        # 保存测试结果用于报告
        self.test_result = {
            'name': 'GetFollowList',
            'method': 'GetFollowList',
            'request': request_data,
            'response': result,  # 保存完整的result，包括success、response、error_code、error_message
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': []
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n============================================================")
        print(f"测试接口: GetFollowList")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"============================================================")
        
        # 断言
        if not result.get('success', False):
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetFollowList 测试失败: {error_msg}")
            self.assertTrue(False, f"API调用失败: {error_msg}")
        else:
            print(f"\n✓ GetFollowList 测试通过")

    def test_getfriendlist(self):
        """测试 GetFriendList 接口"""
        request_data = {}
        
        result = self.client.call_rpc(
            service='Social',
            method='GetFriendList',
            request_data=request_data
        )
        
        # 保存测试结果用于报告
        self.test_result = {
            'name': 'GetFriendList',
            'method': 'GetFriendList',
            'request': request_data,
            'response': result,  # 保存完整的result，包括success、response、error_code、error_message
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': []
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n============================================================")
        print(f"测试接口: GetFriendList")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"============================================================")
        
        # 断言
        if not result.get('success', False):
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetFriendList 测试失败: {error_msg}")
            self.assertTrue(False, f"API调用失败: {error_msg}")
        else:
            print(f"\n✓ GetFriendList 测试通过")

    def test_follow(self):
        """测试 Follow 接口（前置条件：使用有效的target_uid）"""
        # 使用一个有效的 target_uid（不能是自己）
        current_uid = self.current_uid if hasattr(self, 'current_uid') else self.client.uid
        # 使用一个测试用的 target_uid（当前 UID + 1，或者使用一个固定的测试 UID）
        target_uid = current_uid + 1 if current_uid > 0 else 10000001
        
        request_data = {'target_uid': target_uid}
        
        result = self.client.call_rpc(
            service='Social',
            method='Follow',
            request_data=request_data
        )
        
        # 保存测试结果用于报告
        self.test_result = {
            'name': 'Follow',
            'method': 'Follow',
            'request': request_data,
            'response': result,  # 保存完整的result，包括success、response、error_code、error_message
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': ['先关注 (Follow)', '使用有效的 target_uid']
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n============================================================")
        print(f"测试接口: Follow")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"============================================================")
        
        # 断言
        if not result.get('success', False):
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ Follow 测试失败: {error_msg}")
            self.assertTrue(False, f"API调用失败: {error_msg}")
        else:
            print(f"\n✓ Follow 测试通过")

    def test_unfollow(self):
        """测试 Unfollow 接口（前置条件：先关注）"""
        # 前置条件：先关注
        current_uid = self.current_uid if hasattr(self, 'current_uid') else self.client.uid
        target_uid = current_uid + 1 if current_uid > 0 else 10000001
        
        follow_result = self.client.call_rpc(
            service='Social',
            method='Follow',
            request_data={'target_uid': target_uid}
        )
        
        # 即使关注失败也继续测试（可能已经关注过了）
        
        # 使用获取到的 target_uid 调用 Unfollow
        request_data = {'target_uid': target_uid}
        
        result = self.client.call_rpc(
            service='Social',
            method='Unfollow',
            request_data=request_data
        )
        
        # 保存测试结果用于报告
        self.test_result = {
            'name': 'Unfollow',
            'method': 'Unfollow',
            'request': request_data,
            'response': result,  # 保存完整的result，包括success、response、error_code、error_message
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': []
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n============================================================")
        print(f"测试接口: Unfollow")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"============================================================")
        
        # 断言
        if not result.get('success', False):
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ Unfollow 测试失败: {error_msg}")
            self.assertTrue(False, f"API调用失败: {error_msg}")
        else:
            print(f"\n✓ Unfollow 测试通过")

if __name__ == '__main__':
    unittest.main()
