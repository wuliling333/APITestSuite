"""
测试用例生成器基类
提取公共的测试用例生成逻辑，消除代码重复
"""
from typing import Dict, List, Any
from abc import ABC, abstractmethod


class BaseTestCaseGenerator(ABC):
    """测试用例生成器基类"""
    
    def __init__(self, config):
        """初始化生成器"""
        self.config = config
        self.case_counter = 0
    
    def _generate_five_dimension_cases(self, service_name: str, method_name: str, 
                                       request_structure: Dict[str, str]) -> List[Dict]:
        """生成五维度测试用例
        
        Args:
            service_name: 服务名称
            method_name: 方法名称
            request_structure: 请求参数结构（从协议定义中获取）
        """
        cases = []
        
        # 检查接口是否有参数（根据协议定义）
        has_parameters = bool(request_structure and len(request_structure) > 0)
        
        # 1. 正常用例（正例）
        cases.append(self._generate_normal_case(service_name, method_name, request_structure))
        
        # 2. 参数异常（5条高频反例）- 只有当接口有参数时才生成
        if has_parameters:
            cases.extend(self._generate_parameter_abnormal_cases(service_name, method_name, request_structure))
        # 如果接口没有参数，跳过参数异常测试用例的生成
        
        # 3. 业务异常
        cases.extend(self._generate_business_abnormal_cases(service_name, method_name, request_structure))
        
        # 4. 权限安全
        cases.extend(self._generate_security_cases(service_name, method_name, request_structure))
        
        # 5. 性能边界
        cases.extend(self._generate_performance_cases(service_name, method_name, request_structure))
        
        return cases
    
    def _get_business_abnormal_scenarios(self, service_name: str, method_name: str) -> List[Dict]:
        """获取业务异常场景（统一实现）"""
        scenarios = []
        
        if service_name == 'hall':
            # UpdateNickname 只更新当前登录用户的昵称，不涉及其他资源，不需要"资源不存在"场景
            # FetchSimpleUserInfo 需要 target_uid，可以测试资源不存在
            if method_name == 'FetchSimpleUserInfo':
                scenarios.append({
                    'name': '资源不存在',
                    'request_body': {'target_uid': 999999999},
                    'expected_status': '400',
                    'jsonpath': '$.error_code != 200',
                    'remark': '查询不存在的用户'
                })
            # 其他 Update/Delete 操作如果有 target_uid 参数，可以测试资源不存在
            elif ('Update' in method_name or 'Delete' in method_name) and method_name != 'UpdateNickname':
                scenarios.append({
                    'name': '资源不存在',
                    'request_body': {'target_uid': 999999999},
                    'expected_status': '404',
                    'jsonpath': '$.error_code == 404',
                    'remark': '操作不存在的资源'
                })
        
        elif service_name == 'room':
            if 'Team' in method_name or 'Join' in method_name:
                scenarios.append({
                    'name': '队伍不存在',
                    'request_body': {'team_id': 999999999},
                    'expected_status': '400',
                    'jsonpath': '$.error_message contains "team not exist"',
                    'remark': '操作不存在的队伍'
                })
        
        elif service_name == 'social':
            if 'Message' in method_name:
                scenarios.append({
                    'name': '会话不存在',
                    'request_body': {'conv_id': 'invalid_conv_id'},
                    'expected_status': '400',
                    'jsonpath': '$.error_message contains "conv_id"',
                    'remark': '操作不存在的会话'
                })
        
        return scenarios
    
    # 抽象方法，子类必须实现
    @abstractmethod
    def _generate_normal_case(self, service_name: str, method_name: str, 
                              request_structure: Dict[str, str]) -> Dict:
        """生成正常用例（正例）"""
        pass
    
    @abstractmethod
    def _generate_parameter_abnormal_cases(self, service_name: str, method_name: str,
                                          request_structure: Dict[str, str]) -> List[Dict]:
        """生成参数异常用例（5条高频反例）"""
        pass
    
    @abstractmethod
    def _generate_business_abnormal_cases(self, service_name: str, method_name: str,
                                         request_structure: Dict[str, str]) -> List[Dict]:
        """生成业务异常用例"""
        pass
    
    @abstractmethod
    def _generate_security_cases(self, service_name: str, method_name: str,
                                 request_structure: Dict[str, str]) -> List[Dict]:
        """生成权限安全用例"""
        pass
    
    @abstractmethod
    def _generate_performance_cases(self, service_name: str, method_name: str,
                                    request_structure: Dict[str, str]) -> List[Dict]:
        """生成性能边界用例"""
        pass
    
    @abstractmethod
    def _get_preconditions(self, service_name: str, method_name: str) -> str:
        """获取前置条件"""
        pass

