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
from framework.pytest_test_generator import PytestTestGenerator
from framework.test_runner import TestRunner
from framework.report_generator import ReportGenerator
from framework.yaml_test_case_generator import YamlTestCaseGenerator
from framework.test_case_generator import TestCaseGenerator


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='API测试框架')
    parser.add_argument('--run', action='store_true', help='运行测试并生成报告')
    parser.add_argument('--skip-git-check', action='store_true', help='跳过Git更新检查')
    parser.add_argument('--generate-yaml', action='store_true', help='生成五维度测试用例YAML')
    parser.add_argument('--generate-cases', action='store_true', help='生成五维度测试用例Excel（从YAML文件）')
    parser.add_argument('--use-pytest', action='store_true', help='使用pytest框架和PO模式生成测试代码（默认使用unittest）')
    
    args = parser.parse_args()
    
    config = Config()
    
    # 如果只是生成YAML测试用例，先更新Git（除非跳过），然后生成
    if args.generate_yaml:
        # 先更新Git（除非跳过）
        if not args.skip_git_check:
            try:
                print("=" * 80)
                print("检查Git更新...")
                print("=" * 80)
                git_updater = GitUpdater(config)
                git_updater.check_and_update()
            except Exception as e:
                print(f"⚠️  Git更新失败: {e}")
                print("  继续执行...")
        
        print("=" * 80)
        print("生成五维度测试用例YAML...")
        print("=" * 80)
        yaml_generator = YamlTestCaseGenerator(config)
        yaml_generator.generate_yaml_test_cases()
        return
    
    # 如果只是生成测试用例Excel，从YAML文件生成
    if args.generate_cases:
        # 先更新Git（除非跳过）
        if not args.skip_git_check:
            try:
                print("=" * 80)
                print("检查Git更新...")
                print("=" * 80)
                git_updater = GitUpdater(config)
                git_updater.check_and_update()
            except Exception as e:
                print(f"⚠️  Git更新失败: {e}")
                print("  继续执行...")
        
        print("=" * 80)
        print("生成五维度测试用例Excel...")
        print("=" * 80)
        case_generator = TestCaseGenerator(config)
        # 默认运行接口测试，获取真实返回数据
        excel_path = case_generator.generate_test_cases_excel("test_cases_complete.xlsx", run_tests=True)
        print(f"\n✓ 测试用例Excel已生成: {excel_path}")
        print(f"💡 提示: 该Excel包含所有接口的所有测试用例（从YAML文件生成，并实际运行接口获取真实返回数据）")
        return
    
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
    if args.use_pytest:
        # 使用pytest + PO模式
        print("使用pytest框架和PO模式生成测试代码")
        test_generator = PytestTestGenerator(config)
    else:
        # 使用unittest（默认）
        print("使用unittest框架生成测试代码")
        test_generator = TestGenerator(config)
    test_generator.generate_all_tests(interfaces)
    
    # 5. 运行测试（如果指定）
    if args.run:
        try:
            print("\n" + "=" * 80)
            print("运行测试...")
            print("=" * 80)
            test_runner = TestRunner(config)
            test_results = test_runner.run_all_tests()
            
            if not test_results:
                print("⚠️  未获取到测试结果，跳过报告生成")
                return
            
            # 6. 生成报告（HTML和Excel）
            print("\n" + "=" * 80)
            print("生成测试报告...")
            print("=" * 80)
            
            try:
                report_generator = ReportGenerator(config)
                report_paths = report_generator.generate_report(test_results)
                
                html_path = report_paths.get('html', '')
                excel_path = report_paths.get('excel', '')
                
                if html_path:
                    print(f"✓ HTML报告已生成: {html_path}")
                if excel_path:
                    print(f"✓ Excel报告已生成: {excel_path}")
                print(f"\n💡 提示: HTML报告已更新到最新状态，可在浏览器中打开查看")
            except Exception as e:
                print(f"❌ 报告生成失败: {e}")
                import traceback
                traceback.print_exc()
                
        except KeyboardInterrupt:
            print("\n\n⚠️  用户中断测试")
            print("已保存部分测试结果")
            sys.exit(130)
        except Exception as e:
            print(f"\n❌ 测试运行失败: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
    
    print("\n" + "=" * 80)
    print("完成!")
    print("=" * 80)


if __name__ == '__main__':
    main()

