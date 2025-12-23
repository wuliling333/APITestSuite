"""
自动生成的Room服务测试代码
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


class TestRoom(unittest.TestCase):
    """Room服务测试"""
    
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
    

    def test_getuserstate_参数异常_必填参数缺失(self):
        """测试 GetUserState 接口 - 参数异常 - 参数异常_必填参数缺失"""
        request_data = {}
        
        result = self.client.call_rpc(
            service='Room',
            method='GetUserState',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'GetUserState_参数异常_必填参数缺失',
            'method': 'GetUserState',
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
        print(f"测试接口: GetUserState - 参数异常 - 参数异常_必填参数缺失")
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
            print(f"\n✓ GetUserState 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetUserState 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_getuserstate_参数异常_参数类型错误(self):
        """测试 GetUserState 接口 - 参数异常 - 参数异常_参数类型错误"""
        request_data = {}
        
        result = self.client.call_rpc(
            service='Room',
            method='GetUserState',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'GetUserState_参数异常_参数类型错误',
            'method': 'GetUserState',
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
        print(f"测试接口: GetUserState - 参数异常 - 参数异常_参数类型错误")
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
            print(f"\n✓ GetUserState 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetUserState 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_getuserstate_参数异常_参数值为空(self):
        """测试 GetUserState 接口 - 参数异常 - 参数异常_参数值为空"""
        request_data = {}
        
        result = self.client.call_rpc(
            service='Room',
            method='GetUserState',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'GetUserState_参数异常_参数值为空',
            'method': 'GetUserState',
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
        print(f"测试接口: GetUserState - 参数异常 - 参数异常_参数值为空")
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
            print(f"\n✓ GetUserState 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetUserState 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_getuserstate_参数异常_参数值超出范围(self):
        """测试 GetUserState 接口 - 参数异常 - 参数异常_参数值超出范围"""
        request_data = {}
        
        result = self.client.call_rpc(
            service='Room',
            method='GetUserState',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'GetUserState_参数异常_参数值超出范围',
            'method': 'GetUserState',
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
        print(f"测试接口: GetUserState - 参数异常 - 参数异常_参数值超出范围")
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
            print(f"\n✓ GetUserState 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetUserState 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_getuserstate_参数异常_参数格式错误(self):
        """测试 GetUserState 接口 - 参数异常 - 参数异常_参数格式错误"""
        request_data = {}
        
        result = self.client.call_rpc(
            service='Room',
            method='GetUserState',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'GetUserState_参数异常_参数格式错误',
            'method': 'GetUserState',
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
        print(f"测试接口: GetUserState - 参数异常 - 参数异常_参数格式错误")
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
            print(f"\n✓ GetUserState 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetUserState 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_getuserstate_权限安全(self):
        """测试 GetUserState 接口 - 权限安全 - 权限安全"""
        request_data = {}
        
        result = self.client.call_rpc(
            service='Room',
            method='GetUserState',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'GetUserState_权限安全',
            'method': 'GetUserState',
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
        print(f"测试接口: GetUserState - 权限安全 - 权限安全")
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
            print(f"\n✓ GetUserState 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetUserState 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_getuserstate_性能边界(self):
        """测试 GetUserState 接口 - 性能边界 - 性能边界"""
        request_data = {}
        
        result = self.client.call_rpc(
            service='Room',
            method='GetUserState',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'GetUserState_性能边界',
            'method': 'GetUserState',
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
        print(f"测试接口: GetUserState - 性能边界 - 性能边界")
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
            print(f"\n✓ GetUserState 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetUserState 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_createteam_参数异常_必填参数缺失(self):
        """测试 CreateTeam 接口 - 参数异常 - 参数异常_必填参数缺失"""
        request_data = {'game_mode': 0}
        
        result = self.client.call_rpc(
            service='Room',
            method='CreateTeam',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'CreateTeam_参数异常_必填参数缺失',
            'method': 'CreateTeam',
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
        print(f"测试接口: CreateTeam - 参数异常 - 参数异常_必填参数缺失")
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
            print(f"\n✓ CreateTeam 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ CreateTeam 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_createteam_参数异常_参数类型错误(self):
        """测试 CreateTeam 接口 - 参数异常 - 参数异常_参数类型错误"""
        request_data = {'game_mode': 'wrong_type'}
        
        result = self.client.call_rpc(
            service='Room',
            method='CreateTeam',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'CreateTeam_参数异常_参数类型错误',
            'method': 'CreateTeam',
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
        print(f"测试接口: CreateTeam - 参数异常 - 参数异常_参数类型错误")
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
            print(f"\n✓ CreateTeam 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ CreateTeam 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_createteam_参数异常_参数值为空(self):
        """测试 CreateTeam 接口 - 参数异常 - 参数异常_参数值为空"""
        request_data = {'game_mode': 0}
        
        result = self.client.call_rpc(
            service='Room',
            method='CreateTeam',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'CreateTeam_参数异常_参数值为空',
            'method': 'CreateTeam',
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
        print(f"测试接口: CreateTeam - 参数异常 - 参数异常_参数值为空")
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
            print(f"\n✓ CreateTeam 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ CreateTeam 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_createteam_参数异常_参数值超出范围(self):
        """测试 CreateTeam 接口 - 参数异常 - 参数异常_参数值超出范围"""
        request_data = {'game_mode': 999999999}
        
        result = self.client.call_rpc(
            service='Room',
            method='CreateTeam',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'CreateTeam_参数异常_参数值超出范围',
            'method': 'CreateTeam',
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
        print(f"测试接口: CreateTeam - 参数异常 - 参数异常_参数值超出范围")
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
            print(f"\n✓ CreateTeam 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ CreateTeam 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_createteam_参数异常_参数格式错误(self):
        """测试 CreateTeam 接口 - 参数异常 - 参数异常_参数格式错误"""
        request_data = {'game_mode': 'invalid_format_@#$%'}
        
        result = self.client.call_rpc(
            service='Room',
            method='CreateTeam',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'CreateTeam_参数异常_参数格式错误',
            'method': 'CreateTeam',
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
        print(f"测试接口: CreateTeam - 参数异常 - 参数异常_参数格式错误")
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
            print(f"\n✓ CreateTeam 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ CreateTeam 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_createteam_业务异常(self):
        """测试 CreateTeam 接口 - 业务异常 - 业务异常"""
        request_data = {'game_mode': 1}
        
        result = self.client.call_rpc(
            service='Room',
            method='CreateTeam',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'CreateTeam_业务异常',
            'method': 'CreateTeam',
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
        print(f"测试接口: CreateTeam - 业务异常 - 业务异常")
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
            print(f"\n✓ CreateTeam 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ CreateTeam 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_createteam_权限安全(self):
        """测试 CreateTeam 接口 - 权限安全 - 权限安全"""
        request_data = {'game_mode': 1}
        
        result = self.client.call_rpc(
            service='Room',
            method='CreateTeam',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'CreateTeam_权限安全',
            'method': 'CreateTeam',
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
        print(f"测试接口: CreateTeam - 权限安全 - 权限安全")
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
            print(f"\n✓ CreateTeam 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ CreateTeam 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_createteam_性能边界(self):
        """测试 CreateTeam 接口 - 性能边界 - 性能边界"""
        request_data = {'game_mode': 1}
        
        result = self.client.call_rpc(
            service='Room',
            method='CreateTeam',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'CreateTeam_性能边界',
            'method': 'CreateTeam',
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
        print(f"测试接口: CreateTeam - 性能边界 - 性能边界")
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
            print(f"\n✓ CreateTeam 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ CreateTeam 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_jointeam_参数异常_必填参数缺失(self):
        """测试 JoinTeam 接口 - 参数异常 - 参数异常_必填参数缺失"""
        request_data = {'team_id': 0}
        
        result = self.client.call_rpc(
            service='Room',
            method='JoinTeam',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'JoinTeam_参数异常_必填参数缺失',
            'method': 'JoinTeam',
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
        print(f"测试接口: JoinTeam - 参数异常 - 参数异常_必填参数缺失")
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
            print(f"\n✓ JoinTeam 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ JoinTeam 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_jointeam_参数异常_参数类型错误(self):
        """测试 JoinTeam 接口 - 参数异常 - 参数异常_参数类型错误"""
        request_data = {'team_id': 'wrong_type'}
        
        result = self.client.call_rpc(
            service='Room',
            method='JoinTeam',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'JoinTeam_参数异常_参数类型错误',
            'method': 'JoinTeam',
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
        print(f"测试接口: JoinTeam - 参数异常 - 参数异常_参数类型错误")
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
            print(f"\n✓ JoinTeam 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ JoinTeam 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_jointeam_参数异常_参数值为空(self):
        """测试 JoinTeam 接口 - 参数异常 - 参数异常_参数值为空"""
        request_data = {'team_id': 0}
        
        result = self.client.call_rpc(
            service='Room',
            method='JoinTeam',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'JoinTeam_参数异常_参数值为空',
            'method': 'JoinTeam',
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
        print(f"测试接口: JoinTeam - 参数异常 - 参数异常_参数值为空")
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
            print(f"\n✓ JoinTeam 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ JoinTeam 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_jointeam_参数异常_参数值超出范围(self):
        """测试 JoinTeam 接口 - 参数异常 - 参数异常_参数值超出范围"""
        request_data = {'team_id': 999999999}
        
        result = self.client.call_rpc(
            service='Room',
            method='JoinTeam',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'JoinTeam_参数异常_参数值超出范围',
            'method': 'JoinTeam',
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
        print(f"测试接口: JoinTeam - 参数异常 - 参数异常_参数值超出范围")
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
            print(f"\n✓ JoinTeam 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ JoinTeam 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_jointeam_参数异常_参数格式错误(self):
        """测试 JoinTeam 接口 - 参数异常 - 参数异常_参数格式错误"""
        request_data = {'team_id': -1}
        
        result = self.client.call_rpc(
            service='Room',
            method='JoinTeam',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'JoinTeam_参数异常_参数格式错误',
            'method': 'JoinTeam',
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
        print(f"测试接口: JoinTeam - 参数异常 - 参数异常_参数格式错误")
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
            print(f"\n✓ JoinTeam 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ JoinTeam 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_jointeam_业务异常(self):
        """测试 JoinTeam 接口 - 业务异常 - 业务异常"""
        request_data = {'team_id': 999999999}
        
        result = self.client.call_rpc(
            service='Room',
            method='JoinTeam',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'JoinTeam_业务异常',
            'method': 'JoinTeam',
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
        print(f"测试接口: JoinTeam - 业务异常 - 业务异常")
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
            print(f"\n✓ JoinTeam 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ JoinTeam 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_jointeam_权限安全(self):
        """测试 JoinTeam 接口 - 权限安全 - 权限安全"""
        request_data = {'team_id': 1006329}
        
        result = self.client.call_rpc(
            service='Room',
            method='JoinTeam',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'JoinTeam_权限安全',
            'method': 'JoinTeam',
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
        print(f"测试接口: JoinTeam - 权限安全 - 权限安全")
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
            print(f"\n✓ JoinTeam 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ JoinTeam 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_jointeam_性能边界(self):
        """测试 JoinTeam 接口 - 性能边界 - 性能边界"""
        request_data = {'team_id': 1006329}
        
        result = self.client.call_rpc(
            service='Room',
            method='JoinTeam',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'JoinTeam_性能边界',
            'method': 'JoinTeam',
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
        print(f"测试接口: JoinTeam - 性能边界 - 性能边界")
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
            print(f"\n✓ JoinTeam 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ JoinTeam 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_getteaminfo_参数异常_必填参数缺失(self):
        """测试 GetTeamInfo 接口 - 参数异常 - 参数异常_必填参数缺失"""
        request_data = {'team_id': 0}
        
        result = self.client.call_rpc(
            service='Room',
            method='GetTeamInfo',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'GetTeamInfo_参数异常_必填参数缺失',
            'method': 'GetTeamInfo',
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
        print(f"测试接口: GetTeamInfo - 参数异常 - 参数异常_必填参数缺失")
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
            print(f"\n✓ GetTeamInfo 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetTeamInfo 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_getteaminfo_参数异常_参数类型错误(self):
        """测试 GetTeamInfo 接口 - 参数异常 - 参数异常_参数类型错误"""
        request_data = {'team_id': 'wrong_type'}
        
        result = self.client.call_rpc(
            service='Room',
            method='GetTeamInfo',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'GetTeamInfo_参数异常_参数类型错误',
            'method': 'GetTeamInfo',
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
        print(f"测试接口: GetTeamInfo - 参数异常 - 参数异常_参数类型错误")
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
            print(f"\n✓ GetTeamInfo 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetTeamInfo 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_getteaminfo_参数异常_参数值为空(self):
        """测试 GetTeamInfo 接口 - 参数异常 - 参数异常_参数值为空"""
        request_data = {'team_id': 0}
        
        result = self.client.call_rpc(
            service='Room',
            method='GetTeamInfo',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'GetTeamInfo_参数异常_参数值为空',
            'method': 'GetTeamInfo',
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
        print(f"测试接口: GetTeamInfo - 参数异常 - 参数异常_参数值为空")
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
            print(f"\n✓ GetTeamInfo 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetTeamInfo 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_getteaminfo_参数异常_参数值超出范围(self):
        """测试 GetTeamInfo 接口 - 参数异常 - 参数异常_参数值超出范围"""
        request_data = {'team_id': 999999999}
        
        result = self.client.call_rpc(
            service='Room',
            method='GetTeamInfo',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'GetTeamInfo_参数异常_参数值超出范围',
            'method': 'GetTeamInfo',
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
        print(f"测试接口: GetTeamInfo - 参数异常 - 参数异常_参数值超出范围")
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
            print(f"\n✓ GetTeamInfo 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetTeamInfo 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_getteaminfo_参数异常_参数格式错误(self):
        """测试 GetTeamInfo 接口 - 参数异常 - 参数异常_参数格式错误"""
        request_data = {'team_id': -1}
        
        result = self.client.call_rpc(
            service='Room',
            method='GetTeamInfo',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'GetTeamInfo_参数异常_参数格式错误',
            'method': 'GetTeamInfo',
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
        print(f"测试接口: GetTeamInfo - 参数异常 - 参数异常_参数格式错误")
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
            print(f"\n✓ GetTeamInfo 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetTeamInfo 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_getteaminfo_业务异常(self):
        """测试 GetTeamInfo 接口 - 业务异常 - 业务异常"""
        request_data = {'team_id': 999999999}
        
        result = self.client.call_rpc(
            service='Room',
            method='GetTeamInfo',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'GetTeamInfo_业务异常',
            'method': 'GetTeamInfo',
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
        print(f"测试接口: GetTeamInfo - 业务异常 - 业务异常")
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
            print(f"\n✓ GetTeamInfo 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetTeamInfo 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_getteaminfo_权限安全(self):
        """测试 GetTeamInfo 接口 - 权限安全 - 权限安全"""
        request_data = {'team_id': 1006329}
        
        result = self.client.call_rpc(
            service='Room',
            method='GetTeamInfo',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'GetTeamInfo_权限安全',
            'method': 'GetTeamInfo',
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
        print(f"测试接口: GetTeamInfo - 权限安全 - 权限安全")
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
            print(f"\n✓ GetTeamInfo 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetTeamInfo 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_getteaminfo_性能边界(self):
        """测试 GetTeamInfo 接口 - 性能边界 - 性能边界"""
        request_data = {'team_id': 1006329}
        
        result = self.client.call_rpc(
            service='Room',
            method='GetTeamInfo',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'GetTeamInfo_性能边界',
            'method': 'GetTeamInfo',
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
        print(f"测试接口: GetTeamInfo - 性能边界 - 性能边界")
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
            print(f"\n✓ GetTeamInfo 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetTeamInfo 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_changereadystate_参数异常_必填参数缺失(self):
        """测试 ChangeReadyState 接口 - 参数异常 - 参数异常_必填参数缺失"""
        request_data = {'team_id': 0, 'ready': True}
        
        result = self.client.call_rpc(
            service='Room',
            method='ChangeReadyState',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'ChangeReadyState_参数异常_必填参数缺失',
            'method': 'ChangeReadyState',
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
        print(f"测试接口: ChangeReadyState - 参数异常 - 参数异常_必填参数缺失")
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
            print(f"\n✓ ChangeReadyState 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ ChangeReadyState 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_changereadystate_参数异常_参数类型错误(self):
        """测试 ChangeReadyState 接口 - 参数异常 - 参数异常_参数类型错误"""
        request_data = {'team_id': 'wrong_type', 'ready': True}
        
        result = self.client.call_rpc(
            service='Room',
            method='ChangeReadyState',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'ChangeReadyState_参数异常_参数类型错误',
            'method': 'ChangeReadyState',
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
        print(f"测试接口: ChangeReadyState - 参数异常 - 参数异常_参数类型错误")
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
            print(f"\n✓ ChangeReadyState 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ ChangeReadyState 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_changereadystate_参数异常_参数值为空(self):
        """测试 ChangeReadyState 接口 - 参数异常 - 参数异常_参数值为空"""
        request_data = {'team_id': 0, 'ready': True}
        
        result = self.client.call_rpc(
            service='Room',
            method='ChangeReadyState',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'ChangeReadyState_参数异常_参数值为空',
            'method': 'ChangeReadyState',
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
        print(f"测试接口: ChangeReadyState - 参数异常 - 参数异常_参数值为空")
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
            print(f"\n✓ ChangeReadyState 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ ChangeReadyState 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_changereadystate_参数异常_参数值超出范围(self):
        """测试 ChangeReadyState 接口 - 参数异常 - 参数异常_参数值超出范围"""
        request_data = {'team_id': 999999999, 'ready': True}
        
        result = self.client.call_rpc(
            service='Room',
            method='ChangeReadyState',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'ChangeReadyState_参数异常_参数值超出范围',
            'method': 'ChangeReadyState',
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
        print(f"测试接口: ChangeReadyState - 参数异常 - 参数异常_参数值超出范围")
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
            print(f"\n✓ ChangeReadyState 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ ChangeReadyState 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_changereadystate_参数异常_参数格式错误(self):
        """测试 ChangeReadyState 接口 - 参数异常 - 参数异常_参数格式错误"""
        request_data = {'team_id': -1, 'ready': True}
        
        result = self.client.call_rpc(
            service='Room',
            method='ChangeReadyState',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'ChangeReadyState_参数异常_参数格式错误',
            'method': 'ChangeReadyState',
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
        print(f"测试接口: ChangeReadyState - 参数异常 - 参数异常_参数格式错误")
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
            print(f"\n✓ ChangeReadyState 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ ChangeReadyState 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_changereadystate_权限安全(self):
        """测试 ChangeReadyState 接口 - 权限安全 - 权限安全"""
        request_data = {'team_id': 1006329, 'ready': True}
        
        result = self.client.call_rpc(
            service='Room',
            method='ChangeReadyState',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'ChangeReadyState_权限安全',
            'method': 'ChangeReadyState',
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
        print(f"测试接口: ChangeReadyState - 权限安全 - 权限安全")
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
            print(f"\n✓ ChangeReadyState 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ ChangeReadyState 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_changereadystate_性能边界(self):
        """测试 ChangeReadyState 接口 - 性能边界 - 性能边界"""
        request_data = {'team_id': 1006329, 'ready': True}
        
        result = self.client.call_rpc(
            service='Room',
            method='ChangeReadyState',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'ChangeReadyState_性能边界',
            'method': 'ChangeReadyState',
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
        print(f"测试接口: ChangeReadyState - 性能边界 - 性能边界")
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
            print(f"\n✓ ChangeReadyState 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ ChangeReadyState 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_startgamefromteam_参数异常_必填参数缺失(self):
        """测试 StartGameFromTeam 接口 - 参数异常 - 参数异常_必填参数缺失"""
        request_data = {'team_id': 0, 'map_id': 10000263, 'difficulty': 1}
        
        result = self.client.call_rpc(
            service='Room',
            method='StartGameFromTeam',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'StartGameFromTeam_参数异常_必填参数缺失',
            'method': 'StartGameFromTeam',
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
        print(f"测试接口: StartGameFromTeam - 参数异常 - 参数异常_必填参数缺失")
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
            print(f"\n✓ StartGameFromTeam 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ StartGameFromTeam 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_startgamefromteam_参数异常_参数类型错误(self):
        """测试 StartGameFromTeam 接口 - 参数异常 - 参数异常_参数类型错误"""
        request_data = {'team_id': 'wrong_type', 'map_id': 10000263, 'difficulty': 1}
        
        result = self.client.call_rpc(
            service='Room',
            method='StartGameFromTeam',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'StartGameFromTeam_参数异常_参数类型错误',
            'method': 'StartGameFromTeam',
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
        print(f"测试接口: StartGameFromTeam - 参数异常 - 参数异常_参数类型错误")
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
            print(f"\n✓ StartGameFromTeam 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ StartGameFromTeam 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_startgamefromteam_参数异常_参数值为空(self):
        """测试 StartGameFromTeam 接口 - 参数异常 - 参数异常_参数值为空"""
        request_data = {'team_id': 0, 'map_id': 10000263, 'difficulty': 1}
        
        result = self.client.call_rpc(
            service='Room',
            method='StartGameFromTeam',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'StartGameFromTeam_参数异常_参数值为空',
            'method': 'StartGameFromTeam',
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
        print(f"测试接口: StartGameFromTeam - 参数异常 - 参数异常_参数值为空")
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
            print(f"\n✓ StartGameFromTeam 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ StartGameFromTeam 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_startgamefromteam_参数异常_参数值超出范围(self):
        """测试 StartGameFromTeam 接口 - 参数异常 - 参数异常_参数值超出范围"""
        request_data = {'team_id': 999999999, 'map_id': 10000263, 'difficulty': 1}
        
        result = self.client.call_rpc(
            service='Room',
            method='StartGameFromTeam',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'StartGameFromTeam_参数异常_参数值超出范围',
            'method': 'StartGameFromTeam',
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
        print(f"测试接口: StartGameFromTeam - 参数异常 - 参数异常_参数值超出范围")
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
            print(f"\n✓ StartGameFromTeam 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ StartGameFromTeam 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_startgamefromteam_参数异常_参数格式错误(self):
        """测试 StartGameFromTeam 接口 - 参数异常 - 参数异常_参数格式错误"""
        request_data = {'team_id': -1, 'map_id': 10000263, 'difficulty': 1}
        
        result = self.client.call_rpc(
            service='Room',
            method='StartGameFromTeam',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'StartGameFromTeam_参数异常_参数格式错误',
            'method': 'StartGameFromTeam',
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
        print(f"测试接口: StartGameFromTeam - 参数异常 - 参数异常_参数格式错误")
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
            print(f"\n✓ StartGameFromTeam 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ StartGameFromTeam 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_startgamefromteam_业务异常(self):
        """测试 StartGameFromTeam 接口 - 业务异常 - 业务异常"""
        request_data = {'team_id': 999999999, 'map_id': 10000263, 'difficulty': 1}
        
        result = self.client.call_rpc(
            service='Room',
            method='StartGameFromTeam',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'StartGameFromTeam_业务异常',
            'method': 'StartGameFromTeam',
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
        print(f"测试接口: StartGameFromTeam - 业务异常 - 业务异常")
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
            print(f"\n✓ StartGameFromTeam 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ StartGameFromTeam 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_startgamefromteam_权限安全(self):
        """测试 StartGameFromTeam 接口 - 权限安全 - 权限安全"""
        request_data = {'team_id': 1006329, 'map_id': 10000263, 'difficulty': 1}
        
        result = self.client.call_rpc(
            service='Room',
            method='StartGameFromTeam',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'StartGameFromTeam_权限安全',
            'method': 'StartGameFromTeam',
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
        print(f"测试接口: StartGameFromTeam - 权限安全 - 权限安全")
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
            print(f"\n✓ StartGameFromTeam 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ StartGameFromTeam 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_startgamefromteam_性能边界(self):
        """测试 StartGameFromTeam 接口 - 性能边界 - 性能边界"""
        request_data = {'team_id': 1006329, 'map_id': 10000263, 'difficulty': 1}
        
        result = self.client.call_rpc(
            service='Room',
            method='StartGameFromTeam',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'StartGameFromTeam_性能边界',
            'method': 'StartGameFromTeam',
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
        print(f"测试接口: StartGameFromTeam - 性能边界 - 性能边界")
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
            print(f"\n✓ StartGameFromTeam 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ StartGameFromTeam 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_match_参数异常_必填参数缺失(self):
        """测试 Match 接口 - 参数异常 - 参数异常_必填参数缺失"""
        request_data = {'team_id': 0, 'map_id': 10000263, 'difficulty': 1}
        
        result = self.client.call_rpc(
            service='Room',
            method='Match',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'Match_参数异常_必填参数缺失',
            'method': 'Match',
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
        print(f"测试接口: Match - 参数异常 - 参数异常_必填参数缺失")
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
            print(f"\n✓ Match 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ Match 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_match_参数异常_参数类型错误(self):
        """测试 Match 接口 - 参数异常 - 参数异常_参数类型错误"""
        request_data = {'team_id': 'wrong_type', 'map_id': 10000263, 'difficulty': 1}
        
        result = self.client.call_rpc(
            service='Room',
            method='Match',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'Match_参数异常_参数类型错误',
            'method': 'Match',
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
        print(f"测试接口: Match - 参数异常 - 参数异常_参数类型错误")
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
            print(f"\n✓ Match 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ Match 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_match_参数异常_参数值为空(self):
        """测试 Match 接口 - 参数异常 - 参数异常_参数值为空"""
        request_data = {'team_id': 0, 'map_id': 10000263, 'difficulty': 1}
        
        result = self.client.call_rpc(
            service='Room',
            method='Match',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'Match_参数异常_参数值为空',
            'method': 'Match',
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
        print(f"测试接口: Match - 参数异常 - 参数异常_参数值为空")
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
            print(f"\n✓ Match 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ Match 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_match_参数异常_参数值超出范围(self):
        """测试 Match 接口 - 参数异常 - 参数异常_参数值超出范围"""
        request_data = {'team_id': 999999999, 'map_id': 10000263, 'difficulty': 1}
        
        result = self.client.call_rpc(
            service='Room',
            method='Match',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'Match_参数异常_参数值超出范围',
            'method': 'Match',
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
        print(f"测试接口: Match - 参数异常 - 参数异常_参数值超出范围")
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
            print(f"\n✓ Match 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ Match 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_match_参数异常_参数格式错误(self):
        """测试 Match 接口 - 参数异常 - 参数异常_参数格式错误"""
        request_data = {'team_id': -1, 'map_id': 10000263, 'difficulty': 1}
        
        result = self.client.call_rpc(
            service='Room',
            method='Match',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'Match_参数异常_参数格式错误',
            'method': 'Match',
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
        print(f"测试接口: Match - 参数异常 - 参数异常_参数格式错误")
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
            print(f"\n✓ Match 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ Match 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_match_权限安全(self):
        """测试 Match 接口 - 权限安全 - 权限安全"""
        request_data = {'team_id': 1006329, 'map_id': 10000263, 'difficulty': 1}
        
        result = self.client.call_rpc(
            service='Room',
            method='Match',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'Match_权限安全',
            'method': 'Match',
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
        print(f"测试接口: Match - 权限安全 - 权限安全")
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
            print(f"\n✓ Match 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ Match 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_match_性能边界(self):
        """测试 Match 接口 - 性能边界 - 性能边界"""
        request_data = {'team_id': 1006329, 'map_id': 10000263, 'difficulty': 1}
        
        result = self.client.call_rpc(
            service='Room',
            method='Match',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'Match_性能边界',
            'method': 'Match',
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
        print(f"测试接口: Match - 性能边界 - 性能边界")
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
            print(f"\n✓ Match 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ Match 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_cancelmatch_参数异常_必填参数缺失(self):
        """测试 CancelMatch 接口 - 参数异常 - 参数异常_必填参数缺失"""
        request_data = {'team_id': 0}
        
        result = self.client.call_rpc(
            service='Room',
            method='CancelMatch',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'CancelMatch_参数异常_必填参数缺失',
            'method': 'CancelMatch',
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
        print(f"测试接口: CancelMatch - 参数异常 - 参数异常_必填参数缺失")
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
            print(f"\n✓ CancelMatch 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ CancelMatch 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_cancelmatch_参数异常_参数类型错误(self):
        """测试 CancelMatch 接口 - 参数异常 - 参数异常_参数类型错误"""
        request_data = {'team_id': 'wrong_type'}
        
        result = self.client.call_rpc(
            service='Room',
            method='CancelMatch',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'CancelMatch_参数异常_参数类型错误',
            'method': 'CancelMatch',
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
        print(f"测试接口: CancelMatch - 参数异常 - 参数异常_参数类型错误")
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
            print(f"\n✓ CancelMatch 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ CancelMatch 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_cancelmatch_参数异常_参数值为空(self):
        """测试 CancelMatch 接口 - 参数异常 - 参数异常_参数值为空"""
        request_data = {'team_id': 0}
        
        result = self.client.call_rpc(
            service='Room',
            method='CancelMatch',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'CancelMatch_参数异常_参数值为空',
            'method': 'CancelMatch',
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
        print(f"测试接口: CancelMatch - 参数异常 - 参数异常_参数值为空")
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
            print(f"\n✓ CancelMatch 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ CancelMatch 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_cancelmatch_参数异常_参数值超出范围(self):
        """测试 CancelMatch 接口 - 参数异常 - 参数异常_参数值超出范围"""
        request_data = {'team_id': 999999999}
        
        result = self.client.call_rpc(
            service='Room',
            method='CancelMatch',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'CancelMatch_参数异常_参数值超出范围',
            'method': 'CancelMatch',
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
        print(f"测试接口: CancelMatch - 参数异常 - 参数异常_参数值超出范围")
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
            print(f"\n✓ CancelMatch 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ CancelMatch 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_cancelmatch_参数异常_参数格式错误(self):
        """测试 CancelMatch 接口 - 参数异常 - 参数异常_参数格式错误"""
        request_data = {'team_id': -1}
        
        result = self.client.call_rpc(
            service='Room',
            method='CancelMatch',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'CancelMatch_参数异常_参数格式错误',
            'method': 'CancelMatch',
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
        print(f"测试接口: CancelMatch - 参数异常 - 参数异常_参数格式错误")
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
            print(f"\n✓ CancelMatch 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ CancelMatch 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_cancelmatch_权限安全(self):
        """测试 CancelMatch 接口 - 权限安全 - 权限安全"""
        request_data = {'team_id': 1006329}
        
        result = self.client.call_rpc(
            service='Room',
            method='CancelMatch',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'CancelMatch_权限安全',
            'method': 'CancelMatch',
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
        print(f"测试接口: CancelMatch - 权限安全 - 权限安全")
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
            print(f"\n✓ CancelMatch 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ CancelMatch 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_cancelmatch_性能边界(self):
        """测试 CancelMatch 接口 - 性能边界 - 性能边界"""
        request_data = {'team_id': 1006329}
        
        result = self.client.call_rpc(
            service='Room',
            method='CancelMatch',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'CancelMatch_性能边界',
            'method': 'CancelMatch',
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
        print(f"测试接口: CancelMatch - 性能边界 - 性能边界")
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
            print(f"\n✓ CancelMatch 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ CancelMatch 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_getgameinfo_参数异常_必填参数缺失(self):
        """测试 GetGameInfo 接口 - 参数异常 - 参数异常_必填参数缺失"""
        request_data = {'game_id': 0}
        
        result = self.client.call_rpc(
            service='Room',
            method='GetGameInfo',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'GetGameInfo_参数异常_必填参数缺失',
            'method': 'GetGameInfo',
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
        print(f"测试接口: GetGameInfo - 参数异常 - 参数异常_必填参数缺失")
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
            print(f"\n✓ GetGameInfo 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetGameInfo 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_getgameinfo_参数异常_参数类型错误(self):
        """测试 GetGameInfo 接口 - 参数异常 - 参数异常_参数类型错误"""
        request_data = {'game_id': 'wrong_type'}
        
        result = self.client.call_rpc(
            service='Room',
            method='GetGameInfo',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'GetGameInfo_参数异常_参数类型错误',
            'method': 'GetGameInfo',
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
        print(f"测试接口: GetGameInfo - 参数异常 - 参数异常_参数类型错误")
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
            print(f"\n✓ GetGameInfo 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetGameInfo 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_getgameinfo_参数异常_参数值为空(self):
        """测试 GetGameInfo 接口 - 参数异常 - 参数异常_参数值为空"""
        request_data = {'game_id': 0}
        
        result = self.client.call_rpc(
            service='Room',
            method='GetGameInfo',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'GetGameInfo_参数异常_参数值为空',
            'method': 'GetGameInfo',
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
        print(f"测试接口: GetGameInfo - 参数异常 - 参数异常_参数值为空")
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
            print(f"\n✓ GetGameInfo 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetGameInfo 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_getgameinfo_参数异常_参数值超出范围(self):
        """测试 GetGameInfo 接口 - 参数异常 - 参数异常_参数值超出范围"""
        request_data = {'game_id': 999999999}
        
        result = self.client.call_rpc(
            service='Room',
            method='GetGameInfo',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'GetGameInfo_参数异常_参数值超出范围',
            'method': 'GetGameInfo',
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
        print(f"测试接口: GetGameInfo - 参数异常 - 参数异常_参数值超出范围")
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
            print(f"\n✓ GetGameInfo 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetGameInfo 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_getgameinfo_参数异常_参数格式错误(self):
        """测试 GetGameInfo 接口 - 参数异常 - 参数异常_参数格式错误"""
        request_data = {'game_id': -1}
        
        result = self.client.call_rpc(
            service='Room',
            method='GetGameInfo',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'GetGameInfo_参数异常_参数格式错误',
            'method': 'GetGameInfo',
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
        print(f"测试接口: GetGameInfo - 参数异常 - 参数异常_参数格式错误")
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
            print(f"\n✓ GetGameInfo 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetGameInfo 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_getgameinfo_权限安全(self):
        """测试 GetGameInfo 接口 - 权限安全 - 权限安全"""
        request_data = {'game_id': 1001}
        
        result = self.client.call_rpc(
            service='Room',
            method='GetGameInfo',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'GetGameInfo_权限安全',
            'method': 'GetGameInfo',
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
        print(f"测试接口: GetGameInfo - 权限安全 - 权限安全")
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
            print(f"\n✓ GetGameInfo 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetGameInfo 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_getgameinfo_性能边界(self):
        """测试 GetGameInfo 接口 - 性能边界 - 性能边界"""
        request_data = {'game_id': 1001}
        
        result = self.client.call_rpc(
            service='Room',
            method='GetGameInfo',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'GetGameInfo_性能边界',
            'method': 'GetGameInfo',
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
        print(f"测试接口: GetGameInfo - 性能边界 - 性能边界")
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
            print(f"\n✓ GetGameInfo 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetGameInfo 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_leaveteam_参数异常_必填参数缺失(self):
        """测试 LeaveTeam 接口 - 参数异常 - 参数异常_必填参数缺失"""
        request_data = {'team_id': 0}
        
        result = self.client.call_rpc(
            service='Room',
            method='LeaveTeam',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'LeaveTeam_参数异常_必填参数缺失',
            'method': 'LeaveTeam',
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
        print(f"测试接口: LeaveTeam - 参数异常 - 参数异常_必填参数缺失")
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
            print(f"\n✓ LeaveTeam 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ LeaveTeam 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_leaveteam_参数异常_参数类型错误(self):
        """测试 LeaveTeam 接口 - 参数异常 - 参数异常_参数类型错误"""
        request_data = {'team_id': 'wrong_type'}
        
        result = self.client.call_rpc(
            service='Room',
            method='LeaveTeam',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'LeaveTeam_参数异常_参数类型错误',
            'method': 'LeaveTeam',
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
        print(f"测试接口: LeaveTeam - 参数异常 - 参数异常_参数类型错误")
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
            print(f"\n✓ LeaveTeam 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ LeaveTeam 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_leaveteam_参数异常_参数值为空(self):
        """测试 LeaveTeam 接口 - 参数异常 - 参数异常_参数值为空"""
        request_data = {'team_id': 0}
        
        result = self.client.call_rpc(
            service='Room',
            method='LeaveTeam',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'LeaveTeam_参数异常_参数值为空',
            'method': 'LeaveTeam',
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
        print(f"测试接口: LeaveTeam - 参数异常 - 参数异常_参数值为空")
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
            print(f"\n✓ LeaveTeam 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ LeaveTeam 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_leaveteam_参数异常_参数值超出范围(self):
        """测试 LeaveTeam 接口 - 参数异常 - 参数异常_参数值超出范围"""
        request_data = {'team_id': 999999999}
        
        result = self.client.call_rpc(
            service='Room',
            method='LeaveTeam',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'LeaveTeam_参数异常_参数值超出范围',
            'method': 'LeaveTeam',
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
        print(f"测试接口: LeaveTeam - 参数异常 - 参数异常_参数值超出范围")
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
            print(f"\n✓ LeaveTeam 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ LeaveTeam 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_leaveteam_参数异常_参数格式错误(self):
        """测试 LeaveTeam 接口 - 参数异常 - 参数异常_参数格式错误"""
        request_data = {'team_id': -1}
        
        result = self.client.call_rpc(
            service='Room',
            method='LeaveTeam',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'LeaveTeam_参数异常_参数格式错误',
            'method': 'LeaveTeam',
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
        print(f"测试接口: LeaveTeam - 参数异常 - 参数异常_参数格式错误")
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
            print(f"\n✓ LeaveTeam 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ LeaveTeam 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_leaveteam_业务异常(self):
        """测试 LeaveTeam 接口 - 业务异常 - 业务异常"""
        request_data = {'team_id': 999999999}
        
        result = self.client.call_rpc(
            service='Room',
            method='LeaveTeam',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'LeaveTeam_业务异常',
            'method': 'LeaveTeam',
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
        print(f"测试接口: LeaveTeam - 业务异常 - 业务异常")
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
            print(f"\n✓ LeaveTeam 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ LeaveTeam 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_leaveteam_权限安全(self):
        """测试 LeaveTeam 接口 - 权限安全 - 权限安全"""
        request_data = {'team_id': 1006329}
        
        result = self.client.call_rpc(
            service='Room',
            method='LeaveTeam',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'LeaveTeam_权限安全',
            'method': 'LeaveTeam',
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
        print(f"测试接口: LeaveTeam - 权限安全 - 权限安全")
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
            print(f"\n✓ LeaveTeam 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ LeaveTeam 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

    def test_leaveteam_性能边界(self):
        """测试 LeaveTeam 接口 - 性能边界 - 性能边界"""
        request_data = {'team_id': 1006329}
        
        result = self.client.call_rpc(
            service='Room',
            method='LeaveTeam',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {
            'name': 'LeaveTeam_性能边界',
            'method': 'LeaveTeam',
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
        print(f"测试接口: LeaveTeam - 性能边界 - 性能边界")
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
            print(f"\n✓ LeaveTeam 异常测试通过: 返回预期错误码 {error_code}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ LeaveTeam 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {error_msg}")

if __name__ == '__main__':
    unittest.main()
