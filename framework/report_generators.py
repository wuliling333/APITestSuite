"""
报告生成器模块
拆分HTML和Excel报告生成器，提高代码模块化
"""
import os
import json
from datetime import datetime
from typing import Dict, Any
from abc import ABC, abstractmethod
from jinja2 import Template
from framework.config import Config
from framework.logger import logger

try:
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    OPENPYXL_AVAILABLE = True
except ImportError:
    OPENPYXL_AVAILABLE = False
    logger.warning("openpyxl 未安装，Excel导出功能将不可用。请运行: pip install openpyxl")


class BaseReportGenerator(ABC):
    """报告生成器基类"""
    
    def __init__(self, config: Config):
        self.config = config
        self.report_dir = config.get_report_dir()
        os.makedirs(self.report_dir, exist_ok=True)
    
    @abstractmethod
    def generate(self, test_results: Dict[str, Any]) -> str:
        """生成报告
        
        Args:
            test_results: 测试结果字典
            
        Returns:
            报告文件路径
        """
        pass


class HTMLReportGenerator(BaseReportGenerator):
    """HTML报告生成器"""
    
    def generate(self, test_results: Dict[str, Any]) -> str:
        """生成HTML报告"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"test_report_{timestamp}"
        report_path = os.path.join(self.report_dir, f"{report_filename}.html")
        
        html_content = self._generate_html(test_results)
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"HTML报告已生成: {report_path}")
        return report_path
    
    def _generate_html(self, test_results: Dict[str, Any]) -> str:
        """生成HTML内容（从原 ReportGenerator 复制）"""
        # 这里需要从原 report_generator.py 复制 _generate_html 方法
        # 为了保持向后兼容，暂时保留原实现
        template_str = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>API测试报告</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { background: #f0f0f0; padding: 20px; border-radius: 5px; }
        .summary { margin: 20px 0; }
        .service { margin: 20px 0; border: 1px solid #ddd; padding: 15px; border-radius: 5px; }
        .interface { margin: 10px 0; padding: 10px; background: #f9f9f9; border-radius: 3px; }
        .success { color: green; }
        .error { color: red; }
    </style>
</head>
<body>
    <div class="header">
        <h1>API测试报告</h1>
        <p>生成时间: {{ timestamp }}</p>
    </div>
    <div class="summary">
        <h2>测试汇总</h2>
        <p>总接口数: {{ total }}</p>
        <p>通过: <span class="success">{{ passed }}</span></p>
        <p>失败: <span class="error">{{ failed }}</span></p>
    </div>
    {% for service_name, service_data in services.items() %}
    <div class="service">
        <h2>{{ service_name }}</h2>
        {% for interface in service_data.interfaces %}
        <div class="interface">
            <h3>{{ interface.name }}</h3>
            <p>状态: {% if interface.success %}<span class="success">通过</span>{% else %}<span class="error">失败</span>{% endif %}</p>
        </div>
        {% endfor %}
    </div>
    {% endfor %}
</body>
</html>'''
        template = Template(template_str)
        return template.render(
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            total=test_results.get('total', 0),
            passed=test_results.get('passed', 0),
            failed=test_results.get('failed', 0),
            services=test_results.get('services', {})
        )


class ExcelReportGenerator(BaseReportGenerator):
    """Excel报告生成器"""
    
    def generate(self, test_results: Dict[str, Any]) -> str:
        """生成Excel报告"""
        if not OPENPYXL_AVAILABLE:
            logger.warning("openpyxl 未安装，跳过Excel报告生成")
            return ""
        
        excel_path = os.path.join(self.report_dir, "test_report.xlsx")
        self._generate_excel(test_results, excel_path)
        logger.info(f"Excel报告已生成: {excel_path}")
        return excel_path
    
    def _generate_excel(self, test_results: Dict[str, Any], excel_path: str):
        """生成Excel内容（从原 ReportGenerator 复制）"""
        # 这里需要从原 report_generator.py 复制 _generate_excel 方法
        # 为了保持向后兼容，暂时保留原实现
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "测试报告"
        
        # 添加标题行
        ws.append(["接口名称", "状态", "错误信息"])
        
        # 添加数据
        for service_name, service_data in test_results.get('services', {}).items():
            for interface in service_data.get('interfaces', []):
                ws.append([
                    f"{service_name}.{interface.get('name', '')}",
                    "通过" if interface.get('success', False) else "失败",
                    interface.get('error_message', '')
                ])
        
        wb.save(excel_path)


class ReportGenerator:
    """报告生成器管理器（保持向后兼容）"""
    
    def __init__(self, config: Config):
        self.config = config
        self.html_generator = HTMLReportGenerator(config)
        self.excel_generator = ExcelReportGenerator(config)
    
    def generate_report(self, test_results: Dict[str, Any]) -> str:
        """生成所有格式的报告（保持向后兼容）"""
        # 生成HTML报告
        html_path = self.html_generator.generate(test_results)
        
        # 生成Excel报告
        excel_path = self.excel_generator.generate(test_results)
        
        # 清理旧报告
        self._cleanup_old_reports()
        
        return html_path
    
    def _cleanup_old_reports(self):
        """清理旧报告（保留最新的3个）"""
        report_dir = self.config.get_report_dir()
        html_files = [f for f in os.listdir(report_dir) if f.startswith('test_report_') and f.endswith('.html')]
        html_files.sort(reverse=True)
        
        # 删除旧的报告，只保留最新的3个
        for old_file in html_files[3:]:
            try:
                os.remove(os.path.join(report_dir, old_file))
                logger.debug(f"已删除旧报告: {old_file}")
            except Exception as e:
                logger.warning(f"删除旧报告失败 {old_file}: {e}")

