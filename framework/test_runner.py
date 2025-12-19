"""
测试运行器 - 运行测试并收集结果
"""
import unittest
import os
import sys
from typing import Dict, Any, List
from framework.config import Config


class CustomTestResult(unittest.TextTestResult):
    """自定义测试结果收集器"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_instances = {}  # 存储测试实例
    
    def startTest(self, test):
        super().startTest(test)
        # 保存测试实例
        test_id = str(test)
        self.test_instances[test_id] = test


class TestRunner:
    """测试运行器"""
    
    def __init__(self, config: Config):
        self.config = config
        self.test_dir = config.get_test_output_dir()
    
    def run_all_tests(self) -> Dict[str, Any]:
        """运行所有测试"""
        print("=" * 80)
        print("开始运行测试...")
        print("=" * 80)
        
        # 添加测试目录到路径
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        # 发现测试
        loader = unittest.TestLoader()
        suite = unittest.TestSuite()
        
        # 加载所有测试文件
        test_files = [
            f"{self.test_dir}/test_hall.py",
            f"{self.test_dir}/test_room.py",
            f"{self.test_dir}/test_social.py"
        ]
        
        for test_file in test_files:
            if os.path.exists(test_file):
                try:
                    tests = loader.loadTestsFromName(test_file.replace('/', '.').replace('.py', ''))
                    suite.addTests(tests)
                except Exception as e:
                    print(f"⚠ 加载测试文件失败 {test_file}: {e}")
        
        # 运行测试 - 使用自定义结果收集器
        custom_result = CustomTestResult(sys.stdout, True, 2)
        runner = unittest.TextTestRunner(verbosity=2, resultclass=CustomTestResult)
        result = runner.run(suite)
        
        # 保存测试实例引用以便后续收集结果
        self.test_instances = getattr(result, 'test_instances', {})
        
        # 收集结果
        test_results = {
            'total': result.testsRun,
            'passed': result.testsRun - len(result.failures) - len(result.errors),
            'failed': len(result.failures),
            'errors': len(result.errors),
            'services': self._organize_results_by_service(result)
        }
        
        print("\n" + "=" * 80)
        print("测试结果:")
        print(f"  总测试数: {test_results['total']}")
        print(f"  通过: {test_results['passed']}")
        print(f"  失败: {test_results['failed']}")
        print(f"  错误: {test_results['errors']}")
        print("=" * 80)
        
        return test_results
    
    def _organize_results_by_service(self, result) -> Dict[str, Any]:
        """按服务组织测试结果"""
        services = {}
        
        # 获取所有测试实例
        test_instances = getattr(result, 'test_instances', {})
        processed_test_ids = set()
        
        # 处理失败的测试
        for test, error_msg in result.failures:
            test_id = str(test)
            processed_test_ids.add(test_id)
            service_name = self._extract_service_name(test_id)
            
            if service_name not in services:
                services[service_name] = {'test_results': []}
            
            test_info = self._extract_test_info(test, test_id, 'failure', str(error_msg))
            services[service_name]['test_results'].append(test_info)
        
        # 处理错误的测试
        for test, error_msg in result.errors:
            test_id = str(test)
            processed_test_ids.add(test_id)
            service_name = self._extract_service_name(test_id)
            
            if service_name not in services:
                services[service_name] = {'test_results': []}
            
            test_info = self._extract_test_info(test, test_id, 'error', str(error_msg))
            services[service_name]['test_results'].append(test_info)
        
        # 处理成功的测试（不在失败或错误列表中）
        for test_id, test_instance in test_instances.items():
            if test_id not in processed_test_ids:
                service_name = self._extract_service_name(test_id)
                
                if service_name not in services:
                    services[service_name] = {'test_results': []}
                
                test_info = self._extract_test_info(test_instance, test_id, 'success', '')
                services[service_name]['test_results'].append(test_info)
        
        return services
    
    def _extract_test_info(self, test, test_id: str, status: str, error: str) -> Dict:
        """提取测试信息"""
        # 从test_id提取方法名
        method_name = self._extract_test_name(test_id)
        
        test_info = {
            'name': method_name,
            'status': status,
            'request': {},
            'response': {},
            'error': error[:500] if error else ''
        }
        
        # 如果测试实例有test_result属性，使用它
        if hasattr(test, 'test_result') and test.test_result:
            test_result = test.test_result
            # 优先使用 test_result 中的 name，如果没有则使用 method，最后才用提取的 method_name
            test_name = test_result.get('name') or test_result.get('method') or method_name
            error_message = test_result.get('error_message', '')
            
            # 如果 error 参数包含更详细的错误信息（如 traceback），尝试提取其中的关键错误信息
            detailed_error = ''
            if error and 'rpc error' in error.lower():
                # 从 traceback 中提取 rpc error 相关信息
                error_lines = error.split('\n')
                for line in error_lines:
                    if 'rpc error' in line.lower() or 'connection error' in line.lower() or 'unavailable' in line.lower():
                        detailed_error = line.strip()
                        break
                # 如果没有找到，尝试从整个 error 中提取
                if not detailed_error and 'err:' in error:
                    for line in error_lines:
                        if 'err:' in line.lower():
                            detailed_error = line.strip()
                            break
            
            # 合并 error_message 和 detailed_error
            full_error_message = error_message
            if detailed_error and detailed_error not in error_message:
                full_error_message = f"{error_message}\n{detailed_error}" if error_message else detailed_error
            
            # 使用完整的服务器响应（test_result中的response字段已经包含了完整的result结构）
            full_response = test_result.get('response', {})
            # 如果response不是完整的结构，则构建完整的响应结构
            if not isinstance(full_response, dict) or 'success' not in full_response:
                full_response = {
                    'success': test_result.get('success', False),
                    'response': full_response,
                    'error_code': test_result.get('error_code'),
                    'error_message': test_result.get('error_message', '')
                }
            
            # 获取服务器协议定义的请求参数结构
            actual_request = test_result.get('request', {})
            request_to_display = actual_request  # 默认使用实际请求
            
            try:
                from framework.proto_request_formatter import ProtoRequestFormatter
                # 从测试类名或方法名提取服务名
                service_name = self._extract_service_name_from_test(test)
                if service_name:
                    proto_request_structure = ProtoRequestFormatter.get_request_structure(
                        service_name.capitalize(), 
                        test_result.get('method', method_name)
                    )
                    
                    if proto_request_structure:
                        # 如果有协议定义，创建一个包含类型信息的请求结构
                        formatted_request = {}
                        for field_name, field_type in proto_request_structure.items():
                            if field_name in actual_request:
                                formatted_request[field_name] = {
                                    'value': actual_request[field_name],
                                    'type': field_type
                                }
                            else:
                                formatted_request[field_name] = {
                                    'value': None,
                                    'type': field_type
                                }
                        # 如果实际请求中有协议定义中没有的字段（不应该发生，但为了兼容性保留）
                        for field_name, field_value in actual_request.items():
                            if field_name not in formatted_request:
                                formatted_request[field_name] = {
                                    'value': field_value,
                                    'type': 'unknown'
                                }
                        request_to_display = formatted_request
            except Exception as e:
                # 如果获取协议定义失败，使用实际请求
                pass
            
            # 获取请求方法（TCP/gRPC，不是HTTP的POST/GET）
            # 这个系统使用TCP协议通过Gate服务器通信，使用protobuf序列化
            request_method = 'TCP'  # 默认使用TCP协议
            
            test_info.update({
                'name': test_name,
                'method': test_result.get('method', method_name),
                'request_method': request_method,  # 请求方法（TCP/gRPC）
                'request': request_to_display,
                'response': full_response,  # 使用完整的服务器响应
                'error_code': test_result.get('error_code'),
                'error_message': full_error_message,
                'preconditions': test_result.get('preconditions', []),
                'problem_analysis': self._get_problem_analysis(test_name, full_error_message, test_result.get('request', {}), test_result.get('preconditions', []))
            })
        
        return test_info
    
    def _extract_test_name(self, test_str: str) -> str:
        """从测试字符串提取测试名称"""
        # 格式通常是: test_method_name (TestClass) 或 test_method_name
        # 先尝试从括号前提取方法名
        if '(' in test_str:
            method_part = test_str.split('(')[0].strip()
        else:
            method_part = test_str
        
        # 如果包含点号，取最后一部分
        if '.' in method_part:
            method_part = method_part.split('.')[-1]
        
        # 移除test_前缀
        if method_part.startswith('test_'):
            method_part = method_part[5:]
        
        # 转换为驼峰命名
        words = method_part.split('_')
        return ''.join(word.capitalize() for word in words) if words else method_part
    
    def _get_problem_analysis(self, method_name: str, error_message: str, request_data: dict, preconditions: list = None) -> str:
        """根据错误信息总结可能存在的问题"""
        if preconditions is None:
            preconditions = []
        
        analysis_parts = []
        
        # 显示前置条件
        if preconditions:
            analysis_parts.append("前置条件:")
            for precondition in preconditions:
                analysis_parts.append(f"  ✓ {precondition}")
        
        if not error_message:
            return "\n".join(analysis_parts) if analysis_parts else ""
        
        # 显示服务器报错
        analysis_parts.append("")
        analysis_parts.append("服务器报错:")
        # 如果错误信息很长，分行显示
        if len(error_message) > 100:
            # 尝试按行分割
            error_lines = error_message.split('\n')
            for line in error_lines:
                if line.strip():
                    analysis_parts.append(f"  {line.strip()}")
        else:
            analysis_parts.append(f"  {error_message}")
        
        error_lower = error_message.lower()
        method_lower = method_name.lower()
        
        # 可能存在的问题
        problems = []
        
        # internal error 相关
        if 'internal error' in error_lower:
            # 检查是否有 gRPC 连接错误信息
            has_grpc_error = 'rpc error' in error_lower or 'connection error' in error_lower or 'unavailable' in error_lower
            if 'startgame' in method_lower:
                if has_grpc_error:
                    problems.append("• 问题说明：battle 服务 gRPC 连接失败")
                    problems.append("• 可能原因：battle 服务 (10.100.2.28:29601) 不可用或网络连接问题")
                    problems.append("• 可能原因：battle 服务进程未启动或已崩溃")
                    problems.append("• 可能原因：网络防火墙或路由配置问题")
                else:
                    problems.append("• 可能原因：battle 服务不可用或配置错误")
                    problems.append("• 可能原因：玩家信息获取失败")
                    problems.append("• 可能原因：游戏创建流程异常")
                    problems.append("• 问题说明：服务器内部服务调用失败，需要检查 battle 服务状态")
            else:
                if has_grpc_error:
                    problems.append("• 问题说明：依赖服务 gRPC 连接失败")
                    problems.append("• 可能原因：相关微服务不可用或网络连接问题")
                    problems.append("• 可能原因：服务进程未启动或已崩溃")
                else:
                    problems.append("• 可能原因：相关服务不可用或配置错误")
                    problems.append("• 可能原因：服务器内部处理异常")
                    problems.append("• 问题说明：服务器端内部错误，需要查看服务器日志")
        
        # not implemented 相关
        elif 'not implemented' in error_lower:
            problems.append("• 问题说明：该接口在服务器端尚未实现")
            problems.append("• 可能原因：功能开发中或已废弃")
        
        # team not exist 相关
        elif 'team not exist' in error_lower:
            problems.append("• 问题说明：队伍不存在或用户不在队伍中")
            problems.append("• 可能原因：team_id 无效、队伍已解散、用户未加入队伍")
        
        # game not exist 相关
        elif 'game not exist' in error_lower:
            problems.append("• 问题说明：游戏不存在或已结束")
            problems.append("• 可能原因：game_id 无效、游戏已结束、游戏未创建")
        
        # message not found 相关
        elif 'message not found' in error_lower:
            if 'world' in str(request_data.get('conv_id', '')).lower() or 'w_default' in str(request_data.get('conv_id', '')):
                problems.append("• 问题说明：世界聊天消息不支持此操作")
                problems.append("• 可能原因：世界聊天消息存储在 Redis Stream，未持久化到 MongoDB，无法进行消息查询操作")
            else:
                problems.append("• 问题说明：消息不存在或无法访问")
                problems.append("• 可能原因：conv_id 或 seq 无效、消息已删除、消息不存在")
        
        # get reactions failed 相关
        elif 'get reactions failed' in error_lower:
            if 'world' in str(request_data.get('conv_id', '')).lower() or 'w_default' in str(request_data.get('conv_id', '')):
                problems.append("• 问题说明：世界聊天消息不支持获取反应")
                problems.append("• 可能原因：世界聊天消息存储在 Redis Stream，未持久化到 MongoDB，无法查询反应信息")
            else:
                problems.append("• 问题说明：无法获取消息反应")
                problems.append("• 可能原因：消息不存在、消息不支持反应、数据库查询失败")
        
        # invalid request 相关
        elif 'invalid request' in error_lower:
            problems.append("• 问题说明：请求参数无效")
            problems.append("• 可能原因：参数缺失、参数类型错误、参数值不符合要求")
        
        # invalid target_uid 相关
        elif 'invalid target_uid' in error_lower:
            problems.append("• 问题说明：target_uid 参数无效")
            problems.append("• 可能原因：target_uid 为 0 或负数、target_uid 是自己、用户不存在")
        
        # player not ready 相关
        elif 'player not ready' in error_lower:
            problems.append("• 问题说明：玩家未准备")
            problems.append("• 可能原因：队伍中有玩家（除队长外）未设置为准备状态")
        
        # team not idle 相关
        elif 'team not idle' in error_lower:
            problems.append("• 问题说明：队伍状态不正确")
            problems.append("• 可能原因：队伍正在匹配中、队伍正在游戏中、队伍状态不是 Idle")
        
        # map not set 相关
        elif 'map not set' in error_lower:
            problems.append("• 问题说明：地图未设置")
            problems.append("• 可能原因：map_id 为 0 或未提供有效的地图ID")
        
        # only team owner can do 相关
        elif 'only team owner' in error_lower or 'not owner' in error_lower:
            problems.append("• 问题说明：只有队长可以执行此操作")
            problems.append("• 可能原因：当前用户不是队伍队长")
        
        # 如果没有匹配到特定错误，提供通用分析
        if not problems:
            problems.append("• 问题说明：服务器返回错误")
            problems.append("• 可能原因：请求参数错误、服务器配置问题、服务不可用")
        
        # 添加可能存在的问题部分
        if problems:
            analysis_parts.append("")
            analysis_parts.append("可能存在的问题:")
            analysis_parts.extend(problems)
        
        return "\n".join(analysis_parts) if analysis_parts else ""
    
    def _extract_actual_response(self, method_name: str, response: dict) -> dict:
        """提取接口的实际响应内容（去除外层的success、response等）"""
        if not response:
            return {}
        
        # 将方法名转换为小写，用于查找响应字段
        method_lower = method_name.lower()
        
        # 常见的响应字段名格式（protobuf字段名通常是下划线命名，但返回时可能转换为小写）
        # 例如：UpdateNickname -> updatenickname 或 update_nickname
        possible_keys = [
            method_lower,  # updatenickname
            method_lower.replace('_', ''),  # updatenickname (如果原方法名有下划线)
            method_lower.replace('_', '').replace('-', ''),  # 去除所有分隔符
        ]
        
        # 尝试找到实际的响应内容
        for key in possible_keys:
            if key in response:
                return response[key]
        
        # 如果找不到，检查是否有常见的响应结构
        # 例如：{"updatenickname": {...}} 或 {"fetchselffulluserinfo": {...}}
        # 通常响应中只有一个键，且值是字典
        if len(response) == 1:
            for key, value in response.items():
                if isinstance(value, dict):
                    # 如果值是一个字典，可能是实际的响应内容
                    return value
        
        # 如果都找不到，返回原始响应
        return response
    
    def _extract_service_name(self, test_name: str) -> str:
        """从测试名称提取服务名"""
        if 'hall' in test_name.lower():
            return 'hall'
        elif 'room' in test_name.lower():
            return 'room'
        elif 'social' in test_name.lower():
            return 'social'
        return 'unknown'
    
    def _extract_service_name_from_test(self, test) -> str:
        """从测试实例提取服务名"""
        # 从测试类名提取服务名
        test_class_name = test.__class__.__name__ if hasattr(test, '__class__') else ''
        if 'Hall' in test_class_name:
            return 'Hall'
        elif 'Room' in test_class_name:
            return 'Room'
        elif 'Social' in test_class_name:
            return 'Social'
        
        # 如果无法从类名提取，尝试从测试方法名提取
        test_method_name = getattr(test, '_testMethodName', '')
        return self._extract_service_name(test_method_name).capitalize()
    
    def _collect_test_results(self, suite, result):
        """收集所有测试实例的结果"""
        # 遍历所有测试用例
        for test_group in suite:
            if hasattr(test_group, '_tests'):
                for test in test_group._tests:
                    if hasattr(test, '_testMethodName'):
                        # 测试已经运行，结果在result中
                        pass

