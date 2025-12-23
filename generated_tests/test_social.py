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
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': []
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: SendMessage")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 断言
        if not result.get('success', False):
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ SendMessage 测试失败: {error_msg}")
            self.assertTrue(False, f"API调用失败: {error_msg}")
        else:
            print(f"\n✓ SendMessage 测试通过")

    def test_sendmessage_参数异常_必填参数缺失(self):
        """测试 SendMessage 接口 - 参数异常 - 参数异常_必填参数缺失"""
        request_data = {'conv_id': '', 'scene': 4, 'scene_id': 10000263, 'to_uid': 10000263, 'content': None, 'client_msg_id': 10000263}
        
        result = self.client.call_rpc(
            service='Social',
            method='SendMessage',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'SendMessage_参数异常_必填参数缺失',
            'method': 'SendMessage',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_必填参数缺失',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: SendMessage - 参数异常 - 参数异常_必填参数缺失")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ SendMessage 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ SendMessage 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_sendmessage_参数异常_参数类型错误(self):
        """测试 SendMessage 接口 - 参数异常 - 参数异常_参数类型错误"""
        request_data = {'conv_id': 12345, 'scene': 4, 'scene_id': 10000263, 'to_uid': 10000263, 'content': None, 'client_msg_id': 10000263}
        
        result = self.client.call_rpc(
            service='Social',
            method='SendMessage',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'SendMessage_参数异常_参数类型错误',
            'method': 'SendMessage',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_参数类型错误',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: SendMessage - 参数异常 - 参数异常_参数类型错误")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ SendMessage 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ SendMessage 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_sendmessage_参数异常_参数值为空(self):
        """测试 SendMessage 接口 - 参数异常 - 参数异常_参数值为空"""
        request_data = {'conv_id': '', 'scene': 4, 'scene_id': 10000263, 'to_uid': 10000263, 'content': None, 'client_msg_id': 10000263}
        
        result = self.client.call_rpc(
            service='Social',
            method='SendMessage',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'SendMessage_参数异常_参数值为空',
            'method': 'SendMessage',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_参数值为空',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: SendMessage - 参数异常 - 参数异常_参数值为空")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ SendMessage 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ SendMessage 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_sendmessage_参数异常_参数值超出范围(self):
        """测试 SendMessage 接口 - 参数异常 - 参数异常_参数值超出范围"""
        request_data = {'conv_id': 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', 'scene': 4, 'scene_id': 10000263, 'to_uid': 10000263, 'content': None, 'client_msg_id': 10000263}
        
        result = self.client.call_rpc(
            service='Social',
            method='SendMessage',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'SendMessage_参数异常_参数值超出范围',
            'method': 'SendMessage',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_参数值超出范围',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: SendMessage - 参数异常 - 参数异常_参数值超出范围")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ SendMessage 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ SendMessage 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_sendmessage_参数异常_参数格式错误(self):
        """测试 SendMessage 接口 - 参数异常 - 参数异常_参数格式错误"""
        request_data = {'conv_id': -1, 'scene': 4, 'scene_id': 10000263, 'to_uid': 10000263, 'content': None, 'client_msg_id': 10000263}
        
        result = self.client.call_rpc(
            service='Social',
            method='SendMessage',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'SendMessage_参数异常_参数格式错误',
            'method': 'SendMessage',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_参数格式错误',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: SendMessage - 参数异常 - 参数异常_参数格式错误")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ SendMessage 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ SendMessage 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_sendmessage_业务异常(self):
        """测试 SendMessage 接口 - 业务异常 - 业务异常"""
        request_data = {'conv_id': 'invalid_conv_id', 'scene': 4, 'scene_id': 10000263, 'to_uid': 10000263, 'content': None, 'client_msg_id': 10000263}
        
        result = self.client.call_rpc(
            service='Social',
            method='SendMessage',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'SendMessage_业务异常',
            'method': 'SendMessage',
            'dimension': '业务异常',
            'abnormal_type': '业务异常',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: SendMessage - 业务异常 - 业务异常")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ SendMessage 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ SendMessage 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_sendmessage_权限安全(self):
        """测试 SendMessage 接口 - 权限安全 - 权限安全"""
        request_data = {'conv_id': 10000263, 'scene': 4, 'scene_id': 10000263, 'to_uid': 10000263, 'content': None, 'client_msg_id': 10000263}
        
        result = self.client.call_rpc(
            service='Social',
            method='SendMessage',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'SendMessage_权限安全',
            'method': 'SendMessage',
            'dimension': '权限安全',
            'abnormal_type': '权限安全',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '403'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: SendMessage - 权限安全 - 权限安全")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ SendMessage 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ SendMessage 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_sendmessage_性能边界(self):
        """测试 SendMessage 接口 - 性能边界 - 性能边界"""
        request_data = {'conv_id': 10000263, 'scene': 4, 'scene_id': 10000263, 'to_uid': 10000263, 'content': None, 'client_msg_id': 10000263}
        
        result = self.client.call_rpc(
            service='Social',
            method='SendMessage',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'SendMessage_性能边界',
            'method': 'SendMessage',
            'dimension': '性能边界',
            'abnormal_type': '性能边界',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '200'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: SendMessage - 性能边界 - 性能边界")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ SendMessage 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ SendMessage 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_pullmsgs_参数异常_必填参数缺失(self):
        """测试 PullMsgs 接口 - 参数异常 - 参数异常_必填参数缺失"""
        request_data = {'conv_id': '', 'scene': 4, 'scene_id': 10000263, 'start_seq': 1, 'count': 20, 'reverse': True}
        
        result = self.client.call_rpc(
            service='Social',
            method='PullMsgs',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'PullMsgs_参数异常_必填参数缺失',
            'method': 'PullMsgs',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_必填参数缺失',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: PullMsgs - 参数异常 - 参数异常_必填参数缺失")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ PullMsgs 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ PullMsgs 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_pullmsgs_参数异常_参数类型错误(self):
        """测试 PullMsgs 接口 - 参数异常 - 参数异常_参数类型错误"""
        request_data = {'conv_id': 12345, 'scene': 4, 'scene_id': 10000263, 'start_seq': 1, 'count': 20, 'reverse': True}
        
        result = self.client.call_rpc(
            service='Social',
            method='PullMsgs',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'PullMsgs_参数异常_参数类型错误',
            'method': 'PullMsgs',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_参数类型错误',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: PullMsgs - 参数异常 - 参数异常_参数类型错误")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ PullMsgs 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ PullMsgs 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_pullmsgs_参数异常_参数值为空(self):
        """测试 PullMsgs 接口 - 参数异常 - 参数异常_参数值为空"""
        request_data = {'conv_id': '', 'scene': 4, 'scene_id': 10000263, 'start_seq': 1, 'count': 20, 'reverse': True}
        
        result = self.client.call_rpc(
            service='Social',
            method='PullMsgs',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'PullMsgs_参数异常_参数值为空',
            'method': 'PullMsgs',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_参数值为空',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: PullMsgs - 参数异常 - 参数异常_参数值为空")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ PullMsgs 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ PullMsgs 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_pullmsgs_参数异常_参数值超出范围(self):
        """测试 PullMsgs 接口 - 参数异常 - 参数异常_参数值超出范围"""
        request_data = {'conv_id': 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', 'scene': 4, 'scene_id': 10000263, 'start_seq': 1, 'count': 20, 'reverse': True}
        
        result = self.client.call_rpc(
            service='Social',
            method='PullMsgs',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'PullMsgs_参数异常_参数值超出范围',
            'method': 'PullMsgs',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_参数值超出范围',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: PullMsgs - 参数异常 - 参数异常_参数值超出范围")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ PullMsgs 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ PullMsgs 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_pullmsgs_参数异常_参数格式错误(self):
        """测试 PullMsgs 接口 - 参数异常 - 参数异常_参数格式错误"""
        request_data = {'conv_id': -1, 'scene': 4, 'scene_id': 10000263, 'start_seq': 1, 'count': 20, 'reverse': True}
        
        result = self.client.call_rpc(
            service='Social',
            method='PullMsgs',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'PullMsgs_参数异常_参数格式错误',
            'method': 'PullMsgs',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_参数格式错误',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: PullMsgs - 参数异常 - 参数异常_参数格式错误")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ PullMsgs 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ PullMsgs 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_pullmsgs_权限安全(self):
        """测试 PullMsgs 接口 - 权限安全 - 权限安全"""
        request_data = {'conv_id': 10000263, 'scene': 4, 'scene_id': 10000263, 'start_seq': 1, 'count': 20, 'reverse': True}
        
        result = self.client.call_rpc(
            service='Social',
            method='PullMsgs',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'PullMsgs_权限安全',
            'method': 'PullMsgs',
            'dimension': '权限安全',
            'abnormal_type': '权限安全',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '403'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: PullMsgs - 权限安全 - 权限安全")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ PullMsgs 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ PullMsgs 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_pullmsgs_性能边界(self):
        """测试 PullMsgs 接口 - 性能边界 - 性能边界"""
        request_data = {'conv_id': 10000263, 'scene': 4, 'scene_id': 10000263, 'start_seq': 1, 'count': 20, 'reverse': True}
        
        result = self.client.call_rpc(
            service='Social',
            method='PullMsgs',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'PullMsgs_性能边界',
            'method': 'PullMsgs',
            'dimension': '性能边界',
            'abnormal_type': '性能边界',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '200'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: PullMsgs - 性能边界 - 性能边界")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ PullMsgs 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ PullMsgs 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

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
            'preconditions': [
                '发送消息 (SendMessage): to_uid=0, scene=4, scene_id=0',
                '从响应获取: conv_id, seq'
            ]
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n============================================================")
        print(f"测试接口: RevokeMsg")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
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

    def test_revokemsg_参数异常_必填参数缺失(self):
        """测试 RevokeMsg 接口 - 参数异常 - 参数异常_必填参数缺失"""
        request_data = {'conv_id': '', 'seq': 1}
        
        result = self.client.call_rpc(
            service='Social',
            method='RevokeMsg',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'RevokeMsg_参数异常_必填参数缺失',
            'method': 'RevokeMsg',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_必填参数缺失',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: RevokeMsg - 参数异常 - 参数异常_必填参数缺失")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ RevokeMsg 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ RevokeMsg 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_revokemsg_参数异常_参数类型错误(self):
        """测试 RevokeMsg 接口 - 参数异常 - 参数异常_参数类型错误"""
        request_data = {'conv_id': 12345, 'seq': 1}
        
        result = self.client.call_rpc(
            service='Social',
            method='RevokeMsg',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'RevokeMsg_参数异常_参数类型错误',
            'method': 'RevokeMsg',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_参数类型错误',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: RevokeMsg - 参数异常 - 参数异常_参数类型错误")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ RevokeMsg 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ RevokeMsg 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_revokemsg_参数异常_参数值为空(self):
        """测试 RevokeMsg 接口 - 参数异常 - 参数异常_参数值为空"""
        request_data = {'conv_id': '', 'seq': 1}
        
        result = self.client.call_rpc(
            service='Social',
            method='RevokeMsg',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'RevokeMsg_参数异常_参数值为空',
            'method': 'RevokeMsg',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_参数值为空',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: RevokeMsg - 参数异常 - 参数异常_参数值为空")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ RevokeMsg 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ RevokeMsg 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_revokemsg_参数异常_参数值超出范围(self):
        """测试 RevokeMsg 接口 - 参数异常 - 参数异常_参数值超出范围"""
        request_data = {'conv_id': 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', 'seq': 1}
        
        result = self.client.call_rpc(
            service='Social',
            method='RevokeMsg',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'RevokeMsg_参数异常_参数值超出范围',
            'method': 'RevokeMsg',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_参数值超出范围',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: RevokeMsg - 参数异常 - 参数异常_参数值超出范围")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ RevokeMsg 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ RevokeMsg 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_revokemsg_参数异常_参数格式错误(self):
        """测试 RevokeMsg 接口 - 参数异常 - 参数异常_参数格式错误"""
        request_data = {'conv_id': -1, 'seq': 1}
        
        result = self.client.call_rpc(
            service='Social',
            method='RevokeMsg',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'RevokeMsg_参数异常_参数格式错误',
            'method': 'RevokeMsg',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_参数格式错误',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: RevokeMsg - 参数异常 - 参数异常_参数格式错误")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ RevokeMsg 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ RevokeMsg 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_revokemsg_权限安全(self):
        """测试 RevokeMsg 接口 - 权限安全 - 权限安全"""
        request_data = {'conv_id': 10000263, 'seq': 1}
        
        result = self.client.call_rpc(
            service='Social',
            method='RevokeMsg',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'RevokeMsg_权限安全',
            'method': 'RevokeMsg',
            'dimension': '权限安全',
            'abnormal_type': '权限安全',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '403'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: RevokeMsg - 权限安全 - 权限安全")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ RevokeMsg 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ RevokeMsg 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_revokemsg_性能边界(self):
        """测试 RevokeMsg 接口 - 性能边界 - 性能边界"""
        request_data = {'conv_id': 10000263, 'seq': 1}
        
        result = self.client.call_rpc(
            service='Social',
            method='RevokeMsg',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'RevokeMsg_性能边界',
            'method': 'RevokeMsg',
            'dimension': '性能边界',
            'abnormal_type': '性能边界',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '200'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: RevokeMsg - 性能边界 - 性能边界")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ RevokeMsg 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ RevokeMsg 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

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
            'preconditions': [
                '发送消息 (SendMessage): to_uid=0, scene=4, scene_id=0',
                '从响应获取: conv_id, seq'
            ]
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n============================================================")
        print(f"测试接口: DeleteMsg")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
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

    def test_deletemsg_参数异常_必填参数缺失(self):
        """测试 DeleteMsg 接口 - 参数异常 - 参数异常_必填参数缺失"""
        request_data = {'conv_id': '', 'seqs': 1}
        
        result = self.client.call_rpc(
            service='Social',
            method='DeleteMsg',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'DeleteMsg_参数异常_必填参数缺失',
            'method': 'DeleteMsg',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_必填参数缺失',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: DeleteMsg - 参数异常 - 参数异常_必填参数缺失")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ DeleteMsg 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ DeleteMsg 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_deletemsg_参数异常_参数类型错误(self):
        """测试 DeleteMsg 接口 - 参数异常 - 参数异常_参数类型错误"""
        request_data = {'conv_id': 12345, 'seqs': 1}
        
        result = self.client.call_rpc(
            service='Social',
            method='DeleteMsg',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'DeleteMsg_参数异常_参数类型错误',
            'method': 'DeleteMsg',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_参数类型错误',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: DeleteMsg - 参数异常 - 参数异常_参数类型错误")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ DeleteMsg 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ DeleteMsg 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_deletemsg_参数异常_参数值为空(self):
        """测试 DeleteMsg 接口 - 参数异常 - 参数异常_参数值为空"""
        request_data = {'conv_id': '', 'seqs': 1}
        
        result = self.client.call_rpc(
            service='Social',
            method='DeleteMsg',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'DeleteMsg_参数异常_参数值为空',
            'method': 'DeleteMsg',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_参数值为空',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: DeleteMsg - 参数异常 - 参数异常_参数值为空")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ DeleteMsg 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ DeleteMsg 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_deletemsg_参数异常_参数值超出范围(self):
        """测试 DeleteMsg 接口 - 参数异常 - 参数异常_参数值超出范围"""
        request_data = {'conv_id': 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', 'seqs': 1}
        
        result = self.client.call_rpc(
            service='Social',
            method='DeleteMsg',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'DeleteMsg_参数异常_参数值超出范围',
            'method': 'DeleteMsg',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_参数值超出范围',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: DeleteMsg - 参数异常 - 参数异常_参数值超出范围")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ DeleteMsg 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ DeleteMsg 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_deletemsg_参数异常_参数格式错误(self):
        """测试 DeleteMsg 接口 - 参数异常 - 参数异常_参数格式错误"""
        request_data = {'conv_id': -1, 'seqs': 1}
        
        result = self.client.call_rpc(
            service='Social',
            method='DeleteMsg',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'DeleteMsg_参数异常_参数格式错误',
            'method': 'DeleteMsg',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_参数格式错误',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: DeleteMsg - 参数异常 - 参数异常_参数格式错误")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ DeleteMsg 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ DeleteMsg 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_deletemsg_权限安全(self):
        """测试 DeleteMsg 接口 - 权限安全 - 权限安全"""
        request_data = {'conv_id': 10000263, 'seqs': 1}
        
        result = self.client.call_rpc(
            service='Social',
            method='DeleteMsg',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'DeleteMsg_权限安全',
            'method': 'DeleteMsg',
            'dimension': '权限安全',
            'abnormal_type': '权限安全',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '403'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: DeleteMsg - 权限安全 - 权限安全")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ DeleteMsg 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ DeleteMsg 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_deletemsg_性能边界(self):
        """测试 DeleteMsg 接口 - 性能边界 - 性能边界"""
        request_data = {'conv_id': 10000263, 'seqs': 1}
        
        result = self.client.call_rpc(
            service='Social',
            method='DeleteMsg',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'DeleteMsg_性能边界',
            'method': 'DeleteMsg',
            'dimension': '性能边界',
            'abnormal_type': '性能边界',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '200'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: DeleteMsg - 性能边界 - 性能边界")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ DeleteMsg 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ DeleteMsg 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

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
            'preconditions': [
                '发送消息 (SendMessage): to_uid=0, scene=4, scene_id=0',
                '从响应获取: conv_id, seq'
            ]
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n============================================================")
        print(f"测试接口: AddReaction")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
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

    def test_addreaction_参数异常_必填参数缺失(self):
        """测试 AddReaction 接口 - 参数异常 - 参数异常_必填参数缺失"""
        request_data = {'conv_id': '', 'seq': 1, 'reaction_id': 10000263}
        
        result = self.client.call_rpc(
            service='Social',
            method='AddReaction',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'AddReaction_参数异常_必填参数缺失',
            'method': 'AddReaction',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_必填参数缺失',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: AddReaction - 参数异常 - 参数异常_必填参数缺失")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ AddReaction 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ AddReaction 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_addreaction_参数异常_参数类型错误(self):
        """测试 AddReaction 接口 - 参数异常 - 参数异常_参数类型错误"""
        request_data = {'conv_id': 12345, 'seq': 1, 'reaction_id': 10000263}
        
        result = self.client.call_rpc(
            service='Social',
            method='AddReaction',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'AddReaction_参数异常_参数类型错误',
            'method': 'AddReaction',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_参数类型错误',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: AddReaction - 参数异常 - 参数异常_参数类型错误")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ AddReaction 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ AddReaction 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_addreaction_参数异常_参数值为空(self):
        """测试 AddReaction 接口 - 参数异常 - 参数异常_参数值为空"""
        request_data = {'conv_id': '', 'seq': 1, 'reaction_id': 10000263}
        
        result = self.client.call_rpc(
            service='Social',
            method='AddReaction',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'AddReaction_参数异常_参数值为空',
            'method': 'AddReaction',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_参数值为空',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: AddReaction - 参数异常 - 参数异常_参数值为空")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ AddReaction 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ AddReaction 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_addreaction_参数异常_参数值超出范围(self):
        """测试 AddReaction 接口 - 参数异常 - 参数异常_参数值超出范围"""
        request_data = {'conv_id': 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', 'seq': 1, 'reaction_id': 10000263}
        
        result = self.client.call_rpc(
            service='Social',
            method='AddReaction',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'AddReaction_参数异常_参数值超出范围',
            'method': 'AddReaction',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_参数值超出范围',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: AddReaction - 参数异常 - 参数异常_参数值超出范围")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ AddReaction 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ AddReaction 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_addreaction_参数异常_参数格式错误(self):
        """测试 AddReaction 接口 - 参数异常 - 参数异常_参数格式错误"""
        request_data = {'conv_id': -1, 'seq': 1, 'reaction_id': 10000263}
        
        result = self.client.call_rpc(
            service='Social',
            method='AddReaction',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'AddReaction_参数异常_参数格式错误',
            'method': 'AddReaction',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_参数格式错误',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: AddReaction - 参数异常 - 参数异常_参数格式错误")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ AddReaction 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ AddReaction 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_addreaction_权限安全(self):
        """测试 AddReaction 接口 - 权限安全 - 权限安全"""
        request_data = {'conv_id': 10000263, 'seq': 1, 'reaction_id': 10000263}
        
        result = self.client.call_rpc(
            service='Social',
            method='AddReaction',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'AddReaction_权限安全',
            'method': 'AddReaction',
            'dimension': '权限安全',
            'abnormal_type': '权限安全',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '403'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: AddReaction - 权限安全 - 权限安全")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ AddReaction 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ AddReaction 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_addreaction_性能边界(self):
        """测试 AddReaction 接口 - 性能边界 - 性能边界"""
        request_data = {'conv_id': 10000263, 'seq': 1, 'reaction_id': 10000263}
        
        result = self.client.call_rpc(
            service='Social',
            method='AddReaction',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'AddReaction_性能边界',
            'method': 'AddReaction',
            'dimension': '性能边界',
            'abnormal_type': '性能边界',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '200'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: AddReaction - 性能边界 - 性能边界")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ AddReaction 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ AddReaction 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

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
            'preconditions': [
                '发送消息 (SendMessage): to_uid=0, scene=4, scene_id=0',
                '从响应获取: conv_id, seq'
            ]
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n============================================================")
        print(f"测试接口: RemoveReaction")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
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

    def test_removereaction_参数异常_必填参数缺失(self):
        """测试 RemoveReaction 接口 - 参数异常 - 参数异常_必填参数缺失"""
        request_data = {'conv_id': '', 'seq': 1, 'reaction_id': 10000263}
        
        result = self.client.call_rpc(
            service='Social',
            method='RemoveReaction',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'RemoveReaction_参数异常_必填参数缺失',
            'method': 'RemoveReaction',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_必填参数缺失',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: RemoveReaction - 参数异常 - 参数异常_必填参数缺失")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ RemoveReaction 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ RemoveReaction 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_removereaction_参数异常_参数类型错误(self):
        """测试 RemoveReaction 接口 - 参数异常 - 参数异常_参数类型错误"""
        request_data = {'conv_id': 12345, 'seq': 1, 'reaction_id': 10000263}
        
        result = self.client.call_rpc(
            service='Social',
            method='RemoveReaction',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'RemoveReaction_参数异常_参数类型错误',
            'method': 'RemoveReaction',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_参数类型错误',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: RemoveReaction - 参数异常 - 参数异常_参数类型错误")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ RemoveReaction 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ RemoveReaction 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_removereaction_参数异常_参数值为空(self):
        """测试 RemoveReaction 接口 - 参数异常 - 参数异常_参数值为空"""
        request_data = {'conv_id': '', 'seq': 1, 'reaction_id': 10000263}
        
        result = self.client.call_rpc(
            service='Social',
            method='RemoveReaction',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'RemoveReaction_参数异常_参数值为空',
            'method': 'RemoveReaction',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_参数值为空',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: RemoveReaction - 参数异常 - 参数异常_参数值为空")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ RemoveReaction 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ RemoveReaction 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_removereaction_参数异常_参数值超出范围(self):
        """测试 RemoveReaction 接口 - 参数异常 - 参数异常_参数值超出范围"""
        request_data = {'conv_id': 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', 'seq': 1, 'reaction_id': 10000263}
        
        result = self.client.call_rpc(
            service='Social',
            method='RemoveReaction',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'RemoveReaction_参数异常_参数值超出范围',
            'method': 'RemoveReaction',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_参数值超出范围',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: RemoveReaction - 参数异常 - 参数异常_参数值超出范围")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ RemoveReaction 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ RemoveReaction 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_removereaction_参数异常_参数格式错误(self):
        """测试 RemoveReaction 接口 - 参数异常 - 参数异常_参数格式错误"""
        request_data = {'conv_id': -1, 'seq': 1, 'reaction_id': 10000263}
        
        result = self.client.call_rpc(
            service='Social',
            method='RemoveReaction',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'RemoveReaction_参数异常_参数格式错误',
            'method': 'RemoveReaction',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_参数格式错误',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: RemoveReaction - 参数异常 - 参数异常_参数格式错误")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ RemoveReaction 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ RemoveReaction 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_removereaction_权限安全(self):
        """测试 RemoveReaction 接口 - 权限安全 - 权限安全"""
        request_data = {'conv_id': 10000263, 'seq': 1, 'reaction_id': 10000263}
        
        result = self.client.call_rpc(
            service='Social',
            method='RemoveReaction',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'RemoveReaction_权限安全',
            'method': 'RemoveReaction',
            'dimension': '权限安全',
            'abnormal_type': '权限安全',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '403'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: RemoveReaction - 权限安全 - 权限安全")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ RemoveReaction 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ RemoveReaction 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_removereaction_性能边界(self):
        """测试 RemoveReaction 接口 - 性能边界 - 性能边界"""
        request_data = {'conv_id': 10000263, 'seq': 1, 'reaction_id': 10000263}
        
        result = self.client.call_rpc(
            service='Social',
            method='RemoveReaction',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'RemoveReaction_性能边界',
            'method': 'RemoveReaction',
            'dimension': '性能边界',
            'abnormal_type': '性能边界',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '200'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: RemoveReaction - 性能边界 - 性能边界")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ RemoveReaction 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ RemoveReaction 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

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
            'preconditions': [
                '发送消息 (SendMessage): to_uid=0, scene=4, scene_id=0',
                '从响应获取: conv_id, seq'
            ]
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n============================================================")
        print(f"测试接口: GetReactions")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
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

    def test_getreactions_参数异常_必填参数缺失(self):
        """测试 GetReactions 接口 - 参数异常 - 参数异常_必填参数缺失"""
        request_data = {'conv_id': '', 'seq': 1}
        
        result = self.client.call_rpc(
            service='Social',
            method='GetReactions',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'GetReactions_参数异常_必填参数缺失',
            'method': 'GetReactions',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_必填参数缺失',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: GetReactions - 参数异常 - 参数异常_必填参数缺失")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ GetReactions 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetReactions 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_getreactions_参数异常_参数类型错误(self):
        """测试 GetReactions 接口 - 参数异常 - 参数异常_参数类型错误"""
        request_data = {'conv_id': 12345, 'seq': 1}
        
        result = self.client.call_rpc(
            service='Social',
            method='GetReactions',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'GetReactions_参数异常_参数类型错误',
            'method': 'GetReactions',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_参数类型错误',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: GetReactions - 参数异常 - 参数异常_参数类型错误")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ GetReactions 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetReactions 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_getreactions_参数异常_参数值为空(self):
        """测试 GetReactions 接口 - 参数异常 - 参数异常_参数值为空"""
        request_data = {'conv_id': '', 'seq': 1}
        
        result = self.client.call_rpc(
            service='Social',
            method='GetReactions',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'GetReactions_参数异常_参数值为空',
            'method': 'GetReactions',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_参数值为空',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: GetReactions - 参数异常 - 参数异常_参数值为空")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ GetReactions 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetReactions 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_getreactions_参数异常_参数值超出范围(self):
        """测试 GetReactions 接口 - 参数异常 - 参数异常_参数值超出范围"""
        request_data = {'conv_id': 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', 'seq': 1}
        
        result = self.client.call_rpc(
            service='Social',
            method='GetReactions',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'GetReactions_参数异常_参数值超出范围',
            'method': 'GetReactions',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_参数值超出范围',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: GetReactions - 参数异常 - 参数异常_参数值超出范围")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ GetReactions 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetReactions 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_getreactions_参数异常_参数格式错误(self):
        """测试 GetReactions 接口 - 参数异常 - 参数异常_参数格式错误"""
        request_data = {'conv_id': -1, 'seq': 1}
        
        result = self.client.call_rpc(
            service='Social',
            method='GetReactions',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'GetReactions_参数异常_参数格式错误',
            'method': 'GetReactions',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_参数格式错误',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: GetReactions - 参数异常 - 参数异常_参数格式错误")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ GetReactions 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetReactions 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_getreactions_权限安全(self):
        """测试 GetReactions 接口 - 权限安全 - 权限安全"""
        request_data = {'conv_id': 10000263, 'seq': 1}
        
        result = self.client.call_rpc(
            service='Social',
            method='GetReactions',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'GetReactions_权限安全',
            'method': 'GetReactions',
            'dimension': '权限安全',
            'abnormal_type': '权限安全',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '403'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: GetReactions - 权限安全 - 权限安全")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ GetReactions 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetReactions 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_getreactions_性能边界(self):
        """测试 GetReactions 接口 - 性能边界 - 性能边界"""
        request_data = {'conv_id': 10000263, 'seq': 1}
        
        result = self.client.call_rpc(
            service='Social',
            method='GetReactions',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'GetReactions_性能边界',
            'method': 'GetReactions',
            'dimension': '性能边界',
            'abnormal_type': '性能边界',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '200'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: GetReactions - 性能边界 - 性能边界")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ GetReactions 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetReactions 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_getsinglechatconvlist_参数异常_必填参数缺失(self):
        """测试 GetSingleChatConvList 接口 - 参数异常 - 参数异常_必填参数缺失"""
        request_data = {'update_time_after': 0, 'limit': 20, 'offset': 0}
        
        result = self.client.call_rpc(
            service='Social',
            method='GetSingleChatConvList',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'GetSingleChatConvList_参数异常_必填参数缺失',
            'method': 'GetSingleChatConvList',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_必填参数缺失',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: GetSingleChatConvList - 参数异常 - 参数异常_必填参数缺失")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ GetSingleChatConvList 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetSingleChatConvList 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_getsinglechatconvlist_参数异常_参数类型错误(self):
        """测试 GetSingleChatConvList 接口 - 参数异常 - 参数异常_参数类型错误"""
        request_data = {'update_time_after': 'wrong_type', 'limit': 20, 'offset': 0}
        
        result = self.client.call_rpc(
            service='Social',
            method='GetSingleChatConvList',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'GetSingleChatConvList_参数异常_参数类型错误',
            'method': 'GetSingleChatConvList',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_参数类型错误',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: GetSingleChatConvList - 参数异常 - 参数异常_参数类型错误")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ GetSingleChatConvList 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetSingleChatConvList 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_getsinglechatconvlist_参数异常_参数值为空(self):
        """测试 GetSingleChatConvList 接口 - 参数异常 - 参数异常_参数值为空"""
        request_data = {'update_time_after': 0, 'limit': 20, 'offset': 0}
        
        result = self.client.call_rpc(
            service='Social',
            method='GetSingleChatConvList',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'GetSingleChatConvList_参数异常_参数值为空',
            'method': 'GetSingleChatConvList',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_参数值为空',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: GetSingleChatConvList - 参数异常 - 参数异常_参数值为空")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ GetSingleChatConvList 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetSingleChatConvList 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_getsinglechatconvlist_参数异常_参数值超出范围(self):
        """测试 GetSingleChatConvList 接口 - 参数异常 - 参数异常_参数值超出范围"""
        request_data = {'update_time_after': 999999999, 'limit': 20, 'offset': 0}
        
        result = self.client.call_rpc(
            service='Social',
            method='GetSingleChatConvList',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'GetSingleChatConvList_参数异常_参数值超出范围',
            'method': 'GetSingleChatConvList',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_参数值超出范围',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: GetSingleChatConvList - 参数异常 - 参数异常_参数值超出范围")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ GetSingleChatConvList 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetSingleChatConvList 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_getsinglechatconvlist_参数异常_参数格式错误(self):
        """测试 GetSingleChatConvList 接口 - 参数异常 - 参数异常_参数格式错误"""
        request_data = {'update_time_after': 'invalid_format_@#$%', 'limit': 20, 'offset': 0}
        
        result = self.client.call_rpc(
            service='Social',
            method='GetSingleChatConvList',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'GetSingleChatConvList_参数异常_参数格式错误',
            'method': 'GetSingleChatConvList',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_参数格式错误',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: GetSingleChatConvList - 参数异常 - 参数异常_参数格式错误")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ GetSingleChatConvList 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetSingleChatConvList 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_getsinglechatconvlist_权限安全(self):
        """测试 GetSingleChatConvList 接口 - 权限安全 - 权限安全"""
        request_data = {'update_time_after': 1, 'limit': 20, 'offset': 0}
        
        result = self.client.call_rpc(
            service='Social',
            method='GetSingleChatConvList',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'GetSingleChatConvList_权限安全',
            'method': 'GetSingleChatConvList',
            'dimension': '权限安全',
            'abnormal_type': '权限安全',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '403'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: GetSingleChatConvList - 权限安全 - 权限安全")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ GetSingleChatConvList 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetSingleChatConvList 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_getsinglechatconvlist_性能边界(self):
        """测试 GetSingleChatConvList 接口 - 性能边界 - 性能边界"""
        request_data = {'update_time_after': 1, 'limit': 20, 'offset': 0}
        
        result = self.client.call_rpc(
            service='Social',
            method='GetSingleChatConvList',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'GetSingleChatConvList_性能边界',
            'method': 'GetSingleChatConvList',
            'dimension': '性能边界',
            'abnormal_type': '性能边界',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '200'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: GetSingleChatConvList - 性能边界 - 性能边界")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ GetSingleChatConvList 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetSingleChatConvList 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_markread_参数异常_必填参数缺失(self):
        """测试 MarkRead 接口 - 参数异常 - 参数异常_必填参数缺失"""
        request_data = {'conv_id': '', 'read_seq': 1}
        
        result = self.client.call_rpc(
            service='Social',
            method='MarkRead',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'MarkRead_参数异常_必填参数缺失',
            'method': 'MarkRead',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_必填参数缺失',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: MarkRead - 参数异常 - 参数异常_必填参数缺失")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ MarkRead 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ MarkRead 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_markread_参数异常_参数类型错误(self):
        """测试 MarkRead 接口 - 参数异常 - 参数异常_参数类型错误"""
        request_data = {'conv_id': 12345, 'read_seq': 1}
        
        result = self.client.call_rpc(
            service='Social',
            method='MarkRead',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'MarkRead_参数异常_参数类型错误',
            'method': 'MarkRead',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_参数类型错误',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: MarkRead - 参数异常 - 参数异常_参数类型错误")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ MarkRead 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ MarkRead 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_markread_参数异常_参数值为空(self):
        """测试 MarkRead 接口 - 参数异常 - 参数异常_参数值为空"""
        request_data = {'conv_id': '', 'read_seq': 1}
        
        result = self.client.call_rpc(
            service='Social',
            method='MarkRead',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'MarkRead_参数异常_参数值为空',
            'method': 'MarkRead',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_参数值为空',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: MarkRead - 参数异常 - 参数异常_参数值为空")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ MarkRead 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ MarkRead 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_markread_参数异常_参数值超出范围(self):
        """测试 MarkRead 接口 - 参数异常 - 参数异常_参数值超出范围"""
        request_data = {'conv_id': 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', 'read_seq': 1}
        
        result = self.client.call_rpc(
            service='Social',
            method='MarkRead',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'MarkRead_参数异常_参数值超出范围',
            'method': 'MarkRead',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_参数值超出范围',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: MarkRead - 参数异常 - 参数异常_参数值超出范围")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ MarkRead 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ MarkRead 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_markread_参数异常_参数格式错误(self):
        """测试 MarkRead 接口 - 参数异常 - 参数异常_参数格式错误"""
        request_data = {'conv_id': -1, 'read_seq': 1}
        
        result = self.client.call_rpc(
            service='Social',
            method='MarkRead',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'MarkRead_参数异常_参数格式错误',
            'method': 'MarkRead',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_参数格式错误',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: MarkRead - 参数异常 - 参数异常_参数格式错误")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ MarkRead 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ MarkRead 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_markread_权限安全(self):
        """测试 MarkRead 接口 - 权限安全 - 权限安全"""
        request_data = {'conv_id': 10000263, 'read_seq': 1}
        
        result = self.client.call_rpc(
            service='Social',
            method='MarkRead',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'MarkRead_权限安全',
            'method': 'MarkRead',
            'dimension': '权限安全',
            'abnormal_type': '权限安全',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '403'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: MarkRead - 权限安全 - 权限安全")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ MarkRead 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ MarkRead 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_markread_性能边界(self):
        """测试 MarkRead 接口 - 性能边界 - 性能边界"""
        request_data = {'conv_id': 10000263, 'read_seq': 1}
        
        result = self.client.call_rpc(
            service='Social',
            method='MarkRead',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'MarkRead_性能边界',
            'method': 'MarkRead',
            'dimension': '性能边界',
            'abnormal_type': '性能边界',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '200'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: MarkRead - 性能边界 - 性能边界")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ MarkRead 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ MarkRead 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_getfanslist_参数异常_必填参数缺失(self):
        """测试 GetFansList 接口 - 参数异常 - 参数异常_必填参数缺失"""
        request_data = {'last_uid': 0, 'last_create_time_ms': 1, 'limit': 20}
        
        result = self.client.call_rpc(
            service='Social',
            method='GetFansList',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'GetFansList_参数异常_必填参数缺失',
            'method': 'GetFansList',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_必填参数缺失',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: GetFansList - 参数异常 - 参数异常_必填参数缺失")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ GetFansList 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetFansList 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_getfanslist_参数异常_参数类型错误(self):
        """测试 GetFansList 接口 - 参数异常 - 参数异常_参数类型错误"""
        request_data = {'last_uid': 'wrong_type', 'last_create_time_ms': 1, 'limit': 20}
        
        result = self.client.call_rpc(
            service='Social',
            method='GetFansList',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'GetFansList_参数异常_参数类型错误',
            'method': 'GetFansList',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_参数类型错误',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: GetFansList - 参数异常 - 参数异常_参数类型错误")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ GetFansList 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetFansList 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_getfanslist_参数异常_参数值为空(self):
        """测试 GetFansList 接口 - 参数异常 - 参数异常_参数值为空"""
        request_data = {'last_uid': 0, 'last_create_time_ms': 1, 'limit': 20}
        
        result = self.client.call_rpc(
            service='Social',
            method='GetFansList',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'GetFansList_参数异常_参数值为空',
            'method': 'GetFansList',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_参数值为空',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: GetFansList - 参数异常 - 参数异常_参数值为空")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ GetFansList 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetFansList 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_getfanslist_参数异常_参数值超出范围(self):
        """测试 GetFansList 接口 - 参数异常 - 参数异常_参数值超出范围"""
        request_data = {'last_uid': 999999999, 'last_create_time_ms': 1, 'limit': 20}
        
        result = self.client.call_rpc(
            service='Social',
            method='GetFansList',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'GetFansList_参数异常_参数值超出范围',
            'method': 'GetFansList',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_参数值超出范围',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: GetFansList - 参数异常 - 参数异常_参数值超出范围")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ GetFansList 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetFansList 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_getfanslist_参数异常_参数格式错误(self):
        """测试 GetFansList 接口 - 参数异常 - 参数异常_参数格式错误"""
        request_data = {'last_uid': -1, 'last_create_time_ms': 1, 'limit': 20}
        
        result = self.client.call_rpc(
            service='Social',
            method='GetFansList',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'GetFansList_参数异常_参数格式错误',
            'method': 'GetFansList',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_参数格式错误',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: GetFansList - 参数异常 - 参数异常_参数格式错误")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ GetFansList 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetFansList 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_getfanslist_权限安全(self):
        """测试 GetFansList 接口 - 权限安全 - 权限安全"""
        request_data = {'last_uid': 10000263, 'last_create_time_ms': 1, 'limit': 20}
        
        result = self.client.call_rpc(
            service='Social',
            method='GetFansList',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'GetFansList_权限安全',
            'method': 'GetFansList',
            'dimension': '权限安全',
            'abnormal_type': '权限安全',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '403'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: GetFansList - 权限安全 - 权限安全")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ GetFansList 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetFansList 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_getfanslist_性能边界(self):
        """测试 GetFansList 接口 - 性能边界 - 性能边界"""
        request_data = {'last_uid': 10000263, 'last_create_time_ms': 1, 'limit': 20}
        
        result = self.client.call_rpc(
            service='Social',
            method='GetFansList',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'GetFansList_性能边界',
            'method': 'GetFansList',
            'dimension': '性能边界',
            'abnormal_type': '性能边界',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '200'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: GetFansList - 性能边界 - 性能边界")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ GetFansList 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetFansList 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_getfollowlist_参数异常_必填参数缺失(self):
        """测试 GetFollowList 接口 - 参数异常 - 参数异常_必填参数缺失"""
        request_data = {}
        
        result = self.client.call_rpc(
            service='Social',
            method='GetFollowList',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'GetFollowList_参数异常_必填参数缺失',
            'method': 'GetFollowList',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_必填参数缺失',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: GetFollowList - 参数异常 - 参数异常_必填参数缺失")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ GetFollowList 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetFollowList 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_getfollowlist_参数异常_参数类型错误(self):
        """测试 GetFollowList 接口 - 参数异常 - 参数异常_参数类型错误"""
        request_data = {}
        
        result = self.client.call_rpc(
            service='Social',
            method='GetFollowList',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'GetFollowList_参数异常_参数类型错误',
            'method': 'GetFollowList',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_参数类型错误',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: GetFollowList - 参数异常 - 参数异常_参数类型错误")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ GetFollowList 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetFollowList 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_getfollowlist_参数异常_参数值为空(self):
        """测试 GetFollowList 接口 - 参数异常 - 参数异常_参数值为空"""
        request_data = {}
        
        result = self.client.call_rpc(
            service='Social',
            method='GetFollowList',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'GetFollowList_参数异常_参数值为空',
            'method': 'GetFollowList',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_参数值为空',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: GetFollowList - 参数异常 - 参数异常_参数值为空")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ GetFollowList 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetFollowList 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_getfollowlist_参数异常_参数值超出范围(self):
        """测试 GetFollowList 接口 - 参数异常 - 参数异常_参数值超出范围"""
        request_data = {}
        
        result = self.client.call_rpc(
            service='Social',
            method='GetFollowList',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'GetFollowList_参数异常_参数值超出范围',
            'method': 'GetFollowList',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_参数值超出范围',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: GetFollowList - 参数异常 - 参数异常_参数值超出范围")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ GetFollowList 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetFollowList 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_getfollowlist_参数异常_参数格式错误(self):
        """测试 GetFollowList 接口 - 参数异常 - 参数异常_参数格式错误"""
        request_data = {}
        
        result = self.client.call_rpc(
            service='Social',
            method='GetFollowList',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'GetFollowList_参数异常_参数格式错误',
            'method': 'GetFollowList',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_参数格式错误',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: GetFollowList - 参数异常 - 参数异常_参数格式错误")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ GetFollowList 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetFollowList 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_getfollowlist_权限安全(self):
        """测试 GetFollowList 接口 - 权限安全 - 权限安全"""
        request_data = {}
        
        result = self.client.call_rpc(
            service='Social',
            method='GetFollowList',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'GetFollowList_权限安全',
            'method': 'GetFollowList',
            'dimension': '权限安全',
            'abnormal_type': '权限安全',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '403'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: GetFollowList - 权限安全 - 权限安全")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ GetFollowList 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetFollowList 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_getfollowlist_性能边界(self):
        """测试 GetFollowList 接口 - 性能边界 - 性能边界"""
        request_data = {}
        
        result = self.client.call_rpc(
            service='Social',
            method='GetFollowList',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'GetFollowList_性能边界',
            'method': 'GetFollowList',
            'dimension': '性能边界',
            'abnormal_type': '性能边界',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '200'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: GetFollowList - 性能边界 - 性能边界")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ GetFollowList 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetFollowList 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_getfriendlist_参数异常_必填参数缺失(self):
        """测试 GetFriendList 接口 - 参数异常 - 参数异常_必填参数缺失"""
        request_data = {}
        
        result = self.client.call_rpc(
            service='Social',
            method='GetFriendList',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'GetFriendList_参数异常_必填参数缺失',
            'method': 'GetFriendList',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_必填参数缺失',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: GetFriendList - 参数异常 - 参数异常_必填参数缺失")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ GetFriendList 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetFriendList 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_getfriendlist_参数异常_参数类型错误(self):
        """测试 GetFriendList 接口 - 参数异常 - 参数异常_参数类型错误"""
        request_data = {}
        
        result = self.client.call_rpc(
            service='Social',
            method='GetFriendList',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'GetFriendList_参数异常_参数类型错误',
            'method': 'GetFriendList',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_参数类型错误',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: GetFriendList - 参数异常 - 参数异常_参数类型错误")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ GetFriendList 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetFriendList 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_getfriendlist_参数异常_参数值为空(self):
        """测试 GetFriendList 接口 - 参数异常 - 参数异常_参数值为空"""
        request_data = {}
        
        result = self.client.call_rpc(
            service='Social',
            method='GetFriendList',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'GetFriendList_参数异常_参数值为空',
            'method': 'GetFriendList',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_参数值为空',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: GetFriendList - 参数异常 - 参数异常_参数值为空")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ GetFriendList 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetFriendList 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_getfriendlist_参数异常_参数值超出范围(self):
        """测试 GetFriendList 接口 - 参数异常 - 参数异常_参数值超出范围"""
        request_data = {}
        
        result = self.client.call_rpc(
            service='Social',
            method='GetFriendList',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'GetFriendList_参数异常_参数值超出范围',
            'method': 'GetFriendList',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_参数值超出范围',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: GetFriendList - 参数异常 - 参数异常_参数值超出范围")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ GetFriendList 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetFriendList 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_getfriendlist_参数异常_参数格式错误(self):
        """测试 GetFriendList 接口 - 参数异常 - 参数异常_参数格式错误"""
        request_data = {}
        
        result = self.client.call_rpc(
            service='Social',
            method='GetFriendList',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'GetFriendList_参数异常_参数格式错误',
            'method': 'GetFriendList',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_参数格式错误',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: GetFriendList - 参数异常 - 参数异常_参数格式错误")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ GetFriendList 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetFriendList 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_getfriendlist_权限安全(self):
        """测试 GetFriendList 接口 - 权限安全 - 权限安全"""
        request_data = {}
        
        result = self.client.call_rpc(
            service='Social',
            method='GetFriendList',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'GetFriendList_权限安全',
            'method': 'GetFriendList',
            'dimension': '权限安全',
            'abnormal_type': '权限安全',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '403'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: GetFriendList - 权限安全 - 权限安全")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ GetFriendList 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetFriendList 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_getfriendlist_性能边界(self):
        """测试 GetFriendList 接口 - 性能边界 - 性能边界"""
        request_data = {}
        
        result = self.client.call_rpc(
            service='Social',
            method='GetFriendList',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'GetFriendList_性能边界',
            'method': 'GetFriendList',
            'dimension': '性能边界',
            'abnormal_type': '性能边界',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '200'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: GetFriendList - 性能边界 - 性能边界")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ GetFriendList 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetFriendList 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_follow_参数异常_必填参数缺失(self):
        """测试 Follow 接口 - 参数异常 - 参数异常_必填参数缺失"""
        request_data = {'target_uid': 0}
        
        result = self.client.call_rpc(
            service='Social',
            method='Follow',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'Follow_参数异常_必填参数缺失',
            'method': 'Follow',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_必填参数缺失',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: Follow - 参数异常 - 参数异常_必填参数缺失")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ Follow 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ Follow 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_follow_参数异常_参数类型错误(self):
        """测试 Follow 接口 - 参数异常 - 参数异常_参数类型错误"""
        request_data = {'target_uid': 'wrong_type'}
        
        result = self.client.call_rpc(
            service='Social',
            method='Follow',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'Follow_参数异常_参数类型错误',
            'method': 'Follow',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_参数类型错误',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: Follow - 参数异常 - 参数异常_参数类型错误")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ Follow 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ Follow 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_follow_参数异常_参数值为空(self):
        """测试 Follow 接口 - 参数异常 - 参数异常_参数值为空"""
        request_data = {'target_uid': 0}
        
        result = self.client.call_rpc(
            service='Social',
            method='Follow',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'Follow_参数异常_参数值为空',
            'method': 'Follow',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_参数值为空',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: Follow - 参数异常 - 参数异常_参数值为空")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ Follow 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ Follow 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_follow_参数异常_参数值超出范围(self):
        """测试 Follow 接口 - 参数异常 - 参数异常_参数值超出范围"""
        request_data = {'target_uid': 999999999}
        
        result = self.client.call_rpc(
            service='Social',
            method='Follow',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'Follow_参数异常_参数值超出范围',
            'method': 'Follow',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_参数值超出范围',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: Follow - 参数异常 - 参数异常_参数值超出范围")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ Follow 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ Follow 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_follow_参数异常_参数格式错误(self):
        """测试 Follow 接口 - 参数异常 - 参数异常_参数格式错误"""
        request_data = {'target_uid': -1}
        
        result = self.client.call_rpc(
            service='Social',
            method='Follow',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'Follow_参数异常_参数格式错误',
            'method': 'Follow',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_参数格式错误',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: Follow - 参数异常 - 参数异常_参数格式错误")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ Follow 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ Follow 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_follow_权限安全(self):
        """测试 Follow 接口 - 权限安全 - 权限安全"""
        request_data = {'target_uid': 10000263}
        
        result = self.client.call_rpc(
            service='Social',
            method='Follow',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'Follow_权限安全',
            'method': 'Follow',
            'dimension': '权限安全',
            'abnormal_type': '权限安全',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '403'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: Follow - 权限安全 - 权限安全")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ Follow 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ Follow 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_follow_性能边界(self):
        """测试 Follow 接口 - 性能边界 - 性能边界"""
        request_data = {'target_uid': 10000263}
        
        result = self.client.call_rpc(
            service='Social',
            method='Follow',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'Follow_性能边界',
            'method': 'Follow',
            'dimension': '性能边界',
            'abnormal_type': '性能边界',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '200'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: Follow - 性能边界 - 性能边界")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ Follow 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ Follow 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_unfollow_参数异常_必填参数缺失(self):
        """测试 Unfollow 接口 - 参数异常 - 参数异常_必填参数缺失"""
        request_data = {'target_uid': 0}
        
        result = self.client.call_rpc(
            service='Social',
            method='Unfollow',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'Unfollow_参数异常_必填参数缺失',
            'method': 'Unfollow',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_必填参数缺失',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: Unfollow - 参数异常 - 参数异常_必填参数缺失")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ Unfollow 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ Unfollow 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_unfollow_参数异常_参数类型错误(self):
        """测试 Unfollow 接口 - 参数异常 - 参数异常_参数类型错误"""
        request_data = {'target_uid': 'wrong_type'}
        
        result = self.client.call_rpc(
            service='Social',
            method='Unfollow',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'Unfollow_参数异常_参数类型错误',
            'method': 'Unfollow',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_参数类型错误',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: Unfollow - 参数异常 - 参数异常_参数类型错误")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ Unfollow 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ Unfollow 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_unfollow_参数异常_参数值为空(self):
        """测试 Unfollow 接口 - 参数异常 - 参数异常_参数值为空"""
        request_data = {'target_uid': 0}
        
        result = self.client.call_rpc(
            service='Social',
            method='Unfollow',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'Unfollow_参数异常_参数值为空',
            'method': 'Unfollow',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_参数值为空',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: Unfollow - 参数异常 - 参数异常_参数值为空")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ Unfollow 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ Unfollow 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_unfollow_参数异常_参数值超出范围(self):
        """测试 Unfollow 接口 - 参数异常 - 参数异常_参数值超出范围"""
        request_data = {'target_uid': 999999999}
        
        result = self.client.call_rpc(
            service='Social',
            method='Unfollow',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'Unfollow_参数异常_参数值超出范围',
            'method': 'Unfollow',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_参数值超出范围',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: Unfollow - 参数异常 - 参数异常_参数值超出范围")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ Unfollow 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ Unfollow 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_unfollow_参数异常_参数格式错误(self):
        """测试 Unfollow 接口 - 参数异常 - 参数异常_参数格式错误"""
        request_data = {'target_uid': -1}
        
        result = self.client.call_rpc(
            service='Social',
            method='Unfollow',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'Unfollow_参数异常_参数格式错误',
            'method': 'Unfollow',
            'dimension': '参数异常',
            'abnormal_type': '参数异常_参数格式错误',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '400/500'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: Unfollow - 参数异常 - 参数异常_参数格式错误")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ Unfollow 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ Unfollow 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_unfollow_权限安全(self):
        """测试 Unfollow 接口 - 权限安全 - 权限安全"""
        request_data = {'target_uid': 10000263}
        
        result = self.client.call_rpc(
            service='Social',
            method='Unfollow',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'Unfollow_权限安全',
            'method': 'Unfollow',
            'dimension': '权限安全',
            'abnormal_type': '权限安全',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '403'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: Unfollow - 权限安全 - 权限安全")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ Unfollow 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ Unfollow 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_unfollow_性能边界(self):
        """测试 Unfollow 接口 - 性能边界 - 性能边界"""
        request_data = {'target_uid': 10000263}
        
        result = self.client.call_rpc(
            service='Social',
            method='Unfollow',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'Unfollow_性能边界',
            'method': 'Unfollow',
            'dimension': '性能边界',
            'abnormal_type': '性能边界',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '200'
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n{'='*60}")
        print(f"测试接口: Unfollow - 性能边界 - 性能边界")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {safe_json_dumps(result)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"{'='*60}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\n✓ Unfollow 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ Unfollow 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

if __name__ == '__main__':
    unittest.main()
