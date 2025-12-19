"""
配置管理模块
"""
import yaml
import os
from typing import Dict, Any


class Config:
    """配置类"""
    
    def __init__(self, config_path: str = "config.yaml"):
        """初始化配置"""
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        if not os.path.exists(self.config_path):
            # 使用默认配置
            return {
                'servers': {
                    'gate': {'address': '47.84.190.150:29205'},
                    'login': {'url': 'http://47.84.190.150:29002'}
                },
                'jinn_server': {
                    'repo_url': 'https://git.17zjh.com/wegame/jinn_server.git',
                    'branch': 'v0.1.0',
                    'local_path': 'jinn_server',
                    'read_only': True
                },
                'services': {
                    'hall': {'proto_path': 'jinn_server/config/proto_jinn/client'},
                    'room': {'proto_path': 'jinn_server/config/proto_jinn/client'},
                    'social': {'proto_path': 'jinn_server/config/proto_jinn/client'}
                },
                'test': {
                    'output_dir': 'generated_tests',
                    'report_dir': 'reports',
                    'timeout': 30
                }
            }
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}
    
    def get_gate_address(self) -> str:
        """获取Gate服务器地址"""
        return self.config.get('servers', {}).get('gate', {}).get('address', '47.84.190.150:29205')
    
    def get_login_url(self) -> str:
        """获取Login服务器URL"""
        return self.config.get('servers', {}).get('login', {}).get('url', 'http://47.84.190.150:29002')
    
    def get_jinn_server_path(self) -> str:
        """获取jinn_server路径"""
        return self.config.get('jinn_server', {}).get('local_path', 'jinn_server')
    
    def get_jinn_server_repo_url(self) -> str:
        """获取jinn_server仓库URL"""
        return self.config.get('jinn_server', {}).get('repo_url', 'https://git.17zjh.com/wegame/jinn_server.git')
    
    def get_jinn_server_branch(self) -> str:
        """获取jinn_server分支"""
        return self.config.get('jinn_server', {}).get('branch', 'v0.1.0')
    
    def get_service_proto_path(self, service_name: str) -> str:
        """获取服务的proto路径"""
        return self.config.get('services', {}).get(service_name, {}).get('proto_path', 'jinn_server/config/proto_jinn/client')
    
    def get_test_output_dir(self) -> str:
        """获取测试输出目录"""
        return self.config.get('test', {}).get('output_dir', 'generated_tests')
    
    def get_report_dir(self) -> str:
        """获取报告目录"""
        return self.config.get('test', {}).get('report_dir', 'reports')
    
    def get_timeout(self) -> int:
        """获取超时时间"""
        return self.config.get('test', {}).get('timeout', 30)

