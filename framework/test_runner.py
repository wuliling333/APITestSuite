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
        self.test_run_log = []  # 记录测试运行日志
    
    def startTest(self, test):
        super().startTest(test)
        # 保存测试实例
        test_id = str(test)
        self.test_instances[test_id] = test
        
        # 提取测试方法名
        test_method_name = getattr(test, '_testMethodName', 'Unknown')
        test_class_name = test.__class__.__name__ if hasattr(test, '__class__') else 'Unknown'
        
        # 记录测试开始
        log_entry = {
            'test_id': test_id,
            'test_class': test_class_name,
            'test_method': test_method_name,
            'status': 'running',
            'started': True
        }
        self.test_run_log.append(log_entry)
        
        # 打印测试开始信息
        print(f"\n{'='*80}")
        print(f"▶ 开始运行测试: {test_class_name}.{test_method_name}")
        print(f"{'='*80}")
    
    def addSuccess(self, test):
        super().addSuccess(test)
        test_id = str(test)
        test_method_name = getattr(test, '_testMethodName', 'Unknown')
        test_class_name = test.__class__.__name__ if hasattr(test, '__class__') else 'Unknown'
        
        # 检查是否有 test_result（说明接口被调用了）
        has_test_result = hasattr(test, 'test_result') and test.test_result is not None
        has_response = False
        if has_test_result:
            response = test.test_result.get('response', {})
            has_response = bool(response)
        
        # 更新日志
        for log in self.test_run_log:
            if log['test_id'] == test_id:
                log['status'] = 'passed'
                log['has_test_result'] = has_test_result
                log['has_response'] = has_response
                break
        
        # 打印测试通过信息
        print(f"\n✓ 测试通过: {test_class_name}.{test_method_name}")
        if has_test_result:
            print(f"  ✓ 接口已调用，返回数据: {'有' if has_response else '无'}")
        else:
            print(f"  ⚠ 警告: 测试通过但没有 test_result（可能没有调用接口）")
    
    def addFailure(self, test, err):
        super().addFailure(test, err)
        test_id = str(test)
        test_method_name = getattr(test, '_testMethodName', 'Unknown')
        test_class_name = test.__class__.__name__ if hasattr(test, '__class__') else 'Unknown'
        
        # 检查是否有 test_result
        has_test_result = hasattr(test, 'test_result') and test.test_result is not None
        has_response = False
        if has_test_result:
            response = test.test_result.get('response', {})
            has_response = bool(response)
        
        # 更新日志
        for log in self.test_run_log:
            if log['test_id'] == test_id:
                log['status'] = 'failed'
                log['has_test_result'] = has_test_result
                log['has_response'] = has_response
                log['error'] = str(err[1])[:200] if err else ''
                break
        
        # 打印测试失败信息
        print(f"\n✗ 测试失败: {test_class_name}.{test_method_name}")
        if has_test_result:
            print(f"  ✓ 接口已调用，返回数据: {'有' if has_response else '无'}")
        else:
            print(f"  ⚠ 警告: 测试失败且没有 test_result（可能在调用接口前就失败了）")
    
    def addError(self, test, err):
        super().addError(test, err)
        test_id = str(test)
        test_method_name = getattr(test, '_testMethodName', 'Unknown')
        test_class_name = test.__class__.__name__ if hasattr(test, '__class__') else 'Unknown'
        
        # 检查是否有 test_result
        has_test_result = hasattr(test, 'test_result') and test.test_result is not None
        has_response = False
        if has_test_result:
            response = test.test_result.get('response', {})
            has_response = bool(response)
        
        # 更新日志
        for log in self.test_run_log:
            if log['test_id'] == test_id:
                log['status'] = 'error'
                log['has_test_result'] = has_test_result
                log['has_response'] = has_response
                log['error'] = str(err[1])[:200] if err else ''
                break
        
        # 打印测试错误信息
        print(f"\n✗ 测试错误: {test_class_name}.{test_method_name}")
        if has_test_result:
            print(f"  ✓ 接口已调用，返回数据: {'有' if has_response else '无'}")
        else:
            print(f"  ⚠ 警告: 测试错误且没有 test_result（可能在调用接口前就出错了）")


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
        
        # 打印测试运行日志摘要
        test_run_log = getattr(result, 'test_run_log', [])
        if test_run_log:
            print("\n" + "=" * 80)
            print("测试运行日志摘要")
            print("=" * 80)
            
            # 按接口分组统计
            interface_stats = {}
            for log in test_run_log:
                test_method = log.get('test_method', 'Unknown')
                # 提取接口名（例如：test_sendmessage_参数异常 -> SendMessage）
                if '_' in test_method:
                    parts = test_method.split('_')
                    interface_name = parts[1].capitalize() if len(parts) > 1 else test_method
                else:
                    interface_name = test_method.replace('test_', '').capitalize()
                
                if interface_name not in interface_stats:
                    interface_stats[interface_name] = {
                        'total': 0,
                        'passed': 0,
                        'failed': 0,
                        'error': 0,
                        'has_test_result': 0,
                        'has_response': 0,
                        'no_test_result': 0
                    }
                
                stats = interface_stats[interface_name]
                stats['total'] += 1
                status = log.get('status', 'unknown')
                if status == 'passed':
                    stats['passed'] += 1
                elif status == 'failed':
                    stats['failed'] += 1
                elif status == 'error':
                    stats['error'] += 1
                
                if log.get('has_test_result'):
                    stats['has_test_result'] += 1
                    if log.get('has_response'):
                        stats['has_response'] += 1
                else:
                    stats['no_test_result'] += 1
            
            # 打印统计信息
            for interface_name, stats in sorted(interface_stats.items()):
                print(f"\n{interface_name} 接口:")
                print(f"  总测试数: {stats['total']}")
                print(f"  通过: {stats['passed']}, 失败: {stats['failed']}, 错误: {stats['error']}")
                print(f"  接口调用情况: {stats['has_test_result']} 个测试调用了接口, {stats['no_test_result']} 个测试未调用接口")
                print(f"  返回数据情况: {stats['has_response']} 个测试有返回数据")
                
                # 列出没有调用接口的测试
                if stats['no_test_result'] > 0:
                    print(f"  ⚠ 警告: 以下测试没有调用接口:")
                    for log in test_run_log:
                        test_method = log.get('test_method', 'Unknown')
                        if '_' in test_method:
                            parts = test_method.split('_')
                            log_interface = parts[1].capitalize() if len(parts) > 1 else test_method
                        else:
                            log_interface = test_method.replace('test_', '').capitalize()
                        
                        if log_interface == interface_name and not log.get('has_test_result'):
                            print(f"    - {test_method}")
        
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
        """按服务组织测试结果（直接使用测试运行的实际结果）"""
        services = {}
        
        # 获取所有测试实例
        test_instances = getattr(result, 'test_instances', {})
        print(f"📋 收集到的测试实例总数: {len(test_instances)}")
        processed_test_ids = set()
        
        # 处理失败的测试
        for test, error_msg in result.failures:
            test_id = str(test)
            processed_test_ids.add(test_id)
            # 优先从测试实例提取服务名（更准确）
            service_name = self._extract_service_name_from_test(test).lower()
            if service_name == 'unknown':
                # 如果无法从测试实例提取，从测试ID提取
                service_name = self._extract_service_name(test_id)
            
            if service_name not in services:
                services[service_name] = {'test_results': []}
            
            test_info = self._extract_test_info(test, test_id, 'failure', str(error_msg))
            services[service_name]['test_results'].append(test_info)
        
        # 处理错误的测试
        for test, error_msg in result.errors:
            test_id = str(test)
            processed_test_ids.add(test_id)
            # 优先从测试实例提取服务名（更准确）
            service_name = self._extract_service_name_from_test(test).lower()
            if service_name == 'unknown':
                # 如果无法从测试实例提取，从测试ID提取
                service_name = self._extract_service_name(test_id)
            
            if service_name not in services:
                services[service_name] = {'test_results': []}
            
            test_info = self._extract_test_info(test, test_id, 'error', str(error_msg))
            services[service_name]['test_results'].append(test_info)
        
        # 处理成功的测试（不在失败或错误列表中）
        for test_id, test_instance in test_instances.items():
            if test_id not in processed_test_ids:
                # 优先从测试实例提取服务名（更准确）
                service_name = self._extract_service_name_from_test(test_instance).lower()
                if service_name == 'unknown':
                    # 如果无法从测试实例提取，从测试ID提取
                    service_name = self._extract_service_name(test_id)
                
                if service_name not in services:
                    services[service_name] = {'test_results': []}
                
                test_info = self._extract_test_info(test_instance, test_id, 'success', '')
                services[service_name]['test_results'].append(test_info)
        
        # 打印每个服务的测试结果数量
        print(f"\n📊 按服务组织的测试结果:")
        for service_name, service_data in services.items():
            test_count = len(service_data.get('test_results', []))
            print(f"  {service_name.upper()}: {test_count} 个测试结果")
            # 打印前5个测试用例名称
            for i, test in enumerate(service_data.get('test_results', [])[:5]):
                test_name = test.get('name', test.get('method', 'Unknown'))
                print(f"    - {test_name}")
        
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
            
            # 如果 error 参数包含更详细的错误信息（如 traceback），提取关键错误信息
            detailed_error = ''
            if error:
                # 提取 AssertionError 或其他关键错误信息
                error_lines = error.split('\n')
                # 查找 AssertionError 行
                assertion_error_line = ''
                for line in error_lines:
                    if 'AssertionError' in line:
                        assertion_error_line = line.strip()
                        break
                
                # 如果找到 AssertionError，提取错误消息
                if assertion_error_line:
                    # 提取 AssertionError 后面的错误消息
                    if ':' in assertion_error_line:
                        assertion_error_line = assertion_error_line.split(':', 1)[1].strip()
                    detailed_error = assertion_error_line
                elif 'rpc error' in error.lower():
                    # 从 traceback 中提取 rpc error 相关信息
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
                else:
                    # 如果没有找到特定错误，提取第一行非空行（通常是错误类型和消息）
                    for line in error_lines:
                        line = line.strip()
                        if line and not line.startswith('File') and not line.startswith('Traceback'):
                            detailed_error = line
                            break
            
            # 合并 error_message 和 detailed_error（包括完整的 error 信息）
            full_error_message = error_message
            if detailed_error:
                if error_message and detailed_error not in error_message:
                    full_error_message = f"{error_message}\n{detailed_error}"
                elif not error_message:
                    full_error_message = detailed_error
            
            # 如果 error 参数存在且包含完整 traceback，也添加到错误信息中（截断到合理长度）
            if error and error not in full_error_message:
                # 提取 error 中的关键信息（最后几行，通常是错误消息）
                error_lines = error.split('\n')
                # 获取最后3行非空行（通常是错误信息）
                last_error_lines = []
                for line in reversed(error_lines):
                    line = line.strip()
                    if line and not line.startswith('File') and not line.startswith('Traceback'):
                        last_error_lines.insert(0, line)
                        if len(last_error_lines) >= 3:
                            break
                if last_error_lines:
                    error_summary = '\n'.join(last_error_lines)
                    if error_summary not in full_error_message:
                        full_error_message = f"{full_error_message}\n{error_summary}" if full_error_message else error_summary
            
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
            
            # 直接使用实际运行的请求数据，不进行任何格式化或推断
            actual_request = test_result.get('request', {})
            request_to_display = actual_request  # 直接使用实际请求，不添加类型信息
            
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
                'problem_analysis': self._get_problem_analysis(test_name, full_error_message, test_result.get('request', {}), test_result.get('preconditions', [])),
                'dimension': test_result.get('dimension'),  # 测试维度（正常/参数异常/业务异常等）
                'abnormal_type': test_result.get('abnormal_type')  # 异常类型
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
                analysis_parts.append(f"  • {precondition}")
        
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
        test_name_lower = test_name.lower()
        # 检查测试类名（TestHall, TestRoom, TestSocial）
        # 测试ID格式通常是: test_method_name (generated_tests.test_hall.TestHall)
        if 'testhall' in test_name_lower or ('test_hall' in test_name_lower and 'hall' in test_name_lower):
            return 'hall'
        elif 'testroom' in test_name_lower or ('test_room' in test_name_lower and 'room' in test_name_lower):
            return 'room'
        elif 'testsocial' in test_name_lower or ('test_social' in test_name_lower and 'social' in test_name_lower):
            return 'social'
        # 如果包含 hall/room/social 关键字，也识别
        elif 'hall' in test_name_lower and 'room' not in test_name_lower and 'social' not in test_name_lower:
            return 'hall'
        elif 'room' in test_name_lower and 'social' not in test_name_lower:
            return 'room'
        elif 'social' in test_name_lower:
            return 'social'
        return 'unknown'
    
    def _extract_service_name_from_test(self, test) -> str:
        """从测试实例提取服务名"""
        # 从测试类名提取服务名（最准确的方法）
        test_class_name = test.__class__.__name__ if hasattr(test, '__class__') else ''
        if 'Hall' in test_class_name:
            return 'hall'
        elif 'Room' in test_class_name:
            return 'room'
        elif 'Social' in test_class_name:
            return 'social'
        
        # 如果无法从类名提取，尝试从测试方法名提取
        test_method_name = getattr(test, '_testMethodName', '')
        service_name = self._extract_service_name(test_method_name)
        return service_name if service_name != 'unknown' else 'unknown'
    
    def _collect_test_results(self, suite, result):
        """收集所有测试实例的结果"""
        # 遍历所有测试用例
        for test_group in suite:
            if hasattr(test_group, '_tests'):
                for test in test_group._tests:
                    if hasattr(test, '_testMethodName'):
                        # 测试已经运行，结果在result中
                        pass

