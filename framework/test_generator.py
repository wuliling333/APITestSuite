"""
测试代码生成器 - 根据接口定义和YAML测试用例生成Python测试代码
"""
import os
import yaml
import json
from typing import Dict, List, Any, Optional
from framework.config import Config
from framework.request_data_converter import RequestDataConverter


class TestGenerator:
    """测试代码生成器"""
    
    def __init__(self, config: Config):
        self.config = config
        self.output_dir = config.get_test_output_dir()
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_all_tests(self, interfaces: Dict[str, List[Dict]]):
        """生成所有服务的测试代码"""
        print("=" * 80)
        print("生成测试代码...")
        print("=" * 80)
        
        for service_name, service_interfaces in interfaces.items():
            self._generate_service_tests(service_name, service_interfaces)
        
        print("✓ 测试代码生成完成")
    
    def _generate_service_tests(self, service_name: str, interfaces: List[Dict]):
        """生成单个服务的测试代码"""
        # 加载YAML测试用例
        yaml_file = f"test_cases/{service_name}/test_{service_name}.yaml"
        test_cases = self._load_test_cases(yaml_file)
        
        # 打印调试信息
        print(f"\n📋 {service_name.upper()} 服务: 发现 {len(interfaces)} 个接口")
        for interface in interfaces:
            print(f"  - {interface['name']}")
        
        # 生成Python测试文件
        test_file = os.path.join(self.output_dir, f"test_{service_name}.py")
        self._write_test_file(test_file, service_name, interfaces, test_cases)
        
        print(f"✓ 生成 {service_name} 服务测试: {test_file}")
    
    def _load_test_cases(self, yaml_file: str) -> Dict:
        """加载YAML测试用例"""
        if not os.path.exists(yaml_file):
            return {}
        
        with open(yaml_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}
    
    def _write_test_file(self, file_path: str, service_name: str, interfaces: List[Dict], test_cases: Dict):
        """写入测试文件"""
        service_cap = service_name.capitalize()
        
        content = f'''"""
自动生成的{service_cap}服务测试代码
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
                result = {{}}
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
            return {{k: convert_to_dict(v) for k, v in val.items()}}
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


class Test{service_cap}(unittest.TestCase):
    """{service_cap}服务测试"""
    
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
            result = cls.client.call_rpc('Hall', 'FetchSelfFullUserInfo', {{}})
            if result.get('success'):
                response = result.get('response', {{}})
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
    
'''
        
        # 对于Room服务，将LeaveTeam放在最后
        if service_name == 'room':
            # 分离LeaveTeam和其他接口
            leave_team_interface = None
            other_interfaces = []
            for interface in interfaces:
                if interface['name'] == 'LeaveTeam':
                    leave_team_interface = interface
                else:
                    other_interfaces.append(interface)
            
            # 先处理其他接口，最后处理LeaveTeam
            sorted_interfaces = other_interfaces
            if leave_team_interface:
                sorted_interfaces.append(leave_team_interface)
        else:
            sorted_interfaces = interfaces
        
        # 为每个接口生成测试方法
        for interface in sorted_interfaces:
            method_name = interface['name']
            print(f"  🔧 处理接口: {method_name}")
            
            # 获取正常测试用例
            normal_test_case = test_cases.get('test_cases', {}).get(method_name, {})
            if not normal_test_case:
                # 尝试查找带"正常"后缀的测试用例
                normal_test_case = test_cases.get('test_cases', {}).get(f"{method_name}_正常", {})
            
            if normal_test_case:
                print(f"    ✓ 找到正常测试用例: {method_name}_正常")
            else:
                print(f"    ⚠ 未找到正常测试用例: {method_name} 或 {method_name}_正常")
            
            # 获取所有异常测试用例（参数异常、业务异常等）
            abnormal_test_cases = {}
            for test_case_name, test_case_data in test_cases.get('test_cases', {}).items():
                if test_case_name.startswith(f"{method_name}_") and test_case_name != f"{method_name}_正常":
                    dimension = test_case_data.get('dimension', '')
                    if dimension and dimension != '正常':
                        abnormal_test_cases[test_case_name] = test_case_data
            
            print(f"    📊 找到 {len(abnormal_test_cases)} 个异常测试用例")
            
            # 生成正常测试用例
            if normal_test_case:
                test_method_name = f"test_{method_name.lower()}"
                request_data_raw = normal_test_case.get('request', {})
                # 转换YAML格式的请求数据（{"value": ..., "type": ...}）为实际值
                request_data = RequestDataConverter.convert_nested_request_data(request_data_raw)
                
                # 初始化 request_data_str
                request_data_str = repr(request_data)
                should_generate_generic = True  # 标志：是否需要生成通用测试代码
                
                # 特殊处理：FetchSimpleUserInfo 需要 target_uid
                if method_name == 'FetchSimpleUserInfo' and not request_data.get('target_uid'):
                    # 使用当前用户的 UID
                    request_data_str = "{'target_uid': self.current_uid if hasattr(self, 'current_uid') else self.client.uid}"
                # 特殊处理：StashToBackpack 需要从仓库获取有效的 unique_id
                elif method_name == 'StashToBackpack' and service_name == 'hall':
                    # 需要从用户信息中获取仓库物品的 unique_id 和背包空格子的 cell_id
                    content += f'''
    def {test_method_name}(self):
        """测试 {method_name} 接口（前置条件：从仓库获取有效的unique_id和背包空cell_id）"""
        # 前置条件：获取用户信息，找到仓库中的物品和背包中的空格子
        user_info_result = self.client.call_rpc('Hall', 'FetchSelfFullUserInfo', {{}})
        if not user_info_result.get('success'):
            self.skipTest(f"前置条件失败：无法获取用户信息 - {{user_info_result.get('error_message', '未知错误')}}")
        
        user_info = user_info_result.get('response', {{}})
        full_user_info = user_info.get('fetchselffulluserinfo', {{}}).get('full_user_info', {{}})
        stash = full_user_info.get('stash', {{}})
        backpack = full_user_info.get('backpack', {{}})
        
        # 从仓库中找到有效的物品（unique_id > 0）
        unique_id = 0
        for item in stash.get('items', []):
            if isinstance(item, dict) and item.get('unique_id', 0) > 0:
                unique_id = item.get('unique_id')
                break
        
        # 从背包中找到空的格子（carried_item 为空或 item_id == 0）
        cell_id = 0
        for cell in backpack.get('cells', []):
            if isinstance(cell, dict):
                carried_item = cell.get('carried_item', {{}})
                if not carried_item or (isinstance(carried_item, dict) and carried_item.get('item_id', 0) == 0):
                    cell_id = cell.get('cell_id', 0)
                    if cell_id >= 0:  # cell_id 可以是 0
                        break
        
        if unique_id == 0:
            self.skipTest("前置条件失败：仓库中没有有效的物品")
        if cell_id == 0:
            self.skipTest("前置条件失败：背包中没有空的格子")
        
        # 使用获取到的 unique_id 和 cell_id 调用接口
        request_data = {{'unique_id': unique_id, 'cell_id': cell_id}}
        
        result = self.client.call_rpc(
            service='Hall',
            method='{method_name}',
            request_data=request_data
        )
        
        # 保存测试结果用于报告
        self.test_result = {{
            'name': '{method_name}',
            'method': '{method_name}',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': []
        }}
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\\n{{'='*60}}")
        print(f"测试接口: {method_name}")
        print(f"请求参数: {{safe_json_dumps(request_data)}}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {{safe_json_dumps(result)}}")
        print(f"响应数据: {{safe_json_dumps(result.get('response', {{}}))}}")
        print(f"响应码: {{result.get('error_code', 200)}}")
        if result.get('error_message'):
            print(f"错误信息: {{result.get('error_message')}}")
        print(f"{{'='*60}}")
        
        # 断言
        if not result.get('success', False):
            error_msg = result.get('error_message', '未知错误')
            print(f"\\n✗ {method_name} 测试失败: {{error_msg}}")
            self.assertTrue(False, f"API调用失败: {{error_msg}}")
        else:
            print(f"\\n✓ {method_name} 测试通过")
'''
                    should_generate_generic = False
                    # 不要continue，让异常测试用例生成代码执行
                # 特殊处理：BackpackToStash 需要从背包获取有效的 cell_id
                elif method_name == 'BackpackToStash' and service_name == 'hall':
                    # 需要从用户信息中获取背包中有物品的 cell_id
                    content += f'''
    def {test_method_name}(self):
        """测试 {method_name} 接口（前置条件：从背包获取有效的cell_id）"""
        # 前置条件：获取用户信息，找到背包中有物品的格子
        user_info_result = self.client.call_rpc('Hall', 'FetchSelfFullUserInfo', {{}})
        if not user_info_result.get('success'):
            self.skipTest(f"前置条件失败：无法获取用户信息 - {{user_info_result.get('error_message', '未知错误')}}")
        
        user_info = user_info_result.get('response', {{}})
        full_user_info = user_info.get('fetchselffulluserinfo', {{}}).get('full_user_info', {{}})
        backpack = full_user_info.get('backpack', {{}})
        
        # 从背包中找到有物品的格子（carried_item 不为空且 item_id > 0）
        cell_id = 0
        for cell in backpack.get('cells', []):
            if isinstance(cell, dict):
                carried_item = cell.get('carried_item', {{}})
                if isinstance(carried_item, dict) and carried_item.get('item_id', 0) > 0:
                    cell_id = cell.get('cell_id', 0)
                    if cell_id >= 0:  # cell_id 可以是 0
                        break
        
        if cell_id == 0:
            self.skipTest("前置条件失败：背包中没有有效的物品")
        
        # 使用获取到的 cell_id 调用接口
        request_data = {{'cell_id': cell_id}}
        
        result = self.client.call_rpc(
            service='Hall',
            method='{method_name}',
            request_data=request_data
        )
        
        # 保存测试结果用于报告
        self.test_result = {{
            'name': '{method_name}',
            'method': '{method_name}',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': []
        }}
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\\n{{'='*60}}")
        print(f"测试接口: {method_name}")
        print(f"请求参数: {{safe_json_dumps(request_data)}}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {{safe_json_dumps(result)}}")
        print(f"响应数据: {{safe_json_dumps(result.get('response', {{}}))}}")
        print(f"响应码: {{result.get('error_code', 200)}}")
        if result.get('error_message'):
            print(f"错误信息: {{result.get('error_message')}}")
        print(f"{{'='*60}}")
        
        # 断言
        if not result.get('success', False):
            error_msg = result.get('error_message', '未知错误')
            print(f"\\n✗ {method_name} 测试失败: {{error_msg}}")
            self.assertTrue(False, f"API调用失败: {{error_msg}}")
        else:
            print(f"\\n✓ {method_name} 测试通过")
'''
                    should_generate_generic = False
                    # 不要continue，让异常测试用例生成代码执行
                # 特殊处理：ExchangeBackpackItem 需要从背包获取两个有效的 cell_id
                elif method_name == 'ExchangeBackpackItem' and service_name == 'hall':
                    # 需要从用户信息中获取背包中的两个格子
                    content += f'''
    def {test_method_name}(self):
        """测试 {method_name} 接口（前置条件：从背包获取两个有效的cell_id）"""
        # 前置条件：获取用户信息，找到背包中的两个格子
        user_info_result = self.client.call_rpc('Hall', 'FetchSelfFullUserInfo', {{}})
        if not user_info_result.get('success'):
            self.skipTest(f"前置条件失败：无法获取用户信息 - {{user_info_result.get('error_message', '未知错误')}}")
        
        user_info = user_info_result.get('response', {{}})
        full_user_info = user_info.get('fetchselffulluserinfo', {{}}).get('full_user_info', {{}})
        backpack = full_user_info.get('backpack', {{}})
        
        # 从背包中找到两个格子（至少需要两个格子）
        cells = backpack.get('cells', [])
        if len(cells) < 2:
            self.skipTest("前置条件失败：背包中格子数量不足")
        
        source_cell_id = cells[0].get('cell_id', 0)
        target_cell_id = cells[1].get('cell_id', 0)
        
        if source_cell_id == 0 or target_cell_id == 0:
            self.skipTest("前置条件失败：无法获取有效的 cell_id")
        
        # 使用获取到的 cell_id 调用接口
        request_data = {{'source_cell_id': source_cell_id, 'target_cell_id': target_cell_id}}
        
        result = self.client.call_rpc(
            service='Hall',
            method='{method_name}',
            request_data=request_data
        )
        
        # 保存测试结果用于报告
        self.test_result = {{
            'name': '{method_name}',
            'method': '{method_name}',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': []
        }}
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\\n{{'='*60}}")
        print(f"测试接口: {method_name}")
        print(f"请求参数: {{safe_json_dumps(request_data)}}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {{safe_json_dumps(result)}}")
        print(f"响应数据: {{safe_json_dumps(result.get('response', {{}}))}}")
        print(f"响应码: {{result.get('error_code', 200)}}")
        if result.get('error_message'):
            print(f"错误信息: {{result.get('error_message')}}")
        print(f"{{'='*60}}")
        
        # 断言
        if not result.get('success', False):
            error_msg = result.get('error_message', '未知错误')
            print(f"\\n✗ {method_name} 测试失败: {{error_msg}}")
            self.assertTrue(False, f"API调用失败: {{error_msg}}")
        else:
            print(f"\\n✓ {method_name} 测试通过")
'''
                    should_generate_generic = False
                    # 不要continue，让异常测试用例生成代码执行
                # 特殊处理：SendMessage 需要有效的 to_uid（不能给自己发消息）
                elif method_name == 'SendMessage' and service_name == 'social':
                    # 生成带有效 to_uid 的测试代码
                    # 使用世界聊天场景（scene=4），不需要 room_id 或 to_uid
                    content += f'''
    def {test_method_name}(self):
        """测试 {method_name} 接口（使用世界聊天场景）"""
        # 使用世界聊天场景（scene=4），不需要 room_id 或 to_uid，避免私聊需要先关注的问题
        request_data = {{'to_uid': 0, 'conv_id': '', 'scene': 4, 'scene_id': 0, 'content': {{'msg_type': 1, 'text': {{'text': 'test message'}}}}}}
        
        result = self.client.call_rpc(
            service='{service_cap}',
            method='{method_name}',
            request_data=request_data
        )
        
        # 保存测试结果用于报告
        self.test_result = {{
            'name': '{method_name}',
            'method': '{method_name}',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': []
        }}
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\\n{{'='*60}}")
        print(f"测试接口: {method_name}")
        print(f"请求参数: {{safe_json_dumps(request_data)}}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {{safe_json_dumps(result)}}")
        print(f"响应数据: {{safe_json_dumps(result.get('response', {{}}))}}")
        print(f"响应码: {{result.get('error_code', 200)}}")
        if result.get('error_message'):
            print(f"错误信息: {{result.get('error_message')}}")
        print(f"{{'='*60}}")
        
        # 断言
        if not result.get('success', False):
            error_msg = result.get('error_message', '未知错误')
            print(f"\\n✗ {method_name} 测试失败: {{error_msg}}")
            self.assertTrue(False, f"API调用失败: {{error_msg}}")
        else:
            print(f"\\n✓ {method_name} 测试通过")
'''
                    should_generate_generic = False
                    # 不要continue，让异常测试用例生成代码执行
                # 特殊处理：Social服务中需要前置条件的接口
                elif service_name == 'social' and method_name in ['DeleteMsg', 'AddReaction', 'RemoveReaction', 'GetReactions', 'RevokeMsg']:
                    # 需要 conv_id 和 seq，先发送消息获取（使用世界聊天场景）
                    content += f'''
    def {test_method_name}(self):
        """测试 {method_name} 接口（前置条件：先发送消息获取conv_id和seq）"""
        # 前置条件：先发送消息获取 conv_id 和 seq（使用世界聊天场景，避免私聊需要先关注）
        send_result = self.client.call_rpc(
            service='Social',
            method='SendMessage',
            request_data={{'to_uid': 0, 'scene': 4, 'scene_id': 0, 'content': {{'msg_type': 1, 'text': {{'text': 'test message'}}}}}}
        )
        
        if not send_result.get('success'):
            self.skipTest(f"前置条件失败：无法发送消息 - {{send_result.get('error_message', '未知错误')}}")
        
        # 从发送消息的响应中获取 conv_id 和 seq
        send_response = send_result.get('response', {{}})
        conv_id = ''
        seq = 0
        if 'sendmessage' in send_response:
            send_msg = send_response['sendmessage']
            conv_id = send_msg.get('conv_id', '')
            seq = send_msg.get('seq', 0)
        
        if not conv_id or seq == 0:
            self.skipTest("前置条件失败：无法获取有效的 conv_id 和 seq")
        
        # 使用获取到的 conv_id 和 seq 调用接口
        if '{method_name}' == 'DeleteMsg':
            request_data = {{'conv_id': conv_id, 'seqs': [seq]}}
        else:
            request_data = {{'conv_id': conv_id, 'seq': seq}}
        
        result = self.client.call_rpc(
            service='Social',
            method='{method_name}',
            request_data=request_data
        )
        
        # 保存测试结果用于报告
        self.test_result = {{
            'name': '{method_name}',
            'method': '{method_name}',
            'request': request_data,
            'response': result,  # 保存完整的result，包括success、response、error_code、error_message
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [
                '发送消息 (SendMessage): to_uid=0, scene=4, scene_id=0',
                '从响应获取: conv_id, seq'
            ]
        }}
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\\n{'='*60}")
        print(f"测试接口: {method_name}")
        print(f"请求参数: {{safe_json_dumps(request_data)}}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {{safe_json_dumps(result)}}")
        print(f"响应数据: {{safe_json_dumps(result.get('response', {{}}))}}")
        print(f"响应码: {{result.get('error_code', 200)}}")
        if result.get('error_message'):
            print(f"错误信息: {{result.get('error_message')}}")
        print(f"{'='*60}")
        
        # 断言
        if not result.get('success', False):
            error_msg = result.get('error_message', '未知错误')
            print(f"\\n✗ {method_name} 测试失败: {{error_msg}}")
            self.assertTrue(False, f"API调用失败: {{error_msg}}")
        else:
            print(f"\\n✓ {method_name} 测试通过")
'''
                should_generate_generic = False
                # 不要continue，让异常测试用例生成代码执行
            elif service_name == 'social' and method_name == 'PullMsgs':
                # 需要 conv_id，先发送消息获取（使用世界聊天场景）
                content += f'''
    def {test_method_name}(self):
        """测试 {method_name} 接口（前置条件：先发送消息获取conv_id）"""
        # 前置条件：先发送消息获取 conv_id（使用世界聊天场景，避免私聊需要先关注）
        send_result = self.client.call_rpc(
            service='Social',
            method='SendMessage',
            request_data={{'to_uid': 0, 'scene': 4, 'scene_id': 0, 'content': {{'msg_type': 1, 'text': {{'text': 'test message'}}}}}}
        )
        
        if not send_result.get('success'):
            self.skipTest(f"前置条件失败：无法发送消息 - {{send_result.get('error_message', '未知错误')}}")
        
        # 从发送消息的响应中获取 conv_id 和 seq
        send_response = send_result.get('response', {{}})
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
        request_data = {{'conv_id': conv_id, 'scene': 4, 'scene_id': 0, 'start_seq': 0, 'count': 20, 'reverse': False}}
        
        result = self.client.call_rpc(
            service='Social',
            method='{method_name}',
            request_data=request_data
        )
        
        # 保存测试结果用于报告
        self.test_result = {{
            'name': '{method_name}',
            'method': '{method_name}',
            'request': request_data,
            'response': result,  # 保存完整的result，包括success、response、error_code、error_message
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': []
        }}
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\\n{'='*60}")
        print(f"测试接口: {method_name}")
        print(f"请求参数: {{safe_json_dumps(request_data)}}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {{safe_json_dumps(result)}}")
        print(f"响应数据: {{safe_json_dumps(result.get('response', {{}}))}}")
        print(f"响应码: {{result.get('error_code', 200)}}")
        if result.get('error_message'):
            print(f"错误信息: {{result.get('error_message')}}")
        print(f"{'='*60}")
        
        # 断言
        if not result.get('success', False):
            error_msg = result.get('error_message', '未知错误')
            print(f"\\n✗ {method_name} 测试失败: {{error_msg}}")
            self.assertTrue(False, f"API调用失败: {{error_msg}}")
        else:
            print(f"\\n✓ {method_name} 测试通过")
'''
                should_generate_generic = False
                # 注意：不要continue，让异常测试用例生成代码执行
            elif service_name == 'social' and method_name == 'MarkRead':
                # MarkRead 在服务器端未实现，跳过测试
                content += f'''
    def {test_method_name}(self):
        """测试 {method_name} 接口（服务器端未实现）"""
        # MarkRead 接口在服务器端未实现，跳过测试
        self.skipTest("MarkRead 接口在服务器端未实现")
'''
                continue
                # 需要 conv_id，先发送消息获取（使用世界聊天场景）
                content += f'''
    def {test_method_name}(self):
        """测试 {method_name} 接口（前置条件：先发送消息获取conv_id）"""
        # 前置条件：先发送消息获取 conv_id（使用世界聊天场景，避免私聊需要先关注）
        send_result = self.client.call_rpc(
            service='Social',
            method='SendMessage',
            request_data={{'to_uid': 0, 'scene': 4, 'scene_id': 0, 'content': {{'msg_type': 1, 'text': {{'text': 'test message'}}}}}}
        )
        
        if not send_result.get('success'):
            self.skipTest(f"前置条件失败：无法发送消息 - {{send_result.get('error_message', '未知错误')}}")
        
        # 从发送消息的响应中获取 conv_id 和 seq
        send_response = send_result.get('response', {{}})
        conv_id = ''
        seq = 0
        if 'sendmessage' in send_response:
            send_msg = send_response['sendmessage']
            conv_id = send_msg.get('conv_id', '')
            seq = send_msg.get('seq', 0)
        
        if not conv_id:
            self.skipTest("前置条件失败：无法获取有效的 conv_id")
        
        # 使用获取到的 conv_id 调用接口
        if '{method_name}' == 'MarkRead':
            request_data = {{'conv_id': conv_id, 'read_seq': seq}}
        else:
            # PullMsgs 需要 scene 参数，使用世界聊天场景（scene=4）
            request_data = {{'conv_id': conv_id, 'scene': 4, 'scene_id': 0, 'start_seq': 0, 'count': 20, 'reverse': False}}
        
        result = self.client.call_rpc(
            service='Social',
            method='{method_name}',
            request_data=request_data
        )
        
        # 保存测试结果用于报告
        self.test_result = {{
            'name': '{method_name}',
            'method': '{method_name}',
            'request': request_data,
            'response': result,  # 保存完整的result，包括success、response、error_code、error_message
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': []
        }}
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\\n{'='*60}")
        print(f"测试接口: {method_name}")
        print(f"请求参数: {{safe_json_dumps(request_data)}}")
        print(f"响应数据: {{safe_json_dumps(result.get('response', {{}}))}}")
        print(f"响应码: {{result.get('error_code', 200)}}")
        if result.get('error_message'):
            print(f"错误信息: {{result.get('error_message')}}")
        print(f"{'='*60}")
        
        # 断言
        if not result.get('success', False):
            error_msg = result.get('error_message', '未知错误')
            print(f"\\n✗ {method_name} 测试失败: {{error_msg}}")
            self.assertTrue(False, f"API调用失败: {{error_msg}}")
        else:
            print(f"\\n✓ {method_name} 测试通过")
'''
                should_generate_generic = False
                # 注意：不要continue，让异常测试用例生成代码执行
            elif service_name == 'social' and method_name == 'Follow':
                # 需要 target_uid，优先使用YAML中定义的target_uid，如果无效则使用默认值
                # 从YAML测试用例中获取target_uid
                yaml_target_uid = request_data.get('target_uid')
                # 如果YAML中没有target_uid或值为0/null，使用一个有效的默认值
                if not yaml_target_uid or yaml_target_uid == 0:
                    # 使用YAML中正常测试用例使用的target_uid值（10000263）
                    target_uid = 10000263
                else:
                    target_uid = yaml_target_uid
                
                content += f'''
    def {test_method_name}(self):
        """测试 {method_name} 接口（使用有效的target_uid）"""
        # 使用YAML中定义的target_uid或默认值
        target_uid = {target_uid}
        
        request_data = {{'target_uid': target_uid}}
        
        result = self.client.call_rpc(
            service='Social',
            method='Follow',
            request_data=request_data
        )
        
        # 保存测试结果用于报告
        self.test_result = {{
            'name': '{method_name}',
            'method': '{method_name}',
            'request': request_data,
            'response': result,  # 保存完整的result，包括success、response、error_code、error_message
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [
                f'使用有效的 target_uid: {target_uid}'
            ]
        }}
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\\n{'='*60}")
        print(f"测试接口: {method_name}")
        print(f"请求参数: {{safe_json_dumps(request_data)}}")
        print(f"响应数据: {{safe_json_dumps(result.get('response', {{}}))}}")
        print(f"响应码: {{result.get('error_code', 200)}}")
        if result.get('error_message'):
            print(f"错误信息: {{result.get('error_message')}}")
        print(f"{'='*60}")
        
        # 断言
        if not result.get('success', False):
            error_msg = result.get('error_message', '未知错误')
            print(f"\\n✗ {method_name} 测试失败: {{error_msg}}")
            self.assertTrue(False, f"API调用失败: {{error_msg}}")
        else:
            print(f"\\n✓ {method_name} 测试通过")
'''
                should_generate_generic = False
                # 注意：不要continue，让异常测试用例生成代码执行
            elif service_name == 'social' and method_name == 'Unfollow':
                # 需要先关注，然后再取消关注
                # 从YAML测试用例中获取target_uid
                yaml_target_uid = request_data.get('target_uid')
                # 如果YAML中没有target_uid或值为0/null，使用一个有效的默认值
                if not yaml_target_uid or yaml_target_uid == 0:
                    # 使用YAML中正常测试用例使用的target_uid值（10000263）
                    target_uid = 10000263
                else:
                    target_uid = yaml_target_uid
                
                content += f'''
    def {test_method_name}(self):
        """测试 {method_name} 接口（前置条件：先关注）"""
        # 使用YAML中定义的target_uid或默认值
        target_uid = {target_uid}
        
        # 前置条件：先关注
        follow_result = self.client.call_rpc(
            service='Social',
            method='Follow',
            request_data={{'target_uid': target_uid}}
        )
        
        # 即使关注失败也继续测试（可能已经关注过了）
        
        # 使用获取到的 target_uid 调用 Unfollow
        request_data = {{'target_uid': target_uid}}
        
        result = self.client.call_rpc(
            service='Social',
            method='Unfollow',
            request_data=request_data
        )
        
        # 保存测试结果用于报告
        self.test_result = {{
            'name': '{method_name}',
            'method': '{method_name}',
            'request': request_data,
            'response': result,  # 保存完整的result，包括success、response、error_code、error_message
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [
                f'先关注 (Follow): target_uid={{target_uid}}',
                f'取消关注 (Unfollow): target_uid={{target_uid}}'
            ]
        }}
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\\n{'='*60}")
        print(f"测试接口: {method_name}")
        print(f"请求参数: {{safe_json_dumps(request_data)}}")
        print(f"响应数据: {{safe_json_dumps(result.get('response', {{}}))}}")
        print(f"响应码: {{result.get('error_code', 200)}}")
        if result.get('error_message'):
            print(f"错误信息: {{result.get('error_message')}}")
        print(f"{'='*60}")
        
        # 断言
        if not result.get('success', False):
            error_msg = result.get('error_message', '未知错误')
            print(f"\\n✗ {method_name} 测试失败: {{error_msg}}")
            self.assertTrue(False, f"API调用失败: {{error_msg}}")
        else:
            print(f"\\n✓ {method_name} 测试通过")
'''
                should_generate_generic = False
                # 注意：不要continue，让异常测试用例生成代码执行
            # 特殊处理：CancelMatch 需要前置条件（先创建队伍，然后开始匹配）
            elif method_name == 'CancelMatch' and service_name == 'room':
                # 生成带前置条件的测试代码
                content += f'''
    def {test_method_name}(self):
        """测试 {method_name} 接口（前置条件：先创建队伍并开始匹配）"""
        # 前置条件1：先创建队伍
        create_result = self.client.call_rpc(
            service='Room',
            method='CreateTeam',
            request_data={{'game_mode': 1}}
        )
        
        if not create_result.get('success'):
            self.skipTest(f"前置条件失败：无法创建队伍 - {{create_result.get('error_message', '未知错误')}}")
        
        # 从创建队伍的响应中获取 team_id
        create_response = create_result.get('response', {{}})
        team_id = 0
        if 'createteam' in create_response:
            team_info = create_response['createteam'].get('team_info', {{}})
            team_id = team_info.get('team_id', 0)
        
        if team_id == 0:
            self.skipTest("前置条件失败：无法获取有效的 team_id")
        
        # 前置条件2：开始匹配（使队伍状态变为匹配中）
        # Match 需要 map_id，使用默认值 1
        match_result = self.client.call_rpc(
            service='Room',
            method='Match',
            request_data={{'team_id': team_id, 'map_id': 1}}
        )
        
        if not match_result.get('success'):
            self.skipTest(f"前置条件失败：无法开始匹配 - {{match_result.get('error_message', '未知错误')}}")
        
        # 使用获取到的 team_id 调用 CancelMatch
        request_data = {{'team_id': team_id}}
        
        result = self.client.call_rpc(
            service='Room',
            method='{method_name}',
            request_data=request_data
        )
        
        # 保存测试结果用于报告
        self.test_result = {{
            'name': '{method_name}',
            'method': '{method_name}',
            'request': request_data,
            'response': result,  # 保存完整的result，包括success、response、error_code、error_message
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': []
        }}
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\\n{'='*60}")
        print(f"测试接口: {method_name}")
        print(f"请求参数: {{safe_json_dumps(request_data)}}")
        print(f"响应数据: {{safe_json_dumps(result.get('response', {{}}))}}")
        print(f"响应码: {{result.get('error_code', 200)}}")
        if result.get('error_message'):
            print(f"错误信息: {{result.get('error_message')}}")
        print(f"{'='*60}")
        
        # 断言
        if not result.get('success', False):
            error_msg = result.get('error_message', '未知错误')
            print(f"\\n✗ {method_name} 测试失败: {{error_msg}}")
            self.assertTrue(False, f"API调用失败: {{error_msg}}")
        else:
            print(f"\\n✓ {method_name} 测试通过")
'''
                should_generate_generic = False
                # 注意：不要continue，让异常测试用例生成代码执行
            # 特殊处理：JoinTeam 需要前置条件（先创建队伍）
            elif method_name == 'JoinTeam' and service_name == 'room':
                # 生成带前置条件的测试代码
                content += f'''
    def {test_method_name}(self):
        """测试 {method_name} 接口（前置条件：先创建队伍）"""
        # 前置条件：先创建队伍
        create_result = self.client.call_rpc(
            service='Room',
            method='CreateTeam',
            request_data={{'game_mode': 1}}
        )
        
        if not create_result.get('success'):
            self.skipTest(f"前置条件失败：无法创建队伍 - {{create_result.get('error_message', '未知错误')}}")
        
        # 从创建队伍的响应中获取 team_id
        create_response = create_result.get('response', {{}})
        team_id = 0
        if 'createteam' in create_response:
            team_info = create_response['createteam'].get('team_info', {{}})
            team_id = team_info.get('team_id', 0)
        
        if team_id == 0:
            self.skipTest("前置条件失败：无法获取有效的 team_id")
        
        # 使用获取到的 team_id 调用 JoinTeam
        request_data = {{'team_id': team_id}}
        
        result = self.client.call_rpc(
            service='Room',
            method='{method_name}',
            request_data=request_data
        )
        
        # 保存测试结果用于报告
        self.test_result = {{
            'name': '{method_name}',
            'method': '{method_name}',
            'request': request_data,
            'response': result,  # 保存完整的result，包括success、response、error_code、error_message
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [
                '创建队伍 (CreateTeam): game_mode=1',
                '从响应获取: team_id'
            ]
        }}
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\\n{'='*60}")
        print(f"测试接口: {method_name}")
        print(f"请求参数: {{safe_json_dumps(request_data)}}")
        print(f"响应数据: {{safe_json_dumps(result.get('response', {{}}))}}")
        print(f"响应码: {{result.get('error_code', 200)}}")
        if result.get('error_message'):
            print(f"错误信息: {{result.get('error_message')}}")
        print(f"{'='*60}")
        
        # 断言
        if not result.get('success', False):
            error_msg = result.get('error_message', '未知错误')
            print(f"\\n✗ {method_name} 测试失败: {{error_msg}}")
            self.assertTrue(False, f"API调用失败: {{error_msg}}")
        else:
            print(f"\\n✓ {method_name} 测试通过")
'''
                should_generate_generic = False
                # 注意：不要continue，让异常测试用例生成代码执行
            # 特殊处理：GetTeamInfo 需要前置条件（先创建队伍）
            elif method_name == 'GetTeamInfo' and service_name == 'room':
                # 生成带前置条件的测试代码
                content += f'''
    def {test_method_name}(self):
        """测试 {method_name} 接口（前置条件：先创建队伍）"""
        # 前置条件：先创建队伍
        create_result = self.client.call_rpc(
            service='Room',
            method='CreateTeam',
            request_data={{'game_mode': 1}}
        )
        
        if not create_result.get('success'):
            self.skipTest(f"前置条件失败：无法创建队伍 - {{create_result.get('error_message', '未知错误')}}")
        
        # 从创建队伍的响应中获取 team_id
        create_response = create_result.get('response', {{}})
        team_id = 0
        if 'createteam' in create_response:
            team_info = create_response['createteam'].get('team_info', {{}})
            team_id = team_info.get('team_id', 0)
        
        if team_id == 0:
            self.skipTest("前置条件失败：无法获取有效的 team_id")
        
        # 使用获取到的 team_id 调用 GetTeamInfo
        request_data = {{'team_id': team_id}}
        
        result = self.client.call_rpc(
            service='Room',
            method='{method_name}',
            request_data=request_data
        )
        
        # 保存测试结果用于报告
        self.test_result = {{
            'name': '{method_name}',
            'method': '{method_name}',
            'request': request_data,
            'response': result,  # 保存完整的result，包括success、response、error_code、error_message
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': []
        }}
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\\n{'='*60}")
        print(f"测试接口: {method_name}")
        print(f"请求参数: {{safe_json_dumps(request_data)}}")
        print(f"响应数据: {{safe_json_dumps(result.get('response', {{}}))}}")
        print(f"响应码: {{result.get('error_code', 200)}}")
        if result.get('error_message'):
            print(f"错误信息: {{result.get('error_message')}}")
        print(f"{'='*60}")
        
        # 断言
        if not result.get('success', False):
            error_msg = result.get('error_message', '未知错误')
            print(f"\\n✗ {method_name} 测试失败: {{error_msg}}")
            self.assertTrue(False, f"API调用失败: {{error_msg}}")
        else:
            print(f"\\n✓ {method_name} 测试通过")
'''
                should_generate_generic = False
                # 注意：不要continue，让异常测试用例生成代码执行
            # 特殊处理：Match 需要前置条件（先创建队伍）
            elif method_name == 'Match' and service_name == 'room':
                # 生成带前置条件的测试代码
                content += f'''
    def {test_method_name}(self):
        """测试 {method_name} 接口（前置条件：先创建队伍）"""
        # 前置条件：先创建队伍
        create_result = self.client.call_rpc(
            service='Room',
            method='CreateTeam',
            request_data={{'game_mode': 1}}
        )
        
        if not create_result.get('success'):
            self.skipTest(f"前置条件失败：无法创建队伍 - {{create_result.get('error_message', '未知错误')}}")
        
        # 从创建队伍的响应中获取 team_id
        create_response = create_result.get('response', {{}})
        team_id = 0
        if 'createteam' in create_response:
            team_info = create_response['createteam'].get('team_info', {{}})
            team_id = team_info.get('team_id', 0)
        
        if team_id == 0:
            self.skipTest("前置条件失败：无法获取有效的 team_id")
        
        # 使用获取到的 team_id 调用 Match（需要 map_id）
        request_data = {{'team_id': team_id, 'map_id': 1}}
        
        result = self.client.call_rpc(
            service='Room',
            method='{method_name}',
            request_data=request_data
        )
        
        # 保存测试结果用于报告
        self.test_result = {{
            'name': '{method_name}',
            'method': '{method_name}',
            'request': request_data,
            'response': result,  # 保存完整的result，包括success、response、error_code、error_message
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': []
        }}
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\\n{'='*60}")
        print(f"测试接口: {method_name}")
        print(f"请求参数: {{safe_json_dumps(request_data)}}")
        print(f"响应数据: {{safe_json_dumps(result.get('response', {{}}))}}")
        print(f"响应码: {{result.get('error_code', 200)}}")
        if result.get('error_message'):
            print(f"错误信息: {{result.get('error_message')}}")
        print(f"{'='*60}")
        
        # 断言
        if not result.get('success', False):
            error_msg = result.get('error_message', '未知错误')
            print(f"\\n✗ {method_name} 测试失败: {{error_msg}}")
            self.assertTrue(False, f"API调用失败: {{error_msg}}")
        else:
            print(f"\\n✓ {method_name} 测试通过")
'''
                should_generate_generic = False
                # 注意：不要continue，让异常测试用例生成代码执行
            # 特殊处理：StartGameFromTeam 需要前置条件（先创建队伍）
            # 暂时注释掉 StartGameFromTeam 接口测试
            elif False and method_name == 'StartGameFromTeam' and service_name == 'room':
                # 生成带前置条件的测试代码
                content += f'''
    def {test_method_name}(self):
        """测试 {method_name} 接口（前置条件：先创建队伍）"""
        # 前置条件：先创建队伍
        create_result = self.client.call_rpc(
            service='Room',
            method='CreateTeam',
            request_data={{'game_mode': 1}}
        )
        
        if not create_result.get('success'):
            self.skipTest(f"前置条件失败：无法创建队伍 - {{create_result.get('error_message', '未知错误')}}")
        
        # 从创建队伍的响应中获取 team_id
        create_response = create_result.get('response', {{}})
        team_id = 0
        if 'createteam' in create_response:
            team_info = create_response['createteam'].get('team_info', {{}})
            team_id = team_info.get('team_id', 0)
        
        if team_id == 0:
            self.skipTest("前置条件失败：无法获取有效的 team_id")
        
        # 使用获取到的 team_id 调用 StartGameFromTeam（需要 map_id）
        request_data = {{'team_id': team_id, 'map_id': 1}}
        
        result = self.client.call_rpc(
            service='Room',
            method='{method_name}',
            request_data=request_data
        )
        
        # 保存测试结果用于报告
        self.test_result = {{
            'name': '{method_name}',
            'method': '{method_name}',
            'request': request_data,
            'response': result,  # 保存完整的result，包括success、response、error_code、error_message
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': []
        }}
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\\n{'='*60}")
        print(f"测试接口: {method_name}")
        print(f"请求参数: {{safe_json_dumps(request_data)}}")
        print(f"响应数据: {{safe_json_dumps(result.get('response', {{}}))}}")
        print(f"响应码: {{result.get('error_code', 200)}}")
        if result.get('error_message'):
            print(f"错误信息: {{result.get('error_message')}}")
        print(f"{'='*60}")
        
        # 断言
        if not result.get('success', False):
            error_msg = result.get('error_message', '未知错误')
            print(f"\\n✗ {method_name} 测试失败: {{error_msg}}")
            self.assertTrue(False, f"API调用失败: {{error_msg}}")
        else:
            print(f"\\n✓ {method_name} 测试通过")
'''
                should_generate_generic = False
                # 注意：不要continue，让异常测试用例生成代码执行
            # 特殊处理：GetGameInfo 需要前置条件（先创建队伍并开始游戏）
            elif method_name == 'GetGameInfo' and service_name == 'room':
                # 生成带前置条件的测试代码
                content += f'''
    def {test_method_name}(self):
        """测试 {method_name} 接口（前置条件：先创建队伍并开始游戏）"""
        # 前置条件1：先创建队伍
        create_result = self.client.call_rpc(
            service='Room',
            method='CreateTeam',
            request_data={{'game_mode': 1}}
        )
        
        if not create_result.get('success'):
            self.skipTest(f"前置条件失败：无法创建队伍 - {{create_result.get('error_message', '未知错误')}}")
        
        # 从创建队伍的响应中获取 team_id
        create_response = create_result.get('response', {{}})
        team_id = 0
        if 'createteam' in create_response:
            team_info = create_response['createteam'].get('team_info', {{}})
            team_id = team_info.get('team_id', 0)
        
        if team_id == 0:
            self.skipTest("前置条件失败：无法获取有效的 team_id")
        
        # 前置条件2：开始游戏（获取 game_id）
        start_game_result = self.client.call_rpc(
            service='Room',
            method='StartGameFromTeam',
            request_data={{'team_id': team_id, 'map_id': 1}}
        )
        
        if not start_game_result.get('success'):
            self.skipTest(f"前置条件失败：无法开始游戏 - {{start_game_result.get('error_message', '未知错误')}}")
        
        # 从开始游戏的响应中获取 game_id（需要通过 GetUserState 获取）
        user_state_result = self.client.call_rpc('Room', 'GetUserState', {{}})
        game_id = 0
        if user_state_result.get('success'):
            user_state = user_state_result.get('response', {{}})
            if 'getuserstate' in user_state:
                game_id = user_state['getuserstate'].get('game_id', 0)
        
        if game_id == 0:
            self.skipTest("前置条件失败：无法获取有效的 game_id")
        
        # 使用获取到的 game_id 调用 GetGameInfo
        request_data = {{'game_id': game_id}}
        
        result = self.client.call_rpc(
            service='Room',
            method='{method_name}',
            request_data=request_data
        )
        
        # 保存测试结果用于报告
        self.test_result = {{
            'name': '{method_name}',
            'method': '{method_name}',
            'request': request_data,
            'response': result,  # 保存完整的result，包括success、response、error_code、error_message
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': []
        }}
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\\n{'='*60}")
        print(f"测试接口: {method_name}")
        print(f"请求参数: {{safe_json_dumps(request_data)}}")
        print(f"响应数据: {{safe_json_dumps(result.get('response', {{}}))}}")
        print(f"响应码: {{result.get('error_code', 200)}}")
        if result.get('error_message'):
            print(f"错误信息: {{result.get('error_message')}}")
        print(f"{'='*60}")
        
        # 断言
        if not result.get('success', False):
            error_msg = result.get('error_message', '未知错误')
            print(f"\\n✗ {method_name} 测试失败: {{error_msg}}")
            self.assertTrue(False, f"API调用失败: {{error_msg}}")
        else:
            print(f"\\n✓ {method_name} 测试通过")
'''
                should_generate_generic = False
                # 注意：不要continue，让异常测试用例生成代码执行
            # 特殊处理：ChangeReadyState 需要前置条件（先创建队伍）
            elif method_name == 'ChangeReadyState' and service_name == 'room':
                # 生成带前置条件的测试代码
                content += f'''
    def {test_method_name}(self):
        """测试 {method_name} 接口（前置条件：先创建队伍）"""
        # 前置条件：先创建队伍
        create_result = self.client.call_rpc(
            service='Room',
            method='CreateTeam',
            request_data={{'game_mode': 1}}
        )
        
        if not create_result.get('success'):
            self.skipTest(f"前置条件失败：无法创建队伍 - {{create_result.get('error_message', '未知错误')}}")
        
        # 从创建队伍的响应中获取 team_id
        create_response = create_result.get('response', {{}})
        team_id = 0
        if 'createteam' in create_response:
            team_info = create_response['createteam'].get('team_info', {{}})
            team_id = team_info.get('team_id', 0)
        
        if team_id == 0:
            self.skipTest("前置条件失败：无法获取有效的 team_id")
        
        # 使用获取到的 team_id 调用 ChangeReadyState（设置为准备状态）
        request_data = {{'team_id': team_id, 'ready': True}}
        
        result = self.client.call_rpc(
            service='Room',
            method='{method_name}',
            request_data=request_data
        )
        
        # 保存测试结果用于报告
        self.test_result = {{
            'name': '{method_name}',
            'method': '{method_name}',
            'request': request_data,
            'response': result,  # 保存完整的result，包括success、response、error_code、error_message
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': []
        }}
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\\n{'='*60}")
        print(f"测试接口: {method_name}")
        print(f"请求参数: {{safe_json_dumps(request_data)}}")
        print(f"响应数据: {{safe_json_dumps(result.get('response', {{}}))}}")
        print(f"响应码: {{result.get('error_code', 200)}}")
        if result.get('error_message'):
            print(f"错误信息: {{result.get('error_message')}}")
        print(f"{'='*60}")
        
        # 断言
        if not result.get('success', False):
            error_msg = result.get('error_message', '未知错误')
            print(f"\\n✗ {method_name} 测试失败: {{error_msg}}")
            self.assertTrue(False, f"API调用失败: {{error_msg}}")
        else:
            print(f"\\n✓ {method_name} 测试通过")
'''
                should_generate_generic = False
                # 注意：不要continue，让异常测试用例生成代码执行
            # 特殊处理：LeaveTeam 需要前置条件（先创建或加入队伍）
            elif method_name == 'LeaveTeam' and service_name == 'room':
                # 生成带前置条件的测试代码
                content += f'''
    def {test_method_name}(self):
        """测试 {method_name} 接口（前置条件：先创建队伍）"""
        # 前置条件：先创建队伍
        create_result = self.client.call_rpc(
            service='Room',
            method='CreateTeam',
            request_data={{'game_mode': 1}}
        )
        
        if not create_result.get('success'):
            self.skipTest(f"前置条件失败：无法创建队伍 - {{create_result.get('error_message', '未知错误')}}")
        
        # 从创建队伍的响应中获取 team_id
        create_response = create_result.get('response', {{}})
        team_id = 0
        if 'createteam' in create_response:
            team_info = create_response['createteam'].get('team_info', {{}})
            team_id = team_info.get('team_id', 0)
        
        if team_id == 0:
            self.skipTest("前置条件失败：无法获取有效的 team_id")
        
        # 使用获取到的 team_id 调用 LeaveTeam
        request_data = {{'team_id': team_id}}
        
        result = self.client.call_rpc(
            service='Room',
            method='LeaveTeam',
            request_data=request_data
        )
        
        # 保存测试结果用于报告
        self.test_result = {{
            'name': '{method_name}',
            'method': '{method_name}',
            'request': request_data,
            'response': result,  # 保存完整的result，包括success、response、error_code、error_message
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': []
        }}
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\\n{'='*60}")
        print(f"测试接口: {method_name}")
        print(f"请求参数: {{safe_json_dumps(request_data)}}")
        print(f"响应数据: {{safe_json_dumps(result.get('response', {{}}))}}")
        print(f"响应码: {{result.get('error_code', 200)}}")
        if result.get('error_message'):
            print(f"错误信息: {{result.get('error_message')}}")
        print(f"{'='*60}")
        
        # 断言
        if not result.get('success', False):
            error_msg = result.get('error_message', '未知错误')
            print(f"\\n✗ {method_name} 测试失败: {{error_msg}}")
            self.assertTrue(False, f"API调用失败: {{error_msg}}")
        else:
            print(f"\\n✓ {method_name} 测试通过")
'''
            
            # 如果没有特殊处理，则生成通用测试代码（在 if normal_test_case 块内，但在所有特殊处理之后）
            if normal_test_case and should_generate_generic:
                content += f'''
    def {test_method_name}(self):
        """测试 {method_name} 接口"""
        request_data = {request_data_str}
        
        result = self.client.call_rpc(
            service='{service_cap}',
            method='{method_name}',
            request_data=request_data
        )
        
        # 保存测试结果用于报告
        self.test_result = {{
            'name': '{method_name}',
            'method': '{method_name}',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': []
        }}
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\\n{{'='*60}}")
        print(f"测试接口: {method_name}")
        print(f"请求参数: {{safe_json_dumps(request_data)}}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {{safe_json_dumps(result)}}")
        print(f"响应数据: {{safe_json_dumps(result.get('response', {{}}))}}")
        print(f"响应码: {{result.get('error_code', 200)}}")
        if result.get('error_message'):
            print(f"错误信息: {{result.get('error_message')}}")
        print(f"{{'='*60}}")
        
        # 断言
        if not result.get('success', False):
            error_msg = result.get('error_message', '未知错误')
            print(f"\\n✗ {method_name} 测试失败: {{error_msg}}")
            self.assertTrue(False, f"API调用失败: {{error_msg}}")
        else:
            print(f"\\n✓ {method_name} 测试通过")
'''
        
            # 生成异常测试用例（在正常测试用例之后，无论是否有正常测试用例）
            # 注意：异常测试用例的生成应该在 if normal_test_case 块之外，确保即使没有正常测试用例也能生成
            # 将异常测试用例生成移到 if normal_test_case 块外，确保所有接口的异常测试用例都被生成
            for abnormal_case_name, abnormal_case_data in abnormal_test_cases.items():
                # 提取异常类型（参数异常_必填参数缺失 -> 参数异常_必填参数缺失）
                abnormal_type = abnormal_case_name.replace(f"{method_name}_", "")
                # 生成测试方法名：test_fetchselffulluserinfo_参数异常_必填参数缺失
                abnormal_test_method_name = f"test_{method_name.lower()}_{abnormal_type.lower().replace(' ', '_')}"
                abnormal_request_data_raw = abnormal_case_data.get('request', {})
                # 转换YAML格式的请求数据（{"value": ..., "type": ...}）为实际值
                abnormal_request_data = RequestDataConverter.convert_nested_request_data(abnormal_request_data_raw)
                expected_status = abnormal_case_data.get('expected_status', '400/500')
                dimension = abnormal_case_data.get('dimension', '参数异常')
                
                # 格式化请求数据
                if abnormal_request_data:
                    abnormal_request_data_str = repr(abnormal_request_data)
                else:
                    abnormal_request_data_str = "{}"
                
                content += f'''
    def {abnormal_test_method_name}(self):
        """测试 {method_name} 接口 - {dimension} - {abnormal_type}"""
        request_data = {abnormal_request_data_str}
        
        result = self.client.call_rpc(
            service='{service_cap}',
            method='{method_name}',
            request_data=request_data
        )
        
        # 保存测试结果用于报告（包含维度信息）
        self.test_result = {{
            'name': '{abnormal_case_name}',
            'method': '{method_name}',
            'dimension': '{dimension}',
            'abnormal_type': '{abnormal_type}',
            'request': request_data,
            'response': result,
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': [],
            'expected_status': '{expected_status}'
        }}
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\\n{{'='*60}}")
        print(f"测试接口: {method_name} - {dimension} - {abnormal_type}")
        print(f"请求参数: {{safe_json_dumps(request_data)}}")
        # 打印完整的服务器返回结果
        print(f"服务器返回结果: {{safe_json_dumps(result)}}")
        print(f"响应数据: {{safe_json_dumps(result.get('response', {{}}))}}")
        print(f"响应码: {{result.get('error_code', 200)}}")
        if result.get('error_message'):
            print(f"错误信息: {{result.get('error_message')}}")
        print(f"{{'='*60}}")
        
        # 异常测试用例的断言：如果返回了预期的错误码（非200），则认为通过
        error_code = result.get('error_code', 200)
        if error_code != 200:
            # 返回了错误码，符合预期
            print(f"\\n✓ {method_name} 异常测试通过: 返回预期错误码 {{error_code}}")
        else:
            # 返回了200，不符合预期（异常测试应该返回错误）
            error_msg = result.get('error_message', '未知错误')
            print(f"\\n✗ {method_name} 异常测试失败: 预期返回错误码，但返回了200")
            self.assertTrue(False, f"异常测试失败: 预期返回错误码，但返回了200 - {{error_msg}}")
'''
        
        # 在所有接口处理完成后，添加文件结尾（在循环外，但在方法内）
        content += '''
if __name__ == '__main__':
    unittest.main()
'''
        
        # 写入文件（在所有接口处理完成后，在循环外，但在方法内）
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

