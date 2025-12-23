#!/usr/bin/env python3
"""
YAML测试用例生成器 - 按五维度生成YAML格式的测试用例
"""
import os
import yaml
from typing import Dict, List, Any
from framework.config import Config
from framework.protobuf_parser import ProtobufParser
from framework.proto_request_formatter import ProtoRequestFormatter
from framework.base_test_case_generator import BaseTestCaseGenerator


class YamlTestCaseGenerator(BaseTestCaseGenerator):
    """YAML测试用例生成器"""
    
    def __init__(self, config: Config):
        super().__init__(config)
        self.test_cases_dir = "test_cases"
    
    def generate_yaml_test_cases(self):
        """生成YAML格式的测试用例"""
        print("=" * 80)
        print("生成YAML测试用例...")
        print("=" * 80)
        
        # 解析接口
        parser = ProtobufParser(self.config)
        interfaces = parser.discover_interfaces()
        
        # 为每个服务生成YAML测试用例
        for service_name, service_interfaces in interfaces.items():
            print(f"\n处理服务: {service_name}")
            self._generate_service_yaml(service_name, service_interfaces)
        
        print("\n" + "=" * 80)
        print("✓ YAML测试用例生成完成")
        print("=" * 80)
    
    def _generate_service_yaml(self, service_name: str, interfaces: List[Dict]):
        """为单个服务生成YAML测试用例"""
        # 创建服务目录
        service_dir = os.path.join(self.test_cases_dir, service_name)
        os.makedirs(service_dir, exist_ok=True)
        
        # 生成测试用例数据
        test_cases_data = {
            'test_cases': {}
        }
        
        for interface in interfaces:
            method_name = interface['name']
            print(f"  生成接口测试用例: {method_name}")
            
            # 获取请求结构
            service_name_cap = service_name.capitalize()
            request_structure = ProtoRequestFormatter.get_request_structure(service_name_cap, method_name)
            if request_structure is None:
                request_structure = {}
            
            # 生成五维度测试用例
            cases = self._generate_five_dimension_cases(
                service_name, method_name, request_structure
            )
            
            # 添加到test_cases_data
            for case in cases:
                case_key = self._get_case_key(method_name, case['dimension'], case.get('abnormal_type'))
                test_cases_data['test_cases'][case_key] = {
                    'description': case['title'],
                    'priority': case['priority'],
                    'preconditions': case.get('preconditions', '已登录'),
                    'dimension': case['dimension'],
                    'request': self._parse_request_body(case['request_body']),
                    'expected_status': case['expected_status'],
                    'expected_response': self._parse_response(case.get('server_response', '')),
                    'jsonpath_assertion': case.get('jsonpath_assertion', ''),
                    'db_check': case.get('db_check', ''),
                    'remark': case.get('remark', '')
                }
        
        # 保存YAML文件
        yaml_file = os.path.join(service_dir, f"test_{service_name}.yaml")
        with open(yaml_file, 'w', encoding='utf-8') as f:
            yaml.dump(test_cases_data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
        
        print(f"✓ 生成 {service_name} 服务YAML: {yaml_file}")
    
    # _generate_five_dimension_cases 已在基类中实现，这里重写以添加日志
    def _generate_five_dimension_cases(self, service_name: str, method_name: str, 
                                       request_structure: Dict[str, str]) -> List[Dict]:
        """生成五维度测试用例（重写以添加日志）"""
        cases = []
        
        # 检查接口是否有参数（根据协议定义）
        has_parameters = bool(request_structure and len(request_structure) > 0)
        
        # 1. 正常用例（正例）
        cases.append(self._generate_normal_case(service_name, method_name, request_structure))
        
        # 2. 参数异常（5条高频反例）- 只有当接口有参数时才生成
        if has_parameters:
            cases.extend(self._generate_parameter_abnormal_cases(service_name, method_name, request_structure))
            print(f"    ✓ 生成参数异常测试用例（接口有 {len(request_structure)} 个参数）")
        else:
            print(f"    ⚠ 跳过参数异常测试用例（接口无参数，根据协议定义）")
        
        # 3. 业务异常
        cases.extend(self._generate_business_abnormal_cases(service_name, method_name, request_structure))
        
        # 4. 权限安全
        cases.extend(self._generate_security_cases(service_name, method_name, request_structure))
        
        # 5. 性能边界
        cases.extend(self._generate_performance_cases(service_name, method_name, request_structure))
        
        return cases
    
    def _generate_normal_case(self, service_name: str, method_name: str, 
                              request_structure: Dict[str, str]) -> Dict:
        """生成正常用例（正例）"""
        request_body = self._generate_normal_request_body(request_structure)
        expected_response = self._generate_expected_response(service_name, method_name, request_body, True)
        preconditions = self._get_preconditions(service_name, method_name)
        
        return {
            'title': f'{method_name}_正常调用',
            'priority': 'P0',
            'preconditions': preconditions,
            'dimension': '正常',
            'request_body': self._format_request_body_with_types(request_body, request_structure),
            'expected_status': '200',
            'server_response': expected_response,
            'jsonpath_assertion': '$.success == true && $.error_code == 200',
            'db_check': self._generate_db_check(method_name, True),
            'remark': '正常业务流程验证'
        }
    
    def _generate_parameter_abnormal_cases(self, service_name: str, method_name: str,
                                          request_structure: Dict[str, str]) -> List[Dict]:
        """生成参数异常用例（5条高频反例）"""
        cases = []
        abnormal_types = [
            ('必填参数缺失', 'missing_required'),
            ('参数类型错误', 'type_error'),
            ('参数值为空', 'empty_value'),
            ('参数值超出范围', 'out_of_range'),
            ('参数格式错误', 'format_error')
        ]
        
        for abnormal_name, abnormal_type in abnormal_types:
            request_body = self._generate_abnormal_request_body(request_structure, abnormal_type)
            expected_response = self._generate_expected_response(service_name, method_name, request_body, False)
            preconditions = self._get_preconditions(service_name, method_name)
            
            cases.append({
                'title': f'{method_name}_参数异常_{abnormal_name}',
                'priority': 'P1',
                'preconditions': preconditions,
                'dimension': '参数异常',
                'abnormal_type': abnormal_type,
                'request_body': self._format_request_body_with_types(request_body, request_structure),
                'expected_status': '400/500',
                'server_response': expected_response,
                'jsonpath_assertion': '$.error_code != 200',
                'db_check': '数据未变更',
                'remark': f'{abnormal_name}场景验证'
            })
        
        return cases
    
    def _generate_business_abnormal_cases(self, service_name: str, method_name: str,
                                         request_structure: Dict[str, str]) -> List[Dict]:
        """生成业务异常用例"""
        cases = []
        business_abnormal_scenarios = self._get_business_abnormal_scenarios(service_name, method_name)
        
        for scenario in business_abnormal_scenarios:
            request_body = self._generate_business_abnormal_request_body(request_structure, scenario)
            expected_response = self._generate_expected_response(service_name, method_name, request_body, False)
            preconditions = self._get_preconditions(service_name, method_name)
            
            cases.append({
                'title': f'{method_name}_业务异常_{scenario["name"]}',
                'priority': 'P1',
                'preconditions': preconditions,
                'dimension': '业务异常',
                'request_body': self._format_request_body_with_types(request_body, request_structure),
                'expected_status': scenario.get('expected_status', '400'),
                'server_response': expected_response,
                'jsonpath_assertion': scenario.get('jsonpath', '$.error_code != 200'),
                'db_check': scenario.get('db_check', '数据未变更'),
                'remark': scenario.get('remark', '业务异常场景验证')
            })
        
        return cases
    
    def _generate_security_cases(self, service_name: str, method_name: str,
                                request_structure: Dict[str, str]) -> List[Dict]:
        """生成权限安全用例"""
        cases = []
        
        security_scenarios = [
            {
                'name': '未授权访问',
                'request_body': {},
                'expected_status': '401',
                'jsonpath': '$.error_code == 401',
                'remark': 'token缺失或无效'
            },
            {
                'name': '越权访问',
                'request_body': self._generate_normal_request_body(request_structure),
                'expected_status': '403',
                'jsonpath': '$.error_code == 403',
                'remark': '无权限访问他人资源'
            }
        ]
        
        for scenario in security_scenarios:
            expected_response = self._generate_expected_response(service_name, method_name, scenario['request_body'], False)
            preconditions = '已登录' if scenario['name'] == '未授权访问' else self._get_preconditions(service_name, method_name)
            
            cases.append({
                'title': f'{method_name}_权限安全_{scenario["name"]}',
                'priority': 'P0',
                'preconditions': preconditions,
                'dimension': '权限安全',
                'request_body': self._format_request_body_with_types(scenario['request_body'], request_structure),
                'expected_status': scenario['expected_status'],
                'server_response': expected_response,
                'jsonpath_assertion': scenario['jsonpath'],
                'db_check': '数据未变更',
                'remark': scenario['remark']
            })
        
        return cases
    
    def _generate_performance_cases(self, service_name: str, method_name: str,
                                   request_structure: Dict[str, str]) -> List[Dict]:
        """生成性能边界用例"""
        cases = []
        
        performance_scenarios = [
            {
                'name': '大数据量',
                'request_body': self._generate_large_data_request(request_structure),
                'expected_status': '200/413',
                'jsonpath': '$.success == true || $.error_code == 413',
                'remark': '测试大数据量处理能力'
            },
            {
                'name': '并发请求',
                'request_body': self._generate_normal_request_body(request_structure),
                'expected_status': '200',
                'jsonpath': '$.success == true',
                'remark': '并发场景验证（需配合压测工具）'
            }
        ]
        
        for scenario in performance_scenarios:
            expected_response = self._generate_expected_response(service_name, method_name, scenario['request_body'], True)
            preconditions = self._get_preconditions(service_name, method_name)
            
            cases.append({
                'title': f'{method_name}_性能边界_{scenario["name"]}',
                'priority': 'P2',
                'preconditions': preconditions,
                'dimension': '性能边界',
                'request_body': self._format_request_body_with_types(scenario['request_body'], request_structure),
                'expected_status': scenario['expected_status'],
                'server_response': expected_response,
                'jsonpath_assertion': scenario['jsonpath'],
                'db_check': '性能指标正常',
                'remark': scenario['remark']
            })
        
        return cases
    
    def _get_case_key(self, method_name: str, dimension: str, abnormal_type: str = None) -> str:
        """生成用例键名"""
        if dimension == '正常':
            return f"{method_name}_正常"
        elif dimension == '参数异常' and abnormal_type:
            type_map = {
                'missing_required': '必填参数缺失',
                'type_error': '参数类型错误',
                'empty_value': '参数值为空',
                'out_of_range': '参数值超出范围',
                'format_error': '参数格式错误'
            }
            return f"{method_name}_参数异常_{type_map.get(abnormal_type, abnormal_type)}"
        else:
            return f"{method_name}_{dimension}"
    
    def _parse_request_body(self, request_body_str: str) -> Dict:
        """解析请求体字符串为字典"""
        import json
        try:
            return json.loads(request_body_str)
        except:
            return {}
    
    def _parse_response(self, response_str: str) -> Dict:
        """解析响应字符串为字典"""
        import json
        try:
            return json.loads(response_str)
        except:
            return {}
    
    def _generate_normal_request_body(self, request_structure: Dict[str, str]) -> Dict:
        """生成正常请求体"""
        body = {}
        if not request_structure:
            return body
        for field_name, field_type in request_structure.items():
            body[field_name] = self._generate_normal_value(field_name, field_type)
        return body
    
    def _generate_normal_value(self, field_name: str, field_type: str) -> Any:
        """根据字段类型生成正常值"""
        field_lower = field_name.lower()
        type_lower = field_type.lower()
        
        if 'id' in field_lower:
            if 'team' in field_lower:
                return 1006329
            elif 'game' in field_lower:
                return 1001
            elif 'item' in field_lower or 'unique' in field_lower:
                return 1
            else:
                return 10000263
        elif 'uid' in field_lower:
            return 10000263
        elif 'name' in field_lower or 'nickname' in field_lower:
            return "TestName_123"
        elif 'count' in field_lower or 'limit' in field_lower:
            return 20
        elif 'offset' in field_lower:
            return 0
        elif 'seq' in field_lower:
            return 1
        elif 'scene' in field_lower:
            return 4
        elif 'ready' in field_lower or 'ready_state' in field_lower:
            return True
        elif 'map' in field_lower and 'id' in field_lower:
            return 1
        elif 'bool' in type_lower or 'boolean' in type_lower:
            return True
        elif 'int' in type_lower or 'int32' in type_lower or 'int64' in type_lower:
            return 1
        elif 'string' in type_lower:
            if 'conv' in field_lower:
                return "w_default"
            elif 'content' in field_lower or 'text' in field_lower:
                return "test message"
            else:
                return "test_value"
        elif 'repeated' in type_lower:
            return []
        else:
            return None
    
    def _generate_abnormal_request_body(self, request_structure: Dict[str, str], 
                                       abnormal_type: str) -> Dict:
        """生成异常请求体"""
        if not request_structure:
            return {}
        
        first_field = list(request_structure.keys())[0]
        first_type = request_structure[first_field]
        
        body = self._generate_normal_request_body(request_structure)
        
        if abnormal_type == 'missing_required':
            del body[first_field]
        elif abnormal_type == 'type_error':
            if 'string' in first_type.lower():
                body[first_field] = 12345
            else:
                body[first_field] = "wrong_type"
        elif abnormal_type == 'empty_value':
            if 'string' in first_type.lower():
                body[first_field] = ""
            elif 'int' in first_type.lower():
                body[first_field] = 0
            else:
                body[first_field] = None
        elif abnormal_type == 'out_of_range':
            if 'int' in first_type.lower():
                body[first_field] = 999999999
            elif 'string' in first_type.lower():
                body[first_field] = "A" * 10000
        elif abnormal_type == 'format_error':
            if 'id' in first_field.lower() or 'uid' in first_field.lower():
                body[first_field] = -1
            else:
                body[first_field] = "invalid_format_@#$%"
        
        return body
    
    def _generate_business_abnormal_request_body(self, request_structure: Dict[str, str],
                                                  scenario: Dict) -> Dict:
        """生成业务异常请求体"""
        body = self._generate_normal_request_body(request_structure)
        if 'request_body' in scenario:
            body.update(scenario['request_body'])
        return body
    
    def _generate_large_data_request(self, request_structure: Dict[str, str]) -> Dict:
        """生成大数据量请求"""
        body = self._generate_normal_request_body(request_structure)
        for field_name, field_type in request_structure.items():
            if 'repeated' in field_type.lower() or 'list' in field_type.lower():
                body[field_name] = [i for i in range(1000)]
        return body
    
    # _get_business_abnormal_scenarios 已在基类中实现，这里重写以添加 db_check
    def _get_business_abnormal_scenarios(self, service_name: str, method_name: str) -> List[Dict]:
        """获取业务异常场景（重写以添加 db_check）"""
        scenarios = super()._get_business_abnormal_scenarios(service_name, method_name)
        # 为每个场景添加 db_check
        for scenario in scenarios:
            scenario['db_check'] = '数据未变更'
        return scenarios
    
    def _get_preconditions(self, service_name: str, method_name: str) -> str:
        """获取前置条件"""
        preconditions_map = {
            'hall': {
                'FetchSelfFullUserInfo': '已登录',
                'FetchSimpleUserInfo': '已登录',
                'UpdateNickname': '已登录',
                'SellItem': '已登录，背包中有物品',
                'BuyItem': '已登录，有足够现金',
                'StashToBackpack': '已登录，仓库中有物品，背包有空位',
                'BackpackToStash': '已登录，背包中有物品',
                'ExchangeBackpackItem': '已登录，背包中有至少2个物品',
            },
            'room': {
                'GetUserState': '已登录',
                'CreateTeam': '已登录',
                'JoinTeam': '已登录，存在可加入的队伍',
                'LeaveTeam': '已登录，已加入队伍',
                'GetTeamInfo': '已登录，已创建或加入队伍',
                'ChangeReadyState': '已登录，已创建或加入队伍',
                'StartGameFromTeam': '已登录，已创建队伍，所有成员已准备',
                'Match': '已登录，已创建队伍',
                'CancelMatch': '已登录，队伍正在匹配中',
                'GetGameInfo': '已登录，游戏已开始',
            },
            'social': {
                'SendMessage': '已登录',
                'PullMsgs': '已登录，存在会话',
                'RevokeMsg': '已登录，已发送消息',
                'DeleteMsg': '已登录，存在消息',
                'AddReaction': '已登录，存在消息',
                'RemoveReaction': '已登录，已添加反应',
                'GetReactions': '已登录，存在消息',
                'GetSingleChatConvList': '已登录',
                'MarkRead': '已登录，存在会话',
                'GetFansList': '已登录',
                'GetFollowList': '已登录',
                'GetFriendList': '已登录',
                'Follow': '已登录',
                'Unfollow': '已登录，已关注目标用户',
            }
        }
        
        service_preconditions = preconditions_map.get(service_name, {})
        return service_preconditions.get(method_name, '已登录')
    
    def _format_request_body_with_types(self, request_body: Dict, request_structure: Dict[str, str]) -> str:
        """格式化请求体，显示字段类型信息"""
        import json
        formatted_body = {}
        
        for field_name, field_type in request_structure.items():
            field_value = request_body.get(field_name)
            type_name = field_type.replace('repeated ', '')
            formatted_body[field_name] = {
                "value": field_value,
                "type": type_name
            }
        
        return json.dumps(formatted_body, indent=2, ensure_ascii=False)
    
    def _generate_expected_response(self, service_name: str, method_name: str, 
                                    request_body: Dict, is_success: bool) -> str:
        """生成预期的服务器返回"""
        import json
        if is_success:
            response_structure = {
                "success": True,
                "response": self._generate_success_response_data(service_name, method_name, request_body),
                "error_code": 200,
                "error_message": ""
            }
        else:
            response_structure = {
                "success": False,
                "response": {},
                "error_code": 400,
                "error_message": self._generate_error_message(service_name, method_name, request_body)
            }
        
        return json.dumps(response_structure, indent=2, ensure_ascii=False)
    
    def _generate_success_response_data(self, service_name: str, method_name: str, request_body: Dict) -> Dict:
        """生成成功响应的数据部分"""
        method_lower = method_name.lower()
        response_data = {}
        
        if service_name == 'hall':
            if method_name == 'FetchSelfFullUserInfo':
                response_data = {
                    "fetchselffulluserinfo": {
                        "full_user_info": {
                            "uid": 10000263,
                            "nickname": "TestName_123",
                            "cash": 10000,
                            "stash": {"items": []},
                            "backpack": {"cells": []}
                        }
                    }
                }
            elif method_name == 'UpdateNickname':
                response_data = {
                    "updatenickname": {
                        "nickname": request_body.get('nickname', 'TestName_123')
                    }
                }
            elif method_name == 'FetchSimpleUserInfo':
                response_data = {
                    "fetchsimpleuserinfo": {
                        "simple_user_info": {
                            "uid": request_body.get('target_uid', 10000263),
                            "nickname": "TestName_123"
                        }
                    }
                }
            else:
                response_data = {method_lower: {"success": True}}
        
        elif service_name == 'room':
            if method_name == 'CreateTeam':
                response_data = {
                    "createteam": {
                        "team_info": {
                            "team_id": 1006329,
                            "game_mode": request_body.get('game_mode', 1),
                            "members": []
                        }
                    }
                }
            elif method_name == 'GetTeamInfo':
                response_data = {
                    "getteaminfo": {
                        "team_info": {
                            "team_id": request_body.get('team_id', 1006329),
                            "game_mode": 1,
                            "members": []
                        }
                    }
                }
            elif method_name == 'GetUserState':
                response_data = {
                    "getuserstate": {
                        "in_team": True,
                        "team_id": 1006329,
                        "in_game": False,
                        "game_id": 0
                    }
                }
            else:
                response_data = {method_lower: {"success": True}}
        
        elif service_name == 'social':
            if method_name == 'SendMessage':
                response_data = {
                    "sendmessage": {
                        "conv_id": request_body.get('conv_id', 'w_default'),
                        "seq": 1,
                        "msg_id": "msg_123456"
                    }
                }
            elif method_name == 'PullMsgs':
                response_data = {
                    "pullmsgs": {
                        "messages": [],
                        "has_more": False
                    }
                }
            elif method_name == 'Follow':
                response_data = {
                    "follow": {
                        "success": True
                    }
                }
            else:
                response_data = {method_lower: {"success": True}}
        
        return response_data
    
    def _generate_error_message(self, service_name: str, method_name: str, request_body: Dict) -> str:
        """生成错误消息"""
        if not request_body:
            return "invalid request"
        
        for key, value in request_body.items():
            if value is None or value == "":
                return f"invalid {key}"
            if isinstance(value, int) and value < 0:
                return f"invalid {key}"
            if isinstance(value, str) and len(value) > 1000:
                return f"invalid {key}: value too long"
        
        if service_name == 'room' and 'team_id' in request_body:
            return "team not exist"
        elif service_name == 'social' and 'conv_id' in request_body:
            return "conv_id not found"
        elif service_name == 'hall' and 'target_uid' in request_body:
            return "user not exist"
        
        return "invalid request"
    
    def _generate_db_check(self, method_name: str, is_success: bool) -> str:
        """生成数据库校验"""
        if is_success:
            if 'Create' in method_name or 'Add' in method_name:
                return '数据库中存在新记录'
            elif 'Update' in method_name:
                return '数据库记录已更新'
            elif 'Delete' in method_name:
                return '数据库记录已删除'
            else:
                return '数据库状态正常'
        else:
            return '数据未变更'


def main():
    """主函数"""
    config = Config()
    generator = YamlTestCaseGenerator(config)
    generator.generate_yaml_test_cases()


if __name__ == '__main__':
    main()



