"""
pytest测试代码生成器 - 根据接口定义和YAML测试用例生成pytest格式的测试代码（PO模式）
"""
import os
import yaml
import json
from typing import Dict, List, Any


class PytestTestGenerator:
    """pytest测试代码生成器（PO模式）"""
    
    def __init__(self, config):
        self.config = config
        self.output_dir = config.get_test_output_dir()
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_all_tests(self, interfaces: Dict[str, List[Dict]]):
        """生成所有服务的测试代码"""
        print("=" * 80)
        print("生成pytest测试代码（PO模式）...")
        print("=" * 80)
        
        for service_name, service_interfaces in interfaces.items():
            self._generate_service_tests(service_name, service_interfaces)
        
        print("✓ pytest测试代码生成完成")
    
    def _generate_service_tests(self, service_name: str, interfaces: List[Dict]):
        """生成单个服务的测试代码"""
        # 加载YAML测试用例
        yaml_file = f"test_cases/{service_name}/test_{service_name}.yaml"
        test_cases = self._load_test_cases(yaml_file)
        
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
        """写入测试文件（pytest格式，PO模式）"""
        service_cap = service_name.capitalize()
        page_name = f"{service_name}_page"
        
        content = f'''"""
自动生成的{service_cap}服务测试代码（pytest + PO模式）
"""
import pytest
import sys
import os
import json

# 添加框架路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


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


# pytest标记
pytestmark = [pytest.mark.{service_name}]

'''
        
        # 为每个接口生成测试方法
        for interface in interfaces:
            method_name = interface['name']
            
            # 获取正常测试用例
            normal_test_case = test_cases.get('test_cases', {}).get(method_name, {})
            if not normal_test_case:
                normal_test_case = test_cases.get('test_cases', {}).get(f"{method_name}_正常", {})
            
            # 获取所有异常测试用例
            abnormal_test_cases = {}
            for test_case_name, test_case_data in test_cases.get('test_cases', {}).items():
                if test_case_name.startswith(f"{method_name}_") and test_case_name != f"{method_name}_正常":
                    dimension = test_case_data.get('dimension', '')
                    if dimension and dimension != '正常':
                        abnormal_test_cases[test_case_name] = test_case_data
            
            # 生成正常测试用例
            if normal_test_case:
                test_method_name = f"test_{method_name.lower()}"
                request_data = normal_test_case.get('request', {})
                
                # 生成测试方法（使用PO模式）
                content += self._generate_test_method(
                    service_name, method_name, test_method_name, 
                    request_data, normal_test_case, page_name, '正常'
                )
            
            # 生成异常测试用例
            for abnormal_case_name, abnormal_case_data in abnormal_test_cases.items():
                # 提取异常类型（例如：参数异常_必填参数缺失）
                abnormal_type = abnormal_case_name.replace(f"{method_name}_", "")
                test_method_name = f"test_{method_name.lower()}_{abnormal_type.lower().replace(' ', '_')}"
                request_data = abnormal_case_data.get('request', {})
                expected_status = abnormal_case_data.get('expected_status', '400/500')
                
                content += self._generate_test_method(
                    service_name, method_name, test_method_name,
                    request_data, abnormal_case_data, page_name, 
                    abnormal_case_data.get('dimension', '异常'),
                    expected_status=expected_status
                )
        
        # 写入文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _generate_test_method(self, service_name: str, method_name: str, test_method_name: str,
                             request_data: Dict, test_case: Dict, page_name: str, 
                             dimension: str, expected_status: str = '200') -> str:
        """生成单个测试方法（pytest格式，PO模式）"""
        
        # 根据服务名和方法名确定使用哪个页面对象方法
        page_method_name = self._get_page_method_name(method_name)
        
        # 处理特殊前置条件
        preconditions_code = self._generate_preconditions(service_name, method_name, page_name)
        
        # 构建请求数据代码
        request_data_code = self._build_request_data_code(service_name, method_name, request_data, page_name)
        
        # 构建调用代码
        call_code = self._build_call_code(service_name, method_name, page_method_name, request_data_code, page_name)
        
        # 构建断言代码
        assertion_code = self._build_assertion_code(method_name, dimension, expected_status)
        
        method_content = f'''
@pytest.mark.normal
def {test_method_name}({page_name}, current_uid):
    """
    测试 {method_name} 接口
    维度: {dimension}
    预期状态: {expected_status}
    """
{preconditions_code}
    # 准备请求数据
{request_data_code}
    
    # 调用API（使用PO模式）
{call_code}
    
    # 保存测试结果用于报告
    test_result = {{
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
    print(f"\\n{{'='*60}}")
    print(f"测试接口: {method_name}")
    print(f"请求参数: {{safe_json_dumps(request_data)}}")
    print(f"响应数据: {{safe_json_dumps(result.get('response', {{}}))}}")
    print(f"响应码: {{result.get('error_code', 200)}}")
    if result.get('error_message'):
        print(f"错误信息: {{result.get('error_message')}}")
    print(f"{{'='*60}}")
    
    # 断言
{assertion_code}
'''
        return method_content
    
    def _get_page_method_name(self, method_name: str) -> str:
        """将方法名转换为页面对象方法名（驼峰命名）"""
        # 例如：FetchSelfFullUserInfo -> fetch_self_full_user_info
        import re
        # 在大写字母前插入下划线，然后转小写
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', method_name)
        s2 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1)
        return s2.lower()
    
    def _generate_preconditions(self, service_name: str, method_name: str, page_name: str) -> str:
        """生成前置条件代码"""
        if service_name == 'social' and method_name in ['DeleteMsg', 'AddReaction', 'RemoveReaction', 'GetReactions', 'RevokeMsg']:
            return f'''    # 前置条件：先发送消息获取 conv_id 和 seq
    conv_id, seq = {page_name}.send_world_chat_message("test message")
    if not conv_id or seq == 0:
        pytest.skip("前置条件失败：无法获取有效的 conv_id 和 seq")
'''
        elif service_name == 'social' and method_name == 'PullMsgs':
            return f'''    # 前置条件：先发送消息获取 conv_id
    conv_id, seq = {page_name}.send_world_chat_message("test message")
    if not conv_id:
        pytest.skip("前置条件失败：无法获取有效的 conv_id")
'''
        elif service_name == 'social' and method_name == 'Follow':
            return f'''    # 前置条件：使用有效的 target_uid（不能是自己）
    target_uid = current_uid + 1 if current_uid else 10000001
'''
        elif service_name == 'social' and method_name == 'Unfollow':
            return f'''    # 前置条件：先关注，然后取消关注
    target_uid = current_uid + 1 if current_uid else 10000001
    # 先关注
    follow_result = {page_name}.follow(target_uid)
    if not {page_name}.is_success(follow_result):
        pytest.skip(f"前置条件失败：无法关注用户 - {{follow_result.get('error_message', '未知错误')}}")
'''
        elif service_name == 'room' and method_name == 'LeaveTeam':
            return f'''    # 前置条件：先创建队伍
    from framework.pages import RoomPage
    room_page = RoomPage({page_name}.client)
    create_result = room_page.create_team(game_mode=1)
    if not room_page.is_success(create_result):
        pytest.skip(f"前置条件失败：无法创建队伍 - {{create_result.get('error_message', '未知错误')}}")
    # 获取 team_id
    response = room_page.get_response(create_result)
    team_id = None
    if 'createteam' in response:
        team_info = response['createteam']
        if 'team_info' in team_info:
            team_id = team_info['team_info'].get('team_id')
'''
        return "    # 无特殊前置条件\n"
    
    def _build_request_data_code(self, service_name: str, method_name: str, 
                                 request_data: Dict, page_name: str) -> str:
        """构建请求数据代码"""
        if method_name == 'FetchSimpleUserInfo' and not request_data.get('target_uid'):
            return "    request_data = {'target_uid': current_uid if current_uid else 10000001}"
        elif service_name == 'social' and method_name in ['DeleteMsg', 'AddReaction', 'RemoveReaction', 'GetReactions', 'RevokeMsg']:
            if method_name == 'DeleteMsg':
                return "    request_data = {'conv_id': conv_id, 'seqs': [seq]}"
            else:
                return "    request_data = {'conv_id': conv_id, 'seq': seq}"
        elif service_name == 'social' and method_name == 'PullMsgs':
            return "    request_data = {'conv_id': conv_id, 'start_seq': 0, 'count': 20, 'reverse': False}"
        elif service_name == 'social' and method_name == 'Follow':
            return "    request_data = {'target_uid': target_uid}"
        elif service_name == 'social' and method_name == 'Unfollow':
            return "    request_data = {'target_uid': target_uid}"
        else:
            # 使用YAML中的请求数据
            request_data_str = repr(request_data)
            return f"    request_data = {request_data_str}"
    
    def _build_call_code(self, service_name: str, method_name: str, page_method_name: str,
                        request_data_code: str, page_name: str) -> str:
        """构建API调用代码（使用PO模式）"""
        # 根据方法名确定调用方式
        if method_name == 'FetchSimpleUserInfo':
            return f"    result = {page_name}.fetch_simple_user_info(request_data=request_data)"
        elif method_name == 'UpdateNickname':
            nickname = request_data_code.split("'")[1] if "'" in request_data_code else "TestNickname"
            return f"    result = {page_name}.update_nickname(nickname='{nickname}', request_data=request_data)"
        else:
            # 使用通用调用方式
            return f"    result = {page_name}.call_api('{method_name}', request_data)"
    
    def _build_assertion_code(self, method_name: str, dimension: str, expected_status: str) -> str:
        """构建断言代码"""
        if dimension == '正常':
            return '''    # 正常用例：应该成功
    assert result.get('success', False), f"API调用失败: {result.get('error_message', '未知错误')}"
    assert result.get('error_code', 0) == 200, f"预期状态码200，实际: {result.get('error_code', 0)}"
'''
        else:
            # 异常用例：根据expected_status判断
            if expected_status == '400/500':
                return '''    # 异常用例：应该返回错误
    assert not result.get('success', True), f"异常用例应该失败，但返回成功: {result.get('error_message', '')}"
    assert result.get('error_code', 0) != 200, f"异常用例不应该返回200，实际: {result.get('error_code', 0)}"
'''
            else:
                # 特定错误码
                try:
                    expected_code = int(expected_status)
                    return f'''    # 异常用例：应该返回特定错误码
    assert result.get('error_code', 0) == {expected_code}, f"预期状态码{expected_code}，实际: {{result.get('error_code', 0)}}"
'''
                except:
                    return '''    # 异常用例：应该返回错误
    assert not result.get('success', True), f"异常用例应该失败，但返回成功: {result.get('error_message', '')}"
'''



