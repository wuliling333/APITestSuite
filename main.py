#!/usr/bin/env python3
"""
API测试框架主入口
"""
import sys
import os
import argparse

# 添加框架路径
sys.path.insert(0, os.path.dirname(__file__))

from framework.config import Config
from framework.git_updater import GitUpdater
from framework.connection_tester import ConnectionTester
from framework.protobuf_parser import ProtobufParser
from framework.test_generator import TestGenerator
from framework.test_runner import TestRunner
from framework.report_generator import ReportGenerator


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='API测试框架')
    parser.add_argument('--run', action='store_true', help='运行测试并生成报告')
    parser.add_argument('--skip-git-check', action='store_true', help='跳过Git更新检查')
    
    args = parser.parse_args()
    
    config = Config()
    
    # 1. Git更新（除非跳过）
    if not args.skip_git_check:
        try:
            git_updater = GitUpdater(config)
            git_updater.check_and_update()
        except Exception as e:
            print(f"⚠️  Git更新失败: {e}")
            print("  继续执行...")
    
    # 2. 测试连接
    connection_tester = ConnectionTester(config)
    if not connection_tester.test_all_connections():
        print("⚠️  服务器连接测试失败，但继续执行...")
    
    # 3. 解析接口
    print("\n" + "=" * 80)
    print("解析API接口...")
    print("=" * 80)
    
    parser_obj = ProtobufParser(config)
    interfaces = parser_obj.discover_interfaces()
    
    total_interfaces = sum(len(ifs) for ifs in interfaces.values())
    print(f"✓ 发现 {total_interfaces} 个接口")
    for service_name, service_interfaces in interfaces.items():
        print(f"  - {service_name}: {len(service_interfaces)} 个接口")
    
    # 4. 生成测试代码
    test_generator = TestGenerator(config)
    test_generator.generate_all_tests(interfaces)
    
    # 5. 运行测试（如果指定）
    if args.run:
        test_runner = TestRunner(config)
        test_results = test_runner.run_all_tests()
        
        # 6. 生成报告
        print("\n" + "=" * 80)
        print("生成HTML报告...")
        print("=" * 80)
        
        report_generator = ReportGenerator(config)
        report_path = report_generator.generate_report(test_results)
        
        print(f"✓ 报告已生成: {report_path}")
        print("  可以在浏览器中打开查看")
    
    print("\n" + "=" * 80)
    print("完成!")
    print("=" * 80)


if __name__ == '__main__':
    main()

