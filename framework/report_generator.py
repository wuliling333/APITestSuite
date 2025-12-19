"""
HTML报告生成器 - 生成测试报告
"""
import os
import json
from datetime import datetime
from typing import Dict, Any
from jinja2 import Template
from framework.config import Config

try:
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter
    OPENPYXL_AVAILABLE = True
except ImportError:
    OPENPYXL_AVAILABLE = False
    print("⚠ openpyxl 未安装，Excel导出功能将不可用。请运行: pip install openpyxl")


class ReportGenerator:
    """HTML报告生成器"""
    
    def __init__(self, config: Config):
        self.config = config
        self.report_dir = config.get_report_dir()
        os.makedirs(self.report_dir, exist_ok=True)
    
    def generate_report(self, test_results: Dict[str, Any]) -> str:
        """生成HTML和Excel报告"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"test_report_{timestamp}"
        report_path = os.path.join(self.report_dir, f"{report_filename}.html")
        
        # 生成HTML报告
        html_content = self._generate_html(test_results)
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # 生成Excel报告（固定文件名，每次覆盖）
        excel_path = self._generate_excel(test_results, "test_report.xlsx")
        
        # 清理旧报告（只清理HTML，Excel保留最新的）
        self._cleanup_old_reports()
        
        return report_path
    
    def _generate_html(self, test_results: Dict[str, Any]) -> str:
        """生成HTML内容"""
        template_str = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>API测试报告</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            border-bottom: 3px solid #4CAF50;
            padding-bottom: 10px;
        }
        .summary {
            display: flex;
            gap: 20px;
            margin: 30px 0;
        }
        .stat-card {
            flex: 1;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            color: white;
        }
        .stat-card.total { background: #2196F3; }
        .stat-card.passed { background: #4CAF50; }
        .stat-card.failed { background: #f44336; }
        .stat-number {
            font-size: 36px;
            font-weight: bold;
            margin: 10px 0;
        }
        .service-section {
            margin: 40px 0;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            overflow: hidden;
        }
        .service-header {
            background: #f8f9fa;
            padding: 15px 20px;
            font-size: 18px;
            font-weight: bold;
            color: #333;
            border-bottom: 2px solid #e0e0e0;
            cursor: pointer;
        }
        .service-header:hover {
            background: #e9ecef;
        }
        .service-content {
            padding: 20px;
            display: none;
        }
        .service-content.expanded {
            display: block;
        }
        .test-case {
            background: #f8f9fa;
            margin: 10px 0;
            padding: 15px;
            border-radius: 4px;
            border-left: 4px solid #4CAF50;
        }
        .test-case.failed {
            border-left-color: #f44336;
        }
        .test-name {
            font-weight: bold;
            margin-bottom: 10px;
        }
        .test-detail {
            margin: 5px 0;
            font-size: 14px;
        }
        .detail-label {
            font-weight: bold;
            color: #666;
        }
        pre {
            background: #f5f5f5;
            padding: 10px;
            border-radius: 4px;
            overflow-x: auto;
            font-size: 12px;
        }
        .problem-analysis {
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 10px;
            margin-top: 10px;
        }
        .problem-analysis .detail-label {
            color: #856404;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>API测试报告</h1>
        <p>生成时间: {{ timestamp }}</p>
        
        <div class="summary">
            <div class="stat-card total">
                <div class="stat-label">总接口数</div>
                <div class="stat-number">{{ test_results.total }}</div>
            </div>
            <div class="stat-card passed">
                <div class="stat-label">通过</div>
                <div class="stat-number">{{ test_results.passed }}</div>
            </div>
            <div class="stat-card failed">
                <div class="stat-label">失败</div>
                <div class="stat-number">{{ test_results.failed }}</div>
            </div>
        </div>
        
        {% for service_name, service_data in test_results.services.items() %}
        <div class="service-section">
            <div class="service-header" onclick="toggleService('{{ service_name }}')">
                {{ service_name|upper }} 服务
            </div>
            <div class="service-content" id="service-{{ service_name }}">
                {% for test in service_data.test_results %}
                <div class="test-case {{ 'failed' if test.status == 'failure' else '' }}">
                    <div class="test-name">{{ test.name }}</div>
                    <div class="test-detail">
                        <span class="detail-label">请求:</span>
                        <pre>{{ test.request }}</pre>
                    </div>
                    <div class="test-detail">
                        <span class="detail-label">响应:</span>
                        <pre>{{ test.response }}</pre>
                    </div>
                    {% if test.error %}
                    <div class="test-detail">
                        <span class="detail-label">错误:</span>
                        <pre>{{ test.error }}</pre>
                    </div>
                    {% endif %}
                    {% if test.problem_analysis %}
                    <div class="test-detail problem-analysis">
                        <span class="detail-label">问题分析:</span>
                        <pre>{{ test.problem_analysis }}</pre>
                    </div>
                    {% endif %}
                </div>
                {% endfor %}
            </div>
        </div>
        {% endfor %}
    </div>
    
    <script>
        function toggleService(serviceName) {
            const content = document.getElementById('service-' + serviceName);
            content.classList.toggle('expanded');
        }
    </script>
</body>
</html>'''
        
        template = Template(template_str)
        
        # 准备数据 - 将字典转换为JSON字符串
        def format_json(obj):
            # 如果是请求参数（包含value和type的结构），格式化显示
            if isinstance(obj, dict) and obj and isinstance(list(obj.values())[0], dict):
                # 检查是否是格式化的请求结构（包含value和type）
                first_value = list(obj.values())[0]
                if 'value' in first_value and 'type' in first_value:
                    # 格式化请求参数，显示字段名、类型和值
                    formatted = {}
                    for field_name, field_info in obj.items():
                        if isinstance(field_info, dict) and 'value' in field_info and 'type' in field_info:
                            value = field_info['value']
                            field_type = field_info['type']
                            if value is not None:
                                formatted[f"{field_name} ({field_type})"] = value
                            else:
                                formatted[f"{field_name} ({field_type})"] = "[未提供]"
                        else:
                            formatted[field_name] = field_info
                    obj = formatted
            
            # 递归转换 protobuf 对象为字典
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
                                    # 重复字段，需要递归转换每个元素
                                    if field_descriptor.type == field_descriptor.TYPE_MESSAGE:
                                        result[field_name] = [convert_to_dict(item) for item in field_value]
                                    else:
                                        result[field_name] = list(field_value)
                                elif field_descriptor.type == field_descriptor.TYPE_MESSAGE:
                                    # 嵌套消息
                                    if field_value:
                                        result[field_name] = convert_to_dict(field_value)
                                else:
                                    # 基本类型
                                    result[field_name] = field_value
                        except Exception as e:
                            # 如果转换失败，返回字符串表示
                            return str(val)
                        return result
                elif isinstance(val, dict):
                    return {k: convert_to_dict(v) for k, v in val.items()}
                elif isinstance(val, list):
                    return [convert_to_dict(item) for item in val]
                else:
                    return val
            
            try:
                converted = convert_to_dict(obj)
                return json.dumps(converted, indent=2, ensure_ascii=False, default=str)
            except Exception as e:
                # 如果转换失败，返回字符串表示
                return str(obj)
        
        # 处理测试结果，将字典转换为JSON字符串
        processed_results = {
            'total': test_results.get('total', 0),
            'passed': test_results.get('passed', 0),
            'failed': test_results.get('failed', 0),
            'errors': test_results.get('errors', 0),
            'services': {}
        }
        
        for service_name, service_data in test_results.get('services', {}).items():
            processed_results['services'][service_name] = {
                'test_results': []
            }
            for test in service_data.get('test_results', []):
                processed_test = {
                    'name': test.get('name', 'Unknown'),
                    'status': test.get('status', 'unknown'),
                    'request': format_json(test.get('request', {})),
                    'response': format_json(test.get('response', {})),
                    'error': test.get('error', ''),
                    'error_code': test.get('error_code', ''),
                    'error_message': test.get('error_message', ''),
                    'problem_analysis': test.get('problem_analysis', '')
                }
                processed_results['services'][service_name]['test_results'].append(processed_test)
        
        html_data = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'test_results': processed_results
        }
        
        return template.render(**html_data)
    
    def _generate_excel(self, test_results: Dict[str, Any], filename: str) -> str:
        """生成Excel报告"""
        if not OPENPYXL_AVAILABLE:
            print("⚠ Excel导出功能不可用，跳过Excel报告生成")
            return ""
        
        excel_path = os.path.join(self.report_dir, filename)
        
        # 创建工作簿
        wb = openpyxl.Workbook()
        
        # 创建摘要工作表
        summary_sheet = wb.active
        summary_sheet.title = "测试摘要"
        self._write_summary_sheet(summary_sheet, test_results)
        
        # 为每个服务创建详细工作表
        for service_name, service_data in test_results.get('services', {}).items():
            sheet = wb.create_sheet(title=service_name.upper())
            self._write_service_sheet(sheet, service_name, service_data)
        
        # 保存文件
        wb.save(excel_path)
        print(f"✓ Excel报告已生成: {excel_path}")
        
        return excel_path
    
    def _write_summary_sheet(self, sheet, test_results: Dict[str, Any]):
        """写入摘要工作表"""
        # 标题样式
        title_font = Font(bold=True, size=14)
        header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        header_font = Font(bold=True, color="FFFFFF")
        border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )
        
        # 写入标题
        sheet['A1'] = "API测试报告摘要"
        sheet['A1'].font = title_font
        sheet.merge_cells('A1:D1')
        
        # 写入统计信息
        row = 3
        sheet[f'A{row}'] = "生成时间"
        sheet[f'B{row}'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row += 1
        
        sheet[f'A{row}'] = "总测试数"
        sheet[f'B{row}'] = test_results.get('total', 0)
        row += 1
        
        sheet[f'A{row}'] = "通过"
        sheet[f'B{row}'] = test_results.get('passed', 0)
        sheet[f'A{row}'].fill = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
        row += 1
        
        sheet[f'A{row}'] = "失败"
        sheet[f'B{row}'] = test_results.get('failed', 0)
        sheet[f'A{row}'].fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
        row += 1
        
        sheet[f'A{row}'] = "错误"
        sheet[f'B{row}'] = test_results.get('errors', 0)
        sheet[f'A{row}'].fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
        row += 2
        
        # 写入服务统计
        sheet[f'A{row}'] = "服务"
        sheet[f'B{row}'] = "测试数"
        sheet[f'C{row}'] = "通过"
        sheet[f'D{row}'] = "失败"
        sheet[f'E{row}'] = "错误"
        
        for cell in [f'A{row}', f'B{row}', f'C{row}', f'D{row}', f'E{row}']:
            sheet[cell].font = header_font
            sheet[cell].fill = header_fill
            sheet[cell].alignment = Alignment(horizontal='center', vertical='center')
            sheet[cell].border = border
        
        row += 1
        
        for service_name, service_data in test_results.get('services', {}).items():
            test_list = service_data.get('test_results', [])
            total = len(test_list)
            passed = sum(1 for t in test_list if t.get('status') == 'success')
            failed = sum(1 for t in test_list if t.get('status') == 'failure')
            errors = sum(1 for t in test_list if t.get('status') == 'error')
            
            sheet[f'A{row}'] = service_name.upper()
            sheet[f'B{row}'] = total
            sheet[f'C{row}'] = passed
            sheet[f'D{row}'] = failed
            sheet[f'E{row}'] = errors
            
            for col in ['A', 'B', 'C', 'D', 'E']:
                sheet[f'{col}{row}'].border = border
                sheet[f'{col}{row}'].alignment = Alignment(horizontal='center', vertical='center')
            
            row += 1
        
        # 调整列宽
        sheet.column_dimensions['A'].width = 20
        sheet.column_dimensions['B'].width = 15
        sheet.column_dimensions['C'].width = 15
        sheet.column_dimensions['D'].width = 15
        sheet.column_dimensions['E'].width = 15
    
    def _write_service_sheet(self, sheet, service_name: str, service_data: Dict[str, Any]):
        """写入服务详细工作表"""
        # 样式定义
        header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        header_font = Font(bold=True, color="FFFFFF")
        success_fill = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
        failure_fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
        border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )
        
        # 写入表头
        headers = ['接口名称', '请求方法', '状态', '响应码', '请求', '实际输出', '错误信息', '问题分析']
        for col_idx, header in enumerate(headers, start=1):
            cell = sheet.cell(row=1, column=col_idx, value=header)
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
            cell.border = border
        
        # 写入测试数据
        row = 2
        for test in service_data.get('test_results', []):
            status = test.get('status', 'unknown')
            status_text = '通过' if status == 'success' else ('失败' if status == 'failure' else '错误')
            
            # 接口名称
            sheet.cell(row=row, column=1, value=test.get('name', 'Unknown'))
            
            # 请求方法
            request_method = test.get('request_method', 'TCP')
            sheet.cell(row=row, column=2, value=request_method)
            
            # 状态
            status_cell = sheet.cell(row=row, column=3, value=status_text)
            if status == 'success':
                status_cell.fill = success_fill
            else:
                status_cell.fill = failure_fill
            
            # 响应码
            error_code = test.get('error_code', '')
            sheet.cell(row=row, column=4, value=error_code if error_code else 'N/A')
            
            # 请求
            request_data = test.get('request', {})
            request_str = json.dumps(request_data, indent=2, ensure_ascii=False) if request_data else ''
            sheet.cell(row=row, column=5, value=request_str[:5000])  # 限制长度
            
            # 实际输出
            response_data = test.get('response', {})
            response_str = json.dumps(response_data, indent=2, ensure_ascii=False, default=str) if response_data else ''
            sheet.cell(row=row, column=6, value=response_str[:5000])  # 限制长度
            
            # 错误信息
            error_msg = test.get('error_message', '') or test.get('error', '')
            sheet.cell(row=row, column=7, value=error_msg[:1000])  # 限制长度
            
            # 问题分析
            problem_analysis = test.get('problem_analysis', '')
            sheet.cell(row=row, column=8, value=problem_analysis[:2000])  # 限制长度
            
            # 应用样式
            for col in range(1, 9):
                cell = sheet.cell(row=row, column=col)
                cell.border = border
                cell.alignment = Alignment(horizontal='left', vertical='top', wrap_text=True)
            
            row += 1
        
        # 调整列宽
        sheet.column_dimensions['A'].width = 25
        sheet.column_dimensions['B'].width = 12
        sheet.column_dimensions['C'].width = 10
        sheet.column_dimensions['D'].width = 10
        sheet.column_dimensions['E'].width = 40
        sheet.column_dimensions['F'].width = 40
        sheet.column_dimensions['G'].width = 50
        sheet.column_dimensions['H'].width = 60
        
        # 设置行高
        for row_idx in range(2, row):
            sheet.row_dimensions[row_idx].height = 60
    
    def _cleanup_old_reports(self, keep_count: int = 3):
        """清理旧报告"""
        try:
            report_files = []
            if os.path.exists(self.report_dir):
                for filename in os.listdir(self.report_dir):
                    if filename.startswith('test_report_') and filename.endswith('.html'):
                        filepath = os.path.join(self.report_dir, filename)
                        if os.path.isfile(filepath):
                            mtime = os.path.getmtime(filepath)
                            report_files.append((mtime, filepath, filename))
            
            report_files.sort(key=lambda x: x[0], reverse=True)
            
            if len(report_files) > keep_count:
                for mtime, filepath, filename in report_files[keep_count:]:
                    os.remove(filepath)
                    print(f"删除旧报告: {filename}")
        except Exception as e:
            print(f"⚠ 清理旧报告失败: {e}")

